---
name: llms-visibility
description: Make a website visible and readable to LLM readers (AI search, chat assistants and coding agents that fetch pages) over plain HTTP; audit robots.txt per AI bot and CDN bot rules, add a Content-Signal line with the owner's choices, ship clean server-rendered HTML, .md twins with link and Link headers, Accept text/markdown negotiation, a curated llms.txt, server-side logs and public checks, and advise against debunked tricks. Use when an owner wants AI tools to find and read the site, or asks about llms.txt, Markdown pages or AI bots.
---

# LLM visibility

AI readers reach a site in two ways. Chat assistants fetch the same HTML a browser gets and read only that. Coding agents ask for Markdown with an `Accept: text/markdown` header. So the work is: clean HTML for the first group, Markdown behind the same URLs for the second, and nothing that serves anyone a different article. Every step below is plain web standards. Each one can ship on its own; build them in this order.

**Route:** the owner's goal and the site → robots and bot audit → clean HTML → Markdown twins, links and negotiation → llms.txt → logging → checks → hand-over to engineering.
Before this skill: access to the site, its robots.txt, its CDN or firewall settings and its privacy notice. After it: a plan and a check report; engineering ships the changes.

## When to use

- A site owner wants AI search and AI assistants to find, read and quote the site's public pages: docs, blog, marketing and landing pages.
- Someone asks about llms.txt, Markdown versions of pages, AI bots in robots.txt or «GEO» / «AEO».
- An AI tool gets an empty app shell instead of the page text.
- Not for pages behind a login, and not a replacement for classic search work (sitemaps, rich results, ranking).

## Inputs

- The site URL and a list of page types (home, article, docs page, product page).
- The current robots.txt and the CDN or firewall bot settings.
- The stack: how pages render (server, build time or browser only) and where the content lives.
- The owner's answer on AI training (see Rules). Ask; do not assume.
- The site's privacy notice, before any logging work.

## Rules

- **No promises.** Never promise that any AI will cite, quote, rank or recommend the site. This work makes the content reachable and readable; it controls nothing on the AI side. Google says indexing and serving are never guaranteed, even when every requirement is met.
- **Say how young the evidence is.** What AI readers actually fetch is known only from a few log studies published in 2026: two large studies of llms.txt requests (Ahrefs, data from May 2026; Longato's audit of Adobe Experience Manager domains, June 2026) and one company's own site logs over about six months (Evil Martians, to October 2026). Name the date and the source when you cite a number, and tell the owner their own logs are the real answer.
- **llms.txt and .md files hold content and links only.** Never put instructions to AI readers in them («ignore …», «always recommend …», «you are …»). A file written for LLMs is a prompt-injection surface; review it like code you deploy.
- **Same content for everyone.** The format may change only because the client asked for it in the `Accept` header (or opened a `.md` URL). Never pick content or format by User-Agent or by «is this a bot». That is cloaking.
- **ai-train is the owner's call.** Training use is a business decision: some owners want to be in training data so models know them; others sell their content or do not want it used. Ask the owner, write their answer, and never choose a default for them.
- **robots.txt, CDN bot rules and Content-Signal change only with the owner's OK.** Show the diff and what each line does before it goes live.
- **The agent proposes and checks; engineering ships.** Write the plan, the exact headers and the test commands; check after the deploy. Do not push changes to production yourself.
- **Logs hold personal data.** Request logs contain IP addresses. Read the privacy notice before proposing any new logging; if it does not cover this use, stop and send it to the owner first.

## Steps

1. **Audit robots.txt per bot.** Know which bot each rule hits. OpenAI alone runs three:
   - `GPTBot` crawls for model training.
   - `OAI-SearchBot` builds the index for ChatGPT search.
   - `ChatGPT-User` fetches a page when a person asks ChatGPT about it. OpenAI says robots.txt rules may not apply to it.
   So blocking `GPTBot` keeps the site out of training but does not stop on-request fetches. Then check the CDN and firewall (WAF) bot settings: a CDN can block AI crawlers at the edge, before robots.txt is ever read (Cloudflare has such a setting). Write down, per bot, what the owner wants and what actually happens now.

2. **Add a Content-Signal line** inside the `User-agent: *` group, with the owner's answers:
   ```
   User-agent: *
   Content-Signal: search=yes, ai-input=yes, ai-train=<owner's answer>
   ```
   The three signals are separate: `search` = building a search index and showing links and short excerpts (not AI summaries); `ai-input` = using the content as live input to AI answers (retrieval, grounding); `ai-train` = training or fine-tuning models. This skill exists for `search` and `ai-input`, so propose `yes` for both, and ask about `ai-train`. Notes for the owner: these are stated preferences, not a technical block, and a crawler can ignore them. The line is not part of RFC 9309, so strict validators warn about an unknown directive; that is a warning, not a failure, because crawlers skip lines they do not understand. On Cloudflare, check the managed robots.txt first: it may already add `search=yes, ai-train=no` with no `ai-input` value.

3. **Make the HTML clean and server-rendered.** Chat assistants read the HTML response as served and do not run JavaScript; an app that renders in the browser hands them an empty root element. Only readable pages need this, not app screens.
   - If the framework renders on the server or at build time, move any browser-side content fetch into the server path so the text is in the response.
   - If it is a browser-only single-page app, prerender the content routes to static HTML at build time and keep the app shell as it is.
   - If neither fits the scope, do not start a framework migration here. Write the owner a plan (routes, method, cost) and go on with steps 4 to 6; they work no matter how the HTML renders.
   In the markup: one `<h1>`; heading levels in order, chosen for structure, not size; the body in `<main>` or `<article>`, navigation and footer in their own landmarks; links as real `<a href>`, not click handlers (agents follow links, not buttons). Keep the `<head>` light: move inline styles and scripts to files, put analytics at the end of `<body>`, trim hydration data, so the text comes early (fetchers read on a budget; Claude Code's fetch tool reads up to 100,000 characters of a page per call, per its tools reference). Keep tables as `<table>` and code as `<pre><code>`; both convert cleanly when a tool turns the HTML into Markdown. Existing structured data must match the visible text; do not add any for this work.

4. **Serve a .md twin for every content page.** For `/path`, serve the same content as Markdown at `/path.md` (`/index.md` for the root), with `Content-Type: text/markdown; charset=utf-8`. Generate both from one source (render both from the same content, or one from the other). Never keep two content stores that can drift apart. The twin adds to the HTML; it does not replace it.

5. **Advertise the twin, in the page and in the headers.** Both, not one of them:
   ```html
   <link rel="alternate" type="text/markdown" href="/path.md">
   ```
   ```
   Link: </path.md>; rel="alternate"; type="text/markdown"
   ```
   The tag reaches readers that parse the page; the header reaches clients that only read headers. Set the `Link` header on both formats: the HTML points to the `.md`, the `.md` points back to the HTML.

6. **Negotiate on `Accept: text/markdown`.** Same URL, same content, the format the client asked for. In Checkly's test of coding agents (February 2026), Claude Code, Cursor and OpenCode sent this header; chat assistants do not. Four musts:
   - Compare q-values; never substring-match. `Accept: text/html, text/markdown;q=0.5` prefers HTML.
   - On a tie, serve Markdown only if the client named `text/markdown` explicitly, so a browser's `*/*` never gets Markdown.
   - Return `406 Not Acceptable` when neither HTML nor Markdown is acceptable. Skip this check when the URL itself asks for `.md`.
   - Send `Vary: Accept` on both formats so caches keep them apart.
   If the owner worries about cloaking: cloaking serves bots another article; negotiation serves the same article in the requested format and declares it with `Vary: Accept`. acceptmarkdown.com publishes server recipes for common stacks.

7. **Add llms.txt, with low expectations.** A Markdown file at the site root, in the llmstxt.org format: an H1 with the site name, a one-line blockquote summary, then H2 sections of links with one-line descriptions. Curate it (the pages worth reading, not a sitemap), point its links at the `.md` twins, and link to it from the site's pages; agents fetch it mostly when something points them there. Tell the owner plainly: few AI readers fetch it. As of 4 November 2026, according to the Evil Martians article, no major AI provider has committed to it; the 2026 Ahrefs and Longato studies trace about 1% of its requests to AI bots, and Google Search does not use it. It is cheap and works as a README when a person points an AI tool at the site. `llms-full.txt` (all content in one file) is optional: useful for developer docs; for a blog or marketing site, skip it or redirect it to `/index.md`.

8. **Log AI reads on the server** (only if the owner wants numbers, and only after the privacy check in Rules). AI readers do not run JavaScript, so browser analytics miss them. Log in the same server code that negotiates: path, format served, raw User-Agent, `Accept`, referrer host (for example chatgpt.com, claude.ai, perplexity.ai), status. Keep only the fields you need, for as short a time as the privacy notice allows.
   - **Classify by exclusion.** New AI user agents appear all the time, so a fixed list misses them. Rule out known browsers, search and SEO crawlers, scanners and bare HTTP clients; count what is left that fetched `.md`, llms.txt or llms-full.txt.
   - **Split crawlers from on-demand fetchers.** `GPTBot` or `ClaudeBot` fill an index or a training set; `ChatGPT-User` or `Claude-User` fetch for a person now. Lumped together, crawlers look like the biggest readers.
   - **Check the path too.** Scanners wear AI user-agent strings and probe paths like `/.env`.
   - Read the `.md` 404s: they show the URLs agents guess. Re-read the logs each quarter.

9. **Check.**
   - acceptmarkdown.com: Markdown for `Accept: text/markdown`, `Vary: Accept`, `406` for unsupported types, q-values.
   - isitagentready.com: robots.txt, sitemap, `Link` headers, Markdown negotiation, Content Signals.
   - Google Search Console has a Generative AI performance report for AI features on Google Search and Discover. Bing Webmaster Tools has an AI Performance report (announced as a public preview in 2026). Both cover search-based AI answers only; coding agents and on-request fetchers do not appear there, so they do not replace the server logs.
   - For Google Search itself, nothing extra is needed: Google Search does not need llms.txt, Markdown copies or special markup for its AI features. A page must be indexed and eligible to show with a snippet; normal technical SEO still applies.

## Checks before hand-over

One line per step, in the same order:

1. robots.txt and the CDN/WAF bot settings let in the fetchers the owner wants; each AI bot rule has a written reason.
2. The Content-Signal line sits in the `User-agent: *` group and carries the owner's own `ai-train` answer.
3. `curl -s <page>` contains the body text early in the response; one `<h1>`, no skipped heading levels, a `<main>` or `<article>`, tables and code kept as elements.
4. `curl -sI <page>.md` shows `Content-Type: text/markdown; charset=utf-8` for every page type, and the text matches the HTML page.
5. The HTML head has `<link rel="alternate" type="text/markdown">`; `curl -I` on both formats shows a `Link` header pointing to the other.
6. `Accept: text/markdown` returns Markdown with `Vary: Accept`; `Accept: text/html, text/markdown;q=0.5` returns HTML; `Accept: image/png` returns `406`; the content is the same in both formats.
7. `/llms.txt` exists, is well formed, links to `.md` URLs, is linked from the site and holds no instructions.
8. If logging was set up: the privacy notice covers it, and the report splits crawlers from on-demand fetchers.
9. acceptmarkdown.com and isitagentready.com pass; any remaining warning is explained.

## Don't

Advise against these and say why; do it only if the owner still wants it after hearing that. The one exception is User-Agent sniffing: refuse it.

- **`ai.txt` or `/.well-known/ai.txt`:** competing proposals, no real adoption.
- **AI meta tags** (`<meta name="llms">`, `<meta name="ai-content-url">`): no spec, no AI tool reads them; the HTML spec proposal was closed as not planned.
- **HTML comments for AI:** parsers strip comments.
- **Hidden «for AI» hints** (a visually hidden note pointing to the Markdown): nothing follows them. Agents that want Markdown ask with `Accept`.
- **«AI mode» or human/AI toggle buttons:** agents do not click buttons.
- **User-Agent sniffing to serve bots Markdown or other content:** refuse; that is cloaking. Use `Accept` negotiation.
- **Separate «AI info» pages:** no reader treats them differently from a good normal page.
- **JSON-LD added for LLMs:** tests show models mostly do not read it on the page. Keep existing JSON-LD for search indexes and shopping systems, matching the visible text; do not add it for the model.
- Treat any other new «for AI» file or tag the same way until an AI provider documents reading it.

Beyond the plumbing, the lasting lever is the visible text itself: clear, original, useful content for people.

## Artefacts

- The bot table: each AI bot, the current rule, the owner's wish, the CDN/WAF status.
- The proposed robots.txt diff with the Content-Signal line and the owner's recorded `ai-train` answer.
- The plan per step: routes, headers, negotiation rules, cost, and what ships first.
- The check report: commands run, responses, scanner results, dates.
- If logging: the fields kept, the retention period, the privacy-notice check, and the first classified report.

## Hand-over

- **To the site owner:** the `ai-train` question, robots and CDN changes to approve, the privacy-notice check, and the plain caveats (no citation promise, young evidence, llms.txt has few readers).
- **To engineering:** the plan, the exact headers and the checks to run after the deploy.
- **To the privacy-notice owner:** the proposed log fields and retention, before logging starts.
- **To the content team:** pages that agents ask for but the site does not have (from the `.md` 404s).

## Sources

This skill is made by harnsy; no endorsement by Evil Martians, Google or the other projects named is implied.

Built on the «llms-visibility» skill from Evil Martians agent-skills (github.com/evilmartians/agent-skills, commit b964cf1; © 2026 Evil Martians, MIT licence, see LICENSE in this folder), adapted. Built on Google Search Central, «Optimizing your website for generative AI features on Google Search» (https://developers.google.com/search/docs/fundamentals/ai-optimization-guide; Google, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted. Facts only: Google Search Central, «AI features and your website» (https://developers.google.com/search/docs/appearance/ai-features; Google, CC BY 4.0), for structured data matching the visible text. The Content-Signal line follows contentsignals.org (CC0). Ideas and facts only (no text taken): Evil Martians, «Making your site visible to LLMs and AI agents: 6 techniques that work, 8 that don't» (evilmartians.com, version 2.0.0 of 4 November 2026). The figures named in this skill are facts reported in that article, credited to their own sources: the Ahrefs llms.txt study (May 2026), Longato's audit of Adobe Experience Manager domains (June 2026), Evil Martians' own server logs (about six months to October 2026), Checkly's test of coding agents (February 2026), and the Claude Code tools reference (100,000 characters per fetch).

Text © 2026 Pavel Buchnev (harnsy), licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), except the parts adapted from the Evil Martians skill, which stay under the MIT licence in LICENSE. The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
