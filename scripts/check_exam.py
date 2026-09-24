#!/usr/bin/env python3
"""Check a generated Emar 12 grammar exam sheet.

Usage: python check_exam.py ./english-exams/present-perfect-medium.md

The paper runs 1-50 with affirmative, negative and question sentences shuffled
together and nothing announcing which is which. This script works out each
item's form from the sentence and the keyed option, then checks the mix is
balanced and genuinely interleaved - a run of the same form is the giveaway
that labelled parts used to hand students for free.

FAILs are things a teacher would discover in front of the class. WARNs are
quality problems that make the paper easier to guess than to answer.
Exit code 1 if any FAIL.
"""

import re
import sys
from collections import Counter

Q_RE = re.compile(r"^\*\*(\d+)\.\*\*\s*(.+)$")
OPT_RE = re.compile(r"([a-d])\)\s*(.*?)(?=\s{2,}[a-d]\)|\s*$)")
HEAD_RE = re.compile(r"^#{1,6}\s+(.*?)\s*$")
# a heading on the exam sheet that tells the student what form is coming, or
# blocks the paper into numbered chunks, defeats the whole point of shuffling
BANNED_HEAD_RE = re.compile(
    r"^(part|section)\b|\b(affirmative|negative|interrogative|question\s*forms?)\b"
    r"|\bquestions?\s*\d",
    re.I,
)
KEY_HEAD_RE = re.compile(r"^#{1,4}\s*Answer\s*Key", re.I)
KEY_ITEM_RE = re.compile(r"\b(\d{1,2})\.\s*([a-dA-D])\b")
NEG_RE = re.compile(r"(\bnot\b|n[’']t\b)", re.I)

# target mix out of 50, with the tolerance a real paper needs
BANDS = {"affirmative": (16, 24), "negative": (11, 19), "question": (11, 19)}
MAX_RUN = 3

fails, warns = [], []


def fail(msg):
    fails.append(msg)


def warn(msg):
    warns.append(msg)


def classify(sentence, correct_text):
    """Work out the sentence form from the item itself.

    Order matters: a negative question ("Haven't you finished?") is still a
    question as far as the student's task goes, so the '?' test comes first.
    """
    if sentence.rstrip().endswith("?"):
        return "question"
    if NEG_RE.search(sentence) or NEG_RE.search(correct_text or ""):
        return "negative"
    return "affirmative"


def parse(path):
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    questions = []          # (num, sentence, [(letter, text)])
    key = {}
    headings = []           # every heading before the answer key, title included
    in_key = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if KEY_HEAD_RE.match(line):
            in_key = True
            i += 1
            continue
        if in_key:
            for num, letter in KEY_ITEM_RE.findall(line):
                key[int(num)] = letter.lower()
            i += 1
            continue
        hm = HEAD_RE.match(line)
        if hm:
            headings.append(hm.group(1))
        qm = Q_RE.match(line)
        if qm:
            num = int(qm.group(1))
            sentence = qm.group(2).strip()
            opts = []
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                found = OPT_RE.findall(lines[j])
                if len(found) >= 2:
                    opts = [(l, t.strip()) for l, t in found]
                    i = j
            questions.append((num, sentence, opts))
        i += 1
    return questions, key, headings


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    if len(sys.argv) < 2:
        print("usage: check_exam.py <exam.md>")
        return 2
    path = sys.argv[1]
    questions, key, headings = parse(path)

    # --- structure ---
    if len(questions) != 50:
        fail("found %d questions, expected exactly 50" % len(questions))

    nums = [q[0] for q in questions]
    missing = [n for n in range(1, 51) if n not in nums]
    if missing:
        fail("missing question numbers: %s" % missing)
    dupes = [n for n, c in Counter(nums).items() if c > 1]
    if dupes:
        fail("duplicate question numbers: %s" % dupes)

    # the sheet carries its title and nothing else before the key: any further
    # heading either names a form or blocks the paper into chunks, and both
    # hand the student information the shuffle exists to withhold
    for h in headings[1:]:
        if BANNED_HEAD_RE.search(h):
            fail(
                "heading %r splits the paper - affirmative, negative and question items "
                "must run shuffled together with nothing announcing the form or the block" % h
            )
        else:
            warn(
                "unexpected heading %r before the answer key - the exam sheet normally "
                "carries only its title, then the fifty items" % h
            )

    for num, sentence, opts in questions:
        letters = [l for l, _ in opts]
        if letters != ["a", "b", "c", "d"]:
            fail("Q%d: options are %s, expected a, b, c, d on one line"
                 % (num, letters or "missing"))
        if any(not t for _, t in opts):
            fail("Q%d: an option has no text" % num)
        blanks = sentence.count("______")
        if blanks != 1:
            fail("Q%d: %d blanks in the sentence, expected exactly 1" % (num, blanks))

    # --- answer key ---
    if not key:
        fail("no answer key found (needs an '## Answer Key' section)")
    else:
        key_missing = [n for n in range(1, 51) if n not in key]
        if key_missing:
            fail("answer key missing entries for: %s" % key_missing)
        stray = [n for n in key if n < 1 or n > 50]
        if stray:
            fail("answer key has entries outside 1-50: %s" % stray)
        for num, _, opts in questions:
            letter = key.get(num)
            if letter and letter not in [l for l, _ in opts]:
                fail("Q%d: key says '%s' but that option does not exist" % (num, letter))

    # --- the mix ---
    forms = []
    for num, sentence, opts in questions:
        texts = dict(opts)
        correct = texts.get(key.get(num, ""), "")
        forms.append((num, classify(sentence, correct)))

    counts = Counter(f for _, f in forms)
    for form in ("affirmative", "negative", "question"):
        lo, hi = BANDS[form]
        n = counts.get(form, 0)
        if n < 8:
            fail("only %d %s items - the paper is not a real mix of the three forms"
                 % (n, form))
        elif not lo <= n <= hi:
            warn("%d %s items, outside the %d-%d band for a balanced paper"
                 % (n, form, lo, hi))

    runs = []
    for num, form in forms:
        if runs and runs[-1][1] == form:
            runs[-1][2] += 1
        else:
            runs.append([num, form, 1])
    for start, form, length in runs:
        if length > MAX_RUN:
            warn("Q%d starts a run of %d %s items in a row - shuffle them; more than %d "
                 "together is a pattern students ride instead of reading"
                 % (start, length, form, MAX_RUN))

    # --- quality ---
    stems = Counter(s.lower() for _, s, _ in questions)
    repeated = [s for s, c in stems.items() if c > 1]
    if repeated:
        fail("%d sentence(s) appear more than once" % len(repeated))

    optsets = Counter(
        tuple(sorted(t.lower() for _, t in opts)) for _, _, opts in questions if opts
    )
    heavy = [c for c in optsets.values() if c > 2]
    if heavy:
        warn("%d identical option set(s) reused more than twice - vary the verbs" % len(heavy))

    if key:
        dist = Counter(key.values())
        for letter in "abcd":
            n = dist.get(letter, 0)
            if n < 8 or n > 17:
                warn("answer '%s' is correct %d/50 times - spread answers more evenly "
                     "(8-17 each)" % (letter, n))

        longest_hits = 0
        counted = 0
        for num, _, opts in questions:
            if len(opts) != 4 or num not in key:
                continue
            counted += 1
            texts = dict(opts)
            correct = texts.get(key[num], "")
            if correct and len(correct) > max(len(t) for l, t in opts if l != key[num]):
                longest_hits += 1
        if counted:
            rate = longest_hits / counted
            if rate > 0.55:
                warn("the correct option is the longest one in %d/%d questions (%d%%) - "
                     "students will guess by length; chance is about 25%%"
                     % (longest_hits, counted, round(rate * 100)))
            elif rate < 0.10:
                warn("the correct option is the longest one in only %d/%d questions (%d%%) - "
                     "the wrong options look padded, which gives the paper away the other "
                     "way round; chance is about 25%%"
                     % (longest_hits, counted, round(rate * 100)))

    q_items = [(n, s) for (n, s, _), (_, f) in zip(questions, forms) if f == "question"]
    if q_items:
        leading = sum(1 for _, s in q_items if s.lstrip().startswith("______"))
        if leading < len(q_items) / 2:
            warn("only %d/%d question blanks sit at the start of the sentence - the blank "
                 "should usually test the auxiliary + subject + verb order"
                 % (leading, len(q_items)))

    # --- report ---
    for m in fails:
        print("FAIL  %s" % m)
    for m in warns:
        print("WARN  %s" % m)
    mix = " / ".join("%d %s" % (counts.get(f, 0), f)
                     for f in ("affirmative", "negative", "question"))
    if not fails and not warns:
        print("OK    %s: 50 questions, mix %s, shuffled, key complete and consistent."
              % (path, mix))
    elif not fails:
        print("PASS  %s: structure is sound (mix %s); %d quality warning(s) above."
              % (path, mix, len(warns)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
