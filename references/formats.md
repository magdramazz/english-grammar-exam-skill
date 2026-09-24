# File templates

Copy these shapes literally. The checker script expects them, and so does the photocopier.

## 1. The exam sheet

````markdown
# <Grammar Topic> — <Level> Level

**Emar 12 — Grammar Exam | 50 Questions | Time: 45 minutes**

**Name:** ____________________  **Class:** ________  **Mark:** ______ / 50

**Instructions:** Choose the correct verb form (a, b, c or d) to complete each sentence.

---

**1.** My brother ______ to the university every morning.
   a) go   b) goes   c) going   d) gone

**2.** ______ she visited her grandmother in Aleppo last week?
   a) Did   b) Has   c) Does   d) Was

**3.** They ______ the report before the deadline.
   a) didn't finished   b) don't finish   c) didn't finish   d) hasn't finished

**4.** The new library ______ near the old market last year.
   a) built   b) was built   c) is built   d) has built

... through question 50, the three forms shuffled all the way ...

---

## Answer Key

1. b    2. a    3. d    4. b    5. c    6. a    7. b    8. d    9. c    10. a
11. c   12. b   13. a   14. d   15. b   16. c   17. a   18. d   19. b   20. c
21. c   22. a   23. d   24. b   25. c   26. a   27. b   28. d   29. a   30. c
31. b   32. d   33. a   34. c   35. b   36. a   37. c   38. b   39. d   40. a
41. c   42. b   43. d   44. a   45. b   46. c   47. a   48. d   49. b   50. c
````

There are no part headings and no labels telling the student which form an item is. One unbroken run of fifty, with affirmative, negative and question sentences shuffled through each other — that is what makes the paper test anything. The checker rejects a `## Part` heading outright and warns when more than three items of one form sit together.

- Question number as `**N.**` at the start of a line, numbered 1–50 with no gaps.
- Options on **one** line, `a) … b) … c) … d) …`, three spaces between them, indented three spaces.
- Exactly one blank `______` (six underscores) per sentence.
- Roughly 20 affirmative, 15 negative and 15 question items, spread across the whole paper.
- Answer key: ten answers per line, `N. x` with x in a–d, all 50 present.

The checker enforces the numbering, the single blank, the mix and the key. The spacing and indentation are printing conventions it does not check — keep them anyway so the photocopied sheet looks uniform.

**How the checker decides an item's form**, since nothing on the page labels it: a sentence ending in `?` counts as a **question**; otherwise, a negation (`not` or `n't`) anywhere in the sentence *or in the correct option* makes it **negative**; everything else is **affirmative**. Plan the balance against that rule rather than by eye, because it is easy to disagree with. A conditional such as `If the engineers had inspected the pipes, the flood ______ the basement` keys to *wouldn't have damaged* and therefore counts as negative even though the stem reads affirmative — with topics like conditionals or reported speech, half the natural items carry a negation somewhere, and an author counting by instinct lands outside the bands without knowing why.

## 2. Rule box (only when asked)

Insert directly after the **Instructions** line, before the first `---`. Keep it to 5–8 lines — it is a reminder for a student who studied, not a lesson.

```markdown
> **Quick reminder — <Topic>**
> **Form:** subject + have/has + past participle
> **Use:** an action finished at an unstated time, or still connected to now.
> **Signal words:** already, yet, just, ever, never, since, for
> **Negative:** haven't / hasn't + past participle
> **Question:** Have/Has + subject + past participle …?
```

## 3. Teacher key file (only when asked)

A second file at `./english-exams/<topic-slug>-<level>-teacher-key.md`.

```markdown
# <Grammar Topic> — <Level> Level — Teacher Key

**1.** b) goes — third person singular in the present simple; "every morning" marks a habit.
**2.** a) arrived — "last night" fixes a finished past time, so the present perfect is impossible.
```

Break it with a plain `### Questions 1–10`, `### Questions 11–20` heading every ten items — fifty unbroken lines is unreadable for a teacher scanning it mid-lesson. Number-range headings are safe here because the teacher key never reaches a student; do not put them on the exam sheet.

One line per question: number, correct letter and text, then a short reason naming the rule and the clue in the sentence. This is what the teacher reads aloud when a student argues about an answer, so the reason must point at evidence in the sentence, not just restate the rule name.

## 4. Mixed revision paper

Filename `mixed-revision-<level>.md`. Title: `# Mixed Grammar Revision — <Level> Level`.

Keep the same unlabelled run of fifty and the same rough 20/15/15 balance of forms, but draw from 5–8 grammar points and rotate through them so no two consecutive questions test the same one. A mixed paper therefore shuffles on two axes at once — grammar point and sentence form — and neither may settle into a run.

Three ordering rules apply here and they cannot all hold strictly. Rank them: **rotation first** (never two consecutive items on one topic), **then push passive and reported speech into the back half of the paper**, and treat the simple-to-hard ramp as a preference rather than a rule. Rotation wins because a student who meets three passives in a row starts answering by pattern instead of by grammar.

A rule box on a mixed paper cannot use the single-topic layout — use one line per grammar point instead, and keep the whole box to 8 lines:

```markdown
> **Quick reminder — this paper covers:**
> **Present perfect vs past simple:** finished time (yesterday) → past simple; already/yet/since → present perfect.
> **Past perfect:** had + participle for the earlier of two past actions.
> **Passive:** the right tense of *be* + past participle.
> **Conditionals:** type 1 → will + base; type 2 → past form + would.
> **Reported speech:** backshift the tense; no inversion in reported questions.
> **Modals:** modal + bare infinitive, never *to*.
> **Gerund vs infinitive:** enjoy/avoid/finish + -ing; decide/hope/agree + to.
```

The answer key stays plain — no topic tags. If a teacher key is requested, name the grammar point there instead, in each reason line:

```markdown
**7.** c) had left — past perfect; the leaving happened before "when I arrived".
```

## Where the key goes

The answer key is the last thing in the file. Anything numbered placed after it — a note like "50 marks total" — gets read as a key entry and corrupts the check.

## File naming

Lowercase, hyphenated, no spaces:

| Topic | Slug |
|---|---|
| Present perfect | `present-perfect` |
| Past simple vs past continuous | `past-simple-vs-continuous` |
| Passive voice | `passive-voice` |
| Conditionals type 2 | `conditionals-type-2` |
| Reported speech | `reported-speech` |
| Gerund vs infinitive | `gerund-vs-infinitive` |
| Mixed revision | `mixed-revision` |
