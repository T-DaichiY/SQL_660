"""Lesson content for the 6 pages (uniform 4-unit skeleton: ① 説明 ② 手計算 ③ 自作 ④ 白紙再現)."""
import sys
B = sys.modules["__main__"]
C, H, note, warn, teal, table, details, fig = B.C, B.H, B.note, B.warn, B.teal, B.table, B.details, B.fig
import nbdata as N
SETUP = N.SETUP

def build_units(u1, u2, u3, u4):
    return [dict(title="説明する：何のため？", sub="3文で言えるようにする", body=u1),
            dict(title="手で計算する", sub="小さなデータを紙と電卓で", body=u2),
            dict(title="自分で作る", sub="NumPy で書いて、scikit-learn と一致させる", body=u3),
            dict(title="白紙で再現する・よくある間違い", sub="次の日に、見ずにもう一度", body=u4)]

REDO = lambda items: note("<strong>④ 次の日にやること：</strong>ノートブックの「④ 白紙で再現」で、名前の後ろに <code>_2</code> が付いた関数を、③を見ずに書き直します。<strong>10分以内</strong>に ✅ が揃えば合格です。<br>" + items)

# ====================================================================== T1
add = B.add_page
add(slug="py_describe", short="平均・中央値・外れ値", icon="📏", title="平均・中央値・外れ値・歪み", tag="T1 · 670 ML Python 実践",
    lead="データの「顔つき」を知る最初の一歩。平均と中央値の違い、外れ値の見つけ方（1.5×IQR）、歪度を、<strong>自分の関数で</strong>計算します。",
    card="平均 vs 中央値、1.5×IQR ルール、歪度を NumPy で自作し、pandas・scipy と一致させます。",
    tsec="ノートブックの T1", tip="歪みのあるデータでは、平均は外れ値に引っぱられます。「平均と中央値がずれていたら、まず歪みを疑う」が合言葉です。",
    terms=[("mean", "平均", "全部足して件数で割る。外れ値に弱い。"), ("median", "中央値", "小さい順の真ん中。外れ値に強い。"),
           ("IQR", "四分位範囲", "Q3 − Q1。真ん中50%の幅。"), ("skewness", "歪度", "分布の左右の非対称さ。正なら右に裾が長い。")],
    pre=SETUP + "d = np.random.default_rng(1).lognormal(size=200)\n",
    units=build_units(
        [H("<p>モデルを作る前に必ずやるのが<strong>データの要約</strong>です。ここで間違えると、あとの前処理がすべてずれます。</p>"),
         H(table(["", "平均 (mean)", "中央値 (median)"], [["何か", "全部足して件数で割る", "小さい順に並べた真ん中の値"], ["外れ値", "<strong>引っぱられる</strong>", "ほとんど動かない"], ["使う場面", "対称な分布", "歪んだ分布・外れ値あり"]])),
         H(details("📝 3文のお手本（自分で書いてから開く）", "平均は全部の値の合計を件数で割ったもので、極端に大きい値が1つあるだけで大きく動く。中央値は並べた真ん中なので外れ値に強い。<strong>平均が中央値より大きいときは右に歪んでいる</strong>ので、代表値は中央値を信じる。"))],
        [H("<p>5 つのデータ <code>[2, 3, 3, 4, 50]</code> で、紙と電卓でやってみます。</p>"),
         H("<p><strong>平均</strong> ＝ (2+3+3+4+50) ÷ 5 ＝ <strong>12.4</strong>　／　<strong>中央値</strong> ＝ 真ん中（3番目）＝ <strong>3</strong>。50 が 1 つあるだけで、平均は 12.4 まで跳ね上がります。</p>"),
         C("x = [2, 3, 3, 4, 50]\nprint(np.mean(x), np.median(x))"),
         H("<p><strong>1.5×IQR ルール</strong>：Q1 と Q3 を出し、IQR ＝ Q3 − Q1。<code>Q1 − 1.5×IQR</code> より小さい、または <code>Q3 + 1.5×IQR</code> より大きい値を外れ値とします。ここでは Q1＝3、Q3＝4、IQR＝1 なので上限は 5.5。50 は外れ値です。</p>"),
         C("q1, q3 = np.percentile(x, [25, 75])\niqr = q3 - q1\nprint(q1, q3, 'upper =', q3 + 1.5 * iqr)")],
        [H("<p><code>iqr_outliers(x)</code> と <code>skewness(x)</code> を自作します。歪度は「各値の z スコアの 3 乗の平均」です。</p>"),
         C(N.SOL1, show=False), H("<p>pandas と scipy の結果と並べて、一致するかを確かめます（lognormal の右に歪んだ乱数 200 個）。</p>"),
         C("s = pd.Series(d)\nq1, q3 = s.quantile(.25), s.quantile(.75)\nref = (s < q1 - 1.5 * (q3 - q1)) | (s > q3 + 1.5 * (q3 - q1))\nprint('外れ値の数  自作:', iqr_outliers(d).sum(), ' pandas:', ref.sum(), ' 一致:', (iqr_outliers(d) == ref.to_numpy()).all())\nprint('歪度  自作:', round(skewness(d), 4), ' scipy:', round(stats.skew(d), 4), ' pandas .skew():', round(s.skew(), 4))\nprint('平均', round(d.mean(), 3), ' 中央値', round(np.median(d), 3))"),
         note("<strong>pandas の <code>.skew()</code> だけ少し違う値</strong>になりました。scipy の既定は n で割る「標本の歪度」、pandas は小標本の偏りを補正した版だからです。こういう<strong>「ずれの理由」を自分で説明できる</strong>ことが、試験でも強みになります。"),
         C("import matplotlib.pyplot as plt\nfig, ax = plt.subplots(figsize=(7, 3.4))\nax.hist(d, bins=30, color='#8fb3e8', edgecolor='white')\nax.axvline(d.mean(), color='#B84848', lw=2, label=f'mean {d.mean():.2f}')\nax.axvline(np.median(d), color='#3C8A5A', lw=2, label=f'median {np.median(d):.2f}')\nax.legend(); ax.set_title('Right-skewed data: mean > median')", show=False, plot="t1_skew"),
         H(fig("t1_skew", "右に歪んだデータ。平均（赤）が中央値（緑）より右にある。"))],
        [H(REDO("<code>iqr_outliers_2</code>・<code>skewness_2</code>")),
         H(warn("<strong>よくある間違い</strong><ul><li><code>np.percentile</code> に <code>[0.25, 0.75]</code> と渡す（<code>[25, 75]</code> が正しい。<code>np.quantile</code> なら <code>0.25</code>）</li><li>外れ値を見つけたら自動で消す（まず原因を調べる。入力ミスか、本物の極端な値か）</li><li>歪んだデータの平均を「普通の値」と読む</li></ul>")),
         H(details("❓ 確認：平均 12.4・中央値 3 のデータで、「代表的な値」としてふさわしいのは？", "中央値（3）。平均は 50 という 1 つの外れ値に引っぱられている。")),
         H(details("❓ 確認：歪度がプラスのとき、分布のどちらに裾が長い？", "右（大きい方）。平均 > 中央値になりやすい。"))]))

# ====================================================================== T2
add(slug="py_scale", short="標準化", icon="⚖️", title="標準化（z スコア）", tag="T2 · 670 ML Python 実践",
    lead="単位の違う列を同じものさしに揃える<strong>標準化</strong>。z スコアを自作して、<code>StandardScaler</code> と pandas の <code>.std()</code> が<strong>なぜ少しずれるか</strong>まで確かめます。",
    card="z スコアを自作し、訓練データだけで fit する書き方と、n と n−1 のずれを確かめます。",
    tsec="ノートブックの T2", tip="標準化は「平均 0・SD 1 にする」だけ。ただし<strong>平均と SD は訓練データだけから</strong>求める、が試験の定番です。",
    terms=[("z-score", "z スコア", "(x − 平均) ÷ SD。平均から何 SD 離れているか。"), ("standardization", "標準化", "平均 0・SD 1 に揃える変換。"),
           ("ddof", "自由度の補正", "SD を割る数を n − ddof にする。pandas は 1、NumPy・StandardScaler は 0。")],
    pre=SETUP + "Xd, _ = load_diabetes(return_X_y=True)\ncol = Xd[:, 2]\nXa, Xb = Xd[:300], Xd[300:]\n",
    units=build_units(
        [H("<p>身長（cm）と年収（円）のように<strong>単位や大きさが違う列</strong>は、そのまま使うと、数字の大きい列がモデルを支配してしまいます。距離を使うモデル（KNN・SVM・K-Means）や、正則化つきの回帰では特に問題です。標準化は<strong>各列を「平均から何 SD 離れているか」に置き換える</strong>ことです。</p>"),
         H(note("木のモデル（決定木・ランダムフォレスト）は大小関係しか見ないので、標準化は<strong>不要</strong>です。")),
         H(details("📝 3文のお手本", "標準化は各列から平均を引いて SD で割り、平均 0・SD 1 に揃える変換。単位の違う列を公平に扱うため、距離や正則化を使うモデルで必要になる。標準化した列の平均は 0、SD は 1 になる。"))],
        [H("<p>平均 10・SD 2 のとき、x = 14 の z スコアは (14 − 10) ÷ 2 ＝ <strong>2</strong>（平均より 2 SD 上）。x = 7 なら (7 − 10) ÷ 2 ＝ <strong>−1.5</strong>。逆に z = −1 を元の値に戻すと 10 + (−1)×2 ＝ <strong>8</strong>。</p>"),
         C("mu, sd = 10, 2\nprint((14 - mu) / sd, (7 - mu) / sd, mu + (-1) * sd)")],
        [H("<p><code>zscore(x, ddof)</code> と、訓練データだけから平均・SD を求める <code>fit_transform_train_test</code> を自作します。</p>"),
         C(N.SOL2, show=False), C("z = zscore(col)\nprint('自作 z の平均・SD:', round(z.mean(), 6), round(z.std(), 6))\nprint('StandardScaler と一致:', np.allclose(z, StandardScaler().fit_transform(col.reshape(-1, 1)).ravel()))"),
         H("<h3>なぜ pandas とずれる？</h3><p>5 個のデータ <code>[1,2,3,4,5]</code> で、2 つの SD を比べます。</p>"),
         C("data = np.array([1., 2., 3., 4., 5.])\nsc_sd = StandardScaler().fit(data.reshape(-1, 1)).scale_[0]\npd_sd = pd.Series(data).std()\nprint('StandardScaler の SD:', round(sc_sd, 4), ' pandas .std():', round(pd_sd, 4))\nprint('比:', round(sc_sd / pd_sd, 4), ' = sqrt(4/5) =', round(np.sqrt(4 / 5), 4))"),
         note("<code>StandardScaler</code> は <strong>n</strong> で、pandas の <code>.std()</code> は <strong>n−1</strong> で割ります。比は √((n−1)/n)。n が大きいほど差は小さくなりますが、<strong>小さいデータでは見えるずれ</strong>です。"),
         H("<h3>訓練データだけで fit する</h3>"),
         C("a, b = fit_transform_train_test(Xa, Xb)\nprint('訓練の平均（ほぼ 0）:', np.abs(a.mean(axis=0)).max().round(8))\nprint('テストの平均（0 にはならない）:', np.abs(b.mean(axis=0)).max().round(3))"),
         note("テストデータの平均が 0 にならないのは<strong>正しい動き</strong>です。テストの情報を使って平均を求めたら、それがデータ漏れになります（→ T3）。")],
        [H(REDO("<code>zscore_2</code>・<code>fit_transform_train_test_2</code>")),
         H(warn("<strong>よくある間違い</strong><ul><li><strong>全データで fit してから分割</strong>する（データ漏れ）。正しくは分割 → 訓練で fit → 訓練とテストを transform</li><li>テストデータを別に <code>fit_transform</code> する（訓練と違うものさしになる）</li><li>木のモデルに標準化をかけて安心する（効果なし。無害だが不要）</li></ul>")),
         H(details("❓ 確認：標準化した列の平均と SD は？", "平均 0・SD 1（訓練データについて）。")),
         H(details("❓ 確認：なぜテストデータは、訓練の平均と SD で変換する？", "本番では未来のデータの平均は分からない。訓練で決めたものさしで測るのが、本番と同じ条件になるから。"))]))

# ====================================================================== T3
NOISE = "rng = np.random.default_rng(0)\nX_noise = rng.normal(size=(100, 1000))\ny_noise = rng.integers(0, 2, 100)\n"
add(slug="py_split", short="分割・データ漏れ", icon="✂️", title="訓練/テストに分ける・データ漏れ", tag="T3 · 670 ML Python 実践",
    lead="なぜ分けるのか、どこで間違えると<strong>データ漏れ</strong>になるのか。完全なランダムデータで「77%当たる」実験をして、漏れの怖さを体で覚えます。",
    card="分割関数を自作し、ランダムなデータで漏れあり／なしの正解率を比べます。",
    tsec="ノートブックの T3", tip="前処理（標準化・特徴量選択・欠損の補完）は、<strong>必ず分割のあと、訓練データだけ</strong>で fit します。",
    terms=[("train/test split", "訓練/テスト分割", "モデルを作るデータと、評価に隠しておくデータに分ける。"), ("data leakage", "データ漏れ", "テストの情報が訓練に混ざること。評価が甘くなる。"),
           ("random_state / seed", "乱数の種", "同じ値なら毎回同じ分け方になる（再現性）。")],
    pre=SETUP + NOISE,
    units=build_units(
        [H("<p>モデルの目的は「<strong>まだ見ていないデータ</strong>を当てる」ことです。訓練で使ったデータを同じ点数で測ると、暗記しただけでも高得点になります。だから評価用のデータを<strong>隠して</strong>とっておきます。</p>"),
         H(teal("<strong>データ漏れ（leakage）</strong>：テストデータの情報が、訓練のどこかに混ざること。評価が実力より良く見えますが、新しいデータでは当たりません。")),
         H(details("📝 3文のお手本", "モデルは見たことのないデータで評価しないと、暗記か実力か区別できないので、訓練とテストに分ける。データ漏れはテストの情報が訓練に混ざることで、点数が実力より良く見えてしまう。標準化や特徴量選択は分割のあとで、訓練データだけで fit する。"))],
        [H("<p>200 件を <code>test_size=0.25</code> で分けると、テストは 200 × 0.25 ＝ <strong>50 件</strong>、訓練は <strong>150 件</strong>。</p>"),
         C("n = 200\nn_test = int(round(n * 0.25))\nprint('訓練', n - n_test, '/ テスト', n_test)")],
        [H("<p><code>my_train_test_split</code> は、乱数で並べ替えた番号の先頭をテスト、残りを訓練にします。</p>"),
         C(N.SOL3, show=False), C("X = np.arange(40).reshape(-1, 1); y = np.arange(40)\na, b, c, d = my_train_test_split(X, y, 0.25, seed=0)\nprint(len(a), len(b), '重複なし:', len(set(a.ravel()) & set(b.ravel())) == 0)"),
         H("<h3>データ漏れの実験</h3><p>特徴量 1000 個も答えも<strong>完全なランダム</strong>。本当は 50% しか当てられないはずです。「全データで特徴量を選んでから分割」と「分割してから選ぶ」で正解率を比べます（20 回の平均）。</p>"),
         C("leaky = np.mean([run_once(True, s) for s in range(20)])\nhonest = np.mean([run_once(False, s) for s in range(20)])\nprint(f'漏れあり {leaky:.3f} / 漏れなし {honest:.3f}')"),
         C("import matplotlib.pyplot as plt\nfig, ax = plt.subplots(figsize=(5, 3.2))\nax.bar(['leak (select on all data)', 'honest (select on train)'], [leaky, honest], color=['#B84848', '#3C8A5A'])\nax.axhline(0.5, color='gray', ls='--'); ax.set_ylim(0.4, 0.9); ax.set_ylabel('test accuracy')\nax.set_title('Pure noise: 77% is an illusion')\nplt.xticks(fontsize=8)", show=False, plot="t3_leak"),
         H(fig("t3_leak", "ランダムなデータなのに、漏れありだと約77%「当たる」。")),
         note("答えがランダムなのに 77% 当たるのは、<strong>特徴量を選ぶときにテストの答えも見ていた</strong>から。1000 個もあれば、たまたま答えと合う列が必ずあります。")],
        [H(REDO("<code>my_train_test_split_2</code>・<code>run_once_2</code>")),
         H(warn("<strong>よくある間違い</strong><ul><li>標準化・欠損補完・特徴量選択を<strong>分割の前</strong>に全データでやる</li><li>テストの点数を見ながらモデルやパラメータを何度も選び直す（テストが訓練の一部になる）</li><li>クラスの比率が偏るデータで <code>stratify</code> を付けない</li></ul>")),
         H(details("❓ 確認：分割のあとに標準化を fit するのは、訓練・テストのどちら？", "訓練データだけ。テストは同じ平均・SD で transform するだけ。")),
         H(details("❓ 確認：テストの点数を見て、モデルを選び直してよい？", "良くない。選び直すたびにテストの情報が混ざる。選ぶのは検証データか交差検証で行い、テストは最後に1回だけ使う。"))]))

# ====================================================================== T4
SINE = "rng = np.random.default_rng(15)\nx = np.sort(rng.uniform(0, 6, 100)); yy = np.sin(x) + rng.normal(0, 0.4, 100)\nidx = rng.permutation(100); tr, te = idx[:60], idx[60:]\nXs_tr, ys_tr, Xs_te, ys_te = x[tr].reshape(-1, 1), yy[tr], x[te].reshape(-1, 1), yy[te]\nXr, yr = load_diabetes(return_X_y=True)\n"
add(slug="py_overfit", short="過学習・交差検証", icon="🎢", title="過学習・交差検証", tag="T4 · 670 ML Python 実践",
    lead="モデルを複雑にすると、訓練の点数は上がり続けるのに、テストの点数は途中から下がります。決定木の深さで<strong>U字</strong>を描き、交差検証を for ループで自作します。",
    card="決定木の深さで訓練/テストの点数を描き、K分割交差検証を自作します。",
    tsec="ノートブックの T4", tip="「訓練の点数が高いこと」は自慢になりません。<strong>テスト（または交差検証）の点数</strong>で判断します。",
    terms=[("overfitting", "過学習", "訓練データを暗記して、新しいデータで当たらなくなること。"), ("cross-validation", "交差検証", "データを K 分割し、順番に1つをテストにして平均する。"),
           ("hyperparameter", "ハイパーパラメータ", "学習の前に人が決める設定（木の深さなど）。")],
    pre=SETUP + SINE,
    units=build_units(
        [H("<p>複雑なモデルは、訓練データの<strong>ノイズまで覚えて</strong>しまいます。訓練の点数は上がるのに、新しいデータでは当たらない。これが過学習です。</p>"),
         H(table(["状態", "訓練の点数", "テストの点数", "対策"], [["過学習", "とても高い", "低い", "単純なモデルに／データを増やす／正則化"], ["学習不足", "低い", "低い", "複雑なモデルに／特徴量を足す"]])),
         H("<p><strong>交差検証</strong>は、データを K 個に分け、1 つずつテストにして K 回評価し、平均する方法です。1 回の分割の「運」に左右されにくくなります。</p>"),
         H(details("📝 3文のお手本", "過学習は訓練データを暗記して新しいデータで当たらなくなることで、訓練の点数だけ高いのが目印。モデルを複雑にすると訓練の点数は上がり続けるが、テストの点数は途中から下がる。交差検証はデータを K 分割して順番にテストに使い、点数の平均で運に左右されず比べる方法。"))],
        [H("<p>10 件を k = 5 に分けると、1 つのテスト部分は 10 ÷ 5 ＝ <strong>2 件</strong>。11 件を 5 分割すると余りが 1 件出るので、先頭の分割に足して <strong>[3, 2, 2, 2, 2]</strong>（<code>KFold</code> と同じ規則）。</p>"),
         C("print([len(t) for _, t in KFold(5).split(np.arange(10))])\nprint([len(t) for _, t in KFold(5).split(np.arange(11))])")],
        [H("<p><code>kfold_indices</code>（分け方）・<code>my_cv_score</code>（交差検証）・<code>depth_curve</code>（深さごとの点数）を自作します。</p>"),
         C(N.SOL4, show=False), C("print([len(t) for _, t in kfold_indices(11, 5)])\nm = LinearRegression()\nprint('自作 CV:', round(my_cv_score(m, Xr, yr, 5), 6))\nprint('sklearn  :', round(cross_val_score(m, Xr, yr, cv=KFold(5)).mean(), 6))"),
         H("<h3>決定木の深さで U 字を描く</h3><p>sin 曲線にノイズを足したデータ（訓練 60 件・テスト 40 件）を、深さ 1〜15 の木で学習します。</p>"),
         C("train_s, test_s = depth_curve(Xs_tr, ys_tr, Xs_te, ys_te, range(1, 16))\nprint('深さ15 の訓練 R²:', round(train_s[-1], 3), '/ テスト R²:', round(test_s[-1], 3))\nprint('テストが最良の深さ:', 1 + int(np.argmax(test_s)), '（R² =', round(max(test_s), 3), '）')"),
         C("import matplotlib.pyplot as plt\nfig, ax = plt.subplots(figsize=(7, 3.4))\nd = list(range(1, 16))\nax.plot(d, train_s, 'o-', color='#4471B8', label='train')\nax.plot(d, test_s, 's-', color='#B84848', label='test')\nax.axvline(1 + int(np.argmax(test_s)), color='gray', ls='--')\nax.set_xlabel('max_depth'); ax.set_ylabel('R2'); ax.legend(); ax.set_title('Train keeps rising, test peaks then falls')", show=False, plot="t4_depth"),
         H(fig("t4_depth", "訓練（青）は深さとともに 1 に近づくが、テスト（赤）は深さ 3 付近で最良になり、その後下がる。")),
         note("訓練の R² が <strong>ほぼ 1.0</strong>（暗記）なのに、テストは 0.69 まで下がりました。深さ 3 前後が「ちょうどよい複雑さ」です。")],
        [H(REDO("<code>kfold_indices_2</code>・<code>my_cv_score_2</code>・<code>depth_curve_2</code>")),
         H(warn("<strong>よくある間違い</strong><ul><li>訓練の点数だけ見て「良いモデル」と判断する</li><li>テストの点数を見ながら深さを選ぶ（テストが訓練の一部になる）。選ぶのは交差検証、テストは最後の 1 回</li><li>交差検証の各分割ごとに、前処理（標準化など）を全データで fit しておく（漏れ。→ T3）</li></ul>")),
         H(details("❓ 確認：5 分割交差検証では、モデルを何回学習する？", "5 回（各分割で 1 回ずつ）。点数は 5 個の平均で報告し、バラつき（SD）も一緒に見る。")),
         H(details("❓ 確認：訓練 R² = 0.99・テスト R² = 0.60 のとき、何を疑う？", "過学習。モデルを単純にする、データを増やす、正則化（Ridge・Lasso）を使う。"))]))

# ====================================================================== T5
REG = "Xr_tr, Xr_te, yr_tr, yr_te = train_test_split(*load_diabetes(return_X_y=True), test_size=0.25, random_state=0)\npred = LinearRegression().fit(Xr_tr, yr_tr).predict(Xr_te)\n"
add(slug="py_regmetrics", short="RMSE・R²", icon="📈", title="回帰の評価：RMSE・MAE・R²", tag="T5 · 670 ML Python 実践",
    lead="数値を予測するモデルの「当たり具合」を表す 3 つの指標を、<strong>式から</strong>自作します。R² がマイナスになる理由も確かめます。",
    card="RMSE・MAE・R² を NumPy で自作して sklearn と一致させ、R² の意味を確かめます。",
    tsec="ノートブックの T5", tip="RMSE は<strong>y と同じ単位</strong>の「平均的なズレ」。R² は「平均だけを予測するより、どれだけ良いか」。",
    terms=[("RMSE", "二乗平均平方根誤差", "誤差を二乗して平均し、平方根を取る。y と同じ単位。大きな誤差を重く見る。"), ("MAE", "平均絶対誤差", "誤差の絶対値の平均。外れ値に強い。"),
           ("R²", "決定係数", "1 − (誤差の二乗和) ÷ (平均からの差の二乗和)。1 に近いほど良い。")],
    pre=SETUP + REG,
    units=build_units(
        [H("<p>回帰モデルは「どれくらい外したか」を<strong>1つの数字</strong>にして比べます。</p>"),
         H(table(["指標", "意味", "単位", "特徴"], [["RMSE", "平均的なズレの大きさ", "y と同じ", "大きな外れを重く罰する"], ["MAE", "ズレの絶対値の平均", "y と同じ", "外れ値に強い"], ["R²", "ばらつきのうち説明できた割合", "なし（0〜1）", "<strong>平均だけ予測すると 0</strong>、それより悪いとマイナス"]])),
         H(details("📝 3文のお手本", "RMSE は誤差を二乗して平均し平方根を取った値で、y と同じ単位の「平均的なズレ」を表す。R² は平均だけを予測する場合と比べてどれだけ誤差が減ったかの割合で、0 なら平均予測と同じ。訓練データだけで R² が高くても過学習かもしれないので、必ずテストデータで見る。"))],
        [H("<p>実測 <code>[3, 5, 7]</code>・予測 <code>[4, 5, 5]</code> を紙で計算します。誤差（予測 − 実測）は <strong>1, 0, −2</strong>。</p>"),
         H(table(["指標", "計算", "結果"], [["MSE", "(1² + 0² + 2²) ÷ 3 ＝ 5/3", "1.667"], ["RMSE", "√(5/3)", "<strong>1.291</strong>"], ["MAE", "(1 + 0 + 2) ÷ 3", "<strong>1.0</strong>"], ["R²", "SSE ＝ 5、SST ＝ (3−5)²+(5−5)²+(7−5)² ＝ 8 → 1 − 5/8", "<strong>0.375</strong>"]])),
         C("y = np.array([3, 5, 7]); p = np.array([4, 5, 5])\nprint(np.sqrt(np.mean((y - p) ** 2)), np.mean(np.abs(y - p)), 1 - np.sum((y - p) ** 2) / np.sum((y - y.mean()) ** 2))")],
        [H("<p>3 つの関数を書き、糖尿病データ（442 人）の線形回帰の予測で、sklearn と並べます。</p>"),
         C(N.SOL5, show=False), C("print('RMSE 自作:', round(rmse(yr_te, pred), 4), ' sklearn:', round(mean_squared_error(yr_te, pred) ** 0.5, 4))\nprint('MAE  自作:', round(mae(yr_te, pred), 4), ' sklearn:', round(mean_absolute_error(yr_te, pred), 4))\nprint('R2   自作:', round(r2(yr_te, pred), 4), ' sklearn:', round(r2_score(yr_te, pred), 4))"),
         H("<h3>R² の意味を確かめる</h3>"),
         C("baseline = np.full(len(yr_te), np.mean(yr_te))      # 平均だけを予測\nprint('平均だけを予測したときの R²:', round(r2(yr_te, baseline), 6))\nprint('平均より悪い予測の R²:', r2([1, 2, 3], [3, 2, 1]))"),
         note("RMSE ≈ 56 は「予測は平均して約 56 ズレる」という意味です（y の単位は糖尿病の進行指標）。R² ≈ 0.36 は、ばらつきの約 36% を説明できたという意味。<strong>R² は平均より悪い予測ならマイナス</strong>になります。")],
        [H(REDO("<code>rmse_2</code>・<code>mae_2</code>・<code>r2_2</code>")),
         H(warn("<strong>よくある間違い</strong><ul><li>RMSE を「％」だと思う（y と同じ単位）</li><li><strong>訓練データの R²</strong> だけ見て満足する（テストで見る）</li><li>R² は常に 0〜1 だと思う（テストではマイナスになる）</li><li>RMSE と MAE を単位の違う y で比べる</li></ul>")),
         H(details("❓ 確認：RMSE が MAE よりずっと大きいとき、何が起きている？", "少数の大きな誤差がある。RMSE は誤差を二乗するので、大きな外れに強く反応する。")),
         H(details("❓ 確認：R² = 0 は、どんなモデル？", "平均だけを予測するモデルと同じ当たり具合（何も説明できていない）。"))]))

# ====================================================================== T6
CLF = "Xc, yc = load_breast_cancer(return_X_y=True)\nXc_tr, Xc_te, yc_tr, yc_te = train_test_split(Xc, yc, test_size=0.3, random_state=1, stratify=yc)\nsc = StandardScaler().fit(Xc_tr)\nclf = LogisticRegression(max_iter=1000).fit(sc.transform(Xc_tr), yc_tr)\nproba = clf.predict_proba(sc.transform(Xc_te))[:, 1]\n"
add(slug="py_clfmetrics", short="混同行列・P/R", icon="🎯", title="分類の評価：混同行列・precision・recall", tag="T6 · 670 ML Python 実践",
    lead="「当たった／外した」を 4 つに分けて数える<strong>混同行列</strong>から、precision と recall を自作します。しきい値を動かすと、2 つがシーソーのように動く様子も見ます。",
    card="混同行列・precision・recall を自作し、しきい値を動かして2つの動きを確かめます。",
    tsec="ノートブックの T6", tip="<strong>precision</strong>＝「陽性と言った中の的中率」、<strong>recall</strong>＝「本当の陽性を見つけた割合」。見逃しが怖いなら recall、誤報が怖いなら precision。",
    terms=[("confusion matrix", "混同行列", "TP・FP・FN・TN の 4 つの数。"), ("precision", "適合率", "TP ÷ (TP + FP)。陽性と予測した中の的中率。"),
           ("recall", "再現率", "TP ÷ (TP + FN)。本当の陽性を見つけた割合。"), ("threshold", "しきい値", "確率がいくつ以上を陽性とするか。既定は 0.5。")],
    pre=SETUP + CLF,
    units=build_units(
        [H("<p>分類モデルの評価は「正解率」だけでは足りません。たとえば陽性が 3% しかないデータで<strong>「全部陰性」と答える</strong>と、正解率は 97% です。でも陽性は 1 件も見つけていません。</p>"),
         H(table(["", "予測：陽性", "予測：陰性"], [["<strong>実際：陽性</strong>", "TP（正しく陽性）", "FN（見逃し）"], ["<strong>実際：陰性</strong>", "FP（誤報）", "TN（正しく陰性）"]])),
         H("<p><strong>precision</strong> ＝ TP ÷ (TP+FP)、<strong>recall</strong> ＝ TP ÷ (TP+FN)。病気の見逃しを避けたいなら recall、迷惑メール判定で普通のメールを消したくないなら precision を重視します。</p>"),
         H(details("📝 3文のお手本", "precision は陽性と予測した中の的中率で、recall は本当の陽性のうち見つけられた割合。病気の見逃しを避けたいときは recall を重視する。陽性が少ないデータでは、全部陰性と答えても正解率が高くなるので、正解率だけでは判断できない。"))],
        [H("<p>TP = 8、FP = 2、FN = 4、TN = 86（合計 100 件）で計算します。</p>"),
         H(table(["指標", "計算", "結果"], [["precision", "8 ÷ (8+2)", "<strong>0.8</strong>"], ["recall", "8 ÷ (8+4)", "<strong>0.667</strong>"], ["accuracy", "(8+86) ÷ 100", "<strong>0.94</strong>"], ["F1", "2×0.8×0.667 ÷ (0.8+0.667)", "<strong>0.727</strong>"]])),
         C("TP, FP, FN, TN = 8, 2, 4, 86\nprec, rec = TP / (TP + FP), TP / (TP + FN)\nprint(prec, round(rec, 3), (TP + TN) / 100, round(2 * prec * rec / (prec + rec), 3))"),
         H("<p><strong>不均衡データの罠：</strong>1000 件のうち陽性 30 件で、全部陰性と答えると…</p>"),
         C("print('正解率', 970 / 1000, ' recall', 0 / 30)")],
        [H("<p><code>confusion</code> で 4 つを数え、<code>precision</code>・<code>recall</code>・<code>sweep</code>（しきい値ごとの値）を作ります。乳がんデータ（1 = 良性 を陽性とする）のロジスティック回帰で確かめます。</p>"),
         C(N.SOL6, show=False), C("pred = (proba >= 0.5).astype(int)\nprint('自作 :', confusion(yc_te, pred), ' (TN, FP, FN, TP)')\nprint('sklearn:', tuple(confusion_matrix(yc_te, pred).ravel()))\nprint('precision 自作:', round(precision(yc_te, pred), 4), ' sklearn:', round(precision_score(yc_te, pred), 4))\nprint('recall    自作:', round(recall(yc_te, pred), 4), ' sklearn:', round(recall_score(yc_te, pred), 4))"),
         H("<h3>しきい値を動かす</h3>"),
         C("for t, p, r in sweep(yc_te, proba, [0.1, 0.3, 0.5, 0.7, 0.9]):\n    print(f'threshold {t}:  precision {p:.3f}  recall {r:.3f}')"),
         C("import matplotlib.pyplot as plt\nth = np.linspace(0.02, 0.98, 49)\nres = sweep(yc_te, proba, th)\nfig, ax = plt.subplots(figsize=(7, 3.4))\nax.plot(th, [p for _, p, _ in res], color='#4471B8', label='precision')\nax.plot(th, [r for _, _, r in res], color='#B84848', label='recall')\nax.set_xlabel('threshold'); ax.set_ylim(0.8, 1.02); ax.legend(); ax.set_title('Raise the threshold: precision up, recall down')", show=False, plot="t6_threshold"),
         H(fig("t6_threshold", "しきい値を上げると precision は上がり、recall は下がる（シーソー）。")),
         note("しきい値を<strong>下げる</strong>と、少しでも怪しいものを陽性と言うので recall が上がり（見逃しが減る）、代わりに precision が下がります（誤報が増える）。")],
        [H(REDO("<code>confusion_2</code>・<code>precision_2</code>・<code>recall_2</code>・<code>sweep_2</code>")),
         H(warn("<strong>よくある間違い</strong><ul><li>正解率（accuracy）だけで「良いモデル」と判断する（不均衡データで騙される）</li><li><code>confusion_matrix</code> の並び順（<code>[[TN, FP], [FN, TP]]</code>）を取り違える</li><li>precision と recall の分母を入れ替える</li><li>しきい値を 0.5 から動かせると知らない</li></ul>")),
         H(details("❓ 確認：がんの検査で、見逃したくない。しきい値は上げる？下げる？", "下げる。recall が上がり見逃しが減る。誤報（precision の低下）は受け入れる。")),
         H(details("❓ 確認：TP=8・FP=2・FN=4 のとき、precision と recall は？", "precision = 8/10 = 0.8、recall = 8/12 ≈ 0.667。"))]))
