"""670 ML 統計復習 (1/2): explore & prepare, split, regression. Original examples; data are simulated or built into R."""
from lib550 import *

MOD = "670 ML 統計復習"
APT = '''set.seed(670)
n <- 400
apt <- data.frame(area  = round(runif(n, 25, 120)),
                  rooms = sample(1:4, n, replace = TRUE, prob = c(.2, .4, .3, .1)),
                  age   = round(runif(n, 0, 50)))
apt$price <- round(40 + 2.2 * apt$area + 12 * apt$rooms - 0.8 * apt$age + rnorm(n, 0, 25), 1)  # 1000 USD
set.seed(1)
idx   <- sample(n, size = 0.8 * n)
train <- apt[idx, ]
test  <- apt[-idx, ]'''
SKEW = 'skew <- function(x) { x <- x[!is.na(x)]; mean((x - mean(x))^3) / mean((x - mean(x))^2)^1.5 }'
CS = '📌 先に <a href="cheat_ml.html">ML のための統計チートシート</a> で全体の地図を見ておくと、この回の位置づけが分かります。'

# =============================================================== 1. explore & prepare
def ml_explore(P):
    L = dict(slug="ml_explore", mod=MOD, icon="🔍", title="データを見る・整える：要約・外れ値・標準化・欠損",
             tag="ML Prep · Explore &amp; Prepare — Summary Statistics, Skewness, Outliers, z-scores, Missing Values",
             lead="ML のモデルを作る前に必ずやる「データを見る」作業を、統計の言葉で整理します。<strong>平均と中央値の差（歪み）</strong>、<strong>外れ値の判定</strong>、<strong>標準化（z スコア）</strong>、<strong>欠損の補い方</strong>。550 の M2 の復習です。",
             video="670 準備 · 550 M2（記述統計）の復習",
             unav=["① 要約と歪み", "② 外れ値と対数変換", "③ 標準化(z)", "④ 欠損の扱い"],
             terms=[("skewness", "歪度", "分布の左右の非対称さ。右に裾が長いと正。"),
                    ("median", "中央値", "外れ値に強い中心。歪んだデータでは平均より安全。"),
                    ("IQR", "四分位範囲", "Q3 − Q1。真ん中50%の幅。"),
                    ("1.5 × IQR rule", "外れ値の目安", "Q1 − 1.5·IQR より下、Q3 + 1.5·IQR より上。"),
                    ("log transform", "対数変換", "右に歪んだデータを対称に近づける。"),
                    ("z-score", "標準化", "(x − 平均) ÷ SD。平均 0・SD 1 にそろえる。"),
                    ("missing value (NA)", "欠損値", "データが空の所。落とす／補う。"),
                    ("imputation", "補完", "欠損を中央値などで埋めること。")],
             tip="<strong>平均と中央値が大きく違う</strong>ときは、外れ値か歪みのサイン。まず<code>summary()</code>で並べて見る。")
    b = [teal(CS)]
    b.append(unit(1, "要約統計と歪み", "summary() で mean と median を並べる", f'''
  <p>ML の最初の一歩は<strong>データの顔つきを知る</strong>ことです。R の <code>summary()</code> は、最小・四分位・中央値・平均・最大を一度に出します（Python の <code>describe()</code> と同じ）。ここでは R に入っている実データ <code>airquality</code>（ニューヨークの大気データ）のオゾン濃度を使います。</p>
  {P.R('x <- airquality$Ozone\nsummary(x)\nsd(x, na.rm = TRUE)')}
  <p><strong>平均（42.1）が中央値（31.5）より大きい</strong>ことに注目してください。少数の高い値が平均を引き上げています。これが<strong>右に歪んだ</strong>分布です。歪みの大きさは<strong>歪度（skewness）</strong>で数値にできます（正なら右に裾が長い）。</p>
  {P.R(SKEW + '\nskew(x)\nhist(x, breaks = 20, col = "lightblue", main = "Ozone (ppb)", xlab = "Ozone")', plot=True, h=300)}
  {note('📐 <strong>歪度の目安</strong>：0 に近い＝左右対称、<strong>+1 を超える</strong>＝かなり右に歪んでいる。歪んだデータでは<strong>平均より中央値</strong>が「ふつうの値」を表します。')}
'''))
    b.append(unit(2, "外れ値と対数変換", "1.5 × IQR ルールとログで歪みを直す", f'''
  <p>外れ値は、ほかの値から<strong>大きく離れた値</strong>です。550 で学んだ <strong>1.5 × IQR ルール</strong>で、機械的に見つけられます。</p>
  {P.R('q <- quantile(x, c(.25, .75), na.rm = TRUE)\niqr <- unname(diff(q))\nfence <- c(lower = unname(q[1]) - 1.5 * iqr, upper = unname(q[2]) + 1.5 * iqr)\nfence\nsum(x > fence["upper"], na.rm = TRUE)       # how many outliers above the fence')}
  <p>外れ値が見つかったら、<strong>すぐ消さずに理由を考えます</strong>（入力ミスか、本当に珍しい日か）。ML では、次の対策がよく使われます。</p>
  {table(["対策", "いつ使う", "R のコード"], [["そのまま使う", "本物の値で、予測にも大事そう", "—"], ["対数変換", "右に歪んだ正の値（収入・価格・濃度）", "<code>log(x)</code> / <code>log1p(x)</code>"], ["上限で切る（clip）", "極端な値だけ抑えたい", "<code>pmin(x, fence)</code>"], ["取り除く", "明らかな入力ミス", "<code>x[x &lt;= fence]</code>"]])}
  <p>対数変換すると、歪みがどれだけ直るかを確かめましょう。</p>
  {P.R('oz <- airquality$Ozone\nround(c(before = skew(oz), after = skew(log(oz))), 2)\npar(mfrow = c(1, 2))\nhist(oz, breaks = 20, col = "lightblue", main = "raw", xlab = "Ozone")\nhist(log(oz), breaks = 20, col = "lightgreen", main = "log", xlab = "log(Ozone)")', plot=True, w=760, h=300)}
  {practice("p-ml1-u2", "Solar.R の外れ値", "<code>airquality$Solar.R</code> について、<strong>1.5 × IQR ルール</strong>の上限（<code>upper</code>）を求め、それより大きい値の数を数えてください（欠損は無視）。",
             ["quantile", "IQR", "na.rm", "sum"], 'x <- airquality$Solar.R\nq <- quantile(x, c(.25, .75), na.rm = TRUE)\niqr <- unname(diff(q))\nupper <- unname(q[2]) + 1.5 * iqr\nupper\nsum(x > upper, na.rm = TRUE)', "上限は Q3 + 1.5×IQR。<code>na.rm = TRUE</code> を忘れると NA になる。Solar.R はほぼ左右対称なので、上限を超える値はありません。")}
'''))
    b.append(unit(3, "標準化（z スコア）", "桁のちがう列を同じ土俵にそろえる", f'''
  <p>データの列は、単位も大きさもバラバラです（面積は 25〜120、価格は 100〜400）。<strong>距離を使うモデル</strong>（KNN、SVM、クラスタリング、正則化回帰）は、<strong>桁の大きい列だけで決まってしまう</strong>ので、先に<strong>標準化</strong>します。式は 550 で学んだ z スコアそのものです。</p>
  <div class="note-box">📐 <strong>z = (x − 平均) ÷ SD</strong>　→　平均 0、SD 1 にそろう。「平均から SD いくつ分離れているか」を表す。</div>
  {P.R(APT + '\nz_area <- (apt$area - mean(apt$area)) / sd(apt$area)\nround(c(mean = mean(z_area), sd = sd(z_area)), 3)\nhead(round(scale(apt[, c("area", "price")]), 2), 4)     # scale() does the same for every column')}
  {warn('<strong>訓練データだけ</strong>で平均と SD を計算します。テストデータの情報が混ざると<strong>データ漏れ</strong>になります（次の回）。Python では <code>scaler.fit(X_train)</code> のあと <code>transform(X_test)</code> と書きます。')}
  <p>木のモデル（決定木・ランダムフォレスト）は、大小関係だけを見るので標準化は<strong>不要</strong>です。</p>
  {practice("p-ml1-u3", "Wind の z スコア", "<code>airquality$Wind</code> を標準化（z スコア）して、<strong>最初の 5 個</strong>を小数 2 桁で表示してください。",
             ["mean", "sd", "scale"], 'w <- airquality$Wind\nz <- (w - mean(w)) / sd(w)\nround(head(z, 5), 2)', "<code>scale(w)</code> でも同じ値になる（行列で返る）。Wind に欠損はないので na.rm は不要。")}
'''))
    b.append(unit(4, "欠損の扱い", "落とす？ 補う？", f'''
  <p>現実のデータには空の所（NA）があります。多くの ML の関数は NA が入っているとエラーになるので、<strong>落とす</strong>か<strong>補う（補完）</strong>必要があります。</p>
  {P.R('colSums(is.na(airquality))                  # NA count per column\nnrow(airquality); nrow(na.omit(airquality))    # rows left if we drop every row with an NA')}
  <p>行を落とすと、データがかなり減ります（153 行 → 111 行）。そこで<strong>中央値で補う</strong>方法がよく使われます（歪んだ列では平均より安全）。</p>
  {P.R('oz <- airquality$Ozone\nmed <- median(oz, na.rm = TRUE)\noz2 <- ifelse(is.na(oz), med, oz)\nround(c(mean_before = mean(oz, na.rm = TRUE), mean_after = mean(oz2),\n        sd_before = sd(oz, na.rm = TRUE), sd_after = sd(oz2)), 2)')}
  {note('補ったあとは<strong>平均はほぼ同じですが、SD は小さくなります</strong>（同じ値で埋めたぶん、ばらつきが減る）。補完は「便利だが、少しだけ嘘をつく」処理だと覚えておきましょう。欠損が<strong>多い列</strong>は、補うより列ごと落とす方が良いこともあります。')}
  {table(["方法", "長所", "短所"], [["行を落とす（na.omit）", "簡単。嘘が入らない", "データが減る。欠損に偏りがあると結果も偏る"], ["中央値で補う", "データが減らない。外れ値に強い", "SD が小さくなる"], ["平均で補う", "簡単", "外れ値・歪みに弱い"]])}
'''))
    b.append(teal('➡️ <strong>次の回へ：</strong>データを整えたら、モデルを評価するために<strong>訓練とテストに分けます</strong>。<a href="ml_split.html">分ける：訓練とテスト・層化・データ漏れ</a>へ。'))
    q = [('The mean of a variable is much larger than its median. What does this suggest?', 'It is skewed to the right', ['It has no missing values', 'It is already standardized', 'It is perfectly symmetric'], 'A few large values pull the mean up; the median is not affected.'),
         ('Which value would the 1.5 × IQR rule flag as an outlier?', 'A value above Q3 + 1.5 × IQR', ['Any value above the overall mean', 'A value equal to the median', 'Any value outside Q1 and Q3'], 'The fences are Q1 − 1.5·IQR and Q3 + 1.5·IQR.'),
         ('A positive, right-skewed variable (such as income) is often transformed with...', 'A log transform', ['A z-score scaling', 'The median value', 'A 1.5 IQR cutoff'], 'log() compresses large values and makes the distribution more symmetric.'),
         ('After standardizing a variable (z-score), its mean and SD are...', 'Mean 0 and SD 1', ['Mean 1 and SD 0', 'Mean 0 and SD 0', 'Mean 1 and SD 1'], 'z = (x − mean) / SD always gives mean 0 and SD 1.'),
         ('Where should the mean and SD for standardization be calculated?', 'On the training set only', ['On the test data only', 'On all the data together', 'On each row separately'], 'Using test information leaks it into training; compute on train, then apply to test.'),
         ('Missing values are filled with the column median. What happens to the SD?', 'It gets smaller', ['It gets larger', 'It stays the same', 'It drops to zero'], 'The filled-in values all equal the median, so the spread shrinks.')]
    return L, "\n".join(b), q

# =============================================================== 2. split
def ml_split(P):
    L = dict(slug="ml_split", mod=MOD, icon="✂️", title="分ける：訓練とテスト・層化・データ漏れ",
             tag="ML Prep · Splitting Data — Train/Test, Random Seeds, Stratified Sampling, Data Leakage",
             lead="モデルの本当の実力は、<strong>見たことのないデータ</strong>でしか分かりません。<strong>訓練とテストに分ける理由</strong>、<code>set.seed()</code>の役割、クラスの比率を保つ<strong>層化</strong>、成績が不自然に良くなる<strong>データ漏れ</strong>を学びます。",
             video="670 準備 · 550 M4（標本抽出・偏り）の復習",
             unav=["① なぜ分けるか", "② 分け方と乱数", "③ 層化", "④ データ漏れ"],
             terms=[("training set", "訓練データ", "モデルを学習させるデータ（通常 70〜80%）。"),
                    ("test set", "テストデータ", "最後に一度だけ評価に使う、隠しておくデータ。"),
                    ("generalization", "汎化", "新しいデータでもうまく予測できること。"),
                    ("random seed", "乱数の種", "同じ分け方を再現する（set.seed / random_state）。"),
                    ("stratified sampling", "層化抽出", "クラスの比率を保って分ける。"),
                    ("class imbalance", "クラスの偏り", "陽性が極端に少ないデータ。"),
                    ("data leakage", "データ漏れ", "評価で使えないはずの情報が学習に混ざること。"),
                    ("overfitting", "過学習", "訓練データに合いすぎて、新しいデータで悪くなる。")],
             tip="<strong>テストデータはモデルを選び終わるまで見ない</strong>。成績が「良すぎる」ときは、まずデータ漏れを疑う。")
    b = [teal(CS)]
    b.append(unit(1, "なぜ訓練とテストに分けるのか", "訓練データの成績は「甘い」", f'''
  <p>同じデータで学習して、同じデータで評価すると、<strong>成績が実力より良く見えます</strong>。極端な例が、<strong>答えを丸暗記</strong>するモデルです。ここでは、「特徴が最も近い物件の価格をそのまま答える」（最近傍法の最もかんたんな形、<code>k = 1</code>）モデルで、訓練とテストの成績を比べます。</p>
  {P.R(APT + '\nrmse <- function(y, p) sqrt(mean((y - p)^2))\nXs  <- scale(apt[, c("area", "rooms", "age")])           # standardized features\nXtr <- Xs[idx, ]; Xte <- Xs[-idx, ]\nnn1 <- function(Xtr, ytr, Xnew) apply(Xnew, 1, function(v) ytr[which.min(colSums((t(Xtr) - v)^2))])\nround(c(train = rmse(train$price, nn1(Xtr, train$price, Xtr)),\n        test  = rmse(test$price,  nn1(Xtr, train$price, Xte))), 1)')}
  <p><strong>訓練の誤差はほぼ 0</strong>（自分の答えを丸暗記しているため。約 5）なのに、<strong>テストの誤差は約 38</strong>。しかも、次の回で作る単純な線形回帰（テストの RMSE は約 28.5）よりも悪い成績です。これが<strong>過学習</strong>で、訓練データだけの成績は、新しいデータでの実力を教えてくれません。</p>
  {note('📐 <strong>ルール</strong>：学習に使うのは<strong>訓練データだけ</strong>。テストデータは、モデルを選び終えたあとに<strong>一度だけ</strong>使って、「新しいデータでの実力」を見積もります。')}
'''))
    b.append(unit(2, "分け方と乱数", "sample() と set.seed()", f'''
  <p>R では <code>sample()</code> で行番号を無作為に選び、80% を訓練、残りをテストにします（Python の <code>train_test_split</code> と同じ）。</p>
  {P.R('set.seed(1)\nidx   <- sample(nrow(apt), size = 0.8 * nrow(apt))\ntrain <- apt[idx, ]\ntest  <- apt[-idx, ]\nc(train = nrow(train), test = nrow(test))')}
  <p><code>set.seed(1)</code> は「<strong>乱数の種</strong>」です（Python では <code>random_state=42</code>）。種を決めると、毎回同じ分け方になり、<strong>結果を再現</strong>できます。種を変えると、分け方が変わり、テストの成績も少し変わります。</p>
  {P.R('fit_rmse <- function(seed) {\n  set.seed(seed); i <- sample(nrow(apt), 0.8 * nrow(apt))\n  m <- lm(price ~ area + rooms + age, data = apt[i, ])\n  sqrt(mean((apt$price[-i] - predict(m, apt[-i, ]))^2))\n}\nround(sapply(1:6, fit_rmse), 1)')}
  {note('種を変えると RMSE が <strong>約 24〜28.5</strong> の間で動きます。<strong>「小数第1位の差」で優劣を決めない</strong>こと。1回の分け方の結果には、偶然のゆれが含まれています（交差検証で対処：「過学習と交差検証」の回）。')}
  {practice("p-ml2-u2", "70% / 30% に分ける", "<code>set.seed(7)</code> のあと、<code>apt</code> を <strong>70% 訓練・30% テスト</strong>に分けて、それぞれの行数を表示してください。",
             ["set.seed", "sample", "nrow"], 'set.seed(7)\nidx <- sample(nrow(apt), size = 0.7 * nrow(apt))\ntrain <- apt[idx, ]\ntest  <- apt[-idx, ]\nc(train = nrow(train), test = nrow(test))', "400 行の 70% は 280 行、残り 120 行。<code>size</code> に小数が来ても sample() は切り捨てて扱う（0.7 × 400 = 280 ちょうど）。")}
'''))
    b.append(unit(3, "層化：クラスの比率を保つ", "陽性が少ないデータで特に大事", f'''
  <p>分類では、<strong>クラスの比率</strong>が訓練とテストで同じになるよう分けると安心です。これを<strong>層化抽出</strong>（<code>stratify=y</code>）と呼びます。陽性が少ないデータでは、ふつうの無作為な分け方だと、<strong>テストに陽性が 1 つも入らない</strong>ことがあります。</p>
  {P.R('y <- c(rep(1, 5), rep(0, 95))          # 100 cases, only 5 positives (5%)\nset.seed(10)\nmean(replicate(5000, sum(y[sample(100, 20)]) == 0))   # share of random 20% test sets with NO positive')}
  <p>約 3 割の分け方で、テストに陽性がゼロになります（陽性がないと Recall が計算できません）。層化では、<strong>クラスごとに</strong>同じ割合で選びます。</p>
  {P.R('strat_test <- function(y, frac = 0.2) unlist(lapply(split(seq_along(y), y), function(i) sample(i, size = round(frac * length(i)))))\nset.seed(10)\ni <- strat_test(y)\ntable(y[i])                                  # the test set keeps 1 positive and 19 negatives')}
'''))
    b.append(unit(4, "データ漏れ（data leakage）", "「良すぎる成績」を疑う", f'''
  <p><strong>データ漏れ</strong>は、評価の時点では手に入らないはずの情報が、学習に混ざることです。成績が<strong>不自然に良くなる</strong>のが特徴で、本番では全く使えないモデルになります。代表的な例が、<strong>答えから作った列</strong>を特徴にしてしまうことです。</p>
  {P.R(APT + '\napt$price_per_area <- apt$price / apt$area          # built FROM the answer (price)!\nm <- lm(price ~ area + price_per_area, data = apt[idx, ])\nt <- apt[-idx, ]\nleak <- 1 - sum((t$price - predict(m, t))^2) / sum((t$price - mean(t$price))^2)\nhonest <- lm(price ~ area + rooms + age, data = apt[idx, ])\nh <- 1 - sum((t$price - predict(honest, t))^2) / sum((t$price - mean(t$price))^2)\nround(c(R2_with_leak = leak, R2_honest = h), 3)')}
  <p>漏れのあるモデルは R² が <strong>0.95</strong>、漏れのない正直なモデルは <strong>0.83</strong> です。<strong>価格から作った「面積あたり価格」</strong>を使えば、価格が分かるのは当然です。新しい物件では、価格は予測したい未知の値なので、この列は存在しません。実力以上に良く見えるだけで、本番では使えません。</p>
  {table(["漏れの例", "対策"], [["答え（目的変数）から作った列を特徴に使う", "特徴は「予測する時点で分かる情報」だけにする"], ["テストデータの平均や SD で標準化する", "訓練データだけで計算して、テストに適用する"], ["分ける前に、全データで欠損を補う", "分けてから、訓練データの中央値で補う"], ["同じ人・物件の行が訓練とテストに両方ある", "個人やグループ単位で分ける"]])}
'''))
    b.append(teal('➡️ <strong>次の回へ：</strong>分けたデータで、実際にモデルを作ります。<a href="ml_regression.html">回帰：係数・R²・RMSE・残差</a>へ。'))
    q = [('Why is the model evaluated on a separate test set?', 'To estimate performance on new data', ['To make the training set larger', 'To remove the need for a model', 'To lower the error on the training data'], 'Training error is optimistic; the test set shows how the model generalizes.'),
         ('What does set.seed() (random_state in Python) make possible?', 'Reproducing the same split', ['Choosing a better split', 'Removing all random variation', 'Increasing the test set size'], 'The seed fixes the random numbers so the split and results can be repeated.'),
         ('When is stratified splitting especially useful?', 'When one class is rare', ['When all columns are numeric', 'When there are no missing values', 'When the data are already sorted'], 'Stratifying keeps the class proportions the same in train and test.'),
         ('A model scores R² = 0.999 on test data. What should you check first?', 'Whether a column leaks y', ['Whether to collect more data', 'Whether the seed was too small', 'Whether the test set is too big'], 'Unusually high scores often come from data leakage.'),
         ('Which is an example of data leakage?', 'Scaling with the mean of all rows', ['Splitting data with a fixed seed', 'Dropping rows with missing values', 'Printing summary() of the train set'], 'The test rows influence the mean, so test information leaks into training.'),
         ('A 1-nearest-neighbour model has near-zero training error but large test error. This is...', 'Overfitting', ['Underfitting', 'Stratification', 'Standardization'], 'The model memorized the training points and fails on new ones.')]
    return L, "\n".join(b), q

# =============================================================== 3. regression
def ml_regression(P):
    L = dict(slug="ml_regression", mod=MOD, icon="📈", title="回帰：係数・R²・RMSE・残差",
             tag="ML Prep · Regression — lm(), Coefficients, R², RMSE &amp; MAE, Residuals",
             lead="数値を予測する<strong>線形回帰</strong>を、ML の目で見直します。<strong>係数の意味</strong>、<strong>R²・RMSE・MAE</strong>、<strong>基準モデルとの比較</strong>、<strong>残差のグラフ</strong>、係数を比べるための<strong>標準化</strong>。550 の M6 の復習です。",
             video="670 準備 · 550 M6（相関・回帰）の復習",
             unav=["① lm と係数", "② R²・RMSE・MAE", "③ 残差を見る", "④ 標準化して比べる"],
             terms=[("linear regression", "線形回帰", "y を x の1次式で予測する。最小二乗で当てはめる。"),
                    ("coefficient", "係数", "他を固定して x が 1 増えたときの y の変化。"),
                    ("intercept", "切片", "x がすべて 0 のときの予測値。"),
                    ("residual", "残差", "実測値 − 予測値。"),
                    ("R²", "決定係数", "ばらつきのうち、モデルで説明できた割合。"),
                    ("RMSE", "二乗平均平方根誤差", "予測の平均的なズレ。y と同じ単位。"),
                    ("MAE", "平均絶対誤差", "ズレの絶対値の平均。外れ値に強い。"),
                    ("baseline", "基準モデル", "平均を答えるだけのモデル。これに勝てないと意味がない。")],
             tip="<strong>R² も RMSE も、必ずテストデータで</strong>見る。「基準モデル（平均を答える）」より良くなって初めて価値がある。")
    b = [teal(CS)]
    b.append(unit(1, "lm() と係数の意味", "「他を固定して、x が 1 増えると」", f'''
  <p>まず、前の回と同じ<strong>架空のマンション価格データ</strong>（400 件、価格の単位は千ドル）を作ります。価格 = 40 + 2.2×面積 + 12×部屋数 − 0.8×築年数 + 誤差、という関係をわざと入れてあります。</p>
  {P.R(APT + '\nfit <- lm(price ~ area + rooms + age, data = train)\nround(coef(fit), 2)')}
  <p>係数の読み方は、「<strong>他の変数を同じにして、その変数が 1 増えたとき、価格がどれだけ変わるか</strong>」です。面積が 1 m² 増えると価格は約 2.2（千ドル）上がり、築年数が 1 年増えると約 0.8 下がります。真の値（2.2、12、−0.8）に近い値が出ています。</p>
  {P.R('round(summary(fit)$coefficients, 3)')}
  {note('<code>Std. Error</code> は係数の「ゆらぎの幅」、<code>Pr(&gt;|t|)</code> はその係数が 0 かもしれない確率の目安です。ML では、これらの数字より、<strong>テストデータでの誤差</strong>の方を重視します。')}
'''))
    b.append(unit(2, "R²・RMSE・MAE と基準モデル", "テストデータで、基準と比べて評価する", f'''
  <p>予測の良さは、<strong>テストデータ</strong>で測ります。3 つの指標を、式から自分で計算してみましょう。</p>
  {P.R('pred <- predict(fit, newdata = test)\nres  <- test$price - pred\nrmse <- sqrt(mean(res^2))                  # typical size of the error (same unit as price)\nmae  <- mean(abs(res))                     # less sensitive to big errors\nr2   <- 1 - sum(res^2) / sum((test$price - mean(test$price))^2)\nround(c(RMSE = rmse, MAE = mae, R2 = r2), 3)')}
  {table(["指標", "意味", "目安"], [["RMSE", "予測の平均的なズレ（大きな誤差を重く見る）", "小さいほど良い。y の単位で読める"], ["MAE", "ズレの絶対値の平均", "小さいほど良い。外れ値に強い"], ["R²", "説明できたばらつきの割合", "1 に近いほど良い。テストで見る"]])}
  <p>RMSE が「良いか悪いか」は、<strong>基準モデル</strong>と比べて決めます。基準モデルは、「いつも<strong>訓練データの平均</strong>を答える」モデルです。</p>
  {P.R('base_rmse <- sqrt(mean((test$price - mean(train$price))^2))\nround(c(model = rmse, baseline = base_rmse), 1)')}
  {warn('基準モデルの RMSE（約 70）に対して、モデルは約 28.5。<strong>基準に勝てなければ、モデルを作る意味がありません</strong>。まず基準を計算する習慣をつけましょう。')}
  {practice("p-ml3-u2", "テストの MAE", "<code>test</code> に対する <code>fit</code> の予測を作り、<strong>MAE</strong>（絶対誤差の平均）を小数 2 桁で求めてください。",
             ["predict", "abs", "mean"], 'pred <- predict(fit, newdata = test)\nround(mean(abs(test$price - pred)), 2)', "<code>predict(fit, newdata = test)</code> がテストの予測。残差の絶対値の平均が MAE。")}
'''))
    b.append(unit(3, "残差を見る", "数字だけでなく、絵で確認する", f'''
  <p><strong>残差</strong>（実測 − 予測）を予測値に対してプロットすると、モデルの弱点が見えます。良いモデルの残差は、<strong>0 のまわりに、パターンなくばらつきます</strong>。</p>
  {P.R('par(mfrow = c(1, 2))\nplot(fitted(fit), resid(fit), pch = 16, col = "#4471B8", xlab = "Fitted", ylab = "Residual", main = "Good fit")\nabline(h = 0, col = "red", lty = 2)\n# a curved relationship fitted with a straight line\nset.seed(5); x <- runif(200, -3, 3); y <- x^2 + rnorm(200)\nbad <- lm(y ~ x)\nplot(fitted(bad), resid(bad), pch = 16, col = "#B84848", xlab = "Fitted", ylab = "Residual", main = "Curved pattern")\nabline(h = 0, col = "red", lty = 2)', plot=True, w=760, h=320)}
  <p>右の図の残差は<strong>U 字</strong>に並んでいます。真の関係は曲線（x²）なのに、直線を当てはめたため、モデルが捉えられなかった部分が残差に残ったのです。このようなパターンが見えたら、<strong>x² の項を足す</strong>、または<strong>木のモデル</strong>を試します。</p>
  {table(["残差のパターン", "意味", "対策"], [["0 のまわりにランダム", "良い", "—"], ["U 字・曲線", "非線形の関係を取りこぼし", "x² を足す、木モデル"], ["右に行くほど広がる", "大きい値ほど誤差が大きい", "y を対数変換"]])}
'''))
    b.append(unit(4, "標準化して係数を比べる", "どの特徴が一番効いているか", f'''
  <p>係数は単位に依存します（面積は m²、築年数は年）。<strong>「どの特徴が一番効くか」を比べるには、先に標準化</strong>します。標準化した列の係数は、「x が <strong>SD 1 つ分</strong>増えたときの y の変化」になります。</p>
  {P.R('train_s <- as.data.frame(scale(train))      # every column: mean 0, SD 1\nfit_s <- lm(price ~ area + rooms + age, data = train_s)\nround(coef(fit_s)[-1], 2)')}
  <p>面積（約 0.91）が圧倒的に強く、築年数（約 −0.19）と部屋数（約 0.17）は同じくらいです。元の係数だけを見ると「部屋数 11.6 が大きい」と錯覚しやすいのですが、<strong>部屋数は値の幅が小さい</strong>ので、実際の影響は面積よりずっと小さくなります。</p>
  {warn('特徴同士が強く相関していると（例：面積と部屋数）、係数が不安定になります（<strong>多重共線性</strong>）。係数の「大きさ」を解釈するときは、特徴間の相関も <code>cor()</code> で確認しましょう。')}
'''))
    b.append(teal('➡️ <strong>次へ：</strong>分類モデルとその評価は <a href="ml_classification.html">分類：ロジスティック回帰・混同行列・ROC</a> で学びます。'))
    q = [("In a linear regression, a coefficient of 2.2 for 'area' means...", 'Others fixed, +1 area adds 2.2 to y', ['Area explains 2.2% of the variation in y', 'Area and y have a correlation of 2.2', 'The average error of the model is 2.2'], 'A coefficient is the change in y per one-unit change in x, other variables held constant.'),
         ('Which pair of measures should be computed on the test data?', 'RMSE and R²', ['Intercept and slope', 'Seed and split size', 'Mean and median of x'], 'Performance must be judged on data the model has not seen.'),
         ('The baseline model always predicts...', "The training target's mean", ['The median of the test target', 'Zero for every row', 'The largest observed value'], 'If a model cannot beat this simple baseline it adds no value.'),
         ("The model's RMSE is 28 and the baseline RMSE is 70. What does this show?", 'The model beats the baseline', ['The model is overfitting badly', 'The baseline is better here', 'The test set is too small'], 'A much smaller error than the baseline means the model has learned something.'),
         ('A residual plot shows a clear U-shaped curve. What does it suggest?', 'A curve was left unmodeled', ['The model fits perfectly', 'There are no outliers left', 'The data need more rows'], 'Residuals should look random; a curve means structure is left over.'),
         ('Why standardize features before comparing regression coefficients?', 'So they are on the same scale', ['So the intercept becomes zero', 'So the residuals become smaller', 'So the data are split evenly'], 'Standardized coefficients show the effect of one SD change in each feature.')]
    return L, "\n".join(b), q

LESSONS = [ml_explore, ml_split, ml_regression]
