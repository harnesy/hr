---
name: prior-art-search
description: Search for published documents related to an invention - publication status and the owner's written OK first (an unpublished invention is never typed into public tools; neutral feature terms only), a feature breakdown, synonyms and classification codes, a plan across national and foreign patents and non-patent literature, broad then narrow, citations backward and forward, analogous fields by function, full reading of promising documents, the best few references per feature, every step logged. No legal opinion. Use before a patent attorney judges an invention.
---

# Prior-art search

A prior-art search finds documents published before a date that describe something like an invention: patents, applications, papers, books, manuals, web pages. It informs a patent attorney's judgement; it never replaces it. The search must be repeatable (every step logged) and must not itself disclose an unpublished invention.

**Route:** an invention and its owner's request → publication status and written OK → **prior-art-search** (with `source-log` as you go) → `claim-chart` → the patent attorney (a person).

## When to use

- Before an owner decides whether to file a patent application, with an attorney.
- Before designing a product feature that may resemble published work, to brief an attorney.
- To find the technical background of a field.
- Not for legal opinions of any kind: novelty, inventive step or obviousness, validity, infringement and freedom to operate are an attorney's calls, and rules differ by country.

## Inputs

- The invention: what it does and how, from the owner.
- Whether it has been published anywhere (talk, paper, website, sale, filing).
- The owner's written OK to search, and any limits (no public tools, a date range).
- The purpose of the search, and the attorney who will receive it.

## Steps

1. **Publication status and OK.** Ask whether the invention is published. If it is not, explain that typing its description into public search tools could disclose it; get the owner's written OK; search only with neutral, general feature terms, never the confidential description; record this in the log.
2. **Break it into features.** What problem does it solve? What does it do? What effect does it produce? How is it built? From which materials or by which methods? Note also what it does **not** require (a feature the owner thinks is essential may not be).
3. **Terms and codes.** For each feature, list keywords, synonyms, broader and narrower terms, and the words other fields use for the same function. Find candidate classification codes (International or Cooperative Patent Classification) by searching a few known relevant documents and reading their codes.
4. **Plan.** Which databases, in which order (most likely first), and which strategy in each. Three pools:
   - national patents and applications (for example the USPTO's Patent Public Search, https://ppubs.uspto.gov/, and other national offices' databases);
   - foreign and international patents (for example PATENTSCOPE, https://patentscope.wipo.int/, and Espacenet, https://worldwide.espacenet.com/);
   - non-patent literature: scholarly indexes, books, standards, product manuals, websites, conference papers.
5. **Broad, then narrow.** Start wide to find unexpected relevant documents and new terms; then narrow to a number you can read. Operators that include (OR, wildcards) widen; operators that exclude (AND, exact phrases) narrow. Write down the trade-off: narrower means more precise but more misses.
6. **Combine words and codes.** Text search alone is rarely enough; search by classification codes too, and browse a class where words fail (shapes, spatial arrangements).
7. **Look across fields.** Search by function, not by product name: a blade may be anticipated by documents about wings, rotors or propellers.
8. **Follow citations** backward (what a good reference cites) and forward (what later cites it).
9. **Screen, then read.** Screen titles, abstracts and front-page drawings; read promising documents in full: description, drawings and claims.
10. **Keep the best, not the most.** For each feature, keep the few strongest references with a reason; note features where nothing was found.
11. **Log everything** with `source-log` as it happens: database, date, exact query, filters, hits, documents kept.
12. **Say what was not searched:** paid databases, languages, date ranges, fields; suggest a professional searcher where the stakes call for one.

## Rules

- **No legal opinion,** and none of its words used as a finding: the search reports what was found where.
- **Unpublished means confidential:** neutral terms only, and only after the owner's written OK.
- **Read-only:** no account changes, no filings, no contact with inventors, patent offices or competitors.
- **Every step logged and dated.**

## Checks before hand-over

- Publication status and the owner's OK are recorded at the top of the log.
- Every feature has terms, codes and at least one search in each pool, or a stated reason why not.
- Promising documents were read in full.
- The shortlist gives the best few references per feature with reasons.
- Limits of the search are written down.

## Artefacts

- `prior-art/<invention>/features.md`: features, what is not required, terms, codes, plan.
- `prior-art/<invention>/search-log.md`: from `source-log`.
- `prior-art/<invention>/shortlist.md`: references per feature with reasons and where in each document the feature appears.

## Hand-over

- **To `claim-chart`:** the features and the shortlist.
- **To the patent attorney (a person):** the shortlist, the chart and the log; the attorney draws every legal conclusion.
- **To the owner:** a plain summary of what was searched, what was found and what was not searched.

## Sources

Built on the Manual of Patent Examining Procedure, sections 904 and 719.05, and the Multi-Step U.S. Patent Search Strategy page (Source: United States Patent and Trademark Office, www.uspto.gov), adapted from examiners' practice to a researcher's search. Built on the WIPO Guide to Using Patent Information (© WIPO 2021, CC BY 3.0 IGO, https://doi.org/10.34667/tind.46546), search strategies and prior art searches; changes made by harnsy. Database names and addresses are given as places to search, as read on 9 October 2026.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
