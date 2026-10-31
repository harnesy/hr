---
name: course-outline
description: Build a course outline from confirmed objectives: sections in order, each with its objectives, the check that shows them, practice time, content notes, materials and delivery mode, plus a feedback plan for the first run. Use once objectives are confirmed, and again after each run to revise.
---

# Course outline

The outline is the course on one or two pages. Its order comes from the checks: content exists only to lead learners from one check to the next, with practice along the way.

**Route:** confirmed objectives (from `learning-objectives`) → **course-outline** → the requester approves, subject experts review content → `quiz-build` where a section needs one → first run → feedback → revised outline.

## When to use

- Objectives are confirmed and the course needs a structure.
- A course has been taught and the feedback calls for changes.
- Not before objectives are confirmed.

## Inputs

- Confirmed objectives with their planned checks.
- Learner profile, prerequisites and misconceptions.
- Time available and how the course is delivered (live in a room, live online, self-paced).
- Subject experts who will review the content.

## Steps

1. **Order the checks.** Arrange the checks so each builds on the one before. That order is the order of sections.
2. **For each section, write:**
   - its objectives;
   - the check (practice task, short questions, discussion prompt) and how learners get feedback on it;
   - practice time, usually more than the explaining time;
   - content notes: only what learners need to pass the next check;
   - materials (examples, data, handouts) and who provides them;
   - delivery mode for this section.
3. **Match the exercise to the action.** «Choose» or «explain» suits short questions or discussion; «build», «fix» or «submit» needs hands-on work with real-looking material. Beginners get worked examples and partly finished tasks; experienced learners get open problems.
4. **Check often.** A short check every few minutes of new material and a brief reflection at the end of each section. Keep a final test only if a grade or certificate really needs one.
5. **Surface misconceptions early.** Plan one check in the first section that brings out the most common wrong idea.
6. **Plan accessibility.** Materials with text alternatives for images, readable contrast, captions for video, keyboard-usable exercises, and a way to ask for an adjustment. Quizzes go through `quiz-build`.
7. **Plan feedback for the first run.** What to ask learners and the instructor afterwards, and when the outline will be revised.
8. **Version the outline.** A course is a draft until taught; after each run, record what changed and why.

## Rules

- Checks and practice are for learning. Results are not used to rate people for hiring, promotion, pay or any HR decision.
- Collect nothing about learners beyond what the course needs.
- Publishing the course on a learning platform is done by the course owner; any change there is a proposal with a way to undo it.

## Checks before hand-over

- Every section has objectives, a check and practice time.
- Every objective from `learning-objectives` appears in at least one section.
- Content notes contain nothing that no check needs.
- A feedback plan and a version number are present.

## Artefacts

- `learning/<course>/outline.md`: sections, checks, practice, content notes, materials, delivery, version.
- `learning/<course>/feedback-plan.md`: questions for learners and instructors, revision date.
- `learning/<course>/changes.md`: what changed after each run.

## Hand-over

- **To the requester:** the outline, to approve.
- **To subject experts:** content notes to confirm or correct.
- **To the course owner:** the approved outline and materials list, for whoever teaches or publishes it.
- **To `quiz-build`:** sections that need a quiz.

## Sources

This work is derived from work that is Copyright © Software Carpentry, Data Carpentry, Library Carpentry, or The Carpentries: «Collaborative Lesson Development Training», episodes on lesson design, formative assessment and audience (https://carpentries.org; licensed under CC BY 4.0, https://creativecommons.org/licenses/by/4.0/). Changed by harnsy; no endorsement by The Carpentries is implied. Scope from the O*NET 31.0 Database, 13-1151.00 Training and Development Specialists and 25-9031.00 Instructional Coordinators. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
