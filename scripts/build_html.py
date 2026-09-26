#!/usr/bin/env python3
"""Turn a checked exam sheet (.md) into an interactive HTML page students solve on screen.

Usage:
  python build_html.py ./english-exams/present-perfect-grade9-medium.md
  python build_html.py ./english-exams/present-perfect-grade9-medium.md \
      --explanations ./english-exams/present-perfect-grade9-medium-teacher-key.md

Writes the .html next to the .md (same name). Run check_exam.py on the .md first:
this script reads the same questions and key, so the page can never disagree with
the checked paper.

On the page the student:
  - clicks an option (a-d); the choice fills the blank and can be changed
  - clicks "Show answer" on a question: the right option turns green, a wrong
    choice turns red, the question locks (and the teacher-key reason shows,
    when --explanations is given)
  - clicks "Finish" at the end: every question is revealed and a result panel
    shows the score, correct / wrong / unanswered counts, the time taken, and
    links to every wrong question; "Try again" starts over

The answer key is embedded lightly scrambled, so it is not readable in the page
source at a glance. That stops casual peeking, not a determined student.
Exit codes: 0 ok, 1 the sheet is not a complete 50-question paper, 2 bad usage.
"""
import argparse
import base64
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_exam import parse  # noqa: E402  (same parser as the checker)

REASON_RE = re.compile(r"^\*\*(\d+)\.\*\*\s*([a-dA-D])\)\s*(.+?)\s+[—–-]\s+(.+)$")
BLANK = "______"


def esc(text):
    return html.escape(str(text))


def md_inline(text):
    """Escape, then keep **bold** and *italic* from the sheet."""
    text = esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)


def header_parts(lines):
    """Title, the '**Grade N — ...**' line, the instructions, and the rule box lines."""
    title = next((l[2:].strip() for l in lines if l.startswith("# ")), "English Grammar Exam")
    meta = next((l.strip().strip("*").strip() for l in lines if l.startswith("**Grade")), "")
    instructions = next((re.sub(r"^\*\*Instructions:\*\*\s*", "", l).strip()
                         for l in lines if l.startswith("**Instructions:**")), "")
    rule = []
    for line in lines:
        if line.strip() == "---":
            break
        if line.startswith(">"):
            rule.append(line.lstrip(">").strip())
    return title, meta, instructions, rule


def scramble(payload, seed):
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    key = seed.encode("utf-8")
    return base64.b64encode(bytes(b ^ key[i % len(key)] for i, b in enumerate(raw))).decode("ascii")


CSS = """
:root{--bg:#f3f5ff;--card:#fff;--ink:#1e1b4b;--muted:#6b7280;--line:#e5e7eb;--soft:#f8fafc;
--brand:#6366f1;--brand2:#ec4899;--ok:#16a34a;--okbg:#dcfce7;--bad:#dc2626;--badbg:#fee2e2;--sel:#f59e0b;--selbg:#fef3c7;
--a:#6366f1;--b:#0ea5e9;--c:#f59e0b;--d:#ec4899;--shadow:0 1px 2px rgba(30,27,75,.06),0 6px 18px rgba(30,27,75,.07)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0f1024;--card:#1a1b35;--ink:#e0e7ff;--muted:#a5b4fc;
--line:#2e3060;--soft:#141530;--okbg:#0f3a24;--badbg:#45161a;--selbg:#3d2f0c;--shadow:none}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 "Nunito","Cairo","Segoe UI",system-ui,sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:20px 16px 60px}
.hero{background:linear-gradient(120deg,var(--brand),var(--brand2));color:#fff;border-radius:20px;padding:24px;box-shadow:var(--shadow)}
.hero h1{margin:0 0 6px;font-size:clamp(22px,4.5vw,32px);line-height:1.25}
.hero .meta{opacity:.92;font-weight:600}
.namebox{margin-top:14px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.namebox input{flex:1;min-width:180px;border:0;border-radius:12px;padding:10px 14px;font:inherit;color:#1e1b4b}
.card{background:var(--card);border-radius:16px;padding:16px 18px;box-shadow:var(--shadow);margin:14px 0}
.rule{border-inline-start:6px solid var(--brand)}
.rule p{margin:2px 0}
.instr{font-weight:600}
.bar{position:sticky;top:0;z-index:5;background:var(--card);border-radius:0 0 14px 14px;box-shadow:var(--shadow);
padding:10px 16px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;font-weight:700;margin:0 0 6px}
.track{flex:1;min-width:120px;height:10px;background:var(--line);border-radius:99px;overflow:hidden}
.track span{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--brand),var(--brand2));transition:width .3s}
.stat.ok{color:var(--ok)}.stat.bad{color:var(--bad)}
.q{background:var(--card);border-radius:16px;padding:16px 18px;box-shadow:var(--shadow);margin:12px 0;border-inline-start:6px solid var(--line);scroll-margin-top:70px}
.q.is-ok{border-color:var(--ok)}.q.is-bad{border-color:var(--bad)}.q.is-skip{border-color:var(--muted)}
.qhead{display:flex;gap:12px;align-items:flex-start}
.num{flex:none;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;font-weight:800;color:#fff;
background:linear-gradient(135deg,var(--brand),var(--brand2))}
.stem{margin:4px 0 12px;font-size:18px}
.blank{display:inline-block;min-width:80px;border-bottom:2px dashed var(--muted);text-align:center;padding:0 6px;font-weight:800;color:var(--brand)}
.blank.filled{border-bottom-style:solid}
.opts{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
@media (max-width:640px){.opts{grid-template-columns:1fr 1fr}}
.opt{display:flex;align-items:center;gap:8px;text-align:start;border:2px solid var(--line);background:var(--soft);color:var(--ink);
border-radius:12px;padding:8px 10px;font:inherit;font-size:16px;cursor:pointer;transition:transform .08s,border-color .15s,background .15s}
.opt:hover:not(:disabled){border-color:var(--brand);transform:translateY(-1px)}
.opt:focus-visible,.btn:focus-visible{outline:3px solid var(--brand);outline-offset:2px}
.L{flex:none;width:26px;height:26px;border-radius:8px;display:grid;place-items:center;color:#fff;font-weight:800;font-size:14px}
.opt[data-l=a] .L{background:var(--a)}.opt[data-l=b] .L{background:var(--b)}.opt[data-l=c] .L{background:var(--c)}.opt[data-l=d] .L{background:var(--d)}
.opt.sel{border-color:var(--sel);background:var(--selbg)}
.opt.right{border-color:var(--ok);background:var(--okbg)}
.opt.wrong{border-color:var(--bad);background:var(--badbg);text-decoration:line-through}
.opt:disabled{cursor:default}
.qfoot{display:flex;align-items:center;gap:12px;margin-top:10px;flex-wrap:wrap}
.btn{border:0;border-radius:12px;padding:9px 16px;font:inherit;font-weight:700;cursor:pointer;color:#fff;background:var(--brand)}
.btn.ghost{background:transparent;color:var(--brand);border:2px solid var(--brand)}
.btn.big{font-size:19px;padding:14px 26px;background:linear-gradient(120deg,var(--brand),var(--brand2))}
.btn:disabled{opacity:.5;cursor:default}
.verdict{font-weight:800}.verdict.ok{color:var(--ok)}.verdict.bad{color:var(--bad)}.verdict.skip{color:var(--muted)}
.reason{margin:10px 0 0;padding:10px 12px;border-radius:10px;background:var(--soft);border:1px dashed var(--line)}
.finish{text-align:center;margin:28px 0}
.result{text-align:center}
.ring{--p:0;width:170px;height:170px;border-radius:50%;margin:8px auto 12px;display:grid;place-items:center;
background:conic-gradient(var(--ok) calc(var(--p)*1%),var(--line) 0)}
.ring div{width:132px;height:132px;border-radius:50%;background:var(--card);display:grid;place-items:center;font-size:34px;font-weight:800}
.ring small{display:block;font-size:14px;color:var(--muted);font-weight:700}
.msg{font-size:22px;font-weight:800;margin:4px 0 12px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin:14px 0}
.tile{border-radius:14px;padding:12px;background:var(--soft);border-top:5px solid var(--c)}
.tile b{display:block;font-size:28px;color:var(--c)}
.chips{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:6px 0 14px}
.chip{display:inline-block;min-width:38px;padding:4px 8px;border-radius:99px;font-weight:800;text-decoration:none;color:#fff}
.chip.bad{background:var(--bad)}.chip.skip{background:var(--muted)}
.actions{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.muted{color:var(--muted)}
@media print{.bar,.qfoot button,.finish,.actions,.namebox input{display:none}body{background:#fff}
.q,.card{box-shadow:none;border:1px solid #ccc;break-inside:avoid}.hero{print-color-adjust:exact;-webkit-print-color-adjust:exact}}
"""

JS = r"""
(function(){
  var EX = JSON.parse(document.getElementById('exam-data').textContent);
  function decode(){
    var bin = atob(EX.secret), bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i) ^ EX.seed.charCodeAt(i % EX.seed.length);
    return JSON.parse(new TextDecoder().decode(bytes));
  }
  var ANS = decode(), KEY = ANS.key, WHY = ANS.reasons || {}, TOTAL = EX.total;
  var STORE = 'grammar-exam:' + EX.id;
  var st = {picked:{}, shown:{}, start:Date.now(), finished:false, name:''};
  try { var saved = JSON.parse(localStorage.getItem(STORE) || 'null'); if (saved) st = saved; } catch (e) {}
  function save(){ try { localStorage.setItem(STORE, JSON.stringify(st)); } catch (e) {} }
  function $(s, r){ return (r || document).querySelector(s); }
  function $$(s, r){ return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function optText(q, l){ var b = $('.opt[data-l="' + l + '"] .t', q); return b ? b.textContent : ''; }

  function paint(q){
    var n = q.dataset.n, pick = st.picked[n], shown = st.shown[n], key = KEY[n];
    var blank = $('.blank', q);
    blank.textContent = pick ? optText(q, pick) : '______';
    blank.classList.toggle('filled', !!pick);
    $$('.opt', q).forEach(function(b){
      var l = b.dataset.l;
      b.classList.toggle('sel', !shown && l === pick);
      b.classList.toggle('right', !!shown && l === key);
      b.classList.toggle('wrong', !!shown && l === pick && pick !== key);
      b.disabled = !!shown;
      b.setAttribute('aria-pressed', l === pick ? 'true' : 'false');
    });
    var v = $('.verdict', q), btn = $('.reveal', q), why = $('.reason', q);
    q.classList.remove('is-ok', 'is-bad', 'is-skip');
    if (shown) {
      btn.disabled = true;
      var ans = key + ') ' + optText(q, key);
      if (!pick) { v.className = 'verdict skip'; v.textContent = '— Not answered · لم تُجب  →  ' + ans; q.classList.add('is-skip'); }
      else if (pick === key) { v.className = 'verdict ok'; v.textContent = '✓ Correct · صحيح'; q.classList.add('is-ok'); }
      else { v.className = 'verdict bad'; v.textContent = '✗ Wrong · خطأ  →  ' + ans; q.classList.add('is-bad'); }
      if (WHY[n]) { why.textContent = '💡 ' + WHY[n]; why.hidden = false; }
    } else { btn.disabled = false; v.textContent = ''; v.className = 'verdict'; why.hidden = true; }
  }

  function tally(){
    var ok = 0, bad = 0, answered = 0;
    Object.keys(KEY).forEach(function(n){
      var p = st.picked[n];
      if (p) answered++;
      if (st.shown[n] && p) { if (p === KEY[n]) ok++; else bad++; }
    });
    return {ok:ok, bad:bad, answered:answered};
  }

  function bar(){
    var t = tally();
    $('#answered').textContent = t.answered + ' / ' + TOTAL;
    $('#okc').textContent = t.ok; $('#badc').textContent = t.bad;
    $('.track span').style.width = (100 * t.answered / TOTAL) + '%';
  }

  function result(){
    var ok = 0, bad = [], skip = [];
    Object.keys(KEY).forEach(function(n){
      var p = st.picked[n];
      if (!p) skip.push(n); else if (p === KEY[n]) ok++; else bad.push(n);
    });
    var pct = Math.round(100 * ok / TOTAL);
    var msg = pct >= 90 ? '🌟 Excellent! · ممتاز' : pct >= 75 ? '🎉 Very good · جيد جداً'
            : pct >= 50 ? '👍 Good · جيد' : '📚 Keep practising · تحتاج إلى مراجعة';
    var mins = Math.max(1, Math.round(((st.end || Date.now()) - st.start) / 60000));
    var box = $('#result');
    $('.ring', box).style.setProperty('--p', pct);
    $('#pct').firstChild.nodeValue = pct + '%';
    $('#score').textContent = ok + ' / ' + TOTAL;
    $('#msg').textContent = msg;
    $('#who').textContent = st.name ? st.name : '';
    $('#r-ok').textContent = ok; $('#r-bad').textContent = bad.length; $('#r-skip').textContent = skip.length;
    $('#r-time').textContent = mins + ' min';
    function chips(list, cls){ return list.map(function(n){ return '<a class="chip ' + cls + '" href="#q' + n + '">' + n + '</a>'; }).join(''); }
    $('#bad-list').innerHTML = bad.length ? chips(bad, 'bad') : '<span class="muted">—</span>';
    $('#skip-list').innerHTML = skip.length ? chips(skip, 'skip') : '<span class="muted">—</span>';
    box.hidden = false;
    $('#finish').hidden = true;
  }

  $$('.q').forEach(function(q){
    var n = q.dataset.n;
    $$('.opt', q).forEach(function(b){
      b.addEventListener('click', function(){
        if (st.shown[n] || st.finished) return;
        st.picked[n] = b.dataset.l; save(); paint(q); bar();
      });
    });
    $('.reveal', q).addEventListener('click', function(){ st.shown[n] = true; save(); paint(q); bar(); });
    paint(q);
  });

  var name = $('#student');
  name.value = st.name || '';
  name.addEventListener('input', function(){ st.name = name.value; save(); });

  $('#finish-btn').addEventListener('click', function(){
    var left = TOTAL - tally().answered;
    if (left > 0 && !confirm('You have ' + left + ' unanswered question(s). Finish anyway?\nلديك ' + left + ' سؤال بلا إجابة. هل تريد الإنهاء؟')) return;
    st.finished = true; st.end = Date.now();
    Object.keys(KEY).forEach(function(n){ st.shown[n] = true; });
    save(); $$('.q').forEach(paint); bar(); result();
    $('#result').scrollIntoView({behavior:'smooth'});
  });
  $('#again').addEventListener('click', function(){
    if (!confirm('Start again? Your answers will be cleared.\nهل تريد البدء من جديد؟ ستُحذف إجاباتك.')) return;
    st = {picked:{}, shown:{}, start:Date.now(), finished:false, name:st.name}; save();
    $$('.q').forEach(paint); bar(); $('#result').hidden = true; $('#finish').hidden = false; window.scrollTo(0, 0);
  });
  $('#print').addEventListener('click', function(){ window.print(); });

  bar();
  if (st.finished) result();
})();
"""


def build(md_path, reasons_path=None):
    lines = Path(md_path).read_text(encoding="utf-8").splitlines()
    questions, key, _ = parse(md_path)
    problems = []
    if len(questions) != 50:
        problems.append(f"found {len(questions)} questions, expected 50")
    for num, _, opts in questions:
        if [l for l, _ in opts] != ["a", "b", "c", "d"]:
            problems.append(f"Q{num}: options are not a-d")
        if key.get(num) not in ("a", "b", "c", "d"):
            problems.append(f"Q{num}: no valid answer key entry")
    if problems:
        return None, problems

    reasons = {}
    if reasons_path:
        for line in Path(reasons_path).read_text(encoding="utf-8").splitlines():
            m = REASON_RE.match(line.strip())
            if m:
                num, letter, text, why = int(m.group(1)), m.group(2).lower(), m.group(3), m.group(4)
                if key.get(num) != letter:
                    problems.append(f"teacher key Q{num} says '{letter}' but the answer key says '{key.get(num)}'")
                reasons[str(num)] = f"{letter}) {text} — {why}"
        if problems:
            return None, problems

    title, meta, instructions, rule = header_parts(lines)
    exam_id = Path(md_path).stem
    seed = f"{exam_id}-{len(title)}-grammar"
    payload = {"key": {str(n): l for n, l in key.items() if 1 <= n <= 50}, "reasons": reasons}
    data = {"id": exam_id, "total": len(questions), "seed": seed, "secret": scramble(payload, seed)}

    cards = []
    for num, sentence, opts in questions:
        before, _, after = sentence.partition(BLANK)
        stem = f'{md_inline(before)}<span class="blank">______</span>{md_inline(after)}'
        buttons = "".join(
            f'<button type="button" class="opt" data-l="{l}" aria-pressed="false">'
            f'<span class="L">{l}</span><span class="t">{esc(t)}</span></button>' for l, t in opts)
        cards.append(
            f'<article class="q" id="q{num}" data-n="{num}"><div class="qhead"><span class="num">{num}</span>'
            f'<div style="flex:1"><p class="stem">{stem}</p><div class="opts" role="group" aria-label="Question {num} options">'
            f'{buttons}</div></div></div><div class="qfoot"><button type="button" class="btn ghost reveal">'
            f'👁️ Show answer · أظهر الإجابة</button><span class="verdict" aria-live="polite"></span></div>'
            f'<p class="reason" hidden></p></article>')

    rule_html = ""
    if rule:
        rule_html = '<div class="card rule">' + "".join(f"<p>{md_inline(r)}</p>" for r in rule) + "</div>"
    page = f"""<!doctype html>
<html lang="en" dir="ltr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Cairo:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap">
<header class="hero"><h1>📝 {esc(title)}</h1><div class="meta">{esc(meta)}</div>
<label class="namebox">🧑‍🎓 <b>Name · الاسم</b><input id="student" type="text" autocomplete="off" placeholder="Write your name · اكتب اسمك"></label>
</header>
<div class="card instr">✏️ {md_inline(instructions)}<br><span class="muted" style="font-weight:600">
Click an option, then “Show answer” to check it — or answer everything and press “Finish” at the end.
· اختر إجابة ثم اضغط «أظهر الإجابة»، أو أجب عن كل الأسئلة واضغط «إنهاء» في الأخير.</span></div>
{rule_html}
<div class="bar" role="status"><span>📋 <span id="answered">0 / {len(questions)}</span></span>
<div class="track"><span></span></div><span class="stat ok">✓ <span id="okc">0</span></span><span class="stat bad">✗ <span id="badc">0</span></span></div>
{"".join(cards)}
<div class="finish" id="finish"><button type="button" class="btn big" id="finish-btn">🏁 Finish &amp; see my result · إنهاء وعرض النتيجة</button></div>
<section class="card result" id="result" hidden aria-live="polite">
<h2 style="margin:4px 0">🏆 Your result · نتيجتك <span id="who" class="muted"></span></h2>
<div class="ring"><div id="pct">0%<small id="score"></small></div></div>
<div class="msg" id="msg"></div>
<div class="tiles">
<div class="tile" style="--c:var(--ok)"><b id="r-ok">0</b>✓ Correct · صحيحة</div>
<div class="tile" style="--c:var(--bad)"><b id="r-bad">0</b>✗ Wrong · خاطئة</div>
<div class="tile" style="--c:var(--muted)"><b id="r-skip">0</b>— Unanswered · بلا إجابة</div>
<div class="tile" style="--c:var(--brand)"><b id="r-time">0</b>⏱️ Time · الوقت</div>
</div>
<div><b>✗ Wrong questions · الأسئلة الخاطئة</b></div><div class="chips" id="bad-list"></div>
<div><b>— Unanswered · بلا إجابة</b></div><div class="chips" id="skip-list"></div>
<div class="actions"><button type="button" class="btn" id="again">🔄 Try again · أعد المحاولة</button>
<button type="button" class="btn ghost" id="print">🖨️ Print · طباعة</button></div>
</section>
</div>
<script type="application/json" id="exam-data">{json.dumps(data)}</script>
<script>{JS}</script>
</body></html>
"""
    return page, []


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("exam_md")
    p.add_argument("--explanations", help="the teacher key .md; its reasons show after each answer is revealed")
    p.add_argument("--out", help="default: the exam path with .html")
    args = p.parse_args()
    if not Path(args.exam_md).is_file():
        print(f"FAIL  no such file: {args.exam_md}")
        return 2
    page, problems = build(args.exam_md, args.explanations)
    if problems:
        for m in problems:
            print(f"FAIL  {m}")
        return 1
    out = Path(args.out) if args.out else Path(args.exam_md).with_suffix(".html")
    out.write_text(page, encoding="utf-8")
    print(f"OK    {out}: 50 interactive questions" + (" with explanations" if args.explanations else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
