---
name: web-performance-check
description: Check how fast and stable a web page feels to users, using field data from real visits and lab data from test runs, each labelled by source; compare against Google's published Core Web Vitals thresholds (quoted with page and date), mark anything without data «not measured», and list likely causes as potential impact for the frontend team. Use before a launch, after a frontend change, or when users say pages are slow.
---

# Web performance check

Users judge a page by how soon the main content appears, how quickly it reacts, and whether it jumps around. This skill gathers what is known about those three things for a page, keeps real-user numbers apart from test-run numbers, compares them with Google's published thresholds, and lists likely causes. Where there is no data, it says so.

**Route:** a page or a set of pages → **web-performance-check** → a labelled report with likely causes → the frontend developer fixes, measured with profile-first → the check runs again.
Before this skill: the pages that matter and access to any real-user data. After it: a report; code changes belong to the frontend developer.

## When to use

- Before launching a page or a redesign.
- After a frontend change: new framework version, new fonts, new third-party scripts, new images.
- When users or support report slow or jumpy pages.

## Inputs

- The pages (URLs) that matter most, and which devices users mainly use.
- Field data, if any: the site's own real-user monitoring, or a public data set of real Chrome user measurements for the site.
- A way to run lab tests: a browser with developer tools, or a lab testing tool.
- The site's own performance budget, if the owner has set one.

## Rules

- Field data (real users, over a period) and lab data (one synthetic run, one device profile) are different things. Every number is labelled field, lab or trace, with date and settings.
- Core Web Vitals thresholds are quoted only as Google publishes them, with the page and its date (see «Thresholds» below). Before use, check the page again: the metrics and thresholds change over time.
- Where there is no data for a page, metric or device, the report says «not measured». No number is guessed from reading code.
- Findings from code reading are «potential impact», not measured results.
- No invented budgets. A budget appears only if the owner set it.
- Identify the framework and rendering approach before giving framework-specific advice.
- No promised speed. The report describes what was seen and what is likely to help.

## Thresholds

As published by Google on web.dev, «Web Vitals» (last updated 31 October 2024), the «good» values, judged at the 75th percentile of page loads, separately for mobile and desktop:

| Metric | What it reflects | Good |
|---|---|---|
| Largest Contentful Paint (LCP) | loading of the main content | 2.5 s or less |
| Interaction to Next Paint (INP) | response to user input | 200 ms or less |
| Cumulative Layout Shift (CLS) | visual stability | 0.1 or less |

Field data at the 75th percentile is what these thresholds are meant for. Lab runs help to find causes but cannot measure INP directly from real interactions.

## Steps

1. **List the pages and devices** to check, with the owner.
2. **Collect field data** per page, separately for mobile and desktop, at the 75th percentile, with the period it covers. If none exists, write «not measured (no field data)».
3. **Run lab tests** on each page several times, with a stated device profile, CPU slowdown and network speed resembling a mid-range or low-end phone. Record the settings.
4. **Compare** field values with the thresholds above, naming the page and date. Use lab values to explain, not to pass or fail.
5. **Find likely causes** in traces and in the page: a large hero image loaded late, render-blocking styles or scripts, web fonts, heavy third-party scripts, long tasks on the main thread, images or ads without reserved space, slow server response. Label each as measured (with the trace) or potential impact.
6. **Check against the owner's budget,** if one exists; otherwise suggest that the owner set one early and check each page change against it.
7. **Write the report:** per page and device, the labelled numbers, the comparison, the causes ranked by likely effect, and suggested fixes for the frontend developer.
8. **Suggest a guard:** a lab check in the build and ongoing field monitoring, so regressions are caught.

## Checks before hand-over

- Every number is labelled field, lab or trace, with date and settings.
- Thresholds are quoted with Google's page and date; nothing else is presented as a standard.
- Gaps say «not measured»; code-reading findings say «potential impact».
- Mobile and desktop are reported separately.
- No budget or speed promise was invented.

## Artefacts

- `webperf/<site>-<date>.md`: pages, devices, field and lab numbers, comparison, causes, fixes.
- Saved lab reports and traces next to it.

## Hand-over

- **To the frontend developer:** causes and suggested fixes, to be measured with profile-first.
- **To devops or the backend developer:** slow server responses and caching.
- **To the product manager or owner:** the overall picture and the trade-offs of removing third-party scripts.
- **To the designer:** layout shifts caused by the design itself.

## Tools

The browser's developer tools (performance panel, network panel, throttling), a lab testing tool such as Lighthouse, the site's own real-user monitoring if it has one, and the public Chrome UX Report data set for field data where the site is in it.

## Sources

Built on web.dev «Web Vitals», «Defining the Core Web Vitals metrics thresholds» and «Why lab and field data can be different» (Google LLC, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted. Built on agent-skills, «web-performance-auditor» and «performance-optimization» (github.com/addyosmani/agent-skills, commit 1401c8b; © 2025 Addy Osmani, MIT licence), adapted. Built on GOV.UK Service Manual «How to test frontend performance» (Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
