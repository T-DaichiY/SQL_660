"""Generate 550 M1-M3 R coding practice notebooks (t_practice_v3 format: 4 topics x 5 levels)
plus matching auto-graded exercise pages (stats-arena.js) for the stats site.

Each question spec Q(...):
  n, level (1-5), title (EN, notebook), title_ja (web), goal (markdown, EN),
  data   : R code given to the student (eval=TRUE chunk) or ""
  tmpl   : student code (L1: full example; L2: with ___; L3+: comments only)
  ans    : full answer code (run by Rscript to compute check values)
  checks : [(label, R expression, digits)]  -> numbers to type on the web page
  task_ja: web scenario (HTML), hint_ja, explain_ja (may contain {label} placeholders)
"""
import html, json, os, re, subprocess, tempfile

STATS = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern/660 - SQL/Lesson_website/stats"
SRC = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern/550-Basic Stats,R"

LEVELS = {1: "Reference", 2: "Fill-in", 3: "Free Style", 4: "Scenario 1", 5: "Scenario 2"}
TIER = {1: "basic", 2: "basic", 3: "intermediate", 4: "intermediate", 5: "advanced"}

def Q(n, level, title, title_ja, goal, data, tmpl, ans, checks, task_ja, hint_ja, explain_ja):
    return dict(n=n, level=level, title=title, title_ja=title_ja, goal=goal.strip(), data=data.strip("\n"),
                tmpl=tmpl.strip("\n"), ans=ans.strip("\n"), checks=checks, task_ja=task_ja.strip(),
                hint_ja=hint_ja.strip(), explain_ja=explain_ja.strip())

# ------------------------------------------------------------------ R runner
def run_checks(mod):
    tmp = tempfile.mkdtemp(prefix="prac550_")
    lines = ['options(width = 72)']
    for q in mod["questions"]:
        f = os.path.join(tmp, f"q{q['n']}.R")
        code = (q["data"] + "\n" if q["data"] else "") + q["ans"] + "\n"
        open(f, "w", encoding="utf-8").write(code)
        lines.append(f'cat("\\n@@Q{q["n"]}@@\\n")')
        lines.append(f'png(tempfile(fileext = ".png")); source("{f}", echo = FALSE, print.eval = TRUE, local = globalenv()); invisible(dev.off())')
        for lab, expr, dig in q["checks"]:
            lines.append(f'cat(sprintf("@@CHK|{q["n"]}|{lab}|%.12g\\n", as.numeric({expr})))')
    lines.append('cat("\\n@@END@@\\n")')
    rf = os.path.join(tmp, "main.R")
    open(rf, "w", encoding="utf-8").write("\n".join(lines))
    env = dict(os.environ)
    if mod.get("rlib"): env["R_LIBS"] = mod["rlib"]
    r = subprocess.run(["Rscript", "--vanilla", rf], cwd=mod["wd"], capture_output=True, text=True, env=env)
    if "@@END@@" not in r.stdout:
        raise RuntimeError(r.stdout[-3000:] + "\n" + r.stderr[-3000:])
    vals, outs = {}, {}
    for m in re.finditer(r'@@CHK\|(\d+)\|([^|]+)\|(\S+)', r.stdout):
        vals[(int(m.group(1)), m.group(2))] = float(m.group(3))
    parts = re.split(r'\n@@Q(\d+)@@\n', r.stdout.split("\n@@END@@")[0])
    for k in range(1, len(parts), 2):
        outs[int(parts[k])] = re.sub(r'@@CHK\|[^\n]*\n?', '', parts[k + 1]).strip("\n")
    return vals, outs

def fmt(v, d):
    return f"{v:.{d}f}"

# ------------------------------------------------------------------ notebook writer
def notebook(mod, answers=False):
    t = mod["title"] + (" — ANSWER KEY" if answers else "")
    out = [f'''---
title: "{t}"
subtitle: "4 topics × 5 levels: Reference → Fill-in → Free-style → Scenario 1 → Scenario 2"
output:
  html_notebook:
    theme: flatly
    toc: true
    toc_float: true
    number_sections: false
editor_options:
  markdown:
    wrap: 72
---

```{{r setup, include=FALSE}}
knitr::opts_chunk$set(echo = TRUE, eval = {"TRUE" if answers else "FALSE"})
```

------------------------------------------------------------------------

> **How to use this notebook**
>
> Each **topic** (Q1–Q5, Q6–Q10, Q11–Q15, Q16–Q20) contains 5 questions
> that escalate in difficulty:
>
> | Level               | What to do                                            |
> |----------------------------|--------------------------------------------|
> | **L1 — Reference**  | A complete example is given. Run it, study each line. |
> | **L2 — Fill-in**    | Replace `___` with correct code.                      |
> | **L3 — Free style** | Write all code yourself from the goal description.    |
> | **L4 — Scenario 1** | Real-world setting. Write full analysis.              |
> | **L5 — Scenario 2** | Complex multi-step scenario + short report.           |
>
> {mod["data_note"]}
>
> {mod.get("header_link") or ("✅ Check your numbers on the website: " + mod["web_url"])}

------------------------------------------------------------------------
''']
    for ti, (topic, qs) in enumerate(mod["topics"]):
        out.append(f"\n# Topic {'ABCD'[ti]} — {topic}\n")
        for q in qs:
            out.append(f"\n## Q{q['n']} · L{q['level']} · {LEVELS[q['level']]}\n\n**Goal:** {q['goal']}\n")
            if q["data"]:
                out.append(f"```{{r q{q['n']}-data, eval=TRUE}}\n{q['data']}\n```\n")
            code = q["ans"] if (answers or q["level"] == 1) else q["tmpl"]
            ev = ", eval=TRUE" if q["level"] == 1 else ""
            out.append(f"```{{r q{q['n']}-l{q['level']}{ev}}}\n{code}\n```\n")
            out.append("\n------------------------------------------------------------------------\n")
    out.append(f"\n# Quick Reference Card\n\n```{{r ref-card, eval=TRUE}}\ncat(\"\n{mod['card']}\n\")\n```\n")
    out.append(f"\n------------------------------------------------------------------------\n\n*{mod['title']} — DTSC 550 / t-daichiy*\n")
    return "\n".join(out)

# ------------------------------------------------------------------ web page writer
def web_page(mod, vals, outs):
    probs = []
    for topic, qs in mod["topics"]:
        for q in qs:
            ans = []
            for lab, expr, dig in q["checks"]:
                v = vals[(q["n"], lab)]
                ans.append({"label": lab, "value": round(v, dig), "tol": 0.5 if dig == 0 else round(1.1 * 10 ** -dig, dig + 2)})
            rout = "\n".join("# " + l for l in outs[q["n"]].split("\n")) if outs[q["n"]].strip() else ""
            rcode = ((q["data"] + "\n") if q["data"] else "") + q["ans"] + ("\n" + rout if rout else "")
            ex = q["explain_ja"]
            for lab, expr, dig in q["checks"]:
                ex = ex.replace("{" + lab + "}", fmt(vals[(q["n"], lab)], dig))
            scen = q["task_ja"]
            if q["data"]:
                scen += '<pre class="arena-data">' + html.escape(q["data"]) + "</pre>"
            probs.append(dict(id=f"{mod['key']}-q{q['n']}", tier=TIER[q["level"]],
                              title=f"Q{q['n']} · L{q['level']} {q['title_ja']}", concept=f"Topic {'ABCD'[mod['topics'].index((topic, qs))]} — {topic}",
                              scenario=scen, type="num", answers=ans, hint=q["hint_ja"], rcode=rcode, explain=ex))
    js = "var PROBLEMS = " + json.dumps(probs, ensure_ascii=False, indent=1) + ";"
    nb = sum(1 for p in probs if p["tier"] == "basic"); ni = sum(1 for p in probs if p["tier"] == "intermediate"); na = len(probs) - nb - ni
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>演習 {mod["short"]} {mod["name_ja"]}</title>
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="practice-arena.css?v=1">
<style>.arena-data{{background:#0f172a;color:#e2e8f0;border-radius:8px;padding:.6rem .8rem;margin:.5rem 0 0;font-size:.82rem;white-space:pre-wrap;overflow-x:auto}}</style>
</head>
<body>
<header class="site-header">
  <div class="logo">統計 <span>レッスン</span></div>
  <nav class="header-nav">
    <a href="index.html">🏠 概要</a>
    <button type="button" class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navGroups" title="レッスン一覧を開く／閉じる">📚 演習 {mod["short"]} <span class="nav-caret">▾</span></button>
    <div class="nav-groups" id="navGroups">
<!--NAV-->
    </div>
    <script src="nav.js"></script>
  </nav>
</header>
<div class="ch-banner">
<div class="ch-banner-inner">
  <div class="ch-tag">演習 · {mod["short"]}</div>
  <h1>🏋️ {mod["short"].split()[-1]} 演習 — {mod["name_ja"]}</h1>
  <p>練習ノートブック <a href="rmd/{mod["file"]}" download style="color:inherit;font-weight:700">📥 {mod["file"]}</a> の20問（4トピック × 5段階）と<strong>同じ問題・同じ番号</strong>です。RStudio で解いて、出た数値を入力すると自動採点されます。</p>
  <div class="ch-banner unit-nav" style="background:none;padding:0;">
    <a href="#basics">🟢 基礎（L1–L2）</a><a href="#intermediate">🟡 中級（L3–L4）</a><a href="#advanced">🔴 上級（L5）</a><a href="exercises.html">🏋️ 演習ハブ</a>
  </div>
</div>
</div>
<div class="container">

<div class="arena-intro">
  <p>✍️ <strong>使い方：</strong>ノートブックの各問（Q1〜Q20）を RStudio で解き、ここに数値を入力して<strong>✅ 採点</strong>。<strong>L1</strong> は完成した見本（実行して値を確認）、<strong>L2</strong> は <code>___</code> の穴埋め、<strong>L3</strong> は自分で全部書く、<strong>L4・L5</strong> はシナリオ問題（最後に結論や報告をコメントで書く）。分からなければ<strong>💡 ヒント</strong>、最後に<strong>🔑 答えを見る</strong>で解答コードと実行結果を確認できます。</p>
  <p style="margin-top:.5rem">{mod["data_note_ja"]}</p>
  <p style="margin-top:.5rem">📚 対応するレッスン：{mod["lessons_ja"]}</p>
</div>

<div class="tier-section" id="basics">
  <div class="tier-header"><h2>🟢 基礎（L1 見本・L2 穴埋め）</h2><span class="tier-badge basic">Basic · {nb}</span></div>
  <div id="basics-container"></div>
</div>
<div class="tier-section" id="intermediate">
  <div class="tier-header"><h2>🟡 中級（L3 自由記述・L4 シナリオ1）</h2><span class="tier-badge intermediate">Intermediate · {ni}</span></div>
  <div id="intermediate-container"></div>
</div>
<div class="tier-section" id="advanced">
  <div class="tier-header"><h2>🔴 上級（L5 シナリオ2）</h2><span class="tier-badge advanced">Advanced · {na}</span></div>
  <div id="advanced-container"></div>
</div>

</div>

<footer>
  <p>🏋️ 統計レッスン：演習 — {mod["short"]} {mod["name_ja"]}</p>
  <p style="margin-top:.5rem;"><a href="exercises.html">🏋️ 演習ハブ</a> · <a href="index.html">🏠 概要へ</a> · <a href="rmd/{mod["file"]}" download>📥 練習ノートブック</a></p>
</footer>

<script src="stats-arena.js?v=1"></script>
<script>
{js}
renderStatsArena(PROBLEMS, {{
  basicsEl: document.getElementById("basics-container"),
  intermediateEl: document.getElementById("intermediate-container"),
  advancedEl: document.getElementById("advanced-container")
}});
</script>
<script src="../hub-fab.js"></script>
</body>
</html>
'''
