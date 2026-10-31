---
name: kickside-web-component
description: Build a KickSide module's page as a Vue 3 web component that fits the shell - the module owns ui/src and the committed static/ bundle; registry entries fs.directory, http.static, view.component and a ui.nav_item with render component; :host display block, height 100%, min-height 0, the page root owning its scroll; PrimeVue with semantic --p-* tokens; data through named getters of @wippy-fe/proxy; subscribe before the first read and refresh on host visibility; navigation by a composed navigate event; the make dev watcher without a restart. Use when a module needs a new page, a page renders blank, clipped or unthemed, does not refresh, or its index.js answers 404.
---

# A KickSide page as a web component

A KickSide module carries its own screen. The module builds a Vue 3 custom element from `ui/src` into its `static/` folder, serves that folder with its own static route, announces the element to the shell, and adds a menu item that mounts it. The shell gives the element a box of fixed height, a theme, a proxy for authenticated calls and realtime events, and it may keep the element alive while the person is on another page. Everything below follows from those five facts.

**Route:** a screen from the KickSide analyst's spec and an endpoint from the KickSide module developer → **kickside-web-component** (the frame) → kickside-ui-patterns (what goes on the page) → kickside-ui-testing (proof) → the Reviewer → the KickSide QA tester.
Before this skill: the module repository, created from the official module template, and the endpoint's contract (path, answer shape, realtime topic). After it: a page that mounts, themes, scrolls, refreshes and navigates, with `static/` rebuilt and committed.

## When to use

- A new page or a new view of a module.
- A page that is blank, clipped at the bottom, wrongly coloured in dark mode, or stale after a write.
- The page's `index.js` answers 404, or the console shows a module that failed to load.

## Inputs

- The module repository and its `Makefile` (the commands live there; never call npm or vite directly).
- The endpoint path and its answer shape, the realtime topic it publishes after a commit, and the route paths of pages you link to.
- A running DEV copy of KickSide with the module loaded as a workspace replacement (the KickSide specialist sets it up). Never a client's production copy.

## Steps

Steps 2 to 10 were read from the sources named in each step and not tried here: confirm each on the module in front of you and say in the report which ones you confirmed.

1. **Read what is there.** Open the module's `src/_index.yaml` (or the file that holds its UI entries), `ui/package.json`, `ui/vite.config.ts`, `ui/src/index.ts`, `ui/src/styles.css`, the existing page and its spec, and the `Makefile`. Read the module's `AGENTS.md` if it has one. Write down the exact entry ids, the tag name, the base path and the entry file.
   Check: your notes hold tag name, base path, entry point, static mount and the make targets for setup, build, dev, typecheck and test-ui.
2. **Keep the registry chain whole.** Four entries make a page: an `fs.directory` over `./static`; an `http.static` on that filesystem whose server comes from an `ns.requirement` (the host supplies it); a `registry.entry` of type `view.component` that names its `tag_name`, `entry_point` and `base_path` and sets both `auto_register` and `announced` to true; and a `ui.nav_item` whose `component_tag` is that same tag, rendered as `render: component`. Tag, props and description in the registry must match `ui/package.json` (`wippy.tagName`, `wippy.props`, `wippy.description`), and the package keeps `specification: wippy-component-1.0` (read from S2, S3, not tried).
   Check: the tag is spelled the same in all three places; a navigation item is never the access check (that is the endpoint's policy, the KickSide module developer's lane).
3. **Define the element the template's way.** One class extending the Vue element base from `@wippy-fe/webcomponent-vue`, its props schema taken from the package file, `define(import.meta.url, Element)` at module level, and an exported `webComponent` function. A page with any control (button, input, table, dialog, menu, tag) installs PrimeVue through the Wippy PrimeVue plugin and asks the host for `primeVueCssUrl`; every page that uses theme tokens asks for `themeConfigUrl`; every page that scrolls asks for `iframeCssUrl` (read from S3, S5, not tried).
   Check: the host CSS keys match what the page renders; no hand-made button or input where PrimeVue has one.
4. **Size and scroll.** The shell's surface has a definite height and hides overflow. In `styles.css`: `:host` is `display: block; height: 100%; min-height: 0`, the mount wrapper under it is full height too, and the page root has `height: 100%` and `overflow-y: auto` in the same rule. A page that does not own its scroll is cut off with no scrollbar (read from S2, S3, not tried).
   Check: the module's check script (run by `make check` or `make verify`) passes its height and scroll checks; a long list scrolls to its last row in the DEV copy.
5. **Theme with semantic tokens only.** Colours come from semantic `--p-*` names: text, muted text, content background, content border, primary, and the state names danger, success, warn, info, help. No hex values, no numbered surface scale (it does not flip in dark mode), no invented names such as a colour word with a number. Focus rings use the facade's focus-ring tokens; the component only picks which element shows `:focus-visible`. Derived shades use `color-mix` of two semantic tokens (read from S2, S5, not tried).
   Check: a search of `ui/src` for `#` colours and for colour-word tokens finds nothing; the page reads well in light and dark.
6. **Read data through the proxy.** Use the named getters of `@wippy-fe/proxy`: `api` for HTTP (an axios instance that adds the person's token on same-origin calls), `on` for realtime topics, `host` for toast, confirm and navigation. Never read the runtime's globals, never build a raw postMessage protocol, never hard-code another module's URL or a deployment path (read from S2, S5, not tried).
   Check: `ui/src` imports nothing from the runtime's internals and has no absolute host URL.
7. **Subscribe, then load; refresh on reveal.** In setup: call `on(topic, ...)` first, then hand the load function to `useHostVisibilityRefresh` from `@wippy-fe/webcomponent-vue`, which does the first load and reloads each time the host shows the kept element again. The topic handler only reloads from the endpoint; the payload is a wake-up, not data. Count requests, and drop an answer that is older than the latest request or that arrives after unmount. Call the disposer `on` returned in `onUnmounted`. Subscribe once in setup, never inside the visibility callback, or every return to the page adds another subscription. For a page bound to one component instance, subscribe to that component's topic and check the selected id before applying an answer (read from S2, S5, not tried).
   Check: kickside-ui-testing's three refresh tests pass.
8. **Navigate the shell's way.** Inside the shadow root, send a `CustomEvent` named `navigate` with `detail.path` set to a registered route, `bubbles: true` and `composed: true`, from the page root. `host.navigate` also exists; prefer the event inside a page, as the module guides do. Only registered routes (read from S2, not tried).
   Check: the link opens the target page in the DEV copy and the browser back button returns.
9. **Build into static/.** Keep the template's library build (ES format, its entry signature setting, the host-provided packages external, the `process.env` define). The external list must match what the host's import map serves: a package the top document does not map has to be bundled. Run `make typecheck`, `make build`, then confirm `static/index.js` and `static/wippy-meta.json` exist and the meta matches the package. Commit `static/` with the source (read from S3, not tried).
   Check: `git status` shows `static/` changed together with `ui/src`; the check script reports no stale meta.
10. **Dev loop without a restart.** With the module mounted in the DEV copy, run `make setup` once and `make dev`: the watcher rebuilds into `static/` on every save; reload the browser. A restart is needed only when the registry declarations change (static mount, tag, base path, entry point) or Lua changes, and then the KickSide specialist restarts the copy (read from S2, S3, not tried).
   Check: an edit shows after a browser reload with the copy still running.

## Rules (each with its check)

- **The module owns its UI.** Edit `ui/src`, build with make, commit `static/`. Check: no hand edit inside `static/`.
- **Only semantic `--p-*` tokens.** Check: no raw colour and no palette-number token in `ui/src`.
- **The page root scrolls.** Check: `:host` and root rules as in step 4.
- **Subscribe before the first read; dispose on unmount.** Check: test 1 and the unmount assertion in kickside-ui-testing.
- **No secret in the browser.** The page holds no API key, provider token or password; the proxy carries the person's session. Check: a search of `ui/src` and `static/` for key-like strings finds nothing.
- **Docs, then build.** For any Wippy frontend fact use wippy-docs and cite the path; when the module template or its check script disagrees with a page, follow the template and say so. Check: the report lists the doc paths and any disagreement.

## Pitfalls

- PrimeVue theme CSS is added to the shadow root after the module's CSS, so a plain rule on a PrimeVue class loses at equal specificity. Raise specificity on purpose or scope under the component root.
- `onMounted` alone loads once; the shell may keep the element and show it again later with old data.
- A 404 on `index.js`: check the registry entry, the static mount, the build target and the emitted file, in that order. A 5xx is the backend's: hand it to the KickSide module developer with the log line.
- Overlays (Dialog, Drawer) can render outside the shadow root; check them in the running app, not only in jsdom.

## Hand-over

- **To the KickSide module developer:** a missing or wrong endpoint, a topic not published after a commit, a policy that refuses a member.
- **To the KickSide specialist:** the DEV copy, the workspace replacement, a restart, users and roles to test with.
- **To the Reviewer:** the commit hash and what to check: the files changed, the tests that cover them, what was seen live and what was not checked.
- **To the UI designer:** a look or layout that no screen in the platform has yet.
- **To the KickSide QA tester:** the commit, the routes to open and the states to try.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no text taken: S1 the KickSide documentation (github.com/kicksideai/docs, commit 71a4588; CC BY 4.0), S2 the KickSide app and developer handbook (github.com/kicksideai/kickside, commit b7e0106; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI), S3 the official module template (github.com/kicksideai/module, commit 37d16de; MIT, © 2026 Wippy), and S5 the Wippy frontend pages read through the docs endpoints for agents on 2026-10-23 (en/frontend/micro-frontends/web-component, web-component-theming, proxy-api, compliance-checklist; MPL-2.0).

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
