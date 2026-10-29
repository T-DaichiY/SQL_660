"""Insert 'R practice notebook' download boxes into lesson/exercise pages (idempotent: marked with data-nb).
Run after nb_build.py. Pages: SQL_660 stats/ (550 M4-M6) and both copies of the 650 site."""
import glob, os, re

E = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern"
STATS = E + "/660 - SQL/Lesson_website/stats"
R650_DIRS = [E + "/650 - Data Visualization/Lesson_website", E + "/660 - SQL/Lesson_website/r650"]
STYLE = "background:#ccfbf1;border-left:4px solid #0d9488;padding:.8rem 1rem;border-radius:8px;margin:1.2rem 0;color:#134e4a"

def box(file, mod):
    return (f'<div class="nb-download" data-nb="1" style="{STYLE}">📥 <strong>R 練習ノートブック（{mod}）：</strong>'
            f'<a href="rmd/{file}" download>{file}</a> — 4トピック × 5段階（L1 見本 → L2 穴埋め → L3 自由記述 → L4/L5 シナリオ）の20問。'
            f'RStudio で開いて解いてください。</div>\n')

def insert(path, html):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r'<div class="nb-download" data-nb="1"[^>]*>.*?</div>\n', '', s, flags=re.S)   # idempotent
    for anchor in ('<div class="quiz-section"', '<div class="tier-section"', '<footer'):
        i = s.find(anchor)
        if i != -1:
            s = s[:i] + html + s[i:]
            open(path, "w", encoding="utf-8").write(s)
            return True
    return False

def run():
    n = 0
    # --- 550 M4-M6 lessons (+ easy) and their exercise pages
    rules550 = [(r"m3_(basics|testing|estimation)(_easy)?\.html$|ex_550_m3\.html$", "m4_practice_v1.Rmd", "550 M4"),
                (r"m5_[a-z_]+\.html$|ex_550_m5_[a-z]+\.html$", "m5_practice_v1.Rmd", "550 M5"),
                (r"m6_[a-z_]+\.html$|ex_550_m6\.html$", "m6_practice_v1.Rmd", "550 M6")]
    for f in sorted(glob.glob(STATS + "/*.html")):
        b = os.path.basename(f)
        for pat, file, mod in rules550:
            if re.match(pat, b):
                n += insert(f, box(file, mod)); break
    # --- 650 site (both copies)
    rules650 = [(r"m1_[a-z]+\.html$", "650_m1_practice_v1.Rmd", "650 M1"),
                (r"m2_[a-z]+\.html$", "650_m2_practice_v1.Rmd", "650 M2"),
                (r"(na|cor)_[a-z]+\.html$", "650_m3_practice_v1.Rmd", "650 欠損・外れ値・相関"),
                (r"m4_[a-z]+\.html$", "650_m4_practice_v1.Rmd", "650 M4"),
                (r"m5_(ch[0-9_]+|index|regression_glossary)(_easy)?\.html$", "650_m5_practice_v1.Rmd", "650 M5"),
                (r"m6_(ch[0-9]+|index|log_master|logodds_full_course)(_easy)?\.html$", "650_m6_practice_v1.Rmd", "650 M6")]
    for d in R650_DIRS:
        for f in sorted(glob.glob(d + "/*.html")):
            b = os.path.basename(f)
            for pat, file, mod in rules650:
                if re.match(pat, b):
                    n += insert(f, box(file, mod)); break
    print("pages with a download box:", n)

LIST_550 = [("550 M1 R入門・データフレーム・測定水準", "m1_practice_v1.Rmd"), ("550 M2 記述統計", "m2_practice_v1.Rmd"),
            ("550 M3 確率と分布", "m3_practice_v1.Rmd"), ("550 M4 推測の基礎（検定・CI）", "m4_practice_v1.Rmd"),
            ("550 M5 t・ANOVA・χ²", "m5_practice_v1.Rmd"), ("550 M6 相関・回帰", "m6_practice_v1.Rmd")]
LIST_650 = [("650 M1 ggplot2", "650_m1_practice_v1.Rmd"), ("650 M2 読み込み・dplyr", "650_m2_practice_v1.Rmd"),
            ("650 欠損・外れ値・相関", "650_m3_practice_v1.Rmd"), ("650 M4 予測と回帰の仮定", "650_m4_practice_v1.Rmd"),
            ("650 M5 重回帰", "650_m5_practice_v1.Rmd"), ("650 M6 ロジスティック回帰", "650_m6_practice_v1.Rmd")]

def list_box(items, extra=""):
    li = "".join(f'<li>{t}：<a href="rmd/{f}" download>{f}</a></li>' for t, f in items)
    return (f'<div class="nb-download" data-nb="1" style="{STYLE}">📥 <strong>R 練習ノートブック（各20問・4トピック × 5段階）</strong>{extra}'
            f'<ul style="margin:.4rem 0 0 1.2rem">{li}</ul></div>\n')

def run_lists():
    # stats exercise hub: before the first card grid
    p = STATS + "/exercises.html"
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'<div class="nb-download" data-nb="1"[^>]*>.*?</div>\n', '', s, flags=re.S)
    i = s.index('<div class="chapters-grid">')
    j = s.rfind('<div class="section-header', 0, i)
    k = j if j != -1 else i
    s = s[:k] + list_box(LIST_550, "（M1〜M3 は下の演習ページと同じ問題）") + s[k:]
    open(p, "w", encoding="utf-8").write(s)
    # 650 index pages: before the first section header / card grid
    for d in R650_DIRS:
        p = d + "/index.html"
        s = open(p, encoding="utf-8").read()
        s = re.sub(r'<div class="nb-download" data-nb="1"[^>]*>.*?</div>\n', '', s, flags=re.S)
        m = re.search(r'<div class="section-header|<h2', s)
        s = s[:m.start()] + list_box(LIST_650) + s[m.start():]
        open(p, "w", encoding="utf-8").write(s)
    print("lists added: stats/exercises.html + 650 index x2")

if __name__ == "__main__":
    run(); run_lists()
