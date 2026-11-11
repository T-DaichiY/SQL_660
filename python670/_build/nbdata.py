"""Notebook content for the 670 ML Python practice: 6 topics x 4 stages.
Each cell = (kind, student_source, answer_source). Solutions are shared with the lesson pages."""
import re

CELLS = []
def md(t, ans=None): CELLS.append(("md", t, t if ans is None else ans))
def code(student, answer=None): CELLS.append(("code", student, student if answer is None else answer))

def suff(src, names, s="_2"):
    for n in names: src = re.sub(r"\b%s\b" % n, n + s, src)
    return src

# ------------------------------------------------------------------ shared setup (also used by pages)
SETUP = '''import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from scipy import stats
from sklearn.base import clone
from sklearn.datasets import load_diabetes, load_breast_cancer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (confusion_matrix, precision_score, recall_score,
                             mean_squared_error, mean_absolute_error, r2_score)
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

def attempt(fn, *args, **kw):
    """自分の関数がまだ書けていなくても、チェック全体は止めない。"""
    try:
        return fn(*args, **kw)
    except Exception:
        return None

def check(name, ok_fn):
    """ok_fn が True を返せば ✅。まだ書けていない・エラーなら ❌。"""
    try:
        ok = bool(ok_fn())
    except Exception as e:
        print(f"❌ {name}   (まだ書けていない / {type(e).__name__})"); return
    print(("✅ " if ok else "❌ ") + name)
'''

# ------------------------------------------------------------------ solutions (shared)
SOL1 = '''def iqr_outliers(x):
    x = np.asarray(x, dtype=float)
    q1, q3 = np.percentile(x, [25, 75]); iqr = q3 - q1
    return (x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)

def skewness(x):
    x = np.asarray(x, dtype=float)
    return np.mean(((x - x.mean()) / x.std()) ** 3)
'''
SOL2 = '''def zscore(x, ddof=0):
    x = np.asarray(x, dtype=float)
    return (x - x.mean()) / x.std(ddof=ddof)

def fit_transform_train_test(X_tr, X_te):
    mu, sd = X_tr.mean(axis=0), X_tr.std(axis=0)      # 平均・SD は訓練データだけから
    return (X_tr - mu) / sd, (X_te - mu) / sd
'''
SOL3 = '''def my_train_test_split(X, y, test_size=0.25, seed=0):
    n = len(X)
    idx = np.random.default_rng(seed).permutation(n)
    n_te = int(round(n * test_size))
    te, tr = idx[:n_te], idx[n_te:]
    return X[tr], X[te], y[tr], y[te]

def run_once(leak, seed):
    if leak:    # ✗ 全データを見て特徴量を選んでから分割
        Xs = SelectKBest(f_classif, k=10).fit_transform(X_noise, y_noise)
        a, b, c, d = train_test_split(Xs, y_noise, test_size=0.3, random_state=seed)
    else:       # ○ 分割してから、訓練データだけで特徴量を選ぶ
        a, b, c, d = train_test_split(X_noise, y_noise, test_size=0.3, random_state=seed)
        sel = SelectKBest(f_classif, k=10).fit(a, c)
        a, b = sel.transform(a), sel.transform(b)
    return LogisticRegression(max_iter=1000).fit(a, c).score(b, d)
'''
SOL4 = '''def kfold_indices(n, k):
    sizes = [n // k + (1 if i < n % k else 0) for i in range(k)]
    folds, start = [], 0
    for s in sizes:
        te = np.arange(start, start + s)
        tr = np.concatenate([np.arange(0, start), np.arange(start + s, n)])
        folds.append((tr, te)); start += s
    return folds

def my_cv_score(model, X, y, k=5):
    scores = []
    for tr, te in kfold_indices(len(X), k):
        m = clone(model).fit(X[tr], y[tr])
        scores.append(m.score(X[te], y[te]))
    return float(np.mean(scores))

def depth_curve(X_tr, y_tr, X_te, y_te, depths):
    train, test = [], []
    for d in depths:
        m = DecisionTreeRegressor(max_depth=d, random_state=0).fit(X_tr, y_tr)
        train.append(m.score(X_tr, y_tr)); test.append(m.score(X_te, y_te))
    return train, test
'''
SOL5 = '''def rmse(y, p):
    y, p = np.asarray(y, float), np.asarray(p, float)
    return float(np.sqrt(np.mean((y - p) ** 2)))

def mae(y, p):
    y, p = np.asarray(y, float), np.asarray(p, float)
    return float(np.mean(np.abs(y - p)))

def r2(y, p):
    y, p = np.asarray(y, float), np.asarray(p, float)
    return float(1 - np.sum((y - p) ** 2) / np.sum((y - y.mean()) ** 2))
'''
SOL6 = '''def confusion(y_true, y_pred):
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    return tn, fp, fn, tp

def precision(y_true, y_pred):
    tn, fp, fn, tp = confusion(y_true, y_pred)
    return tp / (tp + fp) if tp + fp else 0.0

def recall(y_true, y_pred):
    tn, fp, fn, tp = confusion(y_true, y_pred)
    return tp / (tp + fn) if tp + fn else 0.0

def sweep(y_true, proba, thresholds):
    out = []
    for t in thresholds:
        pred = (np.asarray(proba) >= t).astype(int)
        out.append((t, precision(y_true, pred), recall(y_true, pred)))
    return out
'''

# ------------------------------------------------------------------ title + setup
md('''# 670 ML 統計：Python 練習ノートブック

DTSC 670 の試験は**ノート・LLM・検索が使えません**。このノートブックは「何も見ずに自分で書ける」ようになるための練習です。
6トピックを、それぞれ次の4段階で進めます。

| 段階 | やること | 目安 |
|---|---|---|
| ① 説明する | 白紙に「何か・なぜ必要か・よくある間違い」を3文で書く | 10分 |
| ② 手で計算する | 小さなデータを紙と電卓で計算して、数字を入れる | 15分 |
| ③ 自分で作る | 関数を自作して、scikit-learn の結果と一致させる（**一番大事**） | 30分 |
| ④ 白紙で再現 | **次の日に**、見ずに③をもう一度書く。10分以内なら合格 | 10分 |

**使い方**
- `None` や `...` の所を自分で書き換えます。そのあと下の「✅ チェック」のセルを実行すると、✅ / ❌ が出ます。
- ❌ のときは、自分のコードと scikit-learn の結果を `print` で並べて、どこが違うかを探します。
- 練習の間は LLM に答えを聞かないでください。コードが動いたあとの「なぜ?」の質問だけ使いましょう。
- 解説は勉強サイト（ハブの「670 ML Python 実践」）の同じ名前のページにあります。''')
code(SETUP)

# ------------------------------------------------------------------ T1
md('''---
## T1　平均・中央値・外れ値・歪み''')
md('''### ① 説明する
白紙に 3 文で書きます。「平均と中央値は何が違う？」「外れ値があると平均はどうなる？」「歪んだデータでは、どちらを信じる？」

**あなたの答え：**（ここをダブルクリックして書く）''')
code('''x = [2, 3, 3, 4, 50]
mean_x = None     # 平均を手で計算して、数字を入れる
median_x = None   # 中央値
robust = None     # 外れ値に強いのは "mean" と "median" のどちら？（文字列で）''',
     '''x = [2, 3, 3, 4, 50]
mean_x = 12.4     # (2+3+3+4+50) / 5
median_x = 3      # 小さい順に並べた真ん中
robust = "median"''')
code('''check("② 平均 = 12.4", lambda: abs(mean_x - 12.4) < 1e-9)
check("② 中央値 = 3", lambda: median_x == 3)
check('② 外れ値に強いのは "median"', lambda: robust == "median")''')
md('''### ③ 自分で作る
- `iqr_outliers(x)`：**1.5×IQR ルール**で、外れ値なら `True` の配列を返す（`np.percentile` を使う）
- `skewness(x)`：**歪度** ＝ 各値の z スコアの 3 乗の平均（SD は n で割る = `np.std` の既定）''')
code('''def iqr_outliers(x):
    ...

def skewness(x):
    ...''', SOL1)
code('''def check_t1(f_out, f_skew):
    check("[2,3,3,4,50] は最後だけ外れ値", lambda: list(f_out([2, 3, 3, 4, 50])) == [False, False, False, False, True])
    d = np.random.default_rng(1).lognormal(size=200)
    s = pd.Series(d); q1, q3 = s.quantile(.25), s.quantile(.75)
    ref = ((s < q1 - 1.5 * (q3 - q1)) | (s > q3 + 1.5 * (q3 - q1))).to_numpy()
    check("乱数データでも pandas で作った答えと一致", lambda: (np.asarray(f_out(d)) == ref).all())
    check("歪度が scipy.stats.skew と一致", lambda: abs(f_skew(d) - stats.skew(d)) < 1e-9)

check_t1(iqr_outliers, skewness)''')
md('''**考えてみよう：** pandas の `.skew()` は `scipy.stats.skew` と少し違う値を返します。何が違うのか調べて、ここに書いてください。''',
   '''**考えてみよう：** pandas の `.skew()` は `scipy.stats.skew` と少し違う値を返します。何が違うのか調べて、ここに書いてください。

> **答え：** scipy の既定は「標本の歪度（n で割る）」、pandas の `.skew()` は小標本の偏りを補正した版（n と n−1・n−2 を使う）。n が大きいと差は小さい。''')
md('''### ④ 白紙で再現（次の日に）
②③を**見ずに**、下に書き直します。名前の後ろに `_2` が付いています。10分以内に ✅ が揃えば合格です。''')
code('''def iqr_outliers_2(x):
    ...

def skewness_2(x):
    ...

check_t1(iqr_outliers_2, skewness_2)''',
     suff(SOL1, ["iqr_outliers", "skewness"]) + "\ncheck_t1(iqr_outliers_2, skewness_2)")

# ------------------------------------------------------------------ T2
md('''---
## T2　標準化（z スコア）''')
md('''### ① 説明する
3 文で書きます。「標準化は何をする？」「なぜ必要？（距離や正則化を使うモデルで）」「標準化した列の平均と SD はいくつになる？」

**あなたの答え：**（ここに書く）''')
code('''mu, sd = 10, 2
z14 = None      # x = 14 の z スコア
z7 = None       # x = 7 の z スコア
x_back = None   # z = -1 は、元の値ではいくつ？''',
     '''mu, sd = 10, 2
z14 = 2.0       # (14 - 10) / 2
z7 = -1.5       # (7 - 10) / 2
x_back = 8      # 10 + (-1) * 2''')
code('''check("② z14 = 2", lambda: abs(z14 - 2.0) < 1e-9)
check("② z7 = -1.5", lambda: abs(z7 + 1.5) < 1e-9)
check("② z=-1 は 8", lambda: abs(x_back - 8) < 1e-9)''')
md('''### ③ 自分で作る
- `zscore(x, ddof=0)`：`(x − 平均) / SD`。`ddof` は SD を割る数（`n − ddof`）
- `fit_transform_train_test(X_tr, X_te)`：平均と SD は**訓練データだけ**から求めて、訓練・テストの両方に使う（データ漏れを防ぐ）
- 最後に、**`StandardScaler` と pandas の `.std()` がなぜ少しずれるか**を、比の数字で確かめます。''')
code('''def zscore(x, ddof=0):
    ...

def fit_transform_train_test(X_tr, X_te):
    ...''', SOL2)
code('''Xd, _ = load_diabetes(return_X_y=True)
col = Xd[:, 2]
Xa, Xb = Xd[:300], Xd[300:]

def check_t2(f_z, f_ft):
    check("zscore が StandardScaler と一致", lambda: np.allclose(f_z(col), StandardScaler().fit_transform(col.reshape(-1, 1)).ravel()))
    check("zscore の平均が 0・SD が 1", lambda: abs(np.mean(f_z(col))) < 1e-9 and abs(np.std(f_z(col)) - 1) < 1e-9)
    check("ddof=1 だと pandas の標準化と一致", lambda: np.allclose(f_z(col, ddof=1), (pd.Series(col) - pd.Series(col).mean()) / pd.Series(col).std()))
    sc = StandardScaler().fit(Xa)
    a, b = attempt(f_ft, Xa, Xb) or (None, None)
    check("訓練データの平均・SD だけで変換できている", lambda: np.allclose(a, sc.transform(Xa)) and np.allclose(b, sc.transform(Xb)))
    check("テストデータの平均は ちょうど 0 にはならない（それでよい）", lambda: np.abs(b.mean(axis=0)).max() > 1e-4)

check_t2(zscore, fit_transform_train_test)''')
code('''data = np.array([1., 2., 3., 4., 5.])
ratio = None   # StandardScaler の SD ÷ pandas の .std() の値（数字で。n=5 から計算できる）''',
     '''data = np.array([1., 2., 3., 4., 5.])
ratio = np.sqrt(4 / 5)   # n で割る SD ÷ n-1 で割る SD = sqrt((n-1)/n)''')
code('''check("③ ratio が実際の比と一致", lambda: abs(ratio - StandardScaler().fit(data.reshape(-1, 1)).scale_[0] / pd.Series(data).std()) < 1e-9)''')
md('''### ④ 白紙で再現（次の日に）''')
code('''def zscore_2(x, ddof=0):
    ...

def fit_transform_train_test_2(X_tr, X_te):
    ...

check_t2(zscore_2, fit_transform_train_test_2)''',
     suff(SOL2, ["zscore", "fit_transform_train_test"]) + "\ncheck_t2(zscore_2, fit_transform_train_test_2)")

# ------------------------------------------------------------------ T3
md('''---
## T3　訓練/テストに分ける・データ漏れ''')
md('''### ① 説明する
3 文で書きます。「なぜ訓練とテストに分ける？」「データ漏れ（leakage）とは？」「標準化や特徴量選択は、分割の前と後のどちらでやる？」

**あなたの答え：**（ここに書く）''')
code('''n = 200
n_train = None   # test_size = 0.25 のとき、訓練データの件数
n_test = None    # テストデータの件数''', '''n = 200
n_train = 150
n_test = 50''')
code('''check("② 訓練 150 件", lambda: n_train == 150)
check("② テスト 50 件", lambda: n_test == 50)''')
md('''### ③ 自分で作る
1. `my_train_test_split(X, y, test_size, seed)`：乱数（`np.random.default_rng(seed).permutation`）で並べ替えて分ける。同じ `seed` なら同じ結果になること。
2. **データ漏れの実験**：特徴量も答えも完全なランダムなデータ（本当は 50% しか当てられない）で、`run_once(leak, seed)` を書きます。
   - `leak=True`：**全データ**で特徴量を10個選んでから分割
   - `leak=False`：分割してから、**訓練データだけ**で特徴量を選ぶ
   - どちらも最後は `LogisticRegression` を訓練して、テストの正解率を返す''')
code('''def my_train_test_split(X, y, test_size=0.25, seed=0):
    ...

rng = np.random.default_rng(0)
X_noise = rng.normal(size=(100, 1000))      # 特徴量 1000 個。全部ランダム
y_noise = rng.integers(0, 2, 100)           # 答えもランダム

def run_once(leak, seed):
    ...''', SOL3.split("def run_once")[0] + '''rng = np.random.default_rng(0)
X_noise = rng.normal(size=(100, 1000))      # 特徴量 1000 個。全部ランダム
y_noise = rng.integers(0, 2, 100)           # 答えもランダム

def run_once''' + SOL3.split("def run_once")[1])
code('''def check_t3(f_split, f_run):
    X = np.arange(40).reshape(-1, 1); y = np.arange(40)
    a, b, c, d = attempt(f_split, X, y, 0.25, 0) or (None,) * 4
    check("件数が 30 / 10", lambda: len(a) == 30 and len(b) == 10 and len(c) == 30 and len(d) == 10)
    check("重複も抜けもない", lambda: sorted(np.concatenate([a.ravel(), b.ravel()]).tolist()) == list(range(40)))
    check("X と y の対応が保たれている", lambda: (a.ravel() == c).all() and (b.ravel() == d).all())
    check("同じ seed なら同じ分け方", lambda: (f_split(X, y, 0.25, 0)[1] == b).all())
    check("seed が違えば違う分け方", lambda: not (f_split(X, y, 0.25, 1)[1] == b).all())
    try:
        leaky = np.mean([f_run(True, s) for s in range(20)])
        honest = np.mean([f_run(False, s) for s in range(20)])
    except Exception:
        leaky = honest = float("nan")
    print(f"   正解率（20回の平均）  漏れあり: {leaky:.3f}   漏れなし: {honest:.3f}")
    check("漏れありの方が 0.12 以上『良く見える』", lambda: leaky - honest > 0.12)
    check("漏れなしは 0.65 未満（ランダムなので当てずっぽう）", lambda: honest < 0.65)

check_t3(my_train_test_split, run_once)''')
md('''**考えてみよう：** ランダムなデータなのに、漏れありだと 70% 以上「当たる」のはなぜ？ ここに書いてください。''',
   '''**考えてみよう：** ランダムなデータなのに、漏れありだと 70% 以上「当たる」のはなぜ？ ここに書いてください。

> **答え：** 特徴量を選ぶとき、テストデータの答えも見て「たまたま答えと相関した列」を選んでしまうから。1000 個もあれば、偶然よく合う列が必ずある。それがテストにも効いて見えるだけで、新しいデータでは当たらない。''')
md('''### ④ 白紙で再現（次の日に）''')
code('''def my_train_test_split_2(X, y, test_size=0.25, seed=0):
    ...

def run_once_2(leak, seed):
    ...

check_t3(my_train_test_split_2, run_once_2)''',
     suff(SOL3, ["my_train_test_split", "run_once"]) + "\ncheck_t3(my_train_test_split_2, run_once_2)")

# ------------------------------------------------------------------ T4
md('''---
## T4　過学習・交差検証''')
md('''### ① 説明する
3 文で書きます。「過学習とは？」「訓練の点数とテストの点数は、モデルを複雑にするとどう動く？」「交差検証は何のため？」

**あなたの答え：**（ここに書く）''')
code('''n_per_fold = None   # 10 件を k=5 に分けたとき、テスト部分 1 つの件数
sizes_11 = None     # 11 件を k=5 に分けたとき、各テスト部分の件数のリスト（先頭から）''',
     '''n_per_fold = 2
sizes_11 = [3, 2, 2, 2, 2]   # 余り 1 は最初の分割に足す''')
code('''check("② 10÷5 = 2 件", lambda: n_per_fold == 2)
check("② 11 件は [3,2,2,2,2]", lambda: list(sizes_11) == [3, 2, 2, 2, 2])''')
md('''### ③ 自分で作る
- `kfold_indices(n, k)`：シャッフルしない K 分割。`(訓練の番号, テストの番号)` のリストを返す（`KFold(k)` と同じ分け方）
- `my_cv_score(model, X, y, k)`：for ループで各分割を訓練→テストして、`.score` の平均を返す（`cross_val_score` を使わない）
- `depth_curve(...)`：決定木の深さ 1〜15 で、訓練とテストの R² を返す''')
code('''def kfold_indices(n, k):
    ...

def my_cv_score(model, X, y, k=5):
    ...

def depth_curve(X_tr, y_tr, X_te, y_te, depths):
    ...''', SOL4)
code('''rng = np.random.default_rng(15)
x = np.sort(rng.uniform(0, 6, 100)); yy = np.sin(x) + rng.normal(0, 0.4, 100)
idx = rng.permutation(100); tr, te = idx[:60], idx[60:]
Xs_tr, ys_tr, Xs_te, ys_te = x[tr].reshape(-1, 1), yy[tr], x[te].reshape(-1, 1), yy[te]
Xr, yr = load_diabetes(return_X_y=True)

def check_t4(f_kf, f_cv, f_curve):
    check("kfold_indices(11,5) のテスト件数が KFold と同じ", lambda: [len(t) for _, t in f_kf(11, 5)] == [len(t) for _, t in KFold(5).split(np.arange(11))])
    check("訓練とテストが重ならず、全部使っている", lambda: all(len(set(a) & set(b)) == 0 and len(a) + len(b) == 11 for a, b in f_kf(11, 5)))
    m = LinearRegression()
    check("my_cv_score が cross_val_score(KFold(5)) と一致", lambda: abs(f_cv(m, Xr, yr, 5) - cross_val_score(m, Xr, yr, cv=KFold(5)).mean()) < 1e-9)
    train, test = attempt(f_curve, Xs_tr, ys_tr, Xs_te, ys_te, range(1, 16)) or (None, None)
    check("深さ15 で訓練の R² がほぼ 1（暗記している）", lambda: train[-1] > 0.99)
    check("テストが最良なのは浅い木（深さ 2〜6）", lambda: 2 <= 1 + int(np.argmax(test)) <= 6)
    check("深すぎるとテストが悪化（深さ15 は最良より 0.05 以上悪い）", lambda: test[-1] < max(test) - 0.05)

check_t4(kfold_indices, my_cv_score, depth_curve)''')
code('''best_depth = None   # 上の結果から、テストの点数が最も高い深さを読み取る（自分で計算して数字を入れる）''',
     '''train_s, test_s = depth_curve(Xs_tr, ys_tr, Xs_te, ys_te, range(1, 16))
best_depth = 1 + int(np.argmax(test_s))''')
code('''check("③ best_depth は 3", lambda: best_depth == 3)''')
md('''### ④ 白紙で再現（次の日に）''')
code('''def kfold_indices_2(n, k):
    ...

def my_cv_score_2(model, X, y, k=5):
    ...

def depth_curve_2(X_tr, y_tr, X_te, y_te, depths):
    ...

check_t4(kfold_indices_2, my_cv_score_2, depth_curve_2)''',
     suff(SOL4, ["kfold_indices", "my_cv_score", "depth_curve"]).replace("for tr, te in kfold_indices_2", "for tr, te in kfold_indices_2") + "\ncheck_t4(kfold_indices_2, my_cv_score_2, depth_curve_2)")

# ------------------------------------------------------------------ T5
md('''---
## T5　回帰の評価：RMSE・MAE・R²''')
md('''### ① 説明する
3 文で書きます。「RMSE の単位は？ 何を表す？」「R² = 0 と R² = 1 はそれぞれ何を意味する？」「訓練データで R² が高くても安心できないのはなぜ？」

**あなたの答え：**（ここに書く）''')
code('''y_hand = [3, 5, 7]       # 実測
p_hand = [4, 5, 5]       # 予測
rmse_hand = None   # RMSE（平方根まで計算して、数字を入れる）
mae_hand = None    # MAE
r2_hand = None     # R²  ※ 実測の平均は 5''',
     '''y_hand = [3, 5, 7]       # 実測
p_hand = [4, 5, 5]       # 予測
rmse_hand = (5 / 3) ** 0.5    # 誤差は 1, 0, -2 → 二乗の平均 5/3
mae_hand = 1.0                # (1 + 0 + 2) / 3
r2_hand = 0.375               # 1 - 5/8  （SSE=5, SST=4+0+4=8）''')
code('''check("② RMSE ≈ 1.291", lambda: abs(rmse_hand - (5 / 3) ** 0.5) < 1e-6)
check("② MAE = 1", lambda: abs(mae_hand - 1.0) < 1e-9)
check("② R² = 0.375", lambda: abs(r2_hand - 0.375) < 1e-9)''')
md('''### ③ 自分で作る
`rmse(y, p)`・`mae(y, p)`・`r2(y, p)` を NumPy で書きます（`sklearn.metrics` は答え合わせにだけ使う）。
**R² の式：** 1 − (誤差の二乗の合計) ÷ (実測と平均の差の二乗の合計)''')
code('''def rmse(y, p):
    ...

def mae(y, p):
    ...

def r2(y, p):
    ...''', SOL5)
code('''Xr_tr, Xr_te, yr_tr, yr_te = train_test_split(*load_diabetes(return_X_y=True), test_size=0.25, random_state=0)
pred = LinearRegression().fit(Xr_tr, yr_tr).predict(Xr_te)

def check_t5(f_rmse, f_mae, f_r2):
    check("rmse が sklearn と一致", lambda: abs(f_rmse(yr_te, pred) - mean_squared_error(yr_te, pred) ** 0.5) < 1e-9)
    check("mae が sklearn と一致", lambda: abs(f_mae(yr_te, pred) - mean_absolute_error(yr_te, pred)) < 1e-9)
    check("r2 が sklearn と一致", lambda: abs(f_r2(yr_te, pred) - r2_score(yr_te, pred)) < 1e-9)
    check("平均だけを予測すると R² = 0", lambda: abs(f_r2(yr_te, np.full(len(yr_te), np.mean(yr_te)))) < 1e-9)
    check("平均より悪い予測だと R² はマイナスになる", lambda: f_r2([1, 2, 3], [3, 2, 1]) < 0)
    check("手計算の例（②）と一致", lambda: abs(f_rmse([3, 5, 7], [4, 5, 5]) - (5 / 3) ** 0.5) < 1e-9 and abs(f_r2([3, 5, 7], [4, 5, 5]) - 0.375) < 1e-9)

check_t5(rmse, mae, r2)''')
md('''### ④ 白紙で再現（次の日に）''')
code('''def rmse_2(y, p):
    ...

def mae_2(y, p):
    ...

def r2_2(y, p):
    ...

check_t5(rmse_2, mae_2, r2_2)''',
     suff(SOL5, ["rmse", "mae", "r2"]) + "\ncheck_t5(rmse_2, mae_2, r2_2)")

# ------------------------------------------------------------------ T6
md('''---
## T6　分類の評価：混同行列・precision・recall''')
md('''### ① 説明する
3 文で書きます。「precision と recall は、それぞれ何を聞いている？」「病気の見逃しを避けたいときは、どちらを重視する？」「正解率（accuracy）だけを信じてはいけないのはなぜ？」

**あなたの答え：**（ここに書く）''')
code('''TP, FP, FN, TN = 8, 2, 4, 86
precision_hand = None   # TP / (TP + FP)
recall_hand = None      # TP / (TP + FN)
accuracy_hand = None
f1_hand = None          # 2 * precision * recall / (precision + recall)

# 不均衡データ：1000 件のうち陽性は 30 件。「全部陰性」と答えるモデルの…
acc_always0 = None      # 正解率
rec_always0 = None      # recall''',
     '''TP, FP, FN, TN = 8, 2, 4, 86
precision_hand = 8 / 10
recall_hand = 8 / 12
accuracy_hand = (8 + 86) / 100
f1_hand = 2 * (8 / 10) * (8 / 12) / ((8 / 10) + (8 / 12))

# 不均衡データ：1000 件のうち陽性は 30 件。「全部陰性」と答えるモデルの…
acc_always0 = 970 / 1000     # 正解率は 97%
rec_always0 = 0.0            # でも陽性は 1 件も見つけていない''')
code('''check("② precision = 0.8", lambda: abs(precision_hand - 0.8) < 1e-9)
check("② recall = 2/3", lambda: abs(recall_hand - 2 / 3) < 1e-9)
check("② accuracy = 0.94", lambda: abs(accuracy_hand - 0.94) < 1e-9)
check("② F1 ≈ 0.727", lambda: abs(f1_hand - 0.7272727) < 1e-6)
check("② 全部陰性でも正解率 97%", lambda: abs(acc_always0 - 0.97) < 1e-9)
check("② でも recall は 0", lambda: rec_always0 == 0)''')
md('''### ③ 自分で作る
- `confusion(y_true, y_pred)`：`(TN, FP, FN, TP)` を返す（`1` を陽性とする）
- `precision(...)`・`recall(...)`：`confusion` を使って計算する。分母が 0 のときは `0.0`
- `sweep(y_true, proba, thresholds)`：しきい値ごとに `(しきい値, precision, recall)` のリストを返す
  — しきい値を動かすと precision と recall がシーソーのように動く様子を、数字で確かめます。''')
code('''def confusion(y_true, y_pred):
    ...

def precision(y_true, y_pred):
    ...

def recall(y_true, y_pred):
    ...

def sweep(y_true, proba, thresholds):
    ...''', SOL6)
code('''Xc, yc = load_breast_cancer(return_X_y=True)          # 1 = 良性 を「陽性」として扱う
Xc_tr, Xc_te, yc_tr, yc_te = train_test_split(Xc, yc, test_size=0.3, random_state=1, stratify=yc)
sc = StandardScaler().fit(Xc_tr)
clf = LogisticRegression(max_iter=1000).fit(sc.transform(Xc_tr), yc_tr)
proba = clf.predict_proba(sc.transform(Xc_te))[:, 1]

def check_t6(f_conf, f_prec, f_rec, f_sweep):
    pred = (proba >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(yc_te, pred).ravel()
    check("confusion が sklearn の confusion_matrix と一致", lambda: tuple(f_conf(yc_te, pred)) == (tn, fp, fn, tp))
    check("precision が sklearn と一致", lambda: abs(f_prec(yc_te, pred) - precision_score(yc_te, pred)) < 1e-9)
    check("recall が sklearn と一致", lambda: abs(f_rec(yc_te, pred) - recall_score(yc_te, pred)) < 1e-9)
    res = attempt(f_sweep, yc_te, proba, [0.1, 0.3, 0.5, 0.7, 0.9]) or []
    check("sweep: 5 つのしきい値すべてで sklearn と一致", lambda: len(res) == 5 and all(
        abs(p - precision_score(yc_te, proba >= t)) < 1e-9 and abs(r - recall_score(yc_te, proba >= t)) < 1e-9 for t, p, r in res))
    check("しきい値を上げると recall は下がる（または同じ）", lambda: all(res[i][2] >= res[i + 1][2] for i in range(4)))
    check("0 件予測のとき precision は 0.0（ゼロ割りしない）", lambda: f_prec([1, 1, 0], [0, 0, 0]) == 0.0)

check_t6(confusion, precision, recall, sweep)''')
md('''**考えてみよう：** 今回の「陽性」は良性（1）です。もし陽性が「がん」で、見逃したくないとしたら、しきい値は上げる？下げる？ その理由は？ ここに書いてください。''',
   '''**考えてみよう：** 今回の「陽性」は良性（1）です。もし陽性が「がん」で、見逃したくないとしたら、しきい値は上げる？下げる？ その理由は？ ここに書いてください。

> **答え：** 下げる。しきい値を下げると、少しでも怪しいものを陽性と言うので recall（見逃さない割合）が上がる。代わりに precision（陽性と言った中の的中率）は下がる＝誤報が増える。見逃しのコストが高いなら、誤報を受け入れる。''')
md('''### ④ 白紙で再現（次の日に）''')
code('''def confusion_2(y_true, y_pred):
    ...

def precision_2(y_true, y_pred):
    ...

def recall_2(y_true, y_pred):
    ...

def sweep_2(y_true, proba, thresholds):
    ...

check_t6(confusion_2, precision_2, recall_2, sweep_2)''',
     suff(SOL6, ["confusion", "precision", "recall", "sweep"]) + "\ncheck_t6(confusion_2, precision_2, recall_2, sweep_2)")

md('''---
## おしまい
6トピックすべてで、④が**10分以内に ✅ 全部**になれば、670 の統計の部分は大丈夫です。
一度で終わらせず、**1週間後にもう一度④だけ**やってみてください。思い出す練習が、いちばん記憶に残ります。''')
