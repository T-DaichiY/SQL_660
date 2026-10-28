"""Build 550 M1-M3 lesson pages into stats/. Usage: python3 build_550.py [m1 m2 m3]"""
import re, sys
import lib550
from lib550 import Page, page, quiz, STATS, SRC

MODS = {}
def load():
    import c_m1; MODS["m1"] = (c_m1.LESSONS, SRC + "/Module ２")
    try:
        import c_m2; MODS["m2"] = (c_m2.LESSONS, SRC + "/Module ２")
    except ImportError: pass
    try:
        import c_m3; MODS["m3"] = (c_m3.LESSONS, None)
    except ImportError: pass

def clean(o):
    return re.sub(r'/\S*?/r550_[^/\s]+/c\d+\.R', '<text>', o)

def main(which):
    load()
    seq = []                                  # site-wide order for prev/next
    for k in ("m1", "m2", "m3"):
        if k in MODS: seq += [(k, fn) for fn in MODS[k][0]]
    titles = {}
    built = []
    for k, fn in seq:
        P = Page(fn.__name__, MODS[k][1])
        L, body, q = fn(P)
        titles[fn.__name__] = L["title"].split("：")[0]
        if k in which: built.append((k, fn, P, L, body, q))
    names = [fn.__name__ for _, fn in seq]
    for k, fn, P, L, body, q in built:
        body += "\n" + quiz(L["slug"], q)
        filled, outs = P.fill(body)
        filled = clean(filled)
        i = names.index(fn.__name__)
        prev = (names[i - 1], titles[names[i - 1]]) if i else None
        nxt = (names[i + 1], titles[names[i + 1]]) if i + 1 < len(names) else None
        open(f"{STATS}/{L['slug']}.html", "w", encoding="utf-8").write(page(L, prev, nxt, filled))
        errs = [o for o in outs if "Error" in o]
        print(f"{L['slug']}: {len(P.chunks)} chunks, {len(q)} MCQ, outputs with Error: {len(errs)}")
    print("MCQ issues:", lib550.QUIZ_REPORT or "none")
    print("correct-letter counts A-D:", lib550.POS_COUNT)

if __name__ == "__main__":
    main(sys.argv[1:] or ["m1", "m2", "m3"])
