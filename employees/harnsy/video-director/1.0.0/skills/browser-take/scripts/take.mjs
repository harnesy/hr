#!/usr/bin/env node
// Copyright (c) 2026 Pavel Buchnev (harnsy)
// SPDX-License-Identifier: MIT
//
// take.mjs: record one scripted take of a web product, shot by shot, from a shot file (JSON).
// Playwright drives a Chromium page; a CDP screencast saves every frame with its timestamp.
// A soft cursor is drawn by the page (headless has none). Every shot is padded to its end
// boundary from the shot file, so caption cues and chapters can use the same numbers.
// A shot that runs past its boundary prints WARN; the take is then not usable as it is.
//
// Output: <out>/frames/*.jpg, <out>/frames.json (frame times, shot marks, target boundaries,
// warnings) and <out>/texts.json (the page's visible text at each shot start and end, for
// check-frames.py). Next: check-frames.py <out>, then the video-post skill.
//
// Run with --help for the options. The shot file format is in shots.example.json and SKILL.md («Tools»).

import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';

const HELP = `usage: node take.mjs --shots <shots.json> --out <dir> [options]

Records a scripted take: frames + frames.json, ready for assemble.py.

options:
  --shots FILE        shot file (JSON), required
  --out DIR           output directory, required (frames/ and frames.json go here)
  --base-url URL      base URL of the demo stand; overrides "baseUrl" in the shot file
  --viewport WxH      e.g. 1440x900; overrides "viewport" (default 1440x900)
  --scale N           device scale factor (default 1)
  --color-scheme S    dark | light | no-preference; overrides "colorScheme"
  --locale L          browser locale, e.g. en-US; overrides "locale"
  --quality N         JPEG quality of the screencast frames, 1-100 (default 92)
  --zoom N            push-in scale used by "zoom" actions (default 1.25; 1 = never zoom)
  --until ID          stop after the shot with this id (for smoke runs)
  --browser PATH      Chromium/Chrome binary (default: Playwright's own Chromium)
  --playwright SPEC   module to import: a package name or a path to its index.mjs
                      (default: try "playwright", then "playwright-core")
  --allow-exec        let "exec" actions run local commands (off by default)
  --headed            show the browser window (for rehearsal; still records)
  -h, --help          this text

Values on the command line win over the shot file.`;

let args;
try {
  args = parseArgs({
    options: {
      shots: { type: 'string' }, out: { type: 'string' }, 'base-url': { type: 'string' },
      viewport: { type: 'string' }, scale: { type: 'string' }, 'color-scheme': { type: 'string' },
      locale: { type: 'string' }, quality: { type: 'string' }, zoom: { type: 'string' },
      until: { type: 'string' }, browser: { type: 'string' }, playwright: { type: 'string' },
      'allow-exec': { type: 'boolean' }, headed: { type: 'boolean' }, help: { type: 'boolean', short: 'h' },
    },
  }).values;
} catch (e) {
  console.error(String(e.message || e)); console.error(HELP); process.exit(2);
}
if (args.help) { console.log(HELP); process.exit(0); }
if (!args.shots || !args.out) { console.error(HELP); process.exit(2); }

// ---- configuration ------------------------------------------------------------------------------------------------
const cfg = JSON.parse(fs.readFileSync(args.shots, 'utf8'));
const OUT = args.out;
const BASE = args['base-url'] || cfg.baseUrl;
if (!BASE) { console.error('no base URL: set "baseUrl" in the shot file or pass --base-url'); process.exit(2); }
const [VW, VH] = (args.viewport || (cfg.viewport ? `${cfg.viewport.width}x${cfg.viewport.height}` : '1440x900'))
  .split('x').map(Number);
if (!(VW > 0 && VH > 0)) { console.error('bad --viewport, expected WxH'); process.exit(2); }
const SCALE = Number(args.scale || cfg.deviceScaleFactor || 1);
const COLOR = args['color-scheme'] || cfg.colorScheme || 'no-preference';
const LOCALE = args.locale || cfg.locale || undefined;
const QUALITY = Number(args.quality || cfg.jpegQuality || 92);
const ZOOM = Number(args.zoom || cfg.zoom || 1.25) || 1;
const ZOOM_ROOT = cfg.zoomRoot || 'body';
const CURSOR = cfg.cursor !== false;
const shots = cfg.shots || [];
if (!shots.length) { console.error('the shot file has no "shots"'); process.exit(2); }

// Shot boundaries: B[0] = 0, B[k] = end of shot k. A shot gives "end" (absolute seconds) or "duration".
const B = [0];
for (const s of shots) {
  const end = s.end != null ? Number(s.end) : B.at(-1) + Number(s.duration);
  if (!(end > B.at(-1))) { console.error(`shot ${s.id}: end ${end} is not after ${B.at(-1)}`); process.exit(2); }
  B.push(end);
}
let LAST = shots.length;
if (args.until) {
  const i = shots.findIndex(s => String(s.id) === args.until);
  if (i < 0) { console.error(`--until: no shot with id ${args.until}`); process.exit(2); }
  LAST = i + 1;
}

// ---- Playwright -----------------------------------------------------------------------------------------------------
async function loadPlaywright() {
  const tries = args.playwright ? [args.playwright] : ['playwright', 'playwright-core'];
  for (const spec of tries) {
    try {
      const m = await import(spec.includes('/') ? path.resolve(spec) : spec);
      return m.chromium ? m : m.default;
    } catch { /* try the next one */ }
  }
  console.error(`cannot import Playwright (${tries.join(', ')}). Install it (npm i playwright) or pass --playwright <path to index.mjs>.`);
  process.exit(2);
}
const { chromium } = await loadPlaywright();

fs.mkdirSync(path.join(OUT, 'frames'), { recursive: true });
const browser = await chromium.launch({ headless: !args.headed, ...(args.browser ? { executablePath: args.browser } : {}) });
const ctx = await browser.newContext({
  viewport: { width: VW, height: VH }, deviceScaleFactor: SCALE, colorScheme: COLOR,
  ...(LOCALE ? { locale: LOCALE } : {}),
});

// Storage the shot file asks for (e.g. a closed panel, a dismissed hint), set before every page load.
await ctx.addInitScript(([store, cursor, vw, vh]) => {
  try { for (const [k, v] of Object.entries(store || {})) localStorage.setItem(k, typeof v === 'string' ? v : JSON.stringify(v)); } catch {}
  if (!cursor) return;
  // The soft cursor sits on <html>, outside the zoom root, so a push-in never scales it.
  const add = () => {
    if (document.getElementById('__vr_cursor')) return;
    const c = document.createElement('div');
    c.id = '__vr_cursor';
    c.innerHTML = '<svg width="22" height="22" viewBox="0 0 24 24"><path d="M4 2l15 9-7 1.5L9 20z" fill="#f2f3f5" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>';
    Object.assign(c.style, {
      position: 'fixed', left: Math.round(vw * 0.75) + 'px', top: Math.round(vh * 0.7) + 'px', zIndex: 2147483647,
      pointerEvents: 'none', transition: 'left .7s cubic-bezier(.16,1,.3,1), top .7s cubic-bezier(.16,1,.3,1), transform .12s',
      filter: 'drop-shadow(0 1px 2px rgba(0,0,0,.6))',
    });
    document.documentElement.appendChild(c);
  };
  if (document.readyState === 'loading') window.addEventListener('DOMContentLoaded', add); else add();
}, [cfg.localStorage, CURSOR, VW, VH]);

const p = await ctx.newPage();
const cdp = await ctx.newCDPSession(p);
const frames = [];
cdp.on('Page.screencastFrame', async f => {
  const i = frames.length;
  frames.push(f.metadata.timestamp);
  fs.writeFileSync(path.join(OUT, 'frames', `${String(i).padStart(5, '0')}.jpg`), Buffer.from(f.data, 'base64'));
  await cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }).catch(() => {});
});
const wait = ms => p.waitForTimeout(ms);
const warnings = [];
const warn = s => { warnings.push(s); console.warn('WARN', s); };

// ---- timing ---------------------------------------------------------------------------------------------------------
let T0 = 0;
const marks = [];
const now = () => Date.now() / 1000 - T0;
const mark = n => marks.push([n, Date.now() / 1000]);
async function until(at, what = '') {
  const left = at - now();
  if (left > 0) await wait(left * 1000);
  else if (left < -0.05) warn(`${what || 'step'} due at ${at.toFixed(2)} s ran ${(-left).toFixed(2)} s late`);
}

// ---- targets: role+name, text, label, placeholder, test id or (last resort) a CSS selector -------------------------
function locate(t) {
  if (!t) throw new Error('action has no target');
  const exact = t.exact ?? false;
  let loc;
  if (t.role) loc = p.getByRole(t.role, t.name != null ? { name: t.name, exact } : {});
  else if (t.label) loc = p.getByLabel(t.label, { exact });
  else if (t.placeholder) loc = p.getByPlaceholder(t.placeholder, { exact });
  else if (t.testId) loc = p.getByTestId(t.testId);
  else if (t.text) loc = p.getByText(t.text, { exact });
  else if (t.selector) loc = p.locator(t.selector);
  else throw new Error('target needs role, label, placeholder, testId, text or selector');
  if (t.hasText) loc = loc.filter({ hasText: t.hasText });
  return t.nth != null ? loc.nth(t.nth) : loc.first();
}
const targetOf = a => a.target || a;
const describe = a => JSON.stringify(a.target || Object.fromEntries(Object.entries(a).filter(([k]) => k !== 'do')));

// ---- cursor ----------------------------------------------------------------------------------------------------------
async function moveTo(x, y) {
  await p.evaluate(([x, y]) => { const c = document.getElementById('__vr_cursor'); if (c) { c.style.left = x + 'px'; c.style.top = y + 'px'; } }, [x, y]);
}
async function point(loc, settle) {
  await loc.scrollIntoViewIfNeeded({ timeout: 5000 });
  const r = await loc.boundingBox();
  if (!r) throw new Error('not visible');
  await moveTo(r.x + Math.min(r.width * 0.3, 60), r.y + r.height / 2);
  await wait(settle);
}
async function press() {
  await p.evaluate(() => { const c = document.getElementById('__vr_cursor'); if (c) { c.style.transform = 'scale(.85)'; setTimeout(() => { c.style.transform = ''; }, 140); } });
}
// Park the real pointer in a corner: no stray :hover when the layout moves under it.
const park = () => p.mouse.move(VW - 3, VH - 3);

// ---- push-in: a CSS transform on the zoom root; text stays sharp, the cursor (on <html>) is not scaled -------------
async function zoomIn(box, scale, ms) {
  if (scale <= 1 || !box) return;
  box = { x: box.x - 24, y: box.y - 16, width: box.width + 48, height: box.height + 32 };
  const origin = (a1, a2, L) => {
    const lo = (scale * a2 - L) / (scale - 1), hi = scale * a1 / (scale - 1);
    const o = lo <= hi ? Math.min(Math.max((a1 + a2) / 2, lo), hi) : hi;
    return Math.min(Math.max(o, 0), L);
  };
  const ox = origin(box.x, box.x + box.width, VW), oy = origin(box.y, box.y + box.height, VH);
  await p.evaluate(([sel, ox, oy, s, ms]) => {
    const a = document.querySelector(sel); if (!a) return;
    a.style.transformOrigin = `${ox}px ${oy}px`;
    a.style.transition = `transform ${ms}ms cubic-bezier(.4,0,.2,1)`;
    a.style.transform = `scale(${s})`;
  }, [ZOOM_ROOT, ox, oy, scale, ms]);
  await wait(ms + 50);
}
async function zoomOut(ms) {
  await p.evaluate(([sel, ms]) => { const a = document.querySelector(sel); if (a) { a.style.transition = `transform ${ms}ms cubic-bezier(.4,0,.2,1)`; a.style.transform = ''; } }, [ZOOM_ROOT, ms]);
  await wait(ms + 50);
}

// ---- on-screen label: honest notes such as "sample data" or "sped up" ----------------------------------------------
async function label(text, corner = 'top-right') {
  await p.evaluate(([text, corner]) => {
    let el = document.getElementById('__vr_label');
    if (!text) { el?.remove(); return; }
    if (!el) { el = document.createElement('div'); el.id = '__vr_label'; document.documentElement.appendChild(el); }
    el.textContent = text;
    const [v, h] = corner.split('-');
    Object.assign(el.style, {
      position: 'fixed', top: '', bottom: '', left: '', right: '', [v]: '16px', [h]: '16px', zIndex: 2147483646,
      font: '600 14px/1.2 system-ui, sans-serif', color: '#fff', background: 'rgba(0,0,0,.72)',
      padding: '6px 10px', borderRadius: '6px', pointerEvents: 'none',
    });
  }, [text, corner]);
}

// ---- actions ----------------------------------------------------------------------------------------------------------
async function run(a, base) {
  if (a.at != null) await until(base + Number(a.at), `${a.do} (${describe(a)})`);
  const settle = a.settle ?? 600;
  switch (a.do) {
    case 'goto': await p.goto(new URL(a.url || '/', BASE).href, { waitUntil: a.waitUntil || 'load' }); break;
    case 'point': case 'hover': await point(locate(targetOf(a)), settle); if (a.do === 'hover') await locate(targetOf(a)).hover(); break;
    case 'click': {
      const loc = locate(targetOf(a));
      if (CURSOR) { await point(loc, settle); await press(); }
      await loc.click(); await park(); await wait(a.after ?? 400); break;
    }
    case 'type': {
      const loc = locate(targetOf(a));
      if (CURSOR) await point(loc, settle);
      await loc.click(); await loc.pressSequentially(String(a.text ?? ''), { delay: a.delay ?? 70 }); break;
    }
    case 'press': await p.keyboard.press(a.key); break;
    case 'wait':
      if (a.ms != null) await wait(Number(a.ms));
      else await locate(targetOf(a)).waitFor({ state: a.state || 'visible', timeout: a.timeout ?? 10000 });
      break;
    case 'waitText': await p.waitForFunction(re => new RegExp(re).test(document.body.innerText), a.pattern, { timeout: a.timeout ?? 10000 }); break;
    case 'hold': await wait(Number(a.ms ?? 1000)); break;
    case 'scroll': await p.mouse.move(VW / 2, VH / 2); await p.mouse.wheel(0, Number(a.dy ?? 300)); await wait(a.after ?? 400); break;
    case 'zoom': await zoomIn(await locate(targetOf(a)).boundingBox(), Number(a.scale ?? ZOOM), a.ms ?? 800); break;
    case 'unzoom': await zoomOut(a.ms ?? 400); break;
    case 'label': await label(a.text, a.corner); break;
    case 'blur': // hide an incidental detail (a version string, a clock); never use it to change what the product shows
      await locate(targetOf(a)).evaluate((el, px) => { el.style.filter = `blur(${px}px)`; }, a.px ?? 6); break;
    case 'cursor': await moveTo(Number(a.x), Number(a.y)); await wait(settle); break;
    case 'exec':
      if (!args['allow-exec']) throw new Error('exec needs --allow-exec');
      execFileSync(a.cmd[0], a.cmd.slice(1), { stdio: 'inherit', timeout: (a.timeout ?? 30) * 1000 }); break;
    default: throw new Error(`unknown action "${a.do}"`);
  }
}
async function runList(list, base, where) {
  for (const a of list || []) {
    try { await run(a, base); } catch (e) {
      const msg = `${where}: ${a.do} ${describe(a)}: ${String(e.message || e).split('\n')[0]}`;
      if (a.optional) warn(msg); else throw new Error(msg);
    }
  }
}

// ==================================================================================================================
// Prelude, off camera: open the start page, set the scene, wait for the ready signal.
await p.goto(new URL(cfg.start || '/', BASE).href, { waitUntil: 'load' });
await runList(cfg.prelude, 0, 'prelude');
if (cfg.ready) await locate(cfg.ready).waitFor({ timeout: cfg.ready.timeout ?? 30000 });
if (CURSOR) await moveTo(Math.round(VW * 0.75), Math.round(VH * 0.7));
await park();
await wait(800);

await cdp.send('Page.startScreencast', { format: 'jpeg', quality: QUALITY, maxWidth: VW * SCALE, maxHeight: VH * SCALE, everyNthFrame: 1 });
// A still page sends no frames; a 1px heartbeat keeps the screencast ticking.
await p.evaluate(() => {
  const h = document.createElement('div');
  Object.assign(h.style, { position: 'fixed', right: 0, bottom: 0, width: '1px', height: '1px', opacity: 0.01, pointerEvents: 'none', zIndex: 2147483647 });
  document.documentElement.appendChild(h);
  let k = 0; setInterval(() => { h.style.background = (k++ % 2) ? '#000' : '#010101'; }, 33);
});
await wait(300);
T0 = Date.now() / 1000;

// The visible text of the page (and its URL) at each shot start and end, for the privacy check.
const texts = [];
const snap = async (shot, when) => {
  try { texts.push({ shot, when, url: p.url(), text: await p.evaluate(() => document.body.innerText) }); } catch {}
};
async function takeShots() {
  for (let k = 0; k < LAST; k++) {
    const s = shots[k];
    await until(B[k], k ? `end of shot ${shots[k - 1].id}` : 'start');
    mark(String(s.id));
    console.log(`shot ${s.id} @${now().toFixed(2)} s${s.title ? ' · ' + s.title : ''}`);
    await snap(String(s.id), 'start');
    await runList(s.actions, B[k], `shot ${s.id}`);
    await snap(String(s.id), 'end');
  }
}
await takeShots().catch(e => warn(`take stopped: ${String(e.message || e).split('\n')[0]}`));
await until(B[LAST], 'end of the take');
mark('stop');
await cdp.send('Page.stopScreencast');
await wait(300);

// Targets: the planned start of every shot that was marked, then the planned end of the take.
const targets = [...B.slice(0, marks.length - 1), B[LAST]];
fs.writeFileSync(path.join(OUT, 'frames.json'), JSON.stringify({
  frames, marks, targets, warnings,
  shots: shots.slice(0, LAST).map(s => ({ id: String(s.id), title: s.title || '' })),
  viewport: { width: VW, height: VH, scale: SCALE },
}));
fs.writeFileSync(path.join(OUT, 'texts.json'), JSON.stringify(texts, null, 1));
const t0 = marks[0][1];
console.log('frames', frames.length, frames.length ? `span ${(frames.at(-1) - frames[0]).toFixed(1)} s` : '');
console.log(marks.map(([n, t], i) => `${n} @${(t - t0).toFixed(2)} s (target ${targets[i].toFixed(2)})`).join('\n'));
if (warnings.length) console.log(`${warnings.length} warning(s): read them before accepting the take`);
await browser.close();
process.exit(warnings.length ? 3 : 0);
