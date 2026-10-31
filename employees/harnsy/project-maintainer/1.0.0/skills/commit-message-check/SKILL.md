---
name: commit-message-check
description: Check the commit messages of a series with a small script - summary present and short (warning over 50 characters, flag over 72), no full stop, likely written as an instruction, a blank line after it, a body that says why for larger changes, body lines wrapped, footers in «Token: value» shape, breaking changes declared, an optional «type(scope):» prefix - then review every flag by hand and ask the contributor for the fixes. Counts and flags, not a verdict. Use on every series before a review verdict, or as a check on a single message.
---

# Commit message check

A commit message is read long after the code review is forgotten: by someone searching the history for why a line exists, or which change broke a feature. A short summary written as an instruction, a blank line, and a body that gives the reason make that search quick. This skill runs a script that flags the usual shape problems, then a person reviews each flag, because the script can only guess at meaning.

**Route:** a series under review (`patch-series-review`) or a single message → **commit-message-check** → flags reviewed by hand → the exact asks go to the contributor with the review.

## When to use

- On every series before giving a review verdict.
- On a single message, for example as a check before a commit is made.
- Not to rewrite anyone's history, and not as a substitute for reading the messages.

## Inputs

- The commits of the series, as a log (see Tools), or one message as a file.
- The project's own message rules, if written: limits, whether a «type(scope):» prefix is used, which types are allowed.

## Steps

1. **Run the script** on the series (see Tools), with the project's limits if they differ from the defaults.
2. **Read the count per flag,** then each message's flags.
3. **Review each flag by hand:**
   - **summary-long / summary-too-long:** suggest a shorter summary that keeps the what; details move to the body.
   - **summary-full-stop:** remove it.
   - **not-imperative:** the check is a guess from the first word; confirm by reading, then suggest the instruction form («Add retry to export job» for «Added retry …»).
   - **no-blank-line:** the second line must be empty, or tools treat the body as part of the summary.
   - **no-body / no-reason:** ask for the reason: the problem, why this change solves it, and why this approach over others. A small, obvious change may need no body; say so and drop the flag.
   - **line-long:** wrap the body; links and quoted output may stay long.
   - **trailer-shape:** footers are «Token: value» or «Token #value», with «-» instead of spaces in the token, for example «Refs: PROJ-123» or «Co-authored-by: Name <address>».
   - **breaking-undeclared:** if existing users are affected, the change is declared (a «!» before the colon of a prefixed summary, or a breaking-change footer) and the review checks the migration path.
   - **prefix:** only when the project uses a «type(scope):» prefix.
4. **Drop false alarms** with a short reason; the script is a heuristic.
5. **Write the asks** into the review: commit id, the flag, the exact new wording or the question to answer in the body.

## Rules

- **Counts and flags, not a verdict.** A clean run does not mean the messages are good; a flag does not mean they are bad.
- **Ask, never rewrite.** The contributor changes the messages; a maintainer rewrites a message only where the project's written rules say so (for example when squashing a contributor's commits).
- **The project's rules win** over the defaults; set the limits to match them.
- **About the message, never the person.**

## Checks before hand-over

- Every flag has a decision: an ask to the contributor, or a false alarm with its reason.
- The limits used are stated in the review if they differ from the defaults.
- Breaking-change flags are linked to the matching findings of the series review.

## Artefacts

- The script's report for the series, and the list of asks, added to the review.

## Hand-over

- **To `patch-series-review`:** the asks, as findings with commit ids.
- **To the contributor:** the asks, inside the review.
- **To the project owner:** proposed changes to the written message rules when the same flag keeps appearing.

## Tools

- `python3` 3.8 or newer, standard library only, no network. The script reads text; it runs no other program.
- A series: `git log -z --format='%H%n%B' --shortstat <base>..<head> > series.log`, then `python3 scripts/commit_msg_check.py --log series.log` (or pipe the log in with `--log -`). The size line after each commit lets the script ask for a body on larger changes.
- One message: `python3 scripts/commit_msg_check.py message.txt --changed-lines 35`; lines starting with «#» are ignored.
- Limits: `--soft 50`, `--hard 72` (summary), `--wrap 72` (body lines), `--body-after 20` (changed lines that need a body). `--prefix` turns on the «type(scope):» check, `--types feat,fix,docs` limits the types. `--strict` exits with 1 when any flag other than the soft summary warning is raised, for use in CI.
- Output: one line per commit with its id and flags, a reason under each flag, then a count per flag.

## Sources

Built on the Conventional Commits 1.0.0 specification (conventionalcommits.org contributors; CC BY 3.0, https://creativecommons.org/licenses/by/3.0/), modified: the parts of a message (summary, blank line, body, footers), the footer token shape with «-» for spaces, the breaking-change marker, the optional prefix. The length limits, the instruction form and the «say why» check are common practice, stated here as configurable defaults.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence. The script in `scripts/` is © 2026 Pavel Buchnev (harnsy), MIT License (see LICENSE).
