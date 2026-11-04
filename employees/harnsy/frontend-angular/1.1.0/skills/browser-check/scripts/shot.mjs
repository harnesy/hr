#!/usr/bin/env node
// SPDX-License-Identifier: MIT
// Copyright (c) 2026 Pavel Buchnev (harnsy)
//
// Screenshot a local page at a desktop and a phone width and report what the
// browser complained about.
//
//   node shot.mjs <url> <out-dir> [--color-scheme light|dark] [--wait <ms>]
//
// <url> must be http(s)://localhost, http(s)://127.0.0.1, http(s)://[::1] or file://.
// Every request to another origin is aborted, service workers are blocked, and
// each width gets a fresh browser context (no profile, no cookies, no sessions).
//
// Writes <out-dir>/desktop-1440.png, <out-dir>/mobile-390.png and <out-dir>/report.json.
// Exit codes: 0 no errors, 1 errors found (console errors, page errors, failed
// requests or HTTP errors on the local origin), 2 could not run.
//
// Needs Playwright with a Chromium build installed by the person
// (`npm i -D playwright` and `npx playwright install chromium`); this script installs nothing.

import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const VIEWPORTS = [
  { name: 'desktop-1440', width: 1440, height: 900 },
  { name: 'mobile-390', width: 390, height: 844 },
];
const LOCAL_HOSTS = new Set(['localhost', '127.0.0.1', '[::1]']);

function usage(msg) {
  if (msg) console.error(msg);
  console.error('usage: node shot.mjs <url> <out-dir> [--color-scheme light|dark] [--wait <ms>]');
  process.exit(2);
}

function parseArgs(argv) {
  const pos = [];
  const opts = { colorScheme: 'light', waitMs: 0 };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--color-scheme') {
      const v = argv[++i];
      if (v !== 'light' && v !== 'dark') usage('--color-scheme must be light or dark');
      opts.colorScheme = v;
    } else if (a === '--wait') {
      const v = Number(argv[++i]);
      if (!Number.isInteger(v) || v < 0 || v > 120000) usage('--wait must be 0..120000 ms');
      opts.waitMs = v;
    } else if (a === '-h' || a === '--help') {
      usage();
    } else if (a.startsWith('--')) {
      usage(`unknown option ${a}`);
    } else {
      pos.push(a);
    }
  }
  if (pos.length !== 2) usage();
  return { url: pos[0], outDir: pos[1], ...opts };
}

function checkUrl(raw) {
  let u;
  try {
    u = new URL(raw);
  } catch {
    usage(`not a URL: ${raw}`);
  }
  if (u.protocol === 'file:') return u;
  if ((u.protocol === 'http:' || u.protocol === 'https:') && LOCAL_HOSTS.has(u.hostname)) {
    if (u.username || u.password) usage('refusing a URL with credentials in it');
    return u;
  }
  usage(`refusing ${raw}: only localhost, 127.0.0.1, [::1] or file:// URLs are allowed`);
}

function allowed(target, base) {
  let t;
  try {
    t = new URL(target);
  } catch {
    return false;
  }
  if (t.protocol === 'data:' || t.protocol === 'blob:') return true;
  if (base.protocol === 'file:') return t.protocol === 'file:';
  return t.origin === base.origin;
}

async function loadPlaywright() {
  try {
    return await import('playwright');
  } catch {
    console.error('Playwright is not installed. Ask the person to install it ' +
      '(for example `npm i -D playwright` and `npx playwright install chromium`).');
    process.exit(2);
  }
}

async function shoot(browser, base, vp, opts, outDir) {
  const result = {
    viewport: `${vp.width}x${vp.height}`,
    screenshot: `${vp.name}.png`,
    console: [],
    pageErrors: [],
    failedRequests: [],
    httpErrors: [],
    blockedRequests: [],
    horizontalOverflow: null,
  };
  const context = await browser.newContext({
    viewport: { width: vp.width, height: vp.height },
    deviceScaleFactor: 1,
    colorScheme: opts.colorScheme,
    serviceWorkers: 'block',
    acceptDownloads: false,
  });
  const blocked = new Set();
  await context.route('**/*', (route) => {
    const u = route.request().url();
    if (allowed(u, base)) return route.continue();
    blocked.add(u);
    result.blockedRequests.push(u);
    return route.abort('blockedbyclient');
  });
  if (typeof context.routeWebSocket === 'function') {
    await context.routeWebSocket(/.*/, (ws) => {
      if (allowed(ws.url().replace(/^ws/, 'http'), base)) ws.connectToServer();
      else {
        result.blockedRequests.push(ws.url());
        ws.close();
      }
    });
  }
  const page = await context.newPage();
  page.on('console', (msg) => {
    const type = msg.type();
    if (type === 'error' || type === 'warning') {
      const loc = msg.location();
      // the browser logs our own aborts of other-origin requests; those are listed as blocked
      if (loc && blocked.has(loc.url) && /ERR_BLOCKED_BY_CLIENT/.test(msg.text())) return;
      result.console.push({
        type,
        text: msg.text(),
        location: loc && loc.url ? `${loc.url}:${loc.lineNumber}:${loc.columnNumber}` : '',
      });
    }
  });
  page.on('pageerror', (err) => {
    result.pageErrors.push({ message: String(err && err.message ? err.message : err), stack: err && err.stack ? String(err.stack) : '' });
  });
  page.on('requestfailed', (req) => {
    if (blocked.has(req.url())) return;
    const f = req.failure();
    result.failedRequests.push({ url: req.url(), method: req.method(), error: f ? f.errorText : '' });
  });
  page.on('response', (res) => {
    if (res.status() >= 400 && allowed(res.url(), base)) {
      result.httpErrors.push({ url: res.url(), status: res.status() });
    }
  });

  try {
    await page.goto(base.href, { waitUntil: 'load', timeout: 60000 });
    try {
      await page.waitForLoadState('networkidle', { timeout: 10000 });
    } catch {
      // pages with polling never go idle; the load event is enough
    }
    if (opts.waitMs) await page.waitForTimeout(opts.waitMs);
    result.horizontalOverflow = await page.evaluate(() => {
      const el = document.scrollingElement || document.documentElement;
      return el.scrollWidth > el.clientWidth ? { scrollWidth: el.scrollWidth, clientWidth: el.clientWidth } : false;
    });
    await page.screenshot({ path: path.join(outDir, result.screenshot), fullPage: true });
  } catch (err) {
    result.pageErrors.push({ message: `navigation or screenshot failed: ${err && err.message ? err.message : err}`, stack: '' });
    result.screenshot = null;
  } finally {
    await context.close();
  }
  return result;
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  const base = checkUrl(opts.url);
  const outDir = path.resolve(opts.outDir);
  await mkdir(outDir, { recursive: true });
  const { chromium } = await loadPlaywright();
  let browser;
  try {
    browser = await chromium.launch();
  } catch (err) {
    console.error(`could not start the browser: ${err && err.message ? err.message : err}`);
    process.exit(2);
  }
  const runs = [];
  try {
    for (const vp of VIEWPORTS) runs.push(await shoot(browser, base, vp, opts, outDir));
  } finally {
    await browser.close();
  }
  const count = (r) => r.console.filter((m) => m.type === 'error').length + r.pageErrors.length +
    r.failedRequests.length + r.httpErrors.length;
  const errors = runs.reduce((n, r) => n + count(r), 0);
  const report = {
    url: base.href,
    date: new Date().toISOString(),
    colorScheme: opts.colorScheme,
    errors,
    warnings: runs.reduce((n, r) => n + r.console.filter((m) => m.type === 'warning').length, 0),
    note: 'Blocked requests went to other origins and were not loaded; they are listed, not counted as errors.',
    runs,
  };
  await writeFile(path.join(outDir, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  for (const r of runs) {
    console.log(`${r.viewport}: ${r.screenshot ?? 'no screenshot'}; console errors ${r.console.filter((m) => m.type === 'error').length}, ` +
      `warnings ${r.console.filter((m) => m.type === 'warning').length}, page errors ${r.pageErrors.length}, ` +
      `failed requests ${r.failedRequests.length}, HTTP errors ${r.httpErrors.length}, blocked ${r.blockedRequests.length}, ` +
      `overflow ${r.horizontalOverflow ? 'yes' : 'no'}`);
  }
  console.log(`report: ${path.join(outDir, 'report.json')}`);
  process.exit(errors > 0 ? 1 : 0);
}

main().catch((err) => {
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(2);
});
