---
name: screening-notes
description: Write one screening note per application against the approved job criteria, with evidence and «met», «not met» or «unclear» per criterion, so the hiring manager decides. Use when applications arrive for a role whose criteria are approved. Never ranks, scores in total or rejects.
---

# Screening notes

A screening note shows the hiring manager what each application says about each criterion. The note prepares a decision; it is never the decision. The agent does not rank, total, shortlist or reject.

**Route:** job-post (approved criteria) → applications → **screening-notes** → the hiring manager decides → interviews.
Before this skill: approved, dated criteria from `job-post`. After it: the hiring manager's decision on each candidate.

## When to use

- Applications have arrived for a role, and the criteria were approved before the first one was read.
- Not before the criteria are approved. If they are missing or changed during the round, stop and ask for them; a change applies to every candidate, including those already noted.

## Before the first note

- **Tell the hiring manager about AI use.** In many countries candidates must be told when an AI tool helps in the process, and how. Candidates must also be able to ask for an adjustment or another route. Check that the job post or the first message to candidates says so (wording from the owner). If it does not, say so on the item before writing notes.
- **Know the data rule:** where applications are kept, who may see them, and when they are deleted. Keep everything inside the project.

## Rules

- **Job criteria only.** Each note uses the approved criteria and nothing else.
- **Never a protected trait.** Do not mention, score, comment on or guess age, sex, race, origin, religion, disability, health, pregnancy, family status, sexual orientation, photos, name origin or any similar trait. If an application contains such details, leave them out of the note.
- **No gaps as evidence.** A gap in a CV, a career change or a non-standard path is not «not met». Judge only what the criterion asks.
- **No automatic decisions.** No total score, no ranking, no shortlist, no rejection, no «recommend / do not recommend».
- **Evidence or «unclear».** Every «met» or «not met» quotes or points to the part of the application that shows it. If the application does not say, write «unclear» and suggest a question for the interview.

## Steps

1. **Load the criteria** and their evidence notes. Write the version and approval date at the top of the batch.
2. **For each application,** one note:
   - candidate reference (as the hiring system names it);
   - for each criterion: «met», «not met» or «unclear», the evidence (quote or pointer), and for «unclear» a question that would settle it;
   - adjustments the candidate asked for, passed on as written;
   - nothing else: no overall opinion, no comparison with other candidates.
3. **Read the batch again** for words that judge the person instead of the evidence («seems young», «good culture fit», «foreign degree»). Remove them.
4. **Summarise the batch by counts only:** how many applications, how many with all criteria met, how many with an «unclear» or a «not met». No names in order of merit.
5. **Hand over** to the hiring manager and record that every decision is theirs.

## Checks before hand-over

- Every note uses only the approved criteria, and every point has evidence or «unclear».
- No protected trait, guess about one, or stand-in for one appears anywhere.
- No ranking, total score, shortlist or rejection.
- The AI-use notice and the adjustment route are confirmed or flagged.
- The notes are stored only where the owner's rule says.

## Artefacts

- `screening/<candidate-ref>.md`: one note per application.
- `screening/summary.md`: criteria version, counts, open questions for interviews.

## Hand-over

- **To the hiring manager:** the notes and summary. The person decides who moves on and who does not, and the reason given to each candidate comes from the agreed list and that person.
- **To the interview designer:** the «unclear» points, so interview questions can settle them.
- **To the recruiter's update drafts:** the person's decisions, once made, so every candidate hears back.

## Sources

Built on «Structured Interviews: A Practical Guide» (U.S. OPM, 2008), «Employment Tests and Selection Procedures» (U.S. EEOC, 2007-12-01) and «Algorithms, Artificial Intelligence, and Disability Discrimination in Hiring» (U.S. DOJ, 2022-05-12, not binding): US government works, used for method, not as the law of any other country. Also built on the Sourcegraph handbook talent pages (Apache License 2.0, © 2021 Felix Frederick Becker) and GOV.UK «Employers: preventing discrimination». Contains public sector information licensed under the Open Government Licence v3.0. All adapted. Facts only, not text: EU rules on automated decisions about people and on AI used in recruitment.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
