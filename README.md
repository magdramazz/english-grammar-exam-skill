# English Grammar Exam Builder

A [Claude Code](https://claude.com/claude-code) skill that builds printable (Markdown) or interactive (HTML) English grammar exams for Syrian school students at **any grade — from Grade 1 (first class) up to Grade 12 Bacaloria** (Emar 12).

Each paper has **50 multiple-choice verb-form questions** (a/b/c/d). Affirmative, negative and question sentences are mixed together with no part labels, so students have to read every sentence. Every paper comes with an answer key.

## Features

- **Every grade, 1–12:** the grade sets the vocabulary, sentence length and which structures are fair game. Grade 1 gets short sentences with *am/is/are*, Bacaloria gets complex sentences with conditionals and the passive.
- **Grammar points:** verb to be, have got, there is/are, can/can't, present simple vs continuous, present perfect, past simple vs past continuous, passive voice, conditionals (type 1/2/3), reported speech, modals, relative clauses, gerund vs infinitive, or a `mixed` revision paper
- **Three levels within each grade:** easy / medium / hard. Difficulty comes from how the sentences are built (clause count, time markers, irregular and phrasal verbs), not just from the label.
- **Realistic distractors:** each wrong option is a mistake real students make
- **Optional extras:** a short grammar rule box at the top, and a separate teacher key that explains each answer
- **Interactive HTML page (optional):** a colorful page students solve on a phone or computer. They pick an answer, press **Show answer** on any question to see if they were right (green / red), and press **Finish** to get a result panel: score, correct / wrong / unanswered counts, time taken, and links to every wrong question. Buttons are in English and Arabic. With a teacher key, the reason for each answer appears after it is revealed.
- **Built-in checker:** `scripts/check_exam.py` checks the shape of each paper: 50 continuous items, four options each, a balanced and interleaved mix of sentence forms, an even spread of answer letters, and no "the longest option is always right" giveaway

## Installation

Clone the repository into your Claude Code skills folder:

```bash
# macOS / Linux
git clone https://github.com/magdramazz/english-grammar-exam-skill.git ~/.claude/skills/english-grammar-exam-skill

# Windows (PowerShell)
git clone https://github.com/magdramazz/english-grammar-exam-skill.git "$env:USERPROFILE\.claude\skills\english-grammar-exam-skill"
```

Restart Claude Code and the skill is available.

## Usage

Ask for a grammar exam in plain language:

```
/english-grammar-exam-skill hard passive voice exam for grade 12 with teacher key
```

or simply:

```
Make a grammar quiz for my Grade 4 students
```

If you haven't said which grammar point, grade, level and format (Markdown, HTML or both) you want, the skill asks for them first. It then writes the paper to `./english-exams/<topic>-grade<N>-<level>.md`, for example `./english-exams/verb-to-be-grade2-easy.md`, and for HTML also `./english-exams/verb-to-be-grade2-easy.html` — open it in any browser, or send it to students.

To check a paper yourself, or build its HTML page:

```bash
python scripts/check_exam.py ./english-exams/verb-to-be-grade2-easy.md
python scripts/build_html.py ./english-exams/verb-to-be-grade2-easy.md [--explanations <teacher-key.md>]
```

## Repository layout

| Path | Purpose |
|------|---------|
| `SKILL.md` | The skill's instructions and quality rules |
| `references/topics.md` | Grade guide plus per-topic notes: what to test, how to build distractors, common student mistakes |
| `references/formats.md` | Templates for the exam sheet, rule box, teacher key and mixed paper |
| `scripts/check_exam.py` | Checks the structure of a generated exam sheet (Python 3, no dependencies) |
| `scripts/build_html.py` | Builds the interactive HTML page from a checked sheet (Python 3, no dependencies) |

> The checker checks structure, not grammar. Always read the answer key against the questions before printing.

## License

[MIT](LICENSE.md)
