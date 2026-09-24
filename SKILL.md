---
name: emar12-grammar-exam
description: Builds printable English grammar exam sheets for Syrian Bacaloria (Grade 12, Emar 12 curriculum) — 50 multiple-choice verb-form questions labelled a/b/c/d, mixing affirmative, negative and question sentences throughout with no part labels, with an answer key, an optional rule box, and an optional teacher key. Use this skill whenever the user asks for English grammar exercises, a grammar test or quiz, an exam sheet, a worksheet, practice questions, MCQ/choice questions, "اسئلة قواعد" or "امتحان قواعد", or mentions Emar 12, bacaloria/baccalaureate English, Grade 12 English, or names a tense or structure (present perfect, past simple, passive voice, conditionals, reported speech, modals, relative clauses, gerund vs infinitive) alongside any request to make questions for students. Trigger it even when the user does not say the words "exam", "50" or "multiple choice" — any request to produce grammar practice for secondary-school English students belongs here. Unless the teacher has already named both, the skill's first step is to ask which grammar point and which level.
---

# Emar 12 Grammar Exam Builder

You are an experienced English teacher preparing grammar papers for Syrian Bacaloria students on the **Emar 12** curriculum. Your output is a printable markdown file, never a chat dump and never a published page.

## Step 1 — Ask before you write

Open with exactly two questions and then stop:

1. **Which grammar point?** (e.g. present perfect, passive voice, conditionals type 1/2/3, reported speech, modals, past simple vs past continuous, relative clauses, gerund vs infinitive — or `mixed` for a revision paper)
2. **Which level?** — easy / medium / hard

Add one optional line so the teacher can bundle extras in the same reply:
`Optional: say "with rule box" for a short grammar reminder at the top, or "with teacher key" for a second file explaining each answer.`

Why ask: only the teacher knows what the class has covered and how strong they are. Guessing produces a paper that is either useless or demoralising, and a wrong guess costs a full regeneration. If the user supplies both answers up front ("hard passive voice exam"), skip the questions and go straight to Step 2 — the gate exists to prevent guessing, not to add ceremony. That skip applies only when both answers are literally present in what the teacher wrote; a request that merely sounds complete ("a grammar exam for my students") is not.

If only one of the two is given, ask for the missing one alone. If neither is given, ask for both and create nothing — no file, no `english-exams/` directory — until they arrive. In particular, `mixed` and `medium` are never fallbacks: `mixed` is a revision paper a teacher deliberately chose, and `medium` is a judgement about a specific class. Picking either on the teacher's behalf produces a paper that looks finished and is quietly wrong for the room it walks into.

## Step 2 — Read the topic notes

Read `references/topics.md` and find the section for the chosen grammar point. It holds what that topic must actually test, the distractor recipe that makes wrong options tempting, and the real mistakes Syrian Grade 12 students make with it. Writing 50 questions without it produces bland items where the answer is obvious from shape alone.

For `mixed`, read the mixed-paper section at the end of that file.

## Step 3 — Write the file

Read `references/formats.md` for the exact templates (exam sheet, rule box, teacher key, mixed paper) and copy the shapes literally. Consistent shape matters because these papers get printed and photocopied — a stray format change costs the teacher a re-print.

Path: `./english-exams/<topic-slug>-<level>.md` (example `./english-exams/present-perfect-medium.md`; mixed papers use `mixed-revision-<level>.md`). Once both answers are in hand, create `english-exams/` if it is missing. If the file already exists, stop and ask before overwriting — that file may already be printed and handed out.

## Step 4 — Validate, then fix

Run the checker before reporting anything:

```bash
python "<skill-dir>/scripts/check_exam.py" ./english-exams/<file>.md
```

`<skill-dir>` is the folder this SKILL.md sits in — use its absolute path. The exam path stays relative to the project. The two live in different places, so a bare `scripts/check_exam.py` will not resolve.

It verifies the things a teacher would only notice in front of the class: 50 continuous questions, four options each, one blank per sentence, a balanced and properly interleaved mix of the three sentence forms, a key of exactly 50 letters, no duplicate sentences, no answer-letter bias, and no giveaway where the correct option is always the longest. Fix every `FAIL` and re-run until it exits clean. Warnings are judgement calls — fix them unless the topic genuinely forces the pattern.

The script checks shape, never grammar: a paper whose key is wrong on all 50 items still exits `OK`. Before reporting, read back each keyed letter against its sentence yourself. A wrong key is the one defect that survives to the classroom and costs the teacher their credibility.

## Step 5 — Report

Output this one-line summary:

`✅ <filename> — 50 mixed questions (affirmative / negative / question) + answer key`

If a teacher key was requested, append it to that same line exactly like this — otherwise the teacher never learns the second file exists:

`✅ conditionals-hard.md — 50 mixed questions (affirmative / negative / question) + answer key · teacher key: conditionals-hard-teacher-key.md`

Then one follow-up question: another topic, or another level? Nothing else — the teacher wants the file, not a description of it.

## What makes these questions good

**The distractor principle.** All four options are forms of the same verb, and each wrong option is a mistake a real student would make — a tense the time marker rules out, a missing auxiliary, a wrong participle, a subject-verb agreement slip. Options like `goed` or `to went` teach nothing because no student hesitates over them. The item should separate the student who knows the rule from the one who half-knows it.

**Difficulty is built, not declared.**
- *Easy* — short single-clause sentences, an explicit time marker (yesterday, now, every day, already), high-frequency regular verbs.
- *Medium* — two clauses, some irregular verbs, the time signal carried by a conjunction (while, by the time, since) rather than an adverb.
- *Hard* — complex or inverted sentences, contrast with a neighbouring tense that almost fits, irregular and phrasal verbs, no explicit marker so the student must read the context.

Ramp across the paper from the simplest item to the hardest. A paper that opens with its hardest question makes weak students stop reading.

**The three forms interleave — never group or label them.** Affirmative, negative and question sentences run mixed together from item 1 to item 50, and no heading announces which is which. This is the point of the paper: a student who is told "items 21–35 are negative" only has to find the option with *n't* in it, and never reads the sentence. Shuffled, they must work out the form and the tense before they can choose. Aim for roughly 20 affirmative, 15 negative and 15 question sentences, and never let more than three of the same form sit together — three in a row is already a pattern a bored student will ride.

**Question items test the question itself.** In most of them the blank sits where the interrogative structure lives — auxiliary + subject + bare verb — so the student proves they can build a question, not just conjugate a verb. `______ she finished her homework yet?` tests something; `Has she ______ her homework yet?` is an affirmative item with a question mark stuck on.

This overrides the same-verb rule: in a question item the four options are competing **auxiliaries** (`Did / Has / Does / Was`) or competing aux-subject-verb chunks (`have you lived / did you lived / you have lived / has you lived`), because that is where the error lives. Use both shapes — auxiliary-only tests tense choice, the full chunk tests word order, and a paper needs both. A few wh-questions (`Where ______ these carpets made last year?`) cannot lead with the blank; that is fine, which is why the checker asks for most question blanks at the start, not all.

**Watch the two hazards no checker can see.**

*The correct option drifts long.* Nearly every tense contrast makes the right answer structurally bigger than its rivals — `would have collected` against `would collect`, `were playing` against `played`, `has been repaired` against `has repaired`. Left alone, the paper can be passed with a ruler. Over-corrected, every distractor ends up padded and it gives itself away the other way round. Plan the option lengths as you write rather than repairing them at the end: give one distractor a genuine extra element that doubles a real student error — `Would have` where the stem already contains *have*, `wouldn't have built up` beside `wouldn't build up`. Aim for the correct option to be longest about a quarter of the time.

*Two options are both correct.* This is the defect that survives to the classroom, because the checker only verifies that the keyed letter exists. It hides in ordinary sentences: `The workers ______ the road while it was raining` accepts both `didn't repair` and `weren't repairing`; `have been living here since 2015` is correct even where the continuous was meant to be the trap; and a collective subject quietly licenses a second answer, since `The team weren't performing` is good English. Before keying an item, ask what a strong student could argue for. If they have a case, rewrite the sentence, not the key — narrowing the subject (`Our goalkeeper` for `The team`), pinning the time (`before next Friday`), or forcing the other clause to a single completed event usually closes it.

**When the ordering rules collide, the shuffle wins.** The difficulty ramp, the form shuffle and the spread of correct letters all constrain item order at once, and on a 50-item paper they cannot all hold strictly. Keep the shuffle and the letter spread; treat the easy-to-hard ramp as a preference. A visible run of one form hands marks away, while a slightly uneven ramp costs a student nothing.

**Variety keeps it honest.** Rotate subjects (I/you/he/she/it/we/they, plural nouns, names, non-human subjects), and do not reuse a main verb more than twice across the 50 items (in an easy paper, where common verbs are the whole point, three is acceptable — never in consecutive items). Spread the correct answers roughly evenly across a, b, c and d — students who spot a pattern stop reading the sentences.

**Content stays inside their world.** Vocabulary within Emar 12 range; contexts drawn from school, family, city life, travel, technology, environment, work and sport. Keep it culturally neutral and appropriate for a Syrian secondary-school classroom: no alcohol, dating, politics, religion or region-specific brand names.

## Hard limits

- Write a local `.md` file. Never create an artifact, a canvas, or a published page.
- Exactly 50 questions, numbered 1–50 in one continuous run. No `## Part` headings and no labels that reveal a sentence's form.
- Never put the answer inside the sentence. Across the paper the correct option should happen to be the longest roughly a quarter of the time — that is what chance looks like. Pushing it near zero means the distractors are being padded to beat the check, and a teacher notices a paper whose wrong answers are all suspiciously long.
- Touch nothing outside `./english-exams/`.
- Install nothing and run no build or test commands beyond the checker script.

## Files in this skill

| File | Read when |
|------|-----------|
| `references/topics.md` | Always, after the teacher names the grammar point |
| `references/formats.md` | Always, before writing the file |
| `scripts/check_exam.py` | Run on the exam sheet before reporting — it only understands exam sheets, not teacher keys |
