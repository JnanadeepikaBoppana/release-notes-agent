# Release Notes Agent

A command-line tool that turns merged GitHub pull requests into publishable
release notes, using an LLM to categorise changes and rewrite engineer-written
PR titles into user-facing language.

Writing release notes by hand means opening every merged PR, deciding whether
it matters to users, rewriting the title so a non-engineer can read it, and
grouping the result. On a two-week cycle with 40 PRs that is roughly 90 minutes
of a product manager's time, repeated every release. This tool does it in one
command.

## What it does

1. **Ingest** — pulls merged PRs from the GitHub REST API for a date range
   (title, author, labels, body, URL).
2. **Classify** — sends the batch to Claude in a single call and asks for, per
   PR: a category, a rewritten user-facing headline, a breaking-change flag,
   and an internal-only flag.
3. **Render** — groups the results into Markdown with breaking changes
   surfaced first, internal churn filtered out by default, and a contributor
   credit list.
4. **Report** — prints runtime against a manual baseline so the time saved is
   measurable rather than assumed.

## Quick start

```bash
pip install -r requirements.txt

# Offline demo — no keys, no network, runs in under a second
python release_notes_agent.py --input sample_prs.json --no-llm
```

That writes `RELEASE_NOTES.md` from the 14 bundled sample PRs.

## Against a real repository

```bash
export GITHUB_TOKEN=ghp_...          # optional, raises the rate limit
export ANTHROPIC_API_KEY=sk-ant-...  # optional, enables the LLM rewrite

python release_notes_agent.py --repo owner/name --days 14
python release_notes_agent.py --repo owner/name --since 2026-06-01 --until 2026-07-01
```

## Options

| Flag | Meaning |
|---|---|
| `--repo owner/name` | Repository to pull merged PRs from |
| `--input FILE.json` | Read PRs from a local file instead (offline demo) |
| `--days N` | Look back N days (default 14) |
| `--since` / `--until` | Explicit date range, `YYYY-MM-DD` |
| `--out FILE` | Output path (default `RELEASE_NOTES.md`) |
| `--no-llm` | Skip the LLM, use the keyword classifier |
| `--include-internal` | Keep CI/chore/refactor changes in the output |
| `--minutes-per-pr` | Manual baseline for the savings report (default 2.5) |
| `--model` | Model name (default `claude-sonnet-5`) |

## Design notes

**It always produces output.** If `ANTHROPIC_API_KEY` is missing, or the API
call fails mid-run, the tool falls back to a keyword classifier that reads
Conventional Commit prefixes (`feat:`, `fix:`, `perf:`) and GitHub labels. The
headlines are less polished but the release notes still ship. A tool that
breaks when a dependency is down does not get adopted.

**One LLM call, not N.** All PRs go in a single batched request rather than one
call per PR. On a 40-PR release that is 40x fewer round trips and a
proportionally smaller bill.

**JSON parsing is defensive.** Models sometimes wrap JSON in code fences or add
a sentence of preamble despite instructions not to. The parser strips fences,
and falls back to a regex extraction of the outermost array before giving up.

**Breaking changes are promoted, internal churn is demoted.** Dependabot bumps
and CI tweaks are hidden unless `--include-internal` is passed, because the
audience for release notes is users, not the repo's own maintainers.

## Sample output

```markdown
# Release Notes — sample-data

_Changes merged 2026-07-15 to 2026-07-29 · 14 pull requests_

## ⚠️ Breaking Changes

- Remove deprecated /v1/reports endpoint ([#1216](...))

## Features

- Add support for annual subscription plans ([#1204](...)) — @priya-n
- Add filters for date range and status ([#1227](...)) — @lena-m
- Bulk user import from CSV ([#1236](...)) — @sam-oyelaran

## Bug Fixes

- Resolve crash when uploading files over 50MB ([#1207](...)) — @dmitri-k
...
```

## Known limitations

- The GitHub Search API caps results at 1,000 per query; very large releases
  need to be split by date range.
- The savings report uses a configurable per-PR estimate, not measured human
  timing. Treat it as an order-of-magnitude figure.
- The LLM path has been tested against the Anthropic Messages API only.

## Possible extensions

- Post the generated notes to Slack or a GitHub Release on tag push
- Diff against the previous release to catch changes that were never announced
- Cluster related PRs into a single narrative entry rather than one bullet each
