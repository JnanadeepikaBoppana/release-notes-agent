# Release Notes — sample-data

_Changes merged 2026-07-15 to 2026-07-29 · 14 pull requests_

## ⚠️ Breaking Changes

- Remove deprecated /v1/reports endpoint ([#1216](https://github.com/example/app/pull/1216))

## Features

- Add support for annual subscription plans ([#1204](https://github.com/example/app/pull/1204)) — @priya-n
- Add filters for date range and status ([#1227](https://github.com/example/app/pull/1227)) — @lena-m
- Bulk user import from CSV ([#1236](https://github.com/example/app/pull/1236)) — @sam-oyelaran

## Improvements

- Reduce dashboard load time by caching aggregate queries ([#1213](https://github.com/example/app/pull/1213)) — @sam-oyelaran
- Extract notification logic into its own service ([#1230](https://github.com/example/app/pull/1230)) — @priya-n
- Lazy-load report charts to cut initial bundle by 340KB ([#1242](https://github.com/example/app/pull/1242)) — @priya-n

## Bug Fixes

- Resolve crash when uploading files over 50MB ([#1207](https://github.com/example/app/pull/1207)) — @dmitri-k
- Session no longer expires early on Safari ([#1221](https://github.com/example/app/pull/1221)) — @dmitri-k
- Correct timezone handling in scheduled exports ([#1233](https://github.com/example/app/pull/1233)) — @dmitri-k

## Documentation

- Document the webhook retry policy ([#1218](https://github.com/example/app/pull/1218)) — @lena-m

## Contributors

@dependabot, @dmitri-k, @lena-m, @priya-n, @sam-oyelaran
