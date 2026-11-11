#!/usr/bin/env python3
"""Build python670/: 6 lesson pages + index + practice notebook (student + answers).
Run with a Python that has numpy/pandas/scikit-learn/matplotlib/nbformat/nbclient:
    <venv>/bin/python build.py
Page code is executed for real, so every printed number on the pages is genuine."""
import os, re, sys, json, html, keyword, shutil, ast, io, contextlib, subprocess
import nbformat
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)                       # .../python670
REPO = os.path.dirname(SITE)
sys.path.insert(0, HERE)
import nbdata as N
from nbdata import SETUP

ANSWERS_DIR = os.path.join(os.path.dirname(os.path.dirname(REPO)), "550-Basic Stats,R", "670 ML Review")
NB_NAME = "ml670_py_practice.ipynb"

# ------------------------------------------------------------------ highlighting (static Python colouring)
KW = set(keyword.kwlist)
TOK = re.compile(r'''(?P<cm>\#[^\n]*)|(?P<st>"[^"\n]*"|'[^'\n]*')|(?P<nm>(?<![\w.])\d+\.?\d*(?:e-?\d+)?|(?<![\w])\.\d+)|(?P<id>[A-Za-z_]\w*)|(?P<op>\*\*|>=|<=|==|[-+*/=<>|&~])''', re.X)
def hl(code):
    out, pos = [], 0
    for m in TOK.finditer(code):
        out.append(html.escape(code[pos:m.start()], quote=False))
        t, k = m.group(), m.lastgroup
        if k == 'id':
            after, before = code[m.end():], code[:m.start()]
            if t in KW: k = 'kw'
            elif t in ('True', 'False', 'None'): k = 'nm'
            elif re.match(r'\s*=(?!=)', after) and before.count('(') + before.count('[') > before.count(')') + before.count(']'): k = 'pa'
            elif after.startswith('('): k = 'cls' if t[0].isupper() and '_' not in t else 'fn'
            elif t[0].isupper() and '_' not in t and len(t) > 1 and not t.isupper(): k = 'cls'
            elif before.endswith('.') and not re.search(r'(^|\n)\s*(from|import)\b[^\n]*$', before): k = 'at'
            else: k = None
        e = html.escape(t, quote=False)
        out.append(f'<span class="{k}">{e}</span>' if k else e); pos = m.end()
    out.append(html.escape(code[pos:], quote=False))
    return ''.join(out)

def code_block(src, out=None):
    lines = hl(src.rstrip('\n')).split('\n')
    pre = '<pre class="code-block">\n' + '\n'.join(f'<span class="cl">{l}</span>' for l in lines) + '\n</pre>'
    if out: pre += f'\n<div class="output-reveal">{html.escape(out.rstrip())}</div>'
    return pre

# ------------------------------------------------------------------ running page code for real
RUNNER = r'''
import sys, json, io, ast, contextlib, warnings
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
spec = json.load(open(sys.argv[1])); ns = {}
res = []
for b in spec:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        tree = ast.parse(b["src"]); last = None
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            last = ast.Expression(tree.body.pop().value)
        exec(compile(tree, "<blk>", "exec"), ns)
        if last is not None:
            v = eval(compile(last, "<blk>", "eval"), ns)
            if v is not None: print(repr(v))
    if b.get("plot"):
        plt.gcf().savefig(b["plot"], dpi=130, bbox_inches="tight"); plt.close("all")
    res.append(buf.getvalue())
json.dump(res, open(sys.argv[2], "w"))
'''
def run_blocks(blocks, tag):
    tmp = os.path.join(HERE, "_tmp"); os.makedirs(tmp, exist_ok=True)
    open(os.path.join(tmp, "runner.py"), "w").write(RUNNER)
    json.dump(blocks, open(os.path.join(tmp, tag + ".json"), "w"))
    r = subprocess.run([sys.executable, os.path.join(tmp, "runner.py"), os.path.join(tmp, tag + ".json"), os.path.join(tmp, tag + ".out")],
                       capture_output=True, text=True, cwd=tmp)
    if r.returncode: raise SystemExit(f"[{tag}] page code failed:\n{r.stderr[-1500:]}")
    return json.load(open(os.path.join(tmp, tag + ".out")))

# ------------------------------------------------------------------ pages
def C(src, show=True, plot=None): return dict(kind="code", src=src, show=show, plot=plot)
def H(t): return dict(kind="html", t=t)

def note(t): return f'<div class="note-box">{t}</div>'
def warn(t): return f'<div class="warn-box">⚠️ {t}</div>'
def teal(t): return f'<div class="teal-box">{t}</div>'
def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="compare-table">\n<tr>{h}</tr>\n{b}\n</table>'
def details(q, a): return f'<details class="qa"><summary>{q}</summary><div class="qa-a">{a}</div></details>'
def fig(name, cap): return f'<div class="r-fig"><img src="img/{name}.png" alt="{cap}"><div class="cap">{cap}</div></div>'

def unit(n, title, sub, body):
    return f'''<div class="unit" id="unit{n}">
  <div class="unit-header">
    <div class="unit-num">{"①②③④"[n-1]}</div>
    <div><h2>{title}</h2><div class="unit-sub">{sub}</div></div>
  </div>
{body}
</div>
'''

PAGES = []   # filled by pages.py
def add_page(**kw): PAGES.append(kw)

CSS = '''<style>
.r-fig{margin:.6rem 0 1.2rem;text-align:center}.r-fig img{max-width:100%;height:auto;border:1px solid #e2e8f0;border-radius:10px;background:#fff}.r-fig .cap{font-size:.85rem;color:#64748b;margin-top:.3rem}
.code-block .kw{color:#c4b5fd;font-weight:600}.code-block .fn{color:#fde68a}.code-block .cls{color:#7dd3fc}.code-block .at{color:#a5f3fc}.code-block .pa{color:#fdba74}.code-block .st{color:#86efac}.code-block .nm{color:#fca5a5}.code-block .op{color:#f9a8d4}.code-block .cm{color:#9fb0c8;font-style:normal}
details.qa{background:rgba(255,253,247,.9);border:1px solid #e2e8f0;border-radius:10px;padding:.55rem .9rem;margin:.55rem 0}details.qa summary{cursor:pointer;font-weight:700}.qa-a{margin-top:.5rem}
.nb-download{background:#ccfbf1;border-left:4px solid #0d9488;padding:.8rem 1rem;border-radius:8px;margin:0 0 1.2rem;color:#134e4a}
.stage-table td:first-child{white-space:nowrap;font-weight:700}
</style>'''

NAV = [("py_describe", "📏 平均・中央値・外れ値"), ("py_scale", "⚖️ 標準化"), ("py_split", "✂️ 分割・データ漏れ"),
       ("py_overfit", "🎢 過学習・交差検証"), ("py_regmetrics", "📈 RMSE・R²"), ("py_clfmetrics", "🎯 混同行列・P/R")]

def nb_box(sec):
    return (f'<div class="nb-download">📥 <strong>Python 練習ノートブック：</strong><a href="nb/{NB_NAME}" download>{NB_NAME}</a> — '
            f'このページは<strong>{sec}</strong>の解説です。Jupyter で開いて、同じ名前のセクションを解いてください（自動チェック ✅/❌ 付き）。</div>\n')

def header(cur_label):
    links = "".join(f'<div class="nav-row m1"><span class="nav-mod">670 ML Python 実践</span>' +
                    "".join(f'<span class="navg"><a class="n-main" href="{s}.html">{l}</a></span>' for s, l in NAV) + '</div>' for _ in [0])
    return f'''<header class="site-header">
  <div class="logo">670 ML <span>Python 実践</span></div>
  <nav class="header-nav">
    <a href="index.html">🏠 概要</a>
    <button type="button" class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navGroups" title="レッスン一覧を開く／閉じる">📚 {cur_label} <span class="nav-caret">▾</span></button>
    <div class="nav-groups" id="navGroups">
{links}
    </div>
    <script src="nav.js"></script>
  </nav>
</header>'''

SCRIPTS = '''<script>
var units=document.querySelectorAll('.unit');
var obs=new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting)e.target.classList.add('visible');});},{threshold:0.1});
units.forEach(function(u){obs.observe(u);});
</script>
<script src="practice.js"></script>
<script src="code-summary.js"></script>
<script src="typewriter.js"></script>
<script src="theme-v2.js"></script><script src="code-editor.js"></script>
<script src="../hub-fab.js"></script>'''

def render_page(P, idx):
    # execute all code blocks of the page for real
    blocks = []
    for u in P["units"]:
        for e in u["body"]:
            if not isinstance(e, str) and e["kind"] == "code": blocks.append(dict(src=e["src"], plot=(os.path.join(SITE, "img", e["plot"] + ".png") if e["plot"] else None)))
    pre = [dict(src=P["pre"])]
    outs = run_blocks(pre + blocks, P["slug"])[1:]
    k = 0; body = nb_box(P["tsec"])
    for n, u in enumerate(P["units"], 1):
        parts = []
        for e in u["body"]:
            if isinstance(e, str): parts.append(e)
            elif e["kind"] == "html": parts.append(e["t"])
            else:
                o = outs[k]; k += 1
                parts.append(code_block(e["src"], o if e["show"] else None) if True else "")
        body += unit(n, u["title"], u["sub"], "\n".join(parts))
    terms = "\n".join(f'    <div class="term-item"><div class="term-name">{a}</div><div class="term-en">{b}</div><div class="term-def">{c}</div></div>' for a, b, c in P["terms"])
    unav = "".join(f'<a href="#unit{i}">{l}</a>' for i, l in enumerate(["① 説明", "② 手計算", "③ 自作", "④ 白紙再現"], 1))
    prev = NAV[idx - 1] if idx else None; nxt = NAV[idx + 1] if idx + 1 < len(NAV) else None
    links = ['<a href="index.html">← 概要</a>'] + ([f'<a href="{prev[0]}.html">← {prev[1]}</a>'] if prev else []) + ([f'<a href="{nxt[0]}.html">{nxt[1]} →</a>'] if nxt else [])
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>670 ML Python 実践：{P["title"]}</title>
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="theme-v2.css">
{CSS}
</head>
<body>
{header(P["short"])}
<div class="ch-banner">
<div class="ch-banner-inner">
  <div class="ch-tag">{P["tag"]}</div>
  <h1>{P["icon"]} {P["title"]}</h1>
  <p>{P["lead"]}</p>
  <div class="ch-banner unit-nav" style="background:none;padding:0;">{unav}</div>
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
  <div class="tip-box"><h4>💡 学習のヒント</h4><p>{P["tip"]}</p></div>
</aside>
</div>
<footer>
  <p>🧪 670 ML Python 実践：{P["title"]}</p>
  <p style="margin-top:.5rem;">{" · ".join(links)}</p>
</footer>
{SCRIPTS}
</body></html>
'''

def render_index():
    cards = ""
    colors = ["c-blue", "c-purple", "c-green", "c-teal", "c-blue", "c-purple"]
    for (slug, label), P, c in zip(NAV, PAGES, colors):
        cards += f'''    <div class="chapter-card {c}" style="position:relative;">
      <a href="{slug}.html" style="position:absolute;inset:0;z-index:1;" aria-label="{P["title"]} を開く"></a>
      <div class="card-num">{P["tag"]}</div><div class="card-icon">{P["icon"]}</div>
      <div class="card-title">{P["title"]}</div>
      <div class="card-desc">{P["card"]}</div>
      <div class="card-arrow">→</div>
    </div>
'''
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>670 ML Python 実践</title>
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="theme-v2.css">
{CSS}
</head>
<body>
{header("レッスン一覧")}
<div class="ch-banner">
<div class="ch-banner-inner">
  <div class="ch-tag">DTSC 670 · 試験対策（監視つき・LLM 禁止）</div>
  <h1>🧪 670 ML Python 実践</h1>
  <p>機械学習の試験に出る統計の6項目を、<strong>何も見ずに Python で自分で書ける</strong>ようにするための解説と練習です。各トピックを「① 説明 → ② 手計算 → ③ 自作 → ④ 白紙再現」の4段階で進めます。</p>
</div>
</div>
<div class="container" style="max-width:1080px;margin:0 auto;padding:0 16px 3rem">
{nb_box("全6トピック")}
  <div class="unit visible" style="opacity:1">
    <div class="unit-header"><div class="unit-num">📋</div><div><h2>進め方</h2><div class="unit-sub">1トピック＝解説ページ + ノートブックの同じセクション</div></div></div>
    {table(["段階", "やること", "目安"], [["① 説明する", "白紙に「何か・なぜ必要か・よくある間違い」を3文で書く", "10分"], ["② 手で計算する", "小さなデータを紙と電卓で計算（ノートブックに数字を入れる）", "15分"], ["③ 自分で作る", "NumPy で関数を自作し、scikit-learn の結果と一致させる（一番大事）", "30分"], ["④ 白紙で再現", "<strong>次の日に</strong>、見ずに③をもう一度書く。10分以内なら合格", "10分"]])}
    {note("<strong>合格の目安：</strong>何も見ずに10分でコードが書ける／「なぜ？」を自分の言葉で答えられる。ノートブックの自動チェックが ✅ だけになればOKです。")}
    {warn("DTSC 670 の試験はノート・LLM・検索が禁止です。練習中は LLM に答えを聞かず、コードが動いたあとの「なぜ？」だけ使いましょう。")}
  </div>
  <div class="section-header"><h2>🧪 6つのトピック</h2><p>統計の細かい計算は不要。モデルの「前処理」と「評価」を自分で書けることが目標です。</p></div>
  <div class="chapters-grid">
{cards}  </div>
  <footer style="margin-top:2rem"><p>📌 先に <a href="../stats/cheat_ml.html">ML のための統計チートシート</a> で全体の地図を見ると、位置づけが分かります。</p></footer>
</div>
{SCRIPTS}
</body></html>
'''

# ------------------------------------------------------------------ notebook
def make_nb(answers):
    nb = nbformat.v4.new_notebook()
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    for kind, stu, ans in N.CELLS:
        src = ans if answers else stu
        nb.cells.append(nbformat.v4.new_markdown_cell(src) if kind == "md" else nbformat.v4.new_code_cell(src))
    return nb

def build():
    import pages          # defines PAGES
    os.makedirs(os.path.join(SITE, "img"), exist_ok=True); os.makedirs(os.path.join(SITE, "nb"), exist_ok=True)
    for i, P in enumerate(PAGES):
        open(os.path.join(SITE, P["slug"] + ".html"), "w", encoding="utf-8").write(render_page(P, i))
        print("page", P["slug"])
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(render_index())
    nbformat.write(make_nb(False), os.path.join(SITE, "nb", NB_NAME))
    os.makedirs(ANSWERS_DIR, exist_ok=True)
    nbformat.write(make_nb(True), os.path.join(ANSWERS_DIR, "ml670_py_practice_answers.ipynb"))
    print("notebooks written")

if __name__ == "__main__":
    build()
