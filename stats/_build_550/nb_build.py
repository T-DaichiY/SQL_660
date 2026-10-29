"""Notebook-only builder (no exercise page): question + answer Rmd, copy question Rmd to the site's rmd/ folder.
Usage: python3 nb_build.py n550_m4 n650_m1 ...   (module files are nb_*.py with MOD)"""
import importlib, os, re, shutil, sys
from practice_gen import notebook, run_checks, Q

RLIB = "/private/tmp/claude-501/-Users-apple-Library-CloudStorage-GoogleDrive-daichi-yamamoto-sisbschool-com-My-Drive-AY26-27/54937b34-b184-4991-8035-76ad5d0da3dc/scratchpad/rlib"

def N(n, level, title, goal, data, tmpl, ans, checks=()):
    """Notebook question (no web fields). checks: [(label, expr, digits)] printed only to verify answers."""
    return Q(n, level, title, "", goal, data, tmpl, ans, list(checks), "", "", "")

def build(name):
    mod = importlib.import_module(name).MOD
    mod.setdefault("rlib", RLIB)
    assert [q["n"] for q in mod["questions"]] == list(range(1, 21)), name
    for q in mod["questions"]:
        if q["level"] != 1: assert q["tmpl"].strip(), f"{name} Q{q['n']} needs a template"
    vals, outs = run_checks(mod)
    qfile = os.path.join(mod["folder"], mod["file"])
    afile = qfile.replace(".Rmd", "_answers.Rmd")
    os.makedirs(mod["folder"], exist_ok=True)
    open(qfile, "w", encoding="utf-8").write(notebook(mod, answers=False))
    open(afile, "w", encoding="utf-8").write(notebook(mod, answers=True))
    for site_dir in mod["site_rmd"]:
        os.makedirs(site_dir, exist_ok=True)
        shutil.copy(qfile, os.path.join(site_dir, mod["file"]))
    print(f"{name}: {qfile}")
    for q in mod["questions"]:
        o = outs.get(q["n"], "")
        flag = "  <-- Error" if re.search(r"(^|\n)Error|Error in |Error:", o.replace("Std. Error", "")) else ""
        print(f"  Q{q['n']:>2} L{q['level']} {q['title'][:40]:<40}", ", ".join(f"{l}={vals[(q['n'], l)]:.6g}" for l, _, _ in q["checks"]), flag)
    return vals, outs

if __name__ == "__main__":
    for n in sys.argv[1:]:
        build(n)
