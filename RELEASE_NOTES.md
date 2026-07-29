# Release Notes — facebook/react

_Changes merged 2026-06-29 to 2026-07-29 · 74 pull requests_

## Features

- Add parentEnter/parentExit props to ViewTransition ([#36690](https://github.com/react/react/pull/36690)) — @jackpope
- [react-devtools-facade] add host instance component lookup ([#36820](https://github.com/react/react/pull/36820)) — @hoxyq
- [react-devtools-cdt-mcp] add DOM element component lookup ([#36822](https://github.com/react/react/pull/36822)) — @hoxyq
- [react-devtools-cdt-mcp] add chrome-devtools E2E coverage ([#36823](https://github.com/react/react/pull/36823)) — @hoxyq
- [react-devtools] add parent stack tool ([#36825](https://github.com/react/react/pull/36825)) — @hoxyq
- [react-devtools-facade] Add includeHooks option to component lookup ([#36874](https://github.com/react/react/pull/36874)) — @hoxyq
- [changelog] Add 19.0.x, 19.1.x, 19.2.x patch releases ([#36898](https://github.com/react/react/pull/36898)) — @eps1lon
- [test] Add coverage for multi-byte code units in stream APIs ([#36900](https://github.com/react/react/pull/36900)) — @eps1lon
- [compiler]: add `useWindowVirtualizer` to known incompatible libraries ([#36912](https://github.com/react/react/pull/36912)) — @gtkatakura
- [Fizz] Support nested enter/exit ViewTransition animations ([#36917](https://github.com/react/react/pull/36917)) — @jackpope
- [react-devtools-cdt-mcp] Add explicit register entry ([#36972](https://github.com/react/react/pull/36972)) — @hoxyq
- [react-devtools-cdt-mcp] Throw on import from unsupported environment ([#36975](https://github.com/react/react/pull/36975)) — @hoxyq
- [react-server-dom-turbopack] Support Turbopack's experimental array format for chunks ([#37095](https://github.com/react/react/pull/37095)) — @sampoder
- [Bench] Add JSON output and declare missing dependency ([#37127](https://github.com/react/react/pull/37127)) — @gaearon

## Improvements

- [react-devtools-cdt-mcp] chrome-devtools-mcp integration ([#36600](https://github.com/react/react/pull/36600)) — @hoxyq
- [DevTools] Make component search results directly navigable ([#36786](https://github.com/react/react/pull/36786)) — @Biki-das
- [react-devtools-cdt-mcp] run E2E tests in CI ([#36824](https://github.com/react/react/pull/36824)) — @hoxyq
- [Float] Forward `nonce` option in ReactDOM.preloadModule() ([#36851](https://github.com/react/react/pull/36851)) — @UditDewan
- [compiler] Ensure builds use the current checkout's compiler ([#36881](https://github.com/react/react/pull/36881)) — @eps1lon
- [compiler] Restore code frames in ESLint compiler error messages ([#36901](https://github.com/react/react/pull/36901)) — @javache
- [Fizz] Stop firing `onAllReady` after the shell errored ([#36903](https://github.com/react/react/pull/36903)) — @eps1lon
- [test] Use awaited `serverAct` to drive task loop ([#36908](https://github.com/react/react/pull/36908)) — @eps1lon
- [Perf Tracks] Don't enumerate typed array props in dev ([#36913](https://github.com/react/react/pull/36913)) — @UditDewan
- [Fizz] Guard the shell-error callbacks instead of nulling them out on the request ([#36916](https://github.com/react/react/pull/36916)) — @eps1lon
- [react-devtools] substitute %i and %f in console format strings ([#36929](https://github.com/react/react/pull/36929)) — @anxkhn
- [react-devtools] Keep console specifiers literal when no argument is supplied ([#36930](https://github.com/react/react/pull/36930)) — @anxkhn
- [compiler] Bail out with Todo on using and await using declarations ([#36946](https://github.com/react/react/pull/36946)) — @poteto
- [Fiber] Detect useSyncExternalStore mutations missed while Activity tree was hidden ([#36947](https://github.com/react/react/pull/36947)) — @sophiebits
- [Fiber] Don't invoke effects on moved children in StrictMode ([#36948](https://github.com/react/react/pull/36948)) — @sophiebits
- [Fiber] Don't set .innerHTML when it hasn't changed ([#36949](https://github.com/react/react/pull/36949)) — @sophiebits
- [Fast Refresh] Remount correctly when an edit changes the component kind ([#36950](https://github.com/react/react/pull/36950)) — @sophiebits
- [Fast Refresh] Unify hot reload type resolution ([#36962](https://github.com/react/react/pull/36962)) — @sophiebits
- [Fast Refresh] Derive the fiber tag from the resolved type when mounting ([#36963](https://github.com/react/react/pull/36963)) — @sophiebits
- [Fast Refresh] Make edits to a memo comparison function take effect ([#36964](https://github.com/react/react/pull/36964)) — @sophiebits
- [Fast Refresh] Find and remount wrapper edits behind lazy() ([#36965](https://github.com/react/react/pull/36965)) — @sophiebits
- [react-devtools-cdt-mcp] Make registration idempotent ([#36971](https://github.com/react/react/pull/36971)) — @hoxyq
- [react-devtools-cdt-mcp] Make it esm-only package ([#36973](https://github.com/react/react/pull/36973)) — @hoxyq
- [Fizz] Extend stack overflow recovery to retries ([#36977](https://github.com/react/react/pull/36977)) — @jackpope
- [Fiber] Update input.defaultValue for type=number too ([#36980](https://github.com/react/react/pull/36980)) — @sophiebits
- [RN] Update ReactPrivate and InitializeCore imports (0.87 Strict API) ([#36986](https://github.com/react/react/pull/36986)) — @huntie
- [DevTools] Don't reconnect proxy port while page is prerendering ([#37009](https://github.com/react/react/pull/37009)) — @Saransh-Jainbu
- Clean up flag to enable microtasks in RN ([#37021](https://github.com/react/react/pull/37021)) — @rubennorte
- [devtools] Document that Store consistency throws must not be worked around ([#37035](https://github.com/react/react/pull/37035)) — @eps1lon
- Enable enableEffectEventMutationPhase everywhere ([#37039](https://github.com/react/react/pull/37039)) — @hoxyq
- [DevTools] Type EventEmitter error handling ([#37048](https://github.com/react/react/pull/37048)) — @hoxyq
- [DevTools] Harden Bridge and Wall lifecycle types ([#37049](https://github.com/react/react/pull/37049)) — @hoxyq
- [DevTools] Validate Store operation invariants ([#37050](https://github.com/react/react/pull/37050)) — @hoxyq
- [DOM] Scroll to text siblings of empty Fragments instead of the parent ([#37060](https://github.com/react/react/pull/37060)) — @eps1lon
- [DOM] Handle scrolling of empty Fragments below containers ([#37061](https://github.com/react/react/pull/37061)) — @eps1lon
- [DOM] Handle blur on Fragments below `Document` ([#37062](https://github.com/react/react/pull/37062)) — @eps1lon
- [DevTools] Buffer Bridge messages during extension reconnects ([#37075](https://github.com/react/react/pull/37075)) — @hoxyq
- [DevTools] Shut down standalone Bridge on socket close ([#37076](https://github.com/react/react/pull/37076)) — @hoxyq
- [Flight] Limit fake JSX call site stacks to 10 frames ([#37086](https://github.com/react/react/pull/37086)) — @timneutkens
- [FlightReply] Performance improvements when decoding ([#37087](https://github.com/react/react/pull/37087)) — @eps1lon
- [FlightReply] Performance improvements when decoding ([#37088](https://github.com/react/react/pull/37088)) — @eps1lon
- [FlightReply] Performance improvements when decoding ([#37089](https://github.com/react/react/pull/37089)) — @eps1lon
- [FlightReply] Performance improvements when decoding ([#37090](https://github.com/react/react/pull/37090)) — @gnoff
- [Flight] Define Flight chunk `.then` with `Object.defineProperty` ([#37109](https://github.com/react/react/pull/37109)) — @eps1lon
- [Fiber] only remove properties from singletons on release ([#37112](https://github.com/react/react/pull/37112)) — @gnoff
- [Fiber] Don't reaquire HostSingletons during dev effect validation ([#37113](https://github.com/react/react/pull/37113)) — @gnoff

## Bug Fixes

- [DevTools] Fix WhatChanged scrolling out of view in profiler sidebar ([#36244](https://github.com/react/react/pull/36244)) — @Kertsu
- [compiler] Fix JSX tags prefixed with `_` or `$` incorrectly treated as host elements ([#36688](https://github.com/react/react/pull/36688)) — @sleitor
- [compiler] Fix failing Rust compiler test case for todo-locally-require-fbt ([#36767](https://github.com/react/react/pull/36767)) — @mvitousek
- Treat incomplete tree as an error during recovery ([#36911](https://github.com/react/react/pull/36911)) — @acdlite
- [DevTools] Fix printOperationsArray decode of applied activity slice change ([#36935](https://github.com/react/react/pull/36935)) — @anxkhn
- Fix[flow]: apply new type cast syntax ([#36938](https://github.com/react/react/pull/36938)) — @hoxyq
- [compiler] Port JSX tag classification fix to Rust (not-lowercase is a component) ([#36951](https://github.com/react/react/pull/36951)) — @poteto
- [test] Fix Error Proxy stack assignment in Node.js 21+ ([#36967](https://github.com/react/react/pull/36967)) — @gaearon
- [Fixture] flight-ssr-bench: drain immediates between iterations to fix false memory leak ([#36968](https://github.com/react/react/pull/36968)) — @gaearon
- [Flight] Recognize Node 22+ V8 frames for Promise statics in debug info ([#36969](https://github.com/react/react/pull/36969)) — @gaearon
- [Fiber] Fix false-positive hydration mismatch on `nonce` attributes ([#37030](https://github.com/react/react/pull/37030)) — @MaxwellCohen
- [test] Add Flight regression test for async debug info surviving Promise GC ([#37037](https://github.com/react/react/pull/37037)) — @eps1lon
- [Fiber] Fix hang when updating a dehydrated boundary inside a hidden tree ([#37135](https://github.com/react/react/pull/37135)) — @gaearon

## Documentation

- Remove stale parentType param from validateChildKeys JSDoc ([#36928](https://github.com/react/react/pull/36928)) — @anxkhn

## Contributors

@Biki-das, @Kertsu, @MaxwellCohen, @Saransh-Jainbu, @UditDewan, @acdlite, @anxkhn, @eps1lon, @gaearon, @gnoff, @gtkatakura, @hoxyq, @huntie, @jackpope, @javache, @mvitousek, @poteto, @rubennorte, @sampoder, @sleitor, @sophiebits, @timneutkens
