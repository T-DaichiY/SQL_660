#!/usr/bin/env python3
"""Copy the DTSC 580 site (built in Eastern/580 - Data Manipulation/Lesson_website by its own
generator) into this repo as python580/, add the hub floating buttons, then rebuild the hub.
Run in the repo root:  python3 sync580.py"""
import os, re, shutil, subprocess

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '580 - Data Manipulation', 'Lesson_website')
DST = 'python580'
FAB = '<script src="../hub-fab.js"></script>'

if not os.path.isdir(SRC):
    raise SystemExit('580 site not found: ' + SRC)
shutil.copytree(SRC, DST, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.DS_Store', '__pycache__', '*answers*'))  # answer keys stay private

# keep python580/ in step with the source: drop files that no longer exist there
for root, dirs, files in os.walk(DST):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), DST)
        if not os.path.exists(os.path.join(SRC, rel)) or 'answers' in f:
            os.remove(os.path.join(root, f))

# shared editor: use the repo's copy (it knows python580/ is Python)
shutil.copy('code-editor.js', os.path.join(DST, 'code-editor.js'))
shutil.copy('theme-v2.js', os.path.join(DST, 'theme-v2.js'))   # has the download-link fix

n = 0
for f in os.listdir(DST):
    if not f.endswith('.html'):
        continue
    p = os.path.join(DST, f)
    s = open(p, encoding='utf-8').read()
    if 'hub-fab.js' not in s and '</body>' in s:
        s = s.replace('</body>', FAB + '\n</body>', 1)
        open(p, 'w', encoding='utf-8').write(s)
        n += 1
print(f'synced {SRC} -> {DST}/ ; hub buttons added to {n} pages')
subprocess.run(['python3', 'build_hub.py'], check=True)
