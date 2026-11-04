---
name: tui-layout-render
description: Lay out a terminal screen in whole cells and make it behave - one layout used for both drawing and hit tests, scrolling that survives resize and data change, selection kept by item id, focus and keys, widgets with every state (empty, error, too small included), redraw of only what changed, pixel detail kept inside cell rectangles, and proof at three levels plus a picture. Stack-neutral. Use when building or fixing windows, panes or widgets that live in a terminal grid.
---

# Terminal layout and rendering

A terminal screen is a grid of cells, and everything a person sees or clicks has to land on whole cells. The common failures are quiet: a click one cell off from what is drawn, a list that scrolls into blank space after the data shrinks, a selection that jumps to another item when rows are added, a test suite that passes while the picture is empty. This skill builds the screen so that each of these has a check.

**Route:** terminal-io settles what the terminal can do → **tui-layout-render** builds and checks what goes in the cells → on the worked stack, chicago-shell-window adds that stack's own contract.
Before this skill: the size comes from the host, never from a guess. After it: a layout, widgets with all their states, and proof from text screens and pictures.

## When to use

- A new window, pane or widget in a terminal program.
- Clicks land on the wrong control; a list shows blank rows or jumps; a resize breaks the screen.
- Redraw is slow, or the screen flickers.
- Not for terminal probing, protocols or input decoding: that is terminal-io.

## Inputs

- The content area the host gives you, in cells, on start and on every resize. Frames, borders and themes may take a different amount per mode, so the content area is read, never derived from an outer size.
- The design from the ui designer, if there is one: what goes where, and the look.
- The data, including its smallest case (zero items).

## Steps

1. **Plan in cells.** Describe the screen as nested rows and columns with fixed and flexible parts, padding and gaps counted in cells. Rectangles use one convention for the whole program (for example, 1-based, right and bottom edges excluded); write it down. Pixel sizes are rounded to whole cells before they reach the plan.
   Check: compute the plan at the intended size and at every size down to 1×1. No error; the number of rows equals the height; no row is wider than the width.
2. **One plan for drawing and hits.** The same pure function places a control for the painter and for the hit test. Two separate calculations drift by a cell and nothing fails.
   Check: in a test, press at the centre of every interactive rectangle from the plan and assert the action names that control.
3. **Scroll as an offset of hidden rows.** The offset starts at 0 and is clamped again after anything that changes the rows or the room for them: resize, filter, new data, tab change, zoom. With no items the offset is 0. The wheel scrolls the pane under the pointer, not the focused one. The scrollbar and its drag handler use one thumb calculation. A cell scrollbar needs at least three rows (two arrows and a thumb); below that, show none and keep keys working.
   Check: scroll to the end, shrink the data below one page; the offset is 0 and there is no blank gap. Wheel over another pane; this pane's offset does not move. Drag the thumb past the window edge and release there; the drag ends.
4. **Hold selection by item id.** Store which item is selected, not which row. When rows are inserted above, the same item stays selected; whether to scroll it into view is a decision, made on purpose.
   Check: select an item, insert rows in front of it; the model still holds the same id.
5. **Focus and keys.** Tab and Shift+Tab move through controls in the order of the plan; arrows move inside a widget; Enter or Space activate. Every action reachable by mouse is also reachable by keys, and the focused control is visibly marked in every mode.
   Check: from the first control, Tab reaches every control and comes back; each shows a visible focus mark in the text screen and in the picture.
6. **Pointer capture and focus loss.** A press captures the pointer until release, even outside the window. Losing focus cancels anything armed or being dragged. Key release never triggers an action.
   Check: press a button, move out, release; nothing activates. Take focus away mid-press, give it back, release; nothing activates. Send a key release alone; nothing happens.
7. **Every state is drawn with words.** Normal, focused, selected, disabled, loading, empty, error, and too small. An empty list is its own element with a message (a bare list with no items is a blank field, which reads as broken). An error says what failed and what to do. When the area is too small for the content to work, show a short message or a reduced view, never half a control.
   Check: one text screen and one picture per state, at the smallest size, with a long list and with an empty one.
8. **Redraw only what changed.** Give rows, strips or picture placements stable keys; the same state twice draws nothing; moving a selection redraws the rows it touches; a resize redraws everything. Overlays (menus, tooltips) are drawn last and hit-tested first. Picture placements are listed completely each frame, keep their ids while unchanged, do not overlap inside one window, and are re-rasterised only when their content changed.
   Check: count redrawn rows or placements for: same state, one selection move, a resize. Measure frame time before and after any speed change; state where it was measured.
9. **Pixel detail stays inside cell rectangles.** In pixel mode, decoration and pictures are drawn inside the cell rectangles of the plan; the pointer still speaks cells. A character the pixel font lacks advances like a blank, so icons and arrows in pixel mode come from pictures or drawn shapes, not from font characters.
   Check: the picture and the text screen of one state show the same rows in the same places; every icon is visible in the picture.
10. **Prove it at three levels, and look.** (a) Parts: the pure plan and hit tests. (b) Whole state: the real host or compositor running inside a test, driven by events, read back as a text screen. (c) Whole look: a rendered picture. The three cannot see each other's faults. Then run the whole program in a PTY probe for keys, mouse and resize. The process that paints the test picture must be set up like the real painter (fonts, cell size): a picture with a frame and no text can pass every assertion.
   Check: downscale each picture to at most 800 px JPEG and look at it; compare it with the text screen of the same state. The hand-over lists which levels ran and names any level that did not.

## Rules

- The content area is given, never assumed; check every mode the program offers at the smallest size, since modes can give different areas for the same outer size.
- A test that sends an input checks that the screen changed, not that sending succeeded.
- A function nobody calls is green in every suite: for each new handler, a test reaches it through the real input path.
- Keyboard reach and a visible focus mark are part of done. Screen-reader support and accessibility audits are not promised here; they go to the accessibility engineer.
- Shared widgets and styles belong to their owner: propose a change, do not ship it alone.

## Checks before hand-over

- Plan checks from 1×1 to the intended size, both modes.
- Scroll, selection, focus, capture and every state from the steps, with their results.
- Redraw counts for same state, one change and resize.
- Text screens and downscaled pictures at the intended and the smallest size, with long and empty data.

## Artefacts

- Layout, widget and test code; the text screens and pictures of the checks (kept out of the product unless asked); a short hand-over note: what changed, which checks ran, what is left.

## Hand-over

- Look, colour, type and spacing: ui designer; a change to shared components or tokens: design system keeper.
- Keyboard and focus reviews beyond your own checks, and any accessibility claim: accessibility engineer.
- A new component kind or a contract change between host and windows: software architect and the module's owner.
- Every change: reviewer. Tags and releases: release manager.

## Sources

This employee is a harnsy product, not an official product of these projects.

Built on the shell module's window SDK guide and traps list, «docs/sdk.md» and «docs/traps.md» (github.com/chicago-desktop/shell, commit ceaebf5; © 2026 Wippy, MIT), adapted. Built on tui-desktop, «README»: frame order, pixel chrome, frame cost and verification levels (github.com/chicago-desktop/tui-desktop, commit d62ae9a; © 2026 Wippy, MIT), adapted. Built on the taskman window, «src/window.lua»: too-small state, columns, selection by id (github.com/chicago-desktop/taskman, commit 51db4ff; © 2026 Wippy, MIT), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
