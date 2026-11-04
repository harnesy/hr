---
name: marketplace-rules-check
description: Before a listing or review job, read each platform's live policy pages and record, in your own words, what they say about the task, with the page address, the page's own date or «no date shown», any banner and the day read; add the dated US federal rule on consumer reviews where US buyers are in scope; mark pages that cannot be read as unread. Use before every listing-build or review-reply-drafts job and when a platform is new. Never gives a verdict that something is permitted.
---

# Marketplace rules check

Platform rules change without notice, and memory is the worst source for them. This skill reads the live pages each time, records what they say with dates, and hands that record to the listing and review work. It reports what a page says; it never gives a verdict that a listing or a reply meets the rules, and legal readings go to a professional.

**Route:** a listing or review job (from the seller or the shop's operations lead) → **marketplace-rules-check** → dated record → `listing-build` / `review-reply-drafts` → the seller.

## When to use

- Before every `listing-build` or `review-reply-drafts` job, even if a record exists from last week.
- When a platform is new to the seller.
- When a platform shows a banner about changed policies.

## Inputs

- The platforms in scope and the seller's countries of sale.
- The task: listing fields, review replies, review requests, or reporting a review.
- The previous record, if any, to compare.

## Steps

1. **Open each relevant page live.** Record: the address, the page title, the page's own «last updated» date or «no date shown», any banner (for example «under review»), and the date and time read.
2. **Summarise in your own words** only the rules that matter for the task. Do not paste the platform's text. Write «as read on <date>, the page says …».
3. **Field limits for listings:** record them in the limits file that `listing-build` uses, with the page and read date.
4. **Unreadable page:** if a page will not open (an error, a login wall, a block), record it as unread with the error and the date. State no rule for that platform; ask the seller to read the live page or send it.
5. **Law, US only:** where US buyers are in scope, add the federal rule on consumer reviews (below), with its dates. For other countries write «review rules differ by country; ask a professional». Never give a legal reading.
6. **Compare with the last record.** List what changed, if anything.
7. **Hand over** the record to the next skill and to the seller.

## Platform pages as read on 9 October 2026 (data; reread before every use)

These lines are a starting list of pages and what they said that day, in our own words. They are not current rules: the live page decides.

- **Amazon, Community Guidelines** (amazon.com/gp/help/customer/display.html?nodeId=14279631), no date shown, no banner. Said: reviews must be honest; creating, editing or removing a review in exchange for any compensation (money, refunds, discounts, free products, gift cards and similar) is not permitted, including a seller offering a refund to change a negative review; people with a financial or close personal connection to the seller or brand may not review its products; sellers may ask for an honest review that is not incentivised; free-product reviews only through the platform's own labelled invitation programme; comments about the seller, shipping or packaging belong in seller feedback, not product reviews.
- **Google Play Console Help, ratings and reviews, with the Developer Comment Posting Policy** (support.google.com/googleplay/android-developer/answer/138230), no date shown, no banner. Said: one public reply per user review, editable at any time; the reviewer is notified of the reply; replies should be relevant, clear and truthful, not abusive, dismissive or threatening, and should not solicit or promote; inappropriate reviews are reported rather than answered.
- **Apple App Review Guidelines** (developer.apple.com/app-store/review/guidelines/), «Last Updated: June 8, 2026». Said in §5.6.1: responses to reviews are respectful, targeted to the comment, with no personal information, spam or marketing; ratings are requested only through the provided system prompt, and custom review prompts are not permitted. The opening of §3 said that manipulating reviews or charts with paid, incentivised, filtered or fake feedback may lead to removal from the developer programme.
- **Apple, Ratings, reviews, and responses** (developer.apple.com/app-store/ratings-and-reviews/), no date shown. Said: the system rating prompt is shown no more than three times within 365 days.
- **Etsy seller policy and reviews policy** (etsy.com/legal/): **not read** on 9 October 2026 (the pages refused the request). No Etsy rule is stated here; read the live pages and record their date before any Etsy job.

## US federal rule on consumer reviews (law, facts only)

16 CFR Part 465, Use of Consumer Reviews and Testimonials: final rule published 22 August 2024 (89 FR 68077), in effect since 21 October 2024; eCFR text up to date as of 7 October 2026 (eCFR calls itself authoritative but unofficial). In short, as the rule text reads:

- §465.2: no writing, buying, selling or spreading fake reviews or testimonials.
- §465.4: no compensation or other incentive conditioned, openly or by implication, on a review expressing a particular sentiment.
- §465.5: reviews and testimonials by insiders (officers, managers, employees, agents, their relatives) need a clear disclosure of the relationship; managers may not ask employees or relatives to post reviews without it.
- §465.6: no company-controlled website presented as an independent review source.
- §465.7: no unfounded legal threats, intimidation or knowingly false public accusations to stop or remove a review; no suppressing reviews by their rating, while neutral exclusion rules applied to all reviews alike are permitted by the rule.
- §465.8: no fake indicators of social-media influence.

Our own stricter practice, beyond the rule's text: never filter who is asked for a review by how happy they seem; ask every buyer the same way or nobody. Outside the US, or for any legal question, a professional decides.

## Rules

- **Live page every time.** The list above is a dated starting point, not a source of current rules.
- **Own words.** Summaries, not copies.
- **No verdicts.** «As read on <date>, the page says …», never a statement that something passes, is permitted or is approved.
- **Unread is unread.** No rule is guessed from memory, blogs or another platform.

## Checks before hand-over

- Every platform in scope has a page address, the page's date or «no date shown», any banner and the read date.
- Unreadable pages are marked unread with the error.
- US law appears only when US buyers are in scope, with its dates; other countries carry «ask a professional».
- No line in the record reads as a legal or platform verdict.

## Artefacts

- `marketplace/rules/<date>.md`: the record per platform.
- `marketplace/rules/<platform>-limits-<date>.json`: field limits for `listing-build`.

## Hand-over

- **To `listing-build` and `review-reply-drafts`:** the record and the limits file.
- **To the seller:** the record, with unread pages and questions for a professional listed first.

## Sources

Facts from the Consumer Reviews and Testimonials Rule, 16 CFR Part 465, as published on eCFR (https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-465). Source: United States Federal Trade Commission, www.ftc.gov. Platform facts from the pages listed above, read on 9 October 2026 and restated in our own words; no platform text is reproduced, and no platform endorses this skill. Scope from the O*NET 31.0 Database, 13-1199.06 Online Merchants (nearest occupation). This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
