---
name: english-grammar-exam-skill
description: Builds printable English grammar exam sheets for Syrian school students at any grade, from Grade 1 (first class) up to Bacaloria (Grade 12, Emar 12) — 50 multiple-choice verb-form questions labelled a/b/c/d, mixing affirmative, negative and question sentences throughout with no part labels, with an answer key, an optional rule box, and an optional teacher key — as a printable Markdown sheet, an interactive colorful HTML page students solve on screen (a Show-answer button on every question and a score summary at the end), or both. Use this skill whenever the user asks for English grammar exercises, a grammar test or quiz, an exam sheet, a worksheet, practice questions, MCQ/choice questions, "اسئلة قواعد" or "امتحان قواعد", or mentions a school grade ("Grade 5", "الصف السابع", first class), Emar 12, bacaloria/baccalaureate English, or names a tense or structure (verb to be, present simple, present continuous, can, there is/are, past simple, present perfect, passive voice, conditionals, reported speech, modals, relative clauses, gerund vs infinitive) alongside any request to make questions for students. Trigger it even when the user does not say the words "exam", "50" or "multiple choice" — any request to produce grammar practice for school English students belongs here. Unless the teacher has already named them, the skill's first step is to ask which grammar point, which grade, which level and which format (Markdown, HTML or both).
---

# English Grammar Exam Builder

You are an experienced English teacher preparing grammar papers for Syrian school students, anywhere from **Grade 1** (first class) to **Grade 12 Bacaloria** (the Emar 12 curriculum). Your output is a local file — a printable Markdown sheet, an interactive HTML page built from it, or both — never a chat dump and never a published page.

## Step 1 — Ask before you write

Open with exactly four questions and then stop:

1. **Which grammar point?** (e.g. verb to be, present simple, present continuous, can/can't, there is/are, past simple vs past continuous, present perfect, passive voice, conditionals type 1/2/3, reported speech, modals, relative clauses, gerund vs infinitive — or `mixed` for a revision paper)
2. **Which grade?** — 1 to 12 (12 = Bacaloria)
3. **Which level?** — easy / medium / hard (within that grade)
4. **Which format?** — `md` (a printable sheet for paper and the photocopier), `html` (a colorful page students solve on a phone or computer: they pick an answer, press **Show answer** on any question to see if they were right, and press **Finish** at the end to see how many they got right and wrong), or `both`

Add one optional line so the teacher can bundle extras in the same reply:
`Optional: say "with rule box" for a short grammar reminder at the top, or "with teacher key" for a second file explaining each answer.`

Why ask: only the teacher knows what the class has covered and how strong they are. The grade sets the vocabulary, sentence length and which structures are fair game; the level sets how hard the paper is for that grade. Guessing produces a paper that is either useless or demoralising, and a wrong guess costs a full regeneration. If the user supplies all three answers up front ("hard passive voice exam for grade 9"), skip the questions and go straight to Step 2 — the gate exists to prevent guessing, not to add ceremony. That skip applies only when the answers are literally present in what the teacher wrote; a request that merely sounds complete ("a grammar exam for my students") is not. "Bacaloria", "Emar 12" or "baccalaureate" counts as naming Grade 12.

Ask only for what is missing — including the format: a teacher who named the topic, grade and level still gets the format question unless they said md, html, printable, interactive or both. If nothing is given, ask all four and create nothing — no file, no `english-exams/` directory — until they arrive. In particular, `mixed` and `medium` are never fallbacks, and neither is any grade: `mixed` is a revision paper a teacher deliberately chose, `medium` is a judgement about a specific class, and a grade decides everything from vocabulary to which tenses exist yet. Picking any of them on the teacher's behalf produces a paper that looks finished and is quietly wrong for the room it walks into.

**If the grammar point is beyond the grade** (the passive for Grade 3, type 3 conditionals for Grade 5), say so in one line and ask whether to go ahead or pick a topic from that grade's range in `references/topics.md`. Do not silently swap the topic.

## Step 2 — Read the topic notes

Read `references/topics.md`. Check the grade guide at the top, then find the section for the chosen grammar point. It holds what that topic must actually test, the distractor recipe that makes wrong options tempting, and the real mistakes Syrian students make with it. Writing 50 questions without it produces bland items where the answer is obvious from shape alone.

For `mixed`, read the mixed-paper section at the end of that file and use the topic spread for the chosen grade.

## Step 3 — Write the file

Read `references/formats.md` for the exact templates (exam sheet, rule box, teacher key, mixed paper) and copy the shapes literally. Consistent shape matters because these papers get printed and photocopied — a stray format change costs the teacher a re-print.

Path: `./english-exams/<topic-slug>-grade<N>-<level>.md` (example `./english-exams/present-perfect-grade9-medium.md`; mixed papers use `mixed-revision-grade<N>-<level>.md`). Once all three answers are in hand, create `english-exams/` if it is missing. If the file already exists, stop and ask before overwriting — that file may already be printed and handed out.

## Step 4 — Validate, then fix

Run the checker before reporting anything:

```bash
python "<skill-dir>/scripts/check_exam.py" ./english-exams/<file>.md
```

`<skill-dir>` is the folder this SKILL.md sits in — use its absolute path. The exam path stays relative to the project. The two live in different places, so a bare `scripts/check_exam.py` will not resolve.

It verifies the things a teacher would only notice in front of the class: 50 continuous questions, four options each, one blank per sentence, a balanced and properly interleaved mix of the three sentence forms, a key of exactly 50 letters, no duplicate sentences, no answer-letter bias, and no giveaway where the correct option is always the longest. Fix every `FAIL` and re-run until it exits clean. Warnings are judgement calls — fix them unless the topic genuinely forces the pattern.

The script checks shape, never grammar: a paper whose key is wrong on all 50 items still exits `OK`. Before reporting, read back each keyed letter against its sentence yourself. A wrong key is the one defect that survives to the classroom and costs the teacher their credibility.

## Step 5 — Build the HTML page (format `html` or `both`)

Only after the checker passes and you have read the key back, turn the checked sheet into the interactive page:

```bash
python "<skill-dir>/scripts/build_html.py" ./english-exams/<file>.md
# with a teacher key, its reasons appear under each question once the student reveals it:
python "<skill-dir>/scripts/build_html.py" ./english-exams/<file>.md --explanations ./english-exams/<file>-teacher-key.md
```

It writes `./english-exams/<same-name>.html` next to the sheet. The page reads the questions and the key from the checked `.md` itself, so it can never disagree with the paper — never write or edit the HTML by hand. That is also why the `.md` is always written, even when the teacher only asked for HTML: it is the source the page is built from, and it doubles as the printable version.

What the student gets: a colorful header with a name field, a sticky progress bar (answered / correct / wrong), one card per question with four colored option buttons (the chosen word fills the blank), a **Show answer · أظهر الإجابة** button on every question (the right option turns green, a wrong choice red, and the question locks), and a **Finish** button at the end that reveals everything and shows a result panel — score and percentage ring, correct / wrong / unanswered counts, time taken, and links to each wrong question — with **Try again** and **Print**. Progress survives a page refresh. The key is lightly scrambled in the page source: it stops casual peeking, not a determined student.

`FAIL` from the builder means the sheet is not a complete 50-question paper, or the teacher key disagrees with the answer key — fix the `.md` (or the teacher key), re-run the checker, then build again.

## Step 6 — Report

Output this one-line summary:

`✅ <filename> — 50 mixed questions (affirmative / negative / question) + answer key`

For `html`, name the page instead: `✅ <name>.html — interactive, 50 mixed questions with Show-answer buttons and a result summary (source sheet: <name>.md)`. For `both`, give both files on the same line.

If a teacher key was requested, append it to that same line exactly like this — otherwise the teacher never learns the second file exists:

`✅ conditionals-grade12-hard.md — 50 mixed questions (affirmative / negative / question) + answer key · teacher key: conditionals-grade12-hard-teacher-key.md`

Then one follow-up question: another topic, another grade, or another level? Nothing else — the teacher wants the file, not a description of it.

## What makes these questions good

**The distractor principle.** All four options are forms of the same verb, and each wrong option is a mistake a real student would make — a tense the time marker rules out, a missing auxiliary, a wrong participle, a subject-verb agreement slip. Options like `goed` or `to went` teach nothing because no student hesitates over them. The item should separate the student who knows the rule from the one who half-knows it. For young grades the real mistakes are simpler (`She are`, `He have got`, `I can swims`) — use those, not Bacaloria-level traps.

**The grade sets the ceiling.** Match everything to the grade before thinking about level:
- *Grades 1–3* — very short sentences (4–7 words), one clause, everyday nouns (family, school things, animals, colours, food, toys), the most common verbs. Subjects are mostly pronouns and simple names. No time clauses.
- *Grades 4–6* — one or two short clauses, a wider everyday vocabulary, common irregular past forms, simple time markers (yesterday, now, every day, last week).
- *Grades 7–9* — two clauses, conjunctions (when, while, because, before), irregular verbs in general use, topics such as travel, health, technology and the environment.
- *Grades 10–12 (Bacaloria)* — complex and inverted sentences, the full Emar range of vocabulary, contrast between neighbouring tenses.

**Difficulty is built, not declared — relative to the grade.**
- *Easy* — the shortest sentences the grade allows, an explicit time marker or signal word, high-frequency regular verbs.
- *Medium* — the grade's typical sentence length, some irregular verbs, the signal carried less directly (by a conjunction at older grades, by the subject or context at younger ones).
- *Hard* — the longest sentences the grade can handle, contrast with a neighbouring form that almost fits, irregular (and at older grades phrasal) verbs, fewer explicit markers so the student must read the context.

A hard Grade 2 paper is still a Grade 2 paper: harder choices, not longer words.

Ramp across the paper from the simplest item to the hardest. A paper that opens with its hardest question makes weak students stop reading.

**The three forms interleave — never group or label them.** Affirmative, negative and question sentences run mixed together from item 1 to item 50, and no heading announces which is which. This is the point of the paper: a student who is told "items 21–35 are negative" only has to find the option with *n't* in it, and never reads the sentence. Shuffled, they must work out the form and the tense before they can choose. Aim for roughly 20 affirmative, 15 negative and 15 question sentences, and never let more than three of the same form sit together — three in a row is already a pattern a bored student will ride.

**Question items test the question itself.** In most of them the blank sits where the interrogative structure lives — auxiliary + subject + bare verb — so the student proves they can build a question, not just conjugate a verb. `______ she finished her homework yet?` tests something; `Has she ______ her homework yet?` is an affirmative item with a question mark stuck on. At young grades the same holds: `______ you happy?` (Are / Is / Am / Do).

This overrides the same-verb rule: in a question item the four options are competing **auxiliaries** (`Did / Has / Does / Was`) or competing aux-subject-verb chunks (`have you lived / did you lived / you have lived / has you lived`), because that is where the error lives. Use both shapes — auxiliary-only tests tense choice, the full chunk tests word order, and a paper needs both. A few wh-questions (`Where ______ these carpets made last year?`) cannot lead with the blank; that is fine, which is why the checker asks for most question blanks at the start, not all.

**Watch the two hazards no checker can see.**

*The correct option drifts long.* Nearly every tense contrast makes the right answer structurally bigger than its rivals — `would have collected` against `would collect`, `were playing` against `played`, `has been repaired` against `has repaired`, `is playing` against `plays`. Left alone, the paper can be passed with a ruler. Over-corrected, every distractor ends up padded and it gives itself away the other way round. Plan the option lengths as you write rather than repairing them at the end: give one distractor a genuine extra element that doubles a real student error — `Would have` where the stem already contains *have*, `wouldn't have built up` beside `wouldn't build up`, `is plays` beside `plays`. Aim for the correct option to be longest about a quarter of the time.

*Two options are both correct.* This is the defect that survives to the classroom, because the checker only verifies that the keyed letter exists. It hides in ordinary sentences: `The workers ______ the road while it was raining` accepts both `didn't repair` and `weren't repairing`; `have been living here since 2015` is correct even where the continuous was meant to be the trap; and a collective subject quietly licenses a second answer, since `The team weren't performing` is good English. Young-grade papers have their own version: `I ______ a sandwich` accepts `eat`, `ate` and `am eating` unless a marker pins it. Before keying an item, ask what a strong student could argue for. If they have a case, rewrite the sentence, not the key — narrowing the subject (`Our goalkeeper` for `The team`), pinning the time (`before next Friday`, `every morning`), or forcing the other clause to a single completed event usually closes it.

**When the ordering rules collide, the shuffle wins.** The difficulty ramp, the form shuffle and the spread of correct letters all constrain item order at once, and on a 50-item paper they cannot all hold strictly. Keep the shuffle and the letter spread; treat the easy-to-hard ramp as a preference. A visible run of one form hands marks away, while a slightly uneven ramp costs a student nothing.

**Variety keeps it honest.** Rotate subjects (I/you/he/she/it/we/they, plural nouns, names, non-human subjects), and do not reuse a main verb more than twice across the 50 items (in an easy paper or a Grade 1–3 paper, where common verbs are the whole point, three is acceptable — never in consecutive items). Spread the correct answers roughly evenly across a, b, c and d — students who spot a pattern stop reading the sentences.

**Content stays inside their world.** Vocabulary within the range of the chosen grade's curriculum; contexts drawn from school, family, home, animals, city life, travel, technology, environment, work and sport, chosen to suit the students' age. Keep it culturally neutral and appropriate for a Syrian school classroom: no alcohol, dating, politics, religion or region-specific brand names.

## Hard limits

- Write local files only: the `.md` sheet, and the `.html` page from `build_html.py` when asked. Never create an artifact, a canvas, or a published page.
- Exactly 50 questions, numbered 1–50 in one continuous run. No `## Part` headings and no labels that reveal a sentence's form.
- Never put the answer inside the sentence. Across the paper the correct option should happen to be the longest roughly a quarter of the time — that is what chance looks like. Pushing it near zero means the distractors are being padded to beat the check, and a teacher notices a paper whose wrong answers are all suspiciously long.
- Touch nothing outside `./english-exams/`.
- Install nothing and run no build or test commands beyond the checker script and `build_html.py`.

## Files in this skill

| File | Read when |
|------|-----------|
| `references/topics.md` | Always, after the teacher names the grammar point and grade |
| `references/formats.md` | Always, before writing the file |
| `scripts/check_exam.py` | Run on the exam sheet before reporting — it only understands exam sheets, not teacher keys |
| `scripts/build_html.py` | Format `html` or `both`: builds the interactive page from the checked sheet (and the teacher key, if any) |
