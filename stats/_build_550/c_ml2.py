"""670 ML 統計復習 (2/2): classification, overfitting & CV, uncertainty."""
from lib550 import *
from c_ml1 import MOD, APT, CS

TI = '''d  <- as.data.frame(Titanic)                       # R's built-in Titanic table (2,201 people)
ti <- d[rep(seq_len(nrow(d)), d$Freq), c("Class", "Sex", "Age", "Survived")]
rownames(ti) <- NULL
ti$Survived <- as.integer(ti$Survived == "Yes")
set.seed(1)
idx <- sample(nrow(ti), size = 0.8 * nrow(ti))
tr  <- ti[idx, ]
te  <- ti[-idx, ]
m   <- glm(Survived ~ Class + Sex + Age, data = tr, family = binomial)
p   <- predict(m, newdata = te, type = "response")   # probability of survival
pred <- as.integer(p >= 0.5)'''
AUC = 'auc <- function(y, s) { r <- rank(s); n1 <- sum(y == 1); n0 <- sum(y == 0); (sum(r[y == 1]) - n1 * (n1 + 1) / 2) / (n1 * n0) }'

# =============================================================== 4. classification
def ml_classification(P):
    L = dict(slug="ml_classification", mod=MOD, icon="🎯", title="分類：ロジスティック回帰・混同行列・Precision/Recall・ROC",
             tag="ML Prep · Classification — Probability &amp; Odds, glm(), Confusion Matrix, Precision/Recall, ROC &amp; AUC",
             lead="Yes/No を予測する<strong>分類</strong>の評価を、タイタニック号のデータで学びます。<strong>確率とオッズ</strong>、<code>glm()</code>の<strong>ロジスティック回帰</strong>、<strong>混同行列</strong>、<strong>Precision・Recall・F1</strong>、<strong>しきい値と ROC・AUC</strong>。",
             video="670 準備 · 550 M3（確率・オッズ）／M6（ロジスティック）の復習",
             unav=["① ロジスティック回帰", "② 混同行列", "③ Precision / Recall", "④ しきい値・ROC・AUC"],
             terms=[("logistic regression", "ロジスティック回帰", "確率(0〜1)を出す分類モデル。"),
                    ("odds ratio", "オッズ比", "係数を exp() したもの。1 より大きいと確率が上がる。"),
                    ("confusion matrix", "混同行列", "予測と実際のクロス集計 (TN, FP, FN, TP)。"),
                    ("precision", "適合率", "「陽性」と言った中の的中率 TP/(TP+FP)。"),
                    ("recall", "再現率", "本当の陽性を見つけた割合 TP/(TP+FN)。"),
                    ("F1", "F1 値", "Precision と Recall の調和平均。"),
                    ("threshold", "しきい値", "確率をクラスに変える境目（既定 0.5）。"),
                    ("ROC / AUC", "ROC曲線・AUC", "しきい値を動かした性能の曲線と、その下の面積。")],
             tip="<strong>正解率だけで判断しない</strong>。陽性が少ないデータでは、全部「陰性」と答えても高得点になる。")
    b = [teal(CS)]
    b.append(unit(1, "ロジスティック回帰：確率とオッズ", "glm(..., family = binomial)", f'''
  <p>R に入っている<strong>タイタニック号のデータ</strong>（2,201 人）で、「<strong>生き残ったか（1）／亡くなったか（0）</strong>」を、客室クラス・性別・年齢層から予測します。回帰が数値を出すのに対し、<strong>ロジスティック回帰は「確率」を出します</strong>。</p>
  {P.R(TI + '\nmean(ti$Survived)                        # overall survival rate\nround(head(p, 6), 3)                     # predicted probabilities')}
  <p>係数は<strong>対数オッズ</strong>で出るので、<code>exp()</code> で<strong>オッズ比</strong>に直すと読みやすくなります。</p>
  {P.R('round(exp(coef(m)), 2)')}
  <p>「Female」のオッズ比は約 11。<strong>女性は男性より、生き残るオッズが約 11 倍</strong>（他の条件が同じとき）という意味です。「Class3rd」は 1 より小さいので、1 等（基準）より生き残りにくいことを示します。</p>
  {note('📐 <strong>確率とオッズ</strong>：確率 p のオッズ = p ÷ (1 − p)。確率 0.5 ↔ オッズ 1、確率 0.75 ↔ オッズ 3。<strong>オッズ比が 1</strong> なら影響なし、1 より大きければ増える、小さければ減る。')}
'''))
    b.append(unit(2, "混同行列", "予測と実際を 2×2 に並べる", f'''
  <p>確率に<strong>しきい値</strong>（既定は 0.5）をかけて、「生存／死亡」の予測に変えます。予測と実際のクロス集計が<strong>混同行列</strong>です。</p>
  {P.R('table(Truth = te$Survived, Predicted = pred)')}
  {table(["", "予測：死亡 (0)", "予測：生存 (1)"], [["実際：死亡 (0)", "TN（正しく陰性）", "FP（誤って陽性）"], ["実際：生存 (1)", "FN（見逃し）", "TP（正しく陽性）"]])}
  <p>行が「実際」、列が「予測」です。<strong>FP</strong> は「生存と予測したが実は死亡」、<strong>FN</strong> は「死亡と予測したが実は生存」。この 4 つの数字から、すべての指標が計算できます。</p>
  {P.R('tab <- table(factor(te$Survived, levels = 0:1), factor(pred, levels = 0:1))\nTN <- tab[1, 1]; FP <- tab[1, 2]; FN <- tab[2, 1]; TP <- tab[2, 2]\nc(TN = TN, FP = FP, FN = FN, TP = TP)\naccuracy <- (TP + TN) / sum(tab)\naccuracy')}
'''))
    b.append(unit(3, "Precision・Recall・F1 と偏ったデータ", "正解率だけでは足りない", f'''
  <p>正解率（accuracy）は、<strong>全体のうち当たった割合</strong>ですが、クラスが偏っていると役に立ちません。Precision と Recall を使います。</p>
  {P.R('precision <- TP / (TP + FP)      # of those I called "survived", how many really survived?\nrecall    <- TP / (TP + FN)      # of those who really survived, how many did I find?\nf1 <- 2 * precision * recall / (precision + recall)\nround(c(accuracy = accuracy, precision = precision, recall = recall, F1 = f1), 3)')}
  <p>このデータでは Precision が高く（約 0.74）、Recall は低め（約 0.55）です。「生存」と言うときは慎重ですが、<strong>生存者の半分近くを見逃している</strong>ということです。</p>
  <p>偏りが大きいデータでは、正解率が<strong>だまし</strong>になります。陽性が 3% しかない稀なイベント（1,000 件中 30 件）を考えます。</p>
  {P.R('y <- c(rep(1, 30), rep(0, 970))             # 3% positives\nalways_no <- rep(0, 1000)                # a model that never predicts a positive\nc(accuracy = mean(always_no == y), recall = sum(always_no == 1 & y == 1) / sum(y == 1))')}
  {warn('「全員、陰性」と答えるだけで<strong>正解率 97%</strong>、でも<strong>Recall は 0</strong>（陽性を 1 つも見つけられない）。不正検知や病気の検査のような<strong>偏ったデータでは、正解率は信用できません</strong>。')}
  {table(["こういうとき", "重視する指標"], [["見逃しが怖い（病気・不正）", "Recall"], ["誤って陽性にしたくない（迷惑メール判定）", "Precision"], ["両方のバランス", "F1"]])}
  {practice("p-ml4-u3", "Precision と Recall を計算", "混同行列が <code>TP = 40, FP = 10, FN = 20, TN = 130</code> のとき、<strong>Precision</strong> と <strong>Recall</strong> を求めてください。",
             ["TP", "FP", "FN"], 'TP <- 40; FP <- 10; FN <- 20; TN <- 130\nc(precision = TP / (TP + FP), recall = TP / (TP + FN))', "Precision = 40/50 = 0.8、Recall = 40/60 ≈ 0.667。")}
'''))
    b.append(unit(4, "しきい値・ROC・AUC", "確率を動かして、全体の性能を見る", f'''
  <p>しきい値を 0.5 から動かすと、Precision と Recall は<strong>シーソー</strong>のように動きます（片方を上げると、もう片方が下がる）。</p>
  {P.R('score <- function(th) {\n  pr <- as.integer(p >= th)\n  TP <- sum(pr == 1 & te$Survived == 1); FP <- sum(pr == 1 & te$Survived == 0); FN <- sum(pr == 0 & te$Survived == 1)\n  c(threshold = th, precision = TP / (TP + FP), recall = TP / (TP + FN))\n}\nround(t(sapply(c(0.3, 0.5, 0.7), score)), 3)')}
  <p>しきい値を<strong>下げる</strong>と、陽性と言いやすくなり、Recall が上がって Precision が下がります。<strong>ROC 曲線</strong>は、しきい値を全部動かしたときの「<strong>偽陽性率（横軸）</strong>」と「<strong>真陽性率 = Recall（縦軸）</strong>」の軌跡で、その下の面積が <strong>AUC</strong> です。</p>
  {P.R(AUC + '\nths <- sort(unique(c(0, p, 1)), decreasing = TRUE)\nroc <- t(sapply(ths, function(th) c(fpr = mean(p[te$Survived == 0] >= th), tpr = mean(p[te$Survived == 1] >= th))))\nplot(roc[, 1], roc[, 2], type = "s", lwd = 2, col = "#4471B8", xlab = "False positive rate", ylab = "True positive rate (recall)", main = "ROC curve")\nabline(0, 1, lty = 2, col = "gray50")\nround(auc(te$Survived, p), 3)', plot=True, h=360)}
  {table(["AUC", "読み方"], [["0.5", "当てずっぽう（対角線）"], ["0.7〜0.8", "まずまず"], ["0.9 以上", "とても良い"], ["1.0", "完璧（本当に完璧ならデータ漏れも疑う）"]])}
  <p>AUC は「<strong>ランダムに選んだ陽性と陰性のペアで、陽性の方に高い確率をつけられる割合</strong>」です。しきい値に依存しないので、<strong>モデル同士の比較</strong>に向いています。</p>
'''))
    b.append(teal('➡️ <strong>次の回へ：</strong>評価を信じてよいかは、<strong>過学習</strong>を見て初めて分かります。<a href="ml_overfit.html">過学習と交差検証</a>へ。'))
    q = [('The odds ratio of a variable in logistic regression is 11. What does it mean?', 'The odds are 11 times as high', ['The probability rises by exactly 11%', 'The variable explains 11% of the variance', 'The accuracy of the model is 11 percent'], 'exp(coefficient) is the factor by which the odds are multiplied.'),
         ('In a confusion matrix, what is a false negative (FN)?', 'A real positive predicted as negative', ['A real negative predicted as positive', 'A real positive predicted as positive', 'A real negative predicted as negative'], 'FN means a positive case that the model missed.'),
         ('Precision is defined as...', 'TP / (TP + FP)', ['TP / (TP + FN)', '(TP + TN) / all', 'TN / (TN + FP)'], 'Of the cases called positive, how many were truly positive.'),
         ('A disease screening test must not miss sick patients. Which metric matters most?', 'Recall', ['Precision', 'Accuracy', 'Log loss'], 'Recall = TP / (TP + FN), so it penalizes missed positives.'),
         ("A model predicts 'negative' for everyone in data with 3% positives. Its accuracy is about...", '97%, with a recall of 0', ['3%, with a recall of 1', '50%, with a recall of 0', '97%, with a recall of 1'], 'Accuracy is misleading with imbalanced classes.'),
         ('An AUC of 0.5 means the model is...', 'No better than a coin flip', ['Perfect', 'Always predicting positive', 'Using the wrong threshold'], 'The ROC curve lies on the diagonal when the model cannot separate the classes.')]
    return L, "\n".join(b), q

# =============================================================== 5. overfit & CV
def ml_overfit(P):
    L = dict(slug="ml_overfit", mod=MOD, icon="🌀", title="過学習と交差検証：次数・バイアス/バリアンス・正則化",
             tag="ML Prep · Overfitting — Model Complexity, Train vs Test Error, Cross-Validation, Regularization",
             lead="ML の最重要テーマ、<strong>過学習</strong>。モデルを複雑にすると、<strong>訓練の誤差は下がり続けるのに、テストの誤差は下がってから上がる</strong>ことを、多項式回帰で確かめます。そして<strong>交差検証</strong>で複雑さを選び、<strong>正則化</strong>の考え方に触れます。",
             video="670 準備 · 550 M6（回帰）の応用",
             unav=["① 複雑さを上げると", "② 訓練 vs テスト", "③ 交差検証", "④ バイアス・バリアンス・正則化"],
             terms=[("overfitting", "過学習", "訓練データに合いすぎ、新データで悪化。"),
                    ("underfitting", "学習不足", "単純すぎて、訓練でも悪い。"),
                    ("model complexity", "モデルの複雑さ", "多項式の次数・木の深さなど。"),
                    ("cross-validation (CV)", "交差検証", "データを k 分割し、順に1つをテストにして平均する。"),
                    ("bias", "バイアス", "モデルが単純すぎる偏り（学習不足側）。"),
                    ("variance", "バリアンス", "データが変わるとモデルが大きく揺れる（過学習側）。"),
                    ("regularization", "正則化", "係数を小さく抑えて、複雑さにペナルティを課す。"),
                    ("Ridge / Lasso", "リッジ／ラッソ", "L2 / L1 の正則化。Lasso は係数を 0 にもする。")],
             tip="<strong>訓練の誤差だけ</strong>見て満足しない。<strong>テスト（または CV）の誤差が最小</strong>になる複雑さを選ぶ。")
    b = [teal(CS)]
    b.append(unit(1, "モデルを複雑にするとどうなるか", "多項式の次数 1 と 10", f'''
  <p>sin 波に<strong>ノイズ</strong>を加えた架空のデータ（60 点）を、訓練 25 点とテスト 35 点に分けます。<code>lm(y ~ poly(x, d))</code> の<strong>次数 d</strong>が大きいほど、曲線は複雑に曲がれます。</p>
  {P.R('set.seed(15)\nx <- runif(60, 0, 10); y <- sin(x) + rnorm(60, 0, 0.5)\ndat <- data.frame(x, y)\ntrain <- dat[1:25, ]; test <- dat[26:60, ]\nrmse <- function(a, b) sqrt(mean((a - b)^2))\nfit1  <- lm(y ~ poly(x, 1),  data = train)\nfit10 <- lm(y ~ poly(x, 10), data = train)\nxs <- data.frame(x = seq(0, 10, length.out = 300))\nplot(train$x, train$y, pch = 16, col = "#4471B8", xlab = "x", ylab = "y", ylim = c(-2.5, 3.2))\npoints(test$x, test$y, pch = 17, col = "#B84848")\nlines(xs$x, predict(fit1, xs), lwd = 2, col = "gray40")\nlines(xs$x, predict(fit10, xs), lwd = 2, col = "#3C8A5A")\nlegend("top", c("train", "test", "degree 1", "degree 10"), ncol = 4, pch = c(16, 17, NA, NA), lty = c(NA, NA, 1, 1), col = c("#4471B8", "#B84848", "gray40", "#3C8A5A"), bty = "n")', plot=True, h=360)}
  <p>灰色の<strong>直線（次数 1）</strong>は単純すぎて、波を捉えられません（学習不足）。緑の<strong>次数 10</strong> は訓練の点（青）に沿ってうねりますが、端では不自然に大きく振れています（過学習）。</p>
'''))
    b.append(unit(2, "訓練の誤差とテストの誤差", "テストの誤差は「U 字」になる", f'''
  <p>次数を 1 から 10 まで変えて、訓練とテストの RMSE を比べます。</p>
  {P.R('deg <- 1:10\nerr <- t(sapply(deg, function(d) {\n  f <- lm(y ~ poly(x, d), data = train)\n  c(train = rmse(train$y, predict(f, train)), test = rmse(test$y, predict(f, test)))\n}))\nround(cbind(degree = deg, err), 3)[c(1, 3, 5, 6, 8, 10), ]\nmatplot(deg, err, type = "b", pch = 16, lty = 1, col = c("#4471B8", "#B84848"), xlab = "Polynomial degree", ylab = "RMSE")\nlegend("topright", c("train", "test"), col = c("#4471B8", "#B84848"), lty = 1, pch = 16, bty = "n")', plot=True, h=340)}
  <p><strong>訓練誤差</strong>（青）は次数を上げるほど<strong>下がり続けます</strong>。一方、<strong>テスト誤差</strong>（赤）は<strong>途中まで下がり、あとで上がります</strong>。この U 字の底が、ちょうどよい複雑さです。</p>
  {table(["状態", "訓練誤差", "テスト誤差", "対策"], [["学習不足 (high bias)", "大きい", "大きい", "モデルを複雑に・特徴を増やす"], ["ちょうどよい", "小さい", "小さい", "—"], ["過学習 (high variance)", "とても小さい", "大きい", "データを増やす・単純に・正則化"]])}
'''))
    b.append(unit(3, "交差検証（k-fold CV）", "1回の分け方に頼らない", f'''
  <p>テストが 35 点しかないと、<strong>偶然のゆれ</strong>が大きく、次数の選び方も不安定です。<strong>交差検証</strong>は、データを k 個（ここでは 5 個）に分け、<strong>1 つをテスト・残りを訓練</strong>にする作業を k 回くり返して、<strong>誤差を平均</strong>します。</p>
  {P.R('set.seed(2)\nfolds <- sample(rep(1:5, length.out = nrow(train)))      # fold id for each training row\ncv_rmse <- function(d) mean(sapply(1:5, function(k) {\n  f <- lm(y ~ poly(x, d), data = train[folds != k, ])\n  rmse(train$y[folds == k], predict(f, train[folds == k, ]))\n}))\ncv <- sapply(1:8, cv_rmse)\nround(cv, 3)\nwhich.min(cv)                                  # degree with the lowest CV error')}
  <p>テストデータに触れずに、<strong>訓練データの中だけで</strong>最適な次数を選べました。選んだら、最後にテストデータで<strong>1回だけ</strong>確認します。Python では <code>cross_val_score(model, X, y, cv=5)</code> が、この作業を 1 行でやります。</p>
  {P.R('best <- which.min(cv)\nfinal <- lm(y ~ poly(x, best), data = train)\nround(c(degree = best, test_rmse = rmse(test$y, predict(final, test))), 3)')}
  {practice("p-ml5-u3", "k = 4 の分割", "<code>train</code>（40 行）を <strong>4 つのフォールド</strong>に無作為に分け（<code>set.seed(9)</code>）、<code>table()</code> で各フォールドの行数を表示してください。",
             ["set.seed", "sample", "rep", "table"], 'set.seed(9)\nfolds <- sample(rep(1:4, length.out = nrow(train)))\ntable(folds)', "<code>rep(1:4, length.out = 40)</code> で 1〜4 を 10 回ずつ並べ、<code>sample()</code> でシャッフルする。各フォールドは 10 行。")}
'''))
    b.append(unit(4, "バイアスとバリアンス、正則化", "複雑さにブレーキをかける", f'''
  <p>誤差は 2 つの原因に分けて考えられます。<strong>バイアス</strong>は「モデルが単純すぎて、真の形を捉えられない」偏り、<strong>バリアンス</strong>は「訓練データが変わると、モデルが大きく変わる」ゆらぎです。複雑にするとバイアスは下がり、バリアンスは上がります。このバランスを探すのが ML の基本です。</p>
  <p><strong>正則化</strong>は、モデルを複雑にしすぎないために、<strong>係数が大きくなることにペナルティ</strong>を課します（<strong>Ridge＝L2</strong>、<strong>Lasso＝L1</strong>）。ペナルティの強さ <code>λ</code>（Python では <code>alpha</code>）を上げると、係数が 0 に向かって縮みます。</p>
  {P.R(APT + '\ntrain_s <- as.data.frame(scale(train))\nlam <- c(0, 10, 100, 1000)\nr <- MASS::lm.ridge(price ~ area + rooms + age, data = train_s, lambda = lam)\nround(t(coef(r)), 3)')}
  <p>λ を大きくするほど、3 つの係数が<strong>0 に近づいて</strong>います。係数が小さいモデルは、データのゆらぎに強い（バリアンスが低い）一方で、バイアスが増えます。適切な λ は、<strong>交差検証</strong>で選びます。</p>
  {table(["", "Ridge (L2)", "Lasso (L1)"], [["ペナルティ", "係数の二乗の和", "係数の絶対値の和"], ["効果", "全部の係数を小さくする", "不要な特徴の係数を 0 にする（特徴選択）"], ["Python", "<code>Ridge(alpha=...)</code>", "<code>Lasso(alpha=...)</code>"]])}
'''))
    b.append(teal('➡️ <strong>最後の回へ：</strong>評価の数字には必ず「ゆれ」があります。<a href="ml_uncertainty.html">不確かさ：誤差の幅・ブートストラップ・モデル比較・木・因果</a>へ。'))
    q = [('As model complexity increases, the training error usually...', 'Keeps decreasing', ['Keeps increasing', 'Stays almost constant', 'First rises, then falls'], 'A more flexible model can fit the training data ever more closely.'),
         ('The test error is high while the training error is very low. This is...', 'Overfitting', ['Underfitting', 'Stratification', 'Standardization'], 'The model memorized the training set and does not generalize.'),
         ('What does 5-fold cross-validation do?', 'Tests on each fold in turn', ['Uses five models at once', 'Repeats one split five times', 'Adds five new features'], 'Each fold is used once for testing; the five errors are averaged.'),
         ('A key benefit of cross-validation over one train/test split is...', 'A more stable error estimate', ['It needs no training data at all', 'It removes all random variation', 'It always gives a lower error'], 'Averaging over folds reduces the luck of a single split.'),
         ('Increasing the regularization strength (alpha or lambda) makes coefficients...', 'Shrink toward zero', ['Grow larger', 'Switch signs randomly', 'Stay exactly the same'], 'The penalty on large coefficients forces them to be smaller.'),
         ('High variance means that the model...', 'Changes a lot with the sample', ['Is too simple to learn the pattern', 'Always predicts the training mean', 'Has a perfect score on test data'], 'A high-variance model is sensitive to the particular training sample.')]
    return L, "\n".join(b), q

# =============================================================== 6. uncertainty
def ml_uncertainty(P):
    L = dict(slug="ml_uncertainty", mod=MOD, icon="🎲", title="不確かさ：誤差の幅・ブートストラップ・モデル比較・木・因果",
             tag="ML Prep · Uncertainty — Confidence Intervals for Errors, Bootstrap, Comparing Models, Gini Impurity, Correlation vs Causation",
             lead="「モデル A の RMSE は 24.9、B は 25.3 だから A の勝ち」と言えるでしょうか。評価の数字には<strong>必ずゆれ</strong>があります。<strong>誤差の信頼区間</strong>、<strong>ブートストラップ</strong>、<strong>交差検証での比較</strong>、決定木の<strong>Gini 不純度</strong>、<strong>相関と因果</strong>を学びます。",
             video="670 準備 · 550 M4（SE・信頼区間）の応用",
             unav=["① 誤差の信頼区間", "② ブートストラップ", "③ モデル比較", "④ Gini と平均化", "⑤ 相関 ≠ 因果"],
             terms=[("standard error", "標準誤差", "平均の推定のゆれ。SD ÷ √n。"),
                    ("confidence interval", "信頼区間", "推定値の「偶然の幅」。"),
                    ("bootstrap", "ブートストラップ", "データから復元抽出をくり返して、ゆれを調べる。"),
                    ("paired difference", "対応のある差", "同じフォールドでの 2 モデルの成績の差。"),
                    ("Gini impurity", "Gini 不純度", "1 − Σ(割合²)。0 に近いほど純粋。"),
                    ("bagging", "バギング", "データを復元抽出で変えて木を多数作り、平均する。"),
                    ("confounder", "交絡因子", "2 つの変数の両方に影響する第三の変数。"),
                    ("spurious correlation", "見かけの相関", "原因でないのに相関が出ること。")],
             tip="<strong>差が「ゆれ」より小さければ、同じ</strong>と考える。1 回のテストの小数点以下の差では、優劣を決めない。")
    b = [teal(CS)]
    b.append(unit(1, "誤差の信頼区間", "RMSE にも「偶然の幅」がある", f'''
  <p>550 の M4 で、<strong>標本平均には信頼区間がある</strong>と学びました。<strong>テストでの誤差</strong>も同じです。テスト 1 件ごとの二乗誤差の<strong>平均</strong>（= MSE）には、<strong>標準誤差</strong>があり、信頼区間が作れます。</p>
  {P.R(APT + '\nfit <- lm(price ~ area + rooms + age, data = train)\nsq_err <- (test$price - predict(fit, test))^2         # squared error for each test row\nmse_ci <- t.test(sq_err)$conf.int\nround(c(RMSE = sqrt(mean(sq_err)), lower = sqrt(mse_ci[1]), upper = sqrt(mse_ci[2])), 2)')}
  <p>RMSE は約 28.5 ですが、<strong>「約 24〜32 のどこか」</strong>と幅で見るのが正直です。Python では <code>scipy.stats.t.interval</code> が同じ計算をします。テストが 80 件しかないため、これだけの幅が出ます。<strong>テストが少ないほど、幅は広がります</strong>。</p>
'''))
    b.append(unit(2, "ブートストラップ", "テストデータを何度も引き直す", f'''
  <p>AUC や Precision のように<strong>公式がむずかしい指標</strong>でも、<strong>ブートストラップ</strong>なら信頼区間が作れます。テストデータから、<strong>同じ件数を復元抽出</strong>して指標を計算し、これを何度もくり返して、ばらつきを見ます。</p>
  {P.R(TI + '\n' + AUC + '\nset.seed(7)\nboot <- replicate(1000, { i <- sample(nrow(te), replace = TRUE); auc(te$Survived[i], p[i]) })\nround(c(AUC = auc(te$Survived, p), quantile(boot, c(.025, .975))), 3)\nhist(boot, breaks = 30, col = "lightblue", main = "1,000 bootstrap AUCs", xlab = "AUC")', plot=True, h=300)}
  <p>AUC の点推定は約 0.78 ですが、<strong>95% の範囲は約 0.73〜0.82</strong>。「0.78」より「0.73〜0.82」と報告する方が、現実に近い言い方です。</p>
'''))
    b.append(unit(3, "モデル比較：差はゆれより大きいか", "交差検証の成績を並べる", f'''
  <p>モデル A（面積だけ）と B（面積・部屋数・築年数）を、<strong>同じ 5 分割</strong>で比べます。同じフォールドでの成績の<strong>差</strong>を見るのがコツです（<strong>対応のある差</strong>）。</p>
  {P.R(APT + '\nset.seed(2); folds <- sample(rep(1:5, length.out = nrow(train)))\ncv_fold <- function(formula) sapply(1:5, function(k) {\n  f <- lm(formula, data = train[folds != k, ])\n  sqrt(mean((train$price[folds == k] - predict(f, train[folds == k, ]))^2))\n})\nA <- cv_fold(price ~ area)\nB <- cv_fold(price ~ area + rooms + age)\nround(rbind(A = A, B = B), 1)\nround(c(mean_diff = mean(A - B), sd_diff = sd(A - B)), 2)')}
  <p>A は B より平均で約 <strong>5</strong> 悪く、5 つのフォールドの差のゆれ（SD ≈ 1）の約 5 倍もあります。<strong>B の方が良い</strong>と言えます。では、役に立たない特徴（ただのノイズ）を足した B' はどうでしょうか。</p>
  {P.R('set.seed(11); train$noise <- rnorm(nrow(train))\nB2 <- cv_fold(price ~ area + rooms + age + noise)\nround(c(mean_diff = mean(B - B2), sd_diff = sd(B - B2)), 2)')}
  <p>差の平均は約 −0.24（B2 の方がむしろ少し悪い）で、<strong>ゆれ（SD ≈ 0.29）と同じくらいかそれ以下</strong>。この差では「B2 が悪い／良い」とは言えません。<strong>差が SD に埋もれるときは、同じ</strong>とみなし、単純な方（B）を選びます。</p>
'''))
    b.append(unit(4, "決定木の Gini 不純度と、平均化の力", "木を作る基準と、ランダムフォレストの理由", f'''
  <p>決定木は、データを<strong>できるだけ純粋なグループ</strong>に分ける質問を探します。純粋さの目安が <strong>Gini 不純度</strong>：<code>1 − Σ(各クラスの割合²)</code>。1 クラスだけなら 0、半々なら 0.5（2 クラスの最大）です。タイタニックの生存で、性別で分けると不純度がどれだけ下がるか計算します。</p>
  {P.R('gini <- function(y) { p <- prop.table(table(y)); 1 - sum(p^2) }\ng_all <- gini(ti$Survived)\ng_split <- function(by) sum(sapply(split(ti$Survived, by), function(y) length(y) / nrow(ti) * gini(y)))\nround(c(root = g_all, by_Sex = g_split(ti$Sex), by_Class = g_split(ti$Class), by_Age = g_split(ti$Age)), 3)')}
  <p>性別で分けると、不純度が 0.437 → <strong>0.347</strong> まで最も下がります（クラス 0.400、年齢 0.433 より大きな低下）。木は<strong>一番下がる質問（ここでは性別）を最初に選びます</strong>。</p>
  <p><strong>ランダムフォレスト</strong>は、データを復元抽出で変えながら木をたくさん作って<strong>平均（多数決）</strong>します。なぜ良くなるのか。<strong>独立なゆれを平均すると、ゆれは小さくなる</strong>からです（標準誤差 = SD ÷ √n と同じ考え方）。</p>
  {P.R('set.seed(1)\none  <- rnorm(5000)                                      # one noisy predictor\navg25 <- replicate(5000, mean(rnorm(25)))               # the average of 25 noisy predictors\nround(c(sd_one = sd(one), sd_avg25 = sd(avg25), theory = 1 / sqrt(25)), 3)')}
  {note('25 個を平均すると、ゆれは <strong>1/5（= 1/√25）</strong>になります。1 本の木は不安定でも、多数の木を平均した森は安定する。これがバギングの効果です（実際の木は完全に独立ではないので、効果はこれより小さくなります）。')}
'''))
    b.append(unit(5, "相関 ≠ 因果", "予測できることと、原因であることは別", f'''
  <p>ML は<strong>予測</strong>が得意ですが、<strong>原因</strong>は教えてくれません。2 つの変数が強く相関していても、<strong>第三の変数（交絡因子）</strong>が両方を動かしているだけかもしれません。気温が、アイスの売上と水難事故の両方を増やす例を作ります。</p>
  {P.R('set.seed(8)\ntemp <- rnorm(300, 25, 5)\nice  <- 3 * temp + rnorm(300, 0, 6)\nswim <- 2 * temp + rnorm(300, 0, 6)                   # swimming accidents: depends only on temperature\nround(cor(ice, swim), 2)                              # strong correlation!\nr_ice  <- resid(lm(ice ~ temp)); r_swim <- resid(lm(swim ~ temp))\nround(cor(r_ice, r_swim), 2)                          # after removing temperature')}
  <p>アイスと水難事故の相関は約 0.8 と強いのに、<strong>気温の影響を取り除くとほぼ 0（約 0.1）</strong>です。アイスを禁止しても、事故は減りません。</p>
  {warn('特徴量が目的変数を<strong>予測</strong>できることと、その特徴量が目的変数の<strong>原因</strong>であることは別です。ML の係数や特徴量の重要度を、「これを変えれば結果が変わる」と読むのは危険です。因果を知るには、<strong>無作為化実験</strong>（550 の M4）が必要です。')}
'''))
    b.append(teal('🎉 <strong>復習はここまで。</strong>次は <a href="cheat_ml.html">ML のための統計チートシート</a>で全体を見直し、練習ノートブック（このページの下からダウンロード）で自分の手を動かしましょう。'))
    q = [('The test RMSE is 28.5 with a 95% CI of 24 to 32. How should it be reported?', 'About 28, plausibly 24 to 32', ['Exactly 28.5 on any new data', 'Between 0 and 28.5 for sure', 'Above 32 for sure'], 'An estimate based on a sample test set always carries uncertainty.'),
         ('What does the bootstrap do?', 'Resamples with replacement, often', ['Splits the data into equal folds', 'Removes all outliers from the data', 'Adds noise to the test labels'], 'Each resample gives one value of the statistic; together they show its spread.'),
         ('Model A beats model B by 0.1 RMSE while the SD of the fold differences is 2. What follows?', 'The gap is within the noise', ['A is clearly better', 'B is clearly better', 'Both models have zero error'], 'A difference much smaller than its variability should not decide the choice.'),
         ('A node has 50% class 0 and 50% class 1. Its Gini impurity is...', '0.50', ['0.00', '1.00', '0.25'], '1 − (0.5² + 0.5²) = 0.5, the maximum for two classes.'),
         ('Averaging 25 independent noisy predictions reduces the SD of the result to about...', '1/5 of the original', ['1/25 of the original', 'The same as before', 'Twice the original'], 'SD of an average of n independent values is SD / √n; √25 = 5.'),
         ('Ice cream sales and swimming accidents are strongly correlated. The best explanation is...', 'A shared cause, such as heat', ['Ice cream causes accidents', 'Accidents cause ice cream sales', 'The correlation must be a mistake'], 'A confounder can drive both variables without a causal link between them.')]
    return L, "\n".join(b), q

LESSONS = [ml_classification, ml_overfit, ml_uncertainty]
