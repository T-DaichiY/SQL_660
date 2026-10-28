"""Build practice notebooks (+ answer keys) and exercise pages. Usage: python3 build_practice.py [m1 m2 m3]"""
import importlib, os, shutil, sys
from practice_gen import notebook, web_page, run_checks, STATS

BASE_URL = "https://t-daichiy.github.io/SQL_660/stats/"

def build(key):
    mod = importlib.import_module("p_" + key).MOD
    mod["web_url"] = BASE_URL + mod["web"]
    assert [q["n"] for q in mod["questions"]] == list(range(1, 21)), "Q numbers must be 1..20"
    vals, outs = run_checks(mod)
    qfile = os.path.join(mod["folder"], mod["file"])
    afile = qfile.replace(".Rmd", "_answers.Rmd")
    for f in (qfile, afile):
        if os.path.exists(f) and "--force" not in sys.argv:
            print("exists, overwriting own generated file:", os.path.basename(f))
    open(qfile, "w", encoding="utf-8").write(notebook(mod, answers=False))
    open(afile, "w", encoding="utf-8").write(notebook(mod, answers=True))
    os.makedirs(f"{STATS}/rmd", exist_ok=True)
    shutil.copy(qfile, f"{STATS}/rmd/{mod['file']}")
    open(f"{STATS}/{mod['web']}", "w", encoding="utf-8").write(web_page(mod, vals, outs))
    print(f"{key}: notebook -> {qfile}")
    for q in mod["questions"]:
        print(f"  Q{q['n']:>2} L{q['level']}", ", ".join(f"{lab}={vals[(q['n'], lab)]:.6g}" for lab, _, _ in q["checks"]))
    return vals, outs

if __name__ == "__main__":
    for k in [a for a in sys.argv[1:] if not a.startswith("--")] or ["m1", "m2", "m3"]:
        build(k)
