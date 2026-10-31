---
name: terminal-io
description: Talk to a real terminal safely - find out what it can do by asking it (graphics protocol, cell size in pixels), pick Kitty graphics, Sixel or plain cells with a named reason, send and remove pictures without stray text, decode keys, mouse, focus and paste into one event shape, and leave the terminal as it was found. Stack-neutral. Use when a program draws to a terminal, reads its input or shows pictures in it.
---

# Terminal input and output

A terminal answers questions, but only when asked in the right order, and it stays silent when it does not understand. Most terminal bugs are silent: a picture that never appears, a key that never arrives, a mouse that stops selecting text. This skill covers the edge where a program meets the terminal: what to ask, what to send, what comes back, and how to check each part.

**Route:** a task that reads input from a terminal or draws to it → **terminal-io** for the edge → **tui-layout-render** for what goes inside the cells.
Before this skill: the program that owns the terminal is known (one owner at a time). After it: a probe result, a chosen output path with its reason, and a decoder that turns bytes into events.

## When to use

- A program starts in a terminal and must decide between pictures and cells.
- Pictures appear in the wrong size, stay after they should be gone, or never appear.
- Keys, mouse, wheel, focus or paste behave differently from one terminal to another.
- The terminal is left broken after the program exits or crashes.
- Not for layout, widgets or redraw logic: that is tui-layout-render.

## Inputs

- Which process owns the terminal. Only that one writes control sequences; a window or widget hosted inside another program never does.
- How the program runs: a local terminal, over ssh, under a multiplexer, in a pipe or a test.
- An explicit graphics setting, if the person gave one (a flag or an environment variable of the program).

## Steps

1. **Probe in one write, at start.** Send the Kitty graphics query (action `a=q` with a one-pixel image), the two size requests (`CSI 16 t` for one cell in pixels, `CSI 14 t` for the text area in pixels), and then Primary Device Attributes (`CSI c`) as the last item. Every terminal answers the attributes request, so its answer marks the end of the replies. Wait a short, fixed time (a few hundred milliseconds), not forever.
   Check: run once in a pipe or a test with no terminal behind it. The result must say «no answer», which is different from «answered: no graphics».
2. **Read the answers.** A graphics reply before the attributes reply means Kitty graphics works. Parameter `4` in the attributes reply means Sixel. The cell size comes from `CSI 16 t`, or from `CSI 14 t` divided by the grid size; terminals answer one or the other, so ask both.
   Check: log the parsed answers once in debug output, never on the screen you draw.
3. **Choose the output path, with a reason.** Order: an explicit setting from the person, then the terminal's own answer, then guesses from environment variables. Guesses are often wrong over ssh and inside multiplexers, so they come last. Prefer Kitty graphics when both answer: images have ids and can be replaced or deleted by id. Sixel has no ids. Cells are the fallback, always complete on their own.
   Check: force «off» and confirm the cell view is complete. Force each protocol on in a terminal that has it and confirm the picture appears. «Off» shows or logs its reason (setting, no answer, no protocol), never a silent switch.
4. **Send Kitty pictures in pieces.** The pixel data goes base64-encoded in an APC sequence (`ESC _ G <keys> ; <data> ESC \`). Each piece carries at most 4096 bytes of base64; all pieces but the last carry `m=1`. Place at the cursor, scale into a number of cells (`c`, `r`), keep the cursor still while placing (`C=1`), and use `z` for stacking (below zero draws under text). Delete with `a=d` and a selector: a lowercase selector removes the placement and keeps the data, uppercase frees the data too.
   Check: place, move and remove one picture. No base64 shows as text, the cursor ends where it started, nothing scrolls.
5. **Send Sixel with care.** Sixel is a DCS sequence that paints six pixel rows per band. The picture's size and position are fixed when it is encoded, so a change in cell size or position needs a new encoding. A picture near the bottom row can scroll the screen; mode 80 (`CSI ? 80 h/l`) switches that scrolling behaviour. Removal means drawing the cells again. Encoding is slow (on the order of a hundred nanoseconds per pixel), so cache encodings by content and size.
   Check: draw a picture in the last rows; the screen does not move. Remove it; the cells under it are drawn again.
6. **Clear pictures on purpose.** Clearing the whole screen or switching to the alternate screen removes pictures; erasing lines or characters does not.
   Check: after a view change, no old picture stays on screen.
7. **Turn on only the input modes you use.** Mouse: 1000 (press and release), 1002 (motion while a button is down), 1003 (all motion), 1006 (coordinates as decimal numbers, needed past column 223). Focus reports: 1004 (`ESC [ I`, `ESC [ O`). Bracketed paste: 2004. Alternate screen: 1049. While mouse reporting is on, the person's own text selection needs a modifier (usually Shift); say so in the help text.
   Check: list the modes the program turns on, and match each to a feature.
8. **Decode once, into one event shape.** Keys, mouse, wheel, resize, focus and paste become one kind of event with fixed field names and values: key name, modifiers, press or release; button, action, cell position. Coordinates in one base for the whole program (state which). Release is never treated as a press.
   Check: a scripted terminal (a PTY probe) sends a click, a drag, two wheel notches, a paste and a resize; the parsed events match a written list exactly.
9. **Leave the terminal as found.** Turn every mode off again, leave the alternate screen, show the cursor. Do this on normal exit, on error and on a kill signal where the language allows it.
   Check: kill the program inside a PTY probe; the shell prompt afterwards echoes typed text and the mouse selects text again.

## Rules

- One process owns the terminal. Log lines printed to the same terminal break a diffed frame: send logs to a file or another stream.
- Never trust a guess over an answer, and never trust silence as «no»: silence means nobody answered.
- A fallback is named. Drawing a picture at the wrong size because a cell size was guessed is worse than drawing cells.
- Synthetic events in tests use the exact field names and values the real decoder produces. A misspelt key name is usually dropped without any error. Check: after sending an event, assert that the screen changed, not only that sending returned ok.
- Cut sequences must never leak: when clipping drawn output at a cell boundary, cut between sequences, never inside one.
- Pixel support is a feature of some terminals, not a promise. Do not promise pictures over every connection.

## Checks before hand-over

- Probe results for the terminals tried, including one run with no terminal answering.
- The forced-off run: the cell view is complete.
- The PTY-probe run for input events, with the expected and the parsed list.
- The kill test: the terminal is usable afterwards.

## Artefacts

- The probe and decoder code with tests; the list of modes turned on and why; the PTY-probe script and its output.

## Hand-over

- Layout, widgets and redraw: tui-layout-render.
- A bug in a runtime's own terminal or graphics code that you do not own: to the Go developer (or the owner of that runtime), with the bytes sent, the terminal's reply and the screen.
- A choice of protocol or terminal support that is hard to undo for the product: to the software architect.

## Sources

This employee is a harnsy product, not an official product of these projects.

Built on tui-desktop, «README»: probe, host and verification sections (github.com/chicago-desktop/tui-desktop, commit d62ae9a; © 2026 Wippy, MIT), adapted. Facts from the Kitty terminal graphics protocol (sw.kovidgoyal.net/kitty/graphics-protocol/, read 2026-10-21; Kovid Goyal, GPL-3.0); no text taken. Facts from the control sequences reference maintained by Thomas Dickey (invisible-island.net, «ctlseqs», read 2026-10-21; no licence stated); no text taken. Facts from ECMA-48, «Control functions for coded character sets», 5th edition (ecma-international.org, © Ecma International); no text taken. Facts from the VT330/VT340 Programmer Reference Manual, chapter 14 «Sixel Graphics» (vt100.net/docs/vt3xx-gp/chapter14.html; © Digital Equipment Corporation); no text taken. Facts from the Wippy runtime's terminal probe and graphics code (github.com/wippyai/runtime, read at commit 7bcb546; wippyai, MPL-2.0); no text taken.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
