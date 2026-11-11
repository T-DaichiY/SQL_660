"""Build the 670 ML statistics-review lessons (6 pages) into stats/. Usage: python3 build_ml.py"""
import re, sys
import lib550
from lib550 import Page, page, quiz, STATS
import c_ml1, c_ml2

LESSONS = c_ml1.LESSONS + c_ml2.LESSONS
NB = "ml670_practice_v1.Rmd"

def nb_box():
    return ('<div class="nb-download" data-nb="1" style="background:#ccfbf1;border-left:4px solid #0d9488;padding:.8rem 1rem;border-radius:8px;margin:1.2rem 0;color:#134e4a">'
            f'📥 <strong>R 練習ノートブック（670 ML 統計復習）：</strong><a href="rmd/{NB}" download>{NB}</a> — 4トピック × 5段階（L1 見本 → L2 穴埋め → L3 自由記述 → L4/L5 シナリオ）の20問。'
            'このシリーズ全6回の内容が範囲です。RStudio で開いて解いてください。</div>\n')

def clean(o): return re.sub(r'/\S*?/r550_[^/\s]+/c\d+\.R', '<text>', o)

def main():
    built, titles = [], {}
    for fn in LESSONS:
        P = Page(fn.__name__)
        L, body, q = fn(P)
        titles[L["slug"]] = L["title"].split("：")[0]
        built.append((P, L, body, q))
    names = [L["slug"] for _, L, _, _ in built]
    for P, L, body, q in built:
        body += "\n" + nb_box() + quiz(L["slug"], q)
        filled, outs = P.fill(body)
        filled = clean(filled)
        i = names.index(L["slug"])
        prev = (names[i-1], titles[names[i-1]]) if i else None
        nxt = (names[i+1], titles[names[i+1]]) if i + 1 < len(names) else None
        open(f"{STATS}/{L['slug']}.html", "w", encoding="utf-8").write(page(L, prev, nxt, filled))
        errs = [o for o in outs if "Error" in o]
        print(f"{L['slug']}: {len(P.chunks)} chunks, {len(q)} MCQ, outputs with Error: {len(errs)}")
        for o in errs: print("   ERR:", o[:300])
    print("MCQ issues:", lib550.QUIZ_REPORT or "none"); print("letter counts A-D:", lib550.POS_COUNT)

if __name__ == "__main__":
    main()
