# Emar 12 Grammar Exam Builder

A [Claude Code](https://claude.com/claude-code) skill that builds printable English grammar exam sheets for Syrian Bacaloria students (Grade 12, **Emar 12** curriculum).

Each paper has **50 multiple-choice verb-form questions** (a/b/c/d). Affirmative, negative and question sentences are mixed together with no part labels, so students have to read every sentence. Every paper comes with an answer key.

## Features

- **Grammar points:** present perfect, past simple vs past continuous, passive voice, conditionals (type 1/2/3), reported speech, modals, relative clauses, gerund vs infinitive, or a `mixed` revision paper
- **Three levels:** easy / medium / hard. Difficulty comes from how the sentences are built (clause count, time markers, irregular and phrasal verbs), not just from the label.
- **Realistic distractors:** each wrong option is a mistake real students make
- **Optional extras:** a short grammar rule box at the top, and a separate teacher key that explains each answer
- **Built-in checker:** `scripts/check_exam.py` checks the shape of each paper: 50 continuous items, four options each, a balanced and interleaved mix of sentence forms, an even spread of answer letters, and no "the longest option is always right" giveaway

## Installation

Clone the repository into your Claude Code skills folder:

```bash
# macOS / Linux
git clone https://github.com/magdramazz/emar12-grammar-exam.git ~/.claude/skills/emar12-grammar-exam

# Windows (PowerShell)
git clone https://github.com/magdramazz/emar12-grammar-exam.git "$env:USERPROFILE\.claude\skills\emar12-grammar-exam"
```

Restart Claude Code and the skill is available.

## Usage

Ask for a grammar exam in plain language:

```
/emar12-grammar-exam hard passive voice exam with teacher key
```

or simply:

```
Make a grammar quiz for my Grade 12 students
```

If you haven't said which grammar point and level you want, the skill asks for them first. It then writes the paper to `./english-exams/<topic>-<level>.md`, for example `./english-exams/present-perfect-medium.md`.

To check a paper yourself:

```bash
python scripts/check_exam.py ./english-exams/present-perfect-medium.md
```

## Repository layout

| Path | Purpose |
|------|---------|
| `SKILL.md` | The skill's instructions and quality rules |
| `references/topics.md` | Per-topic notes: what to test, how to build distractors, common student mistakes |
| `references/formats.md` | Templates for the exam sheet, rule box, teacher key and mixed paper |
| `scripts/check_exam.py` | Checks the structure of a generated exam sheet (Python 3, no dependencies) |

> The checker checks structure, not grammar. Always read the answer key against the questions before printing.

## License

[MIT](LICENSE.md)
