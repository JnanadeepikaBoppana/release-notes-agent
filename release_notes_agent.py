#!/usr/bin/env python3
"""
Release Notes Agent
===================

Turns merged GitHub pull requests into publishable release notes.

Pipeline:
    1. Pull merged PRs from the GitHub REST API for a date range or tag range.
    2. Ask an LLM to categorise each PR, rewrite the title in user-facing
       language, and flag breaking changes.
    3. Render grouped Markdown release notes and print a savings report.

Runs offline against bundled sample data (`--input sample_prs.json`) and
degrades to a keyword-based classifier when no LLM key is present, so the
tool always produces output.

Usage:
    python release_notes_agent.py --input sample_prs.json --no-llm
    python release_notes_agent.py --repo facebook/react --days 14
    python release_notes_agent.py --repo myorg/myrepo --since 2026-06-01 --until 2026-07-01
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:  # pragma: no cover
    sys.exit("Missing dependency. Run: pip install -r requirements.txt")


GITHUB_API = "https://api.github.com"
ANTHROPIC_API = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-5"

CATEGORIES = [
    "Features",
    "Improvements",
    "Bug Fixes",
    "Infrastructure",
    "Documentation",
]

# Minutes a human spends reading one PR and writing one release-note line.
# Used only for the savings estimate; override with --minutes-per-pr.
DEFAULT_MINUTES_PER_PR = 2.5


# --------------------------------------------------------------------------
# 1. Ingest
# --------------------------------------------------------------------------

def fetch_merged_prs(
    repo: str,
    since: str,
    until: str,
    token: str | None = None,
    max_prs: int = 300,
) -> list[dict[str, Any]]:
    """Fetch merged PRs for `repo` merged between `since` and `until` (YYYY-MM-DD).

    Uses the paginated /pulls endpoint and filters on merged_at client-side.
    The /search/issues endpoint supports date qualifiers directly but rejects
    some otherwise-valid queries with HTTP 422, so it is not used here.
    """
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    since_dt = datetime.fromisoformat(since).replace(tzinfo=timezone.utc)
    until_dt = datetime.fromisoformat(until).replace(
        tzinfo=timezone.utc
    ) + timedelta(days=1)

    prs: list[dict[str, Any]] = []
    page = 1
    max_pages = 15
    empty_streak = 0

    while page <= max_pages and len(prs) < max_prs:
        try:
            resp = requests.get(
                f"{GITHUB_API}/repos/{repo}/pulls",
                headers=headers,
                params={
                    "state": "closed",
                    "sort": "updated",
                    "direction": "desc",
                    "per_page": 100,
                    "page": page,
                },
                timeout=30,
            )
        except requests.RequestException as exc:
            raise RuntimeError(
                f"Could not reach the GitHub API: {exc}\n"
                "Check your network, or run offline with "
                "--input sample_prs.json"
            ) from exc

        if resp.status_code == 404:
            raise RuntimeError(
                f"Repository '{repo}' not found. Check the owner/name spelling, "
                "and note that private repos need a GITHUB_TOKEN."
            )
        if resp.status_code in (403, 429):
            raise RuntimeError(
                "GitHub rate limit hit (60 requests/hour without a token).\n"
                "Wait an hour, or set GITHUB_TOKEN for 5,000/hour."
            )
        if not resp.ok:
            raise RuntimeError(
                f"GitHub returned HTTP {resp.status_code}: {resp.text[:200]}"
            )

        items = resp.json()
        if not items:
            break

        matched = 0
        for item in items:
            merged_at = item.get("merged_at")
            if not merged_at:
                continue  # closed but never merged
            merged_dt = datetime.fromisoformat(merged_at.replace("Z", "+00:00"))
            if not (since_dt <= merged_dt < until_dt):
                continue
            matched += 1
            prs.append(
                {
                    "number": item["number"],
                    "title": item["title"],
                    "author": (item.get("user") or {}).get("login", "unknown"),
                    "url": item["html_url"],
                    "labels": [lbl["name"] for lbl in item.get("labels", [])],
                    "body": (item.get("body") or "")[:600],
                    "merged_at": merged_at,
                }
            )

        # Results are ordered by last update, not merge date, so a page with no
        # matches is not proof we are past the window. Give it a few pages.
        empty_streak = empty_streak + 1 if matched == 0 else 0
        if empty_streak >= 3:
            break
        if len(items) < 100:
            break
        page += 1

    prs.sort(key=lambda p: p["number"])
    return prs[:max_prs]


def load_prs_from_file(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON array of PR objects.")
    return data


# --------------------------------------------------------------------------
# 2. Classify
# --------------------------------------------------------------------------

CLASSIFY_PROMPT = """\
You are drafting release notes for a software product.

For each pull request below, return a JSON object with these keys:
  "number"   - the PR number, unchanged
  "category" - exactly one of: {categories}
  "headline" - a one-line, user-facing rewrite of the title. Present tense,
               no ticket IDs, no "feat:"/"fix:" prefixes, no trailing period.
               Describe the user-visible effect, not the implementation.
  "breaking" - true only if this change requires action from users or
               integrators (removed endpoint, changed default, migration)
  "internal" - true if this is invisible to end users (CI, refactor, tests)

Return ONLY a JSON array. No prose, no code fences.

Pull requests:
{prs}
"""


def classify_with_llm(
    prs: list[dict[str, Any]], api_key: str, model: str = MODEL
) -> list[dict[str, Any]]:
    """Categorise and rewrite PR titles using the Anthropic Messages API."""
    compact = [
        {
            "number": pr["number"],
            "title": pr["title"],
            "labels": pr.get("labels", []),
            "body": (pr.get("body") or "")[:300],
        }
        for pr in prs
    ]

    prompt = CLASSIFY_PROMPT.format(
        categories=", ".join(CATEGORIES),
        prs=json.dumps(compact, indent=2),
    )

    resp = requests.post(
        ANTHROPIC_API,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=120,
    )
    resp.raise_for_status()
    text = resp.json()["content"][0]["text"].strip()

    # Strip code fences if the model added them anyway.
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if not match:
            raise RuntimeError(f"Could not parse LLM response:\n{text[:400]}")
        return json.loads(match.group(0))


LABEL_MAP = {
    "bug": "Bug Fixes",
    "fix": "Bug Fixes",
    "feature": "Features",
    "enhancement": "Improvements",
    "docs": "Documentation",
    "documentation": "Documentation",
    "ci": "Infrastructure",
    "chore": "Infrastructure",
    "dependencies": "Infrastructure",
}

PREFIX_MAP = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "perf": "Improvements",
    "refactor": "Improvements",
    "docs": "Documentation",
    "chore": "Infrastructure",
    "ci": "Infrastructure",
    "build": "Infrastructure",
    "test": "Infrastructure",
}


def classify_heuristic(prs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keyword fallback so the tool still runs with no LLM key."""
    out = []
    for pr in prs:
        title = pr["title"]
        category = None

        prefix = re.match(r"^\s*([a-z]+)(?:\([^)]*\))?!?:", title, re.I)
        if prefix:
            category = PREFIX_MAP.get(prefix.group(1).lower())

        if category is None:
            for label in pr.get("labels", []):
                if label.lower() in LABEL_MAP:
                    category = LABEL_MAP[label.lower()]
                    break

        if category is None:
            lowered = title.lower()
            if any(w in lowered for w in ("fix", "bug", "crash", "regression")):
                category = "Bug Fixes"
            elif any(w in lowered for w in ("add", "introduce", "support", "new")):
                category = "Features"
            else:
                category = "Improvements"

        headline = re.sub(r"^\s*[a-z]+(?:\([^)]*\))?!?:\s*", "", title, flags=re.I)
        headline = re.sub(r"\s*\(#\d+\)\s*$", "", headline).rstrip(".")
        headline = headline[0].upper() + headline[1:] if headline else title

        out.append(
            {
                "number": pr["number"],
                "category": category,
                "headline": headline,
                "breaking": "!" in title.split(":")[0] or "breaking" in title.lower(),
                "internal": category == "Infrastructure",
            }
        )
    return out


# --------------------------------------------------------------------------
# 3. Render
# --------------------------------------------------------------------------

def render_markdown(
    prs: list[dict[str, Any]],
    classified: list[dict[str, Any]],
    repo: str,
    since: str,
    until: str,
    include_internal: bool = False,
) -> str:
    by_number = {pr["number"]: pr for pr in prs}
    merged: list[dict[str, Any]] = []
    for entry in classified:
        pr = by_number.get(entry["number"])
        if pr:
            merged.append({**pr, **entry})

    lines = [
        f"# Release Notes — {repo}",
        "",
        f"_Changes merged {since} to {until} · {len(merged)} pull requests_",
        "",
    ]

    breaking = [m for m in merged if m.get("breaking")]
    if breaking:
        lines += ["## ⚠️ Breaking Changes", ""]
        for item in breaking:
            lines.append(
                f"- {item['headline']} "
                f"([#{item['number']}]({item['url']}))"
            )
        lines.append("")

    for category in CATEGORIES:
        if category == "Infrastructure" and not include_internal:
            continue
        items = [
            m
            for m in merged
            if m.get("category") == category and not m.get("breaking")
        ]
        if not items:
            continue
        lines += [f"## {category}", ""]
        for item in sorted(items, key=lambda x: x["number"]):
            lines.append(
                f"- {item['headline']} "
                f"([#{item['number']}]({item['url']})) — @{item['author']}"
            )
        lines.append("")

    contributors = sorted({m["author"] for m in merged})
    if contributors:
        lines += [
            "## Contributors",
            "",
            ", ".join(f"@{c}" for c in contributors),
            "",
        ]

    return "\n".join(lines)


def savings_report(
    n_prs: int, elapsed: float, minutes_per_pr: float
) -> str:
    manual_minutes = n_prs * minutes_per_pr
    automated_minutes = elapsed / 60
    saved = manual_minutes - automated_minutes
    pct = (saved / manual_minutes * 100) if manual_minutes else 0
    return (
        f"\nProcessed {n_prs} PRs in {elapsed:.2f}s.\n"
        f"Manual baseline: {manual_minutes:.0f} min "
        f"({minutes_per_pr} min/PR).\n"
        f"Automated: {automated_minutes:.2f} min. "
        f"Reduction: {pct:.1f}%.\n"
    )


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate release notes from merged GitHub pull requests."
    )
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--repo", help="GitHub repo as owner/name")
    src.add_argument("--input", type=Path, help="Local JSON file of PRs (offline demo)")

    p.add_argument("--since", help="Start date YYYY-MM-DD")
    p.add_argument("--until", help="End date YYYY-MM-DD")
    p.add_argument("--days", type=int, default=14, help="Look back N days (default 14)")
    p.add_argument("--out", type=Path, default=Path("RELEASE_NOTES.md"))
    p.add_argument("--model", default=MODEL)
    p.add_argument("--no-llm", action="store_true", help="Use keyword classifier only")
    p.add_argument(
        "--include-internal",
        action="store_true",
        help="Include infrastructure/chore changes in the output",
    )
    p.add_argument("--minutes-per-pr", type=float, default=DEFAULT_MINUTES_PER_PR)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    start = time.perf_counter()

    until = args.until or datetime.now(timezone.utc).date().isoformat()
    since = args.since or (
        datetime.fromisoformat(until) - timedelta(days=args.days)
    ).date().isoformat()

    if args.input:
        prs = load_prs_from_file(args.input)
        repo = "sample-data"
        print(f"Loaded {len(prs)} PRs from {args.input}")
    else:
        repo = args.repo
        print(f"Fetching merged PRs for {repo} ({since} to {until})...")
        try:
            prs = fetch_merged_prs(repo, since, until, os.getenv("GITHUB_TOKEN"))
        except RuntimeError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        print(f"Found {len(prs)} merged PRs.")

    if not prs:
        print("No merged pull requests in that range. Nothing to write.")
        return 0

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if args.no_llm or not api_key:
        if not args.no_llm:
            print("No ANTHROPIC_API_KEY found — using keyword classifier.")
        classified = classify_heuristic(prs)
    else:
        print(f"Classifying {len(prs)} PRs with {args.model}...")
        try:
            classified = classify_with_llm(prs, api_key, args.model)
        except Exception as exc:  # noqa: BLE001
            print(f"LLM step failed ({exc}). Falling back to keyword classifier.")
            classified = classify_heuristic(prs)

    notes = render_markdown(
        prs, classified, repo, since, until, args.include_internal
    )
    args.out.write_text(notes, encoding="utf-8")

    elapsed = time.perf_counter() - start
    print(f"\nWrote {args.out} ({len(notes.splitlines())} lines).")
    print(savings_report(len(prs), elapsed, args.minutes_per_pr))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
