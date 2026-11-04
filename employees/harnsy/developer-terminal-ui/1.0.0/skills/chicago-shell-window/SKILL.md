---
name: chicago-shell-window
description: Add or repair a window of the Chicago shell on the Wippy runtime - read the module's own docs and agent skills first, declare the window entry, write init/view/update in Lua against the shell SDK, support cells always and pixels as an extra, check it at the smallest size with long and empty data in both modes, prove it with a text screen and a picture through the module's own harness, and build or try it live through the app's workshop over MCP on a scratch app. Use for any window, widget or picture work in a Chicago shell module or app.
---

# A Chicago shell window on Wippy

The Chicago shell is a desktop that runs in a terminal on the Wippy runtime: a compositor owns the screen, and every window is a Lua process that draws into its own area through the shell SDK. This skill is the worked stack for the general rules in terminal-io and tui-layout-render. Code ids such as `chicago.shell.sdk:app` are written exactly as the module declares them.

**Route:** a window task in a Chicago module or app → **chicago-shell-window** (with tui-layout-render for the general layout and checks) → reviewer.
Before this skill: the module, its commit and who else is changing it are known. After it: a window that opens from the Start menu, works in both modes and at its smallest size, with proof attached.

## When to use

- A new window, widget or picture in a module or app built on the Chicago shell.
- A window that breaks on resize, scroll, empty data, focus or mode change.
- Trying a window live in a running scratch app before it goes into module sources.
- Not for services, processes, module packaging or registry design beyond the window's own entry: that is the Lua developer (Wippy). Not for the runtime's Go code: that is the Go developer.

## Inputs

- The module or app repository, its commit, and any uncommitted changes of other people in it (read them, never overwrite them).
- The module's own docs: the window SDK guide and the traps list in the shell module, the base desktop's README, and the agent skills the shell module ships (read them in the installed module; this skill does not repeat them).
- The runtime build the module needs. The shell needs the runtime's `gfx` module for pixels; a release build without it can fail to load the module at all. Check which build you run before you trust any result.

## Steps

1. **Read before editing.** The SDK guide, the traps list and the shipped agent skills in the module version you work on; the app's dependency declarations and lock; uncommitted changes in the working copy.
   Check: the hand-over names the module, its commit and the docs read.
2. **Declare the window.** One `process.lua` entry whose `meta.type` is `tui_desktop.window`, carrying a title, an outer `width` and `height` in cells (frame included), a menu `group`, an `image`, `resizable`, and for pixel support `pixel_render: chicago.shell.sdk:render` with `pixel_state` naming the same entry. Import the SDK as `app: chicago.shell.sdk:app` and attach the window policy the shell documents. The file ends by returning both `main` and the `definition` table, so tests can drive the same code. A module that uses another module's pictures or components declares it as a dependency by its GitHub component with a version range.
   Check: on a scratch desktop the window appears in the Start menu through the registry, with no hand-made menu list.
3. **Write `init`, `view` and `update`.** `view` is pure: no files, no messages, plain data out, a stable unique `id` on every interactive control. `update` returns false when nothing changed. Long work runs through the SDK's timers or channel watching, never blocking `update`. A close may be refused only through the SDK's stay call; `dispose` frees what the window took. A picture in the tree is PNG bytes, never a raster object: raster objects do not cross the process boundary. An inline PNG may be at most 1024×1024 pixels, and at most 1,400,000 characters once base64-encoded.
   Check: force an error in `update`; the window shows an error state with a way to close, instead of vanishing.
4. **Mind Lua numbers.** Lua 5.4 has integer and float subtypes of one number type. Pixel-to-cell arithmetic easily yields floats; integer format verbs refuse a float with a fraction, and the runtime's Lua has its own differences that the traps list names. Round sizes to whole cells before they are used or formatted.
   Check: a test at an odd size formats every count and size shown on screen.
5. **Read the size, never derive it.** The client area comes from `context.width` and `context.height` and changes with the mode: the cell theme and the pixel theme take different frames from the same outer size. The cell scrollbar needs three list rows; the pixel bar shows with fewer, so the two modes differ at small sizes. The SDK list scrolls 3 rows per wheel notch by default.
   Check: open the window in both modes at its declared size and at the smallest the frame allows; compare the client sizes and what each mode shows.
6. **Make the hard states visible.** An empty data set is its own label with a message (the SDK list with no items draws a blank field). Below a usable size, show a short «enlarge the window» message or a reduced view. Keep selection by item id; clamp the scroll offset after data changes.
   Check: in a test, replace long data by a few rows while scrolled to the end (offset 0, no gap); insert rows in front of the selection (same id selected); clear the data (the message is on the text screen).
7. **Drive it like the runtime does.** Synthetic events in tests copy the runtime's exact field values (for example, a letter key arrives with the runtime's own `key_type` spelling); a misspelt value is dropped without an error. Every input test asserts that the screen changed.
   Check: each key test fails when its key value is altered.
8. **Prove it with the module's harness.** Lint and tests run with the runtime build that has `gfx`, pointed to by the harness's `WIPPY` setting; run the narrowest test entry, full suites only for shared SDK changes. Text proof: the cell rows, a viewport snapshot or the compositor's screen command. Whole-state proof: the real compositor started inside a test on a viewport, the window opened and resized through it, both modes. Picture proof: the SDK's placement renderer or the theme's paint written to PNG. The process that paints the picture needs the same fonts and cell size as the compositor, or the picture comes out with a frame and no text while every assertion passes. Whole-program proof: the module's PTY probe script, with graphics forced off for a deterministic cell run.
   Check: downscale each PNG to at most 800 px JPEG and look at it next to the text screen of the same state; the hand-over lists the commands and their results.
9. **Try it live through the app's workshop over MCP.** Only on a scratch full app with its own ports and a throw-away account, never on a person's running desktop. Create an MCP credential that may use the workshop trait, connect, activate the trait (`app.workshop:trait`), then use the workshop tool: build the window from source with its imports and pixel renderer and open it; list windows; read its text screen; type keys; open it again at a small size; close it; remove the build. Read each answer's `success` and `error` fields: a refused build still comes back as a normal MCP result. Read the geometry back from the window list, since the size asked for can be adjusted. Building again under the same name replaces the stored window, but windows already open keep the old code until closed and reopened. The text screen is the client area; for pixel windows the proof stays a PNG from step 8.
   Check: the build answers live, the screen shows the expected text at both sizes, and after removal the stored list is empty and no probe window is left open.
10. **Use the right command path.** The base desktop's HTTP command channel looks for the stock desktop's name; a refusal from it while the Chicago shell is running is not proof that the desktop is down. Drive the Chicago desktop through the app's workshop or the PTY probe.
   Check: when a command path refuses, confirm the desktop state through a second path before reporting.

## Rules

- The compositor owns the frame, moving, sizing, focus and stacking. A window never writes control sequences and never enters the alternate screen.
- Focus loss reaches the window as a runtime event; the SDK drops armed buttons and drags. Do not keep your own armed state past it.
- Cells always work; pixels are an extra. A window that needs pixels says so in its declaration, and its text mode then shows only a caption.
- A shared SDK component or theme change is proposed to the module owner and the design system keeper, never shipped inside a window change.
- Never point a check at a person's running desktop, never push to the module repositories, never publish or tag.
- The module's own agent skills and docs win over this skill where they differ; report the difference.

## Checks before hand-over

- The module, commit and docs read.
- Start-menu discovery; both modes at declared and smallest size; long, empty and changed data; focus and key checks.
- Text screens and downscaled pictures of the same states; the harness commands with their results; the PTY probe output if the whole desktop was run.
- If the workshop was used: the scratch app, the calls made, and confirmation that the probe build was removed.

## Artefacts

- The window entry, its Lua and its tests in the module; the proof (commands, text screens, pictures) in the hand-over note, not in the module.

## Hand-over

- Look and style: ui designer; shared components and theme: design system keeper.
- Services, processes, module boundaries, dependencies and the lock: Lua developer (Wippy).
- The runtime's Go code (terminal service, graphics encoders, probe): Go developer, with a reproduction and the screen.
- A new component kind or SDK contract change: software architect and the module owner.
- Keyboard and focus reviews and any accessibility claim: accessibility engineer.
- Every change: reviewer. Tags and releases: release manager.

## Sources

This employee is a harnsy product, not an official product of these projects. Chicago and Wippy are named only to say which stack this skill works with.

Built on the shell module's window SDK guide and traps list, «docs/sdk.md» and «docs/traps.md» (github.com/chicago-desktop/shell, commit ceaebf5; © 2026 Wippy, MIT), adapted. Built on tui-desktop, «README»: windows in the registry, verification, PTY probe and the workshop endpoint (github.com/chicago-desktop/tui-desktop, commit d62ae9a; © 2026 Wippy, MIT), adapted. Built on the calculator module's declarations, «src/_index.yaml» (github.com/chicago-desktop/calculator, commit b45ab57; © 2026 Wippy, MIT), adapted. Built on the taskman window, «src/window.lua» (github.com/chicago-desktop/taskman, commit 51db4ff; © 2026 Wippy, MIT), adapted. Facts from the Wippy runtime's terminal and graphics code (github.com/wippyai/runtime, read at commit 7bcb546; wippyai, MPL-2.0); no text taken. Facts from the Lua 5.4 Reference Manual (lua.org/manual/5.4/; Lua.org, PUC-Rio, Lua license); no text taken.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
