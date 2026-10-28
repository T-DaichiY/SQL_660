"""Helpers for the 550 M1-M3 lesson generator (stats/ site skeleton, R outputs computed by Rscript)."""
import html, os, re, subprocess, tempfile, json

STATS = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern/660 - SQL/Lesson_website/stats"
SRC = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern/550-Basic Stats,R"
IMG_DIR = "img550"

def esc(s):
    return html.escape(s, quote=False)

# ---------------------------------------------------------------- R code display
KW = {"function", "TRUE", "FALSE", "NA", "NULL", "Inf", "NaN", "if", "else", "for", "in", "T", "F"}
TOK = re.compile(r'(#[^\n]*)|("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')|(\b\d+\.?\d*(?:e-?\d+)?\b)|'
                 r'([A-Za-z_.][A-Za-z0-9_.]*(?=\s*\())|(\b(?:' + "|".join(KW) + r')\b)')

def _hl_line(line):
    out, pos = [], 0
    for m in TOK.finditer(line):
        out.append(esc(line[pos:m.start()]))
        t = esc(m.group(0))
        if m.group(1): out.append(f'<span class="cm">{t}</span>')
        elif m.group(2): out.append(f'<span class="st">{t}</span>')
        elif m.group(3): out.append(f'<span class="nm">{t}</span>')
        else: out.append(f'<span class="kw">{t}</span>')
        pos = m.end()
    out.append(esc(line[pos:]))
    return "".join(out)

def code_html(src):
    lines = src.strip("\n").split("\n")
    return '<pre class="code-block">\n' + "\n".join(f'<span class="cl">{_hl_line(l)}</span>' for l in lines) + '\n</pre>'

# ---------------------------------------------------------------- R chunks (run per page)
class Page:
    def __init__(self, slug, wd=None):
        self.slug, self.wd, self.chunks = slug, wd, []

    def R(self, src, plot=False, show_code=True, w=720, h=400):
        """Register an R chunk; returns a placeholder replaced by code + real output."""
        i = len(self.chunks)
        self.chunks.append(dict(src=src.strip("\n"), plot=plot, show=show_code, w=w, h=h))
        return f"@@R{i}@@"

    def run(self):
        if not self.chunks: return []
        tmp = tempfile.mkdtemp(prefix="r550_")
        os.makedirs(f"{STATS}/{IMG_DIR}", exist_ok=True)
        lines = ['options(width = 72)']
        for i, c in enumerate(self.chunks):
            f = os.path.join(tmp, f"c{i}.R")
            open(f, "w", encoding="utf-8").write(c["src"] + "\n")
            lines.append(f'cat("\\n@@OUT{i}@@\\n")')
            if c["plot"]:
                lines.append(f'png("{STATS}/{IMG_DIR}/{self.slug}_{i}.png", width = {c["w"]}, height = {c["h"]}, res = 96)')
            lines.append(
                'withCallingHandlers(tryCatch(source("%s", echo = FALSE, print.eval = TRUE, local = globalenv()),'
                ' error = function(e) cat("Error:", conditionMessage(e), "\\n")),'
                ' warning = function(w) { cat("Warning message:\\n", conditionMessage(w), "\\n"); invokeRestart("muffleWarning") })' % f)
            if c["plot"]:
                lines.append('invisible(dev.off())')
        lines.append('cat("\\n@@END@@\\n")')
        rf = os.path.join(tmp, "main.R")
        open(rf, "w", encoding="utf-8").write("\n".join(lines))
        r = subprocess.run(["Rscript", "--vanilla", rf], cwd=self.wd or tmp, capture_output=True, text=True)
        if "@@END@@" not in r.stdout:
            raise RuntimeError(f"R failed for {self.slug}:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
        parts = re.split(r'\n@@OUT(\d+)@@\n', r.stdout.split("\n@@END@@")[0])
        outs = [""] * len(self.chunks)
        for k in range(1, len(parts), 2):
            outs[int(parts[k])] = parts[k + 1].strip("\n")
        return outs

    def fill(self, body):
        outs = self.run()
        def rep(m):
            i = int(m.group(1)); c = self.chunks[i]; o = outs[i]
            s = code_html(c["src"]) if c["show"] else ""
            if o.strip(): s += f'\n<div class="output-reveal">{esc(o)}</div>'
            if c["plot"]:
                s += (f'\n<figure class="r-fig"><img src="{IMG_DIR}/{self.slug}_{i}.png" alt="R の出力グラフ" loading="lazy"></figure>')
            return s
        return re.sub(r'@@R(\d+)@@', rep, body), outs

# ---------------------------------------------------------------- boxes
def note(t): return f'<div class="note-box">{t}</div>'
def warn(t): return f'<div class="warn-box">⚠️ {t}</div>'
def teal(t): return f'<div class="teal-box">{t}</div>'
def simple(t): return f'<div class="simple-box"><div class="simple-title">🍎 かんたん説明</div><p>{t}</p></div>'
def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="compare-table">\n<tr>{h}</tr>\n{b}\n</table>'

def practice(pid, title, task, keywords, answer_src, note_txt):
    kw = json.dumps(keywords, ensure_ascii=False).replace('"', "'")
    return f'''<div class="practice-card" id="{pid}">
    <div class="ptitle">💻 ミニ練習：{title}</div>
    <p class="ptask">{task}</p>
    <textarea class="code-editor" id="{pid}-input" rows="5"># ここにRコードを書いてください
</textarea>
    <div class="practice-toolbar">
      <button class="check-btn" onclick="checkPractice('{pid}', {kw})">✅ 答え合わせ</button>
      <button class="reveal-btn" onclick="toggleAnswer('{pid}', this)">💡 答えを見る</button>
    </div>
    <div class="check-result" id="{pid}-result"></div>
    <div class="answer-reveal" id="{pid}-answer" hidden>
      {code_html(answer_src)}
      <p class="answer-note">{note_txt}</p>
    </div>
  </div>'''

def unit(n, title, sub, body):
    circ = "①②③④⑤⑥"[n - 1]
    return f'''<div class="unit" id="unit{n}">
  <div class="unit-header">
    <div class="unit-num">{circ}</div>
    <div><h2>{title}</h2><div class="unit-sub">{sub}</div></div>
  </div>
{body}
</div>
'''

# ---------------------------------------------------------------- quiz (MCQ house rules enforced)
_PATTERN = [1, 3, 0, 2, 2, 0, 3, 1]
_counter = [0]
QUIZ_REPORT = []
POS_COUNT = [0, 0, 0, 0]

def quiz(slug, items):
    """items: (question, correct, [3 wrongs], feedback)."""
    qs, answers, fbs = [], [], []
    for qi, (q, ok, wrongs, fb) in enumerate(items, 1):
        assert len(wrongs) == 3, (slug, qi)
        pos = _PATTERN[_counter[0] % len(_PATTERN)]; _counter[0] += 1
        opts = list(wrongs); opts.insert(pos, ok)
        POS_COUNT[pos] += 1
        L = sorted((len(o) for o in opts), reverse=True)
        if len(ok) == L[0] and len(ok) > L[1]:
            QUIZ_REPORT.append(f"{slug} Q{qi}: correct is longest ({len(ok)} vs {L[1]})")
        if L[0] > L[1] * 1.15:
            QUIZ_REPORT.append(f"{slug} Q{qi}: longest >15% over 2nd ({L[0]} vs {L[1]})")
        btns = "\n".join(
            f'<button class="option-btn" data-q="{qi}" data-idx="{i}" onclick="handleQ(this)">'
            f'<span class="opt-letter">{"ABCD"[i]}</span>{o}</button>' for i, o in enumerate(opts))
        qs.append(f'<div class="quiz-q" id="q{qi}">\n  <div class="q-num">Question {qi}</div>\n'
                  f'  <div class="q-text">{q}</div>\n  <div class="options">{btns}</div>\n'
                  f'  <div class="q-feedback" id="fb{qi}"></div>\n</div>')
        answers.append(pos); fbs.append(fb)
    n = len(items)
    return f'''<div class="quiz-section" id="quiz">
  <div class="quiz-header">
    <h2>📝 確認クイズ</h2>
    <div class="quiz-score" id="score">0 / {n}</div>
  </div>
  <div class="progress-wrap"><div class="progress-bar" id="prog" style="width:0%"></div></div>
  <div class="quiz-lang-note">✏️ Questions are in English — answers are checked instantly.</div>

{chr(10).join(qs)}
</div>
<script>
var ANSWERS={json.dumps(answers)};
var FEEDBACKS={json.dumps(fbs, ensure_ascii=False)};
var score=0,done=0,total={n};
function handleQ(btn){{
  var q=+btn.dataset.q, idx=+btn.dataset.idx;
  var btns=document.querySelectorAll('[data-q="'+q+'"]');
  btns.forEach(function(b){{b.disabled=true;}});
  var fb=document.getElementById('fb'+q);
  fb.classList.add('show');
  if(idx===ANSWERS[q-1]){{
    btn.classList.add('correct');
    fb.className='q-feedback show correct-fb';
    fb.textContent='✅ Correct! '+FEEDBACKS[q-1];
    score++;
  }}else{{
    btn.classList.add('wrong');
    btns[ANSWERS[q-1]].classList.add('correct');
    fb.className='q-feedback show wrong-fb';
    fb.textContent='❌ '+FEEDBACKS[q-1];
  }}
  done++;
  document.getElementById('score').textContent=score+' / '+total;
  document.getElementById('prog').style.width=(done/total*100)+'%';
}}
</script>'''

# ---------------------------------------------------------------- page
FIG_CSS = ('<style>.r-fig{margin:.6rem 0 1.2rem;text-align:center}'
           '.r-fig img{max-width:100%;height:auto;border:1px solid #e2e8f0;border-radius:10px;background:#fff}</style>')

def page(L, prev, nxt, body):
    """L: dict(slug, mod, tag, icon, title, lead, video, units=[(id,label)], terms=[(name,en,def)], tip, footer)."""
    unav = "".join(f'<a href="#unit{i}">{lab}</a>' for i, lab in enumerate(L["unav"], 1)) + '<a href="#quiz">📝 Quiz</a>'
    terms = "\n".join(f'    <div class="term-item"><div class="term-name">{a}</div><div class="term-en">{b}</div>'
                      f'<div class="term-def">{c}</div></div>' for a, b, c in L["terms"])
    links = ['<a href="index.html">← 概要</a>']
    if prev: links.append(f'<a href="{prev[0]}.html">← {prev[1]}</a>')
    if nxt: links.append(f'<a href="{nxt[0]}.html">{nxt[1]} →</a>')
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{L["mod"]} {L["title"]}</title>
<link rel="stylesheet" href="style.css">
{FIG_CSS}
</head>
<body>
<header class="site-header">
  <div class="logo">統計 <span>レッスン</span></div>
  <nav class="header-nav">
    <a href="index.html">🏠 概要</a>
    <button type="button" class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navGroups" title="レッスン一覧を開く／閉じる">📚 {L["mod"]} <span class="nav-caret">▾</span></button>
    <div class="nav-groups" id="navGroups">
<!--NAV-->
    </div>
    <script src="nav.js"></script>
  </nav>
</header>
<div class="ch-banner">
<div class="ch-banner-inner">
  <div class="ch-tag">{L["tag"]}</div>
  <h1>{L["icon"]} {L["title"]}</h1>
  <p>{L["lead"]}</p>
  <p style="font-size:.9rem">📺 講義動画: {L["video"]}</p>
  <div class="ch-banner unit-nav" style="background:none;padding:0;">
    {unav}
  </div>
</div>
</div>
<div class="page-layout">
<main>
{body}
</main>
<aside class="sidebar">
  <div class="glossary">
    <h3>📖 用語集</h3>
{terms}
  </div>
  <div class="tip-box"><h4>💡 学習のヒント</h4><p>{L["tip"]}</p></div>
</aside>
</div>

<footer>
  <p>📊 統計レッスン：{L["mod"]} {L["title"]}</p>
  <p style="margin-top:.5rem;">{" · ".join(links)}</p>
</footer>
<script>
var units=document.querySelectorAll('.unit');
var obs=new IntersectionObserver(function(entries){{
  entries.forEach(function(e){{if(e.isIntersecting)e.target.classList.add('visible');}});
}},{{threshold:0.1}});
units.forEach(function(u){{obs.observe(u);}});
</script>
<script src="practice.js"></script>
<script src="code-summary.js"></script>
<script src="typewriter.js"></script>
<script src="../hub-fab.js"></script>
</body></html>
'''
