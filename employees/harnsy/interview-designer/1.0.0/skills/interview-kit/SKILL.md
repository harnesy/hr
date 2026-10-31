---
name: interview-kit
description: Build a structured interview kit from approved job criteria: a few job-related competencies, the same questions and fixed probes for every candidate, and a scale whose levels are described before the first interview. Use when a role opens, when the job changes, or before a new hiring round. Never scores, ranks or decides on candidates.
---

# Interview kit

A kit makes an interview round fair and comparable: every candidate meets the same questions, and every interviewer judges answers against the same written levels. The kit is a tool for the panel; the hiring manager decides every hire.

**Route:** approved job criteria (from `job-post`) and «unclear» points (from `screening-notes`) → **interview-kit** → `work-sample-task` if a stage needs one → `interviewer-briefing` → interviews by people → the hiring manager decides.

## When to use

- A role is opening and the job criteria are approved.
- The job has changed since the last round, or the old kit was never written down.
- Not during a running round: the kit stays as it is until the round ends; changes go into the next round.
- Not for screening applications (that is `screening-notes`) or for writing the job post (`job-post`).

## Inputs

Ask the hiring manager; do not start without these:

- **Country** where the person will work. Hiring rules differ; open legal points go to an employment professional through the HR generalist.
- **The approved criteria** and their date.
- **The work:** what the person will do in the first months, what must be there on day one, what can be learned on the job.
- **Stages:** how many interviews, who sits on each panel, and whether a work sample is planned.
- **Scale length:** how many points the hiring manager wants (for example 1-4). It is the manager's choice and is written into the kit.
- **AI use:** whether any AI tool takes part in the process (including this kit), so candidates can be told.

## Steps

1. **Analyse the job.** From the criteria and the talk with the hiring manager, write down the main tasks and what success looks like after a few months. Keep these notes; they explain later why each competency is in the kit.
2. **Pick four to six competencies.** Each is one line describing behaviour someone could observe at work («explains a technical trade-off to a non-specialist in writing»). Drop labels that cannot be observed, such as «fit», «energy» or «polish»; ask the manager what behaviour is meant and write that instead.
3. **Write questions.** Each question belongs to one competency. Use two shapes: questions about past work («Tell me about a time you…») and questions about a realistic situation from the job («Suppose a customer…, what would you do?»). Two questions per competency is usually enough.
4. **Fix the probes.** For each question, two or three follow-ups decided in advance («What did you do first?», «What happened next?», «What would you change?»). Every candidate gets the same ones.
5. **Describe the levels.** For each question, write in a sentence or two what a weak, an acceptable and a strong answer contains, using the scale length the manager chose. Describe the answer, not the person.
6. **Split the panel.** Give each interviewer named competencies, so nobody covers everything thinly. Write which gaps one interviewer hands to the next.
7. **Write the candidate notice.** What the stages are, how long they take, that the same questions are asked of everyone, whether an AI tool takes part and how, and how to ask for an adjustment (more time, another format). The recruiter sends it; wording on AI use comes from the owner. In the US, the Justice Department's guidance of 12 May 2022 (not legally binding) asks employers to tell applicants about such tools and how to ask for an adjustment; elsewhere, check with an employment professional.
8. **Trial the kit.** Ask two or three colleagues to answer the questions. Fix wording that confused them and replace questions everyone answered the same way.
9. **Record how the kit was built:** the job notes, who contributed, the trial and what changed. Then ask the hiring manager to approve it and freeze it for the round.

## Rules

- **Job-related only.** No question touches age, sex, race, origin, religion, disability, health, pregnancy, family, sexuality, politics or any similar trait, and none invites a candidate to talk about them.
- **Gaps and career changes are not evidence against anyone.** Ask about the work, not about why a path looks unusual.
- **No scores from the agent.** The kit describes levels; interviewers rate; the hiring manager decides. The agent never scores, ranks, shortlists or rejects.
- **No recording assumed.** If the employer wants to record or transcribe interviews, the candidate is told in advance with the purpose and an alternative, and the hiring manager decides.

## Checks before hand-over

- Every question maps to one competency, and every competency to the job notes.
- Every question has fixed probes and a description for each level of the scale.
- Nothing in the kit asks about, or invites talk about, a protected trait.
- The candidate notice covers the stages, AI use and how to ask for an adjustment.
- The trial happened, and its changes are recorded.
- The kit has a version and a date and is marked frozen for the round once approved.

## Artefacts

- `hiring/<role>/kit.md`: competencies, questions, probes, level descriptions, scale, panel split, version and date.
- `hiring/<role>/candidate-notice.md`: draft for the recruiter to send.
- `hiring/<role>/kit-record.md`: job notes, contributors, trial results and changes.

## Hand-over

- **To the hiring manager:** the kit and its record, for approval. The manager decides every hire.
- **To the recruiter:** the approved kit for scheduling, and the candidate notice to send.
- **To `interviewer-briefing`:** the approved kit, to brief each interviewer.

## Sources

Built on «Structured Interviews: A Practical Guide» (U.S. Office of Personnel Management, September 2008; a work of the U.S. government; used for method, US) and «Algorithms, Artificial Intelligence, and Disability Discrimination in Hiring» (U.S. Department of Justice, 12 May 2022; not legally binding; US). Adapted from the interview-prep skill in github.com/anthropics/knowledge-work-plugins, human-resources folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Also built on the 18F Guides, engineering hiring pages (18F, U.S. General Services Administration; CC0 1.0) and the Sourcegraph handbook (archived) interview training pages (© 2021 Felix Frederick Becker; Apache License 2.0). Changed by harnsy. Scope from the O*NET 31.0 Database, 13-1071.00 Human Resources Specialists. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
