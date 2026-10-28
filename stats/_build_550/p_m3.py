"""M3 practice: probability & simulation, conditional probability & Bayes, discrete and continuous distributions.
All data are made up (no course data reused)."""
from practice_gen import Q, SRC

SHOP = '''shop <- matrix(c(90, 30, 60, 20,
                 110, 90, 40, 60), nrow = 2, byrow = TRUE,
               dimnames = list(device = c("Phone", "Computer"),
                               result = c("Bought", "Browsed", "Cart", "Left")))'''

A = [
Q(1, 1, "Rolling a die 600 times", "サイコロを600回（見本）",
  "Simulate 600 rolls of a fair die and compare the proportion of sixes with 1/6.",
  "", "",
  '''# === Complete example — read and run ===
die <- 1:6
set.seed(42)
rolls <- sample(die, size = 600, replace = TRUE)
table(rolls)
prop_six <- mean(rolls == 6)
prop_six
1 / 6''',
  [("prop_six", "prop_six", 3)],
  "<code>set.seed(42)</code> でサイコロを600回振り、6 が出た割合 <code>prop_six</code>（小数第3位）を入力してください（見本を実行）。",
  "<code>mean(rolls == 6)</code> は TRUE の割合。",
  "6 の割合は {prop_six}。理論値 1/6 ≈ 0.167 に近い値です。"),
Q(2, 2, "Coin flips and odds", "コイン投げとオッズ（穴埋め）",
  "Flip a coin 1,000 times with `set.seed(7)`. Find the proportion of heads and the odds of heads.",
  "", '''set.seed(7)
flips <- sample(c("H", "T"), size = ___, replace = ___)
p_heads <- mean(flips == "___")
odds_heads <- p_heads / (1 - ___)
round(c(p_heads, odds_heads), 3)''',
  '''set.seed(7)
flips <- sample(c("H", "T"), size = 1000, replace = TRUE)
p_heads <- mean(flips == "H")
odds_heads <- p_heads / (1 - p_heads)
round(c(p_heads, odds_heads), 3)''',
  [("p_heads", "p_heads", 3), ("odds_heads", "odds_heads", 3)],
  "<code>set.seed(7)</code> でコインを1,000回投げ、表の割合 <code>p_heads</code> とオッズ <code>odds_heads</code>（どちらも小数第3位）を求めてください。",
  "オッズ = p ÷ (1 − p)。",
  "表の割合 {p_heads}、オッズ {odds_heads}。確率 0.5 ならオッズは 1（1:1）。"),
Q(3, 3, "Sum of two dice", "サイコロ2個の和（自由記述）",
  "With `set.seed(2026)`, simulate 10,000 throws of two dice. Estimate P(sum = 7) and compare it with the exact value 6/36 (3 decimals).",
  "", '''# Write all your code here
''',
  '''set.seed(2026)
d1 <- sample(1:6, 10000, replace = TRUE)
d2 <- sample(1:6, 10000, replace = TRUE)
est7 <- round(mean(d1 + d2 == 7), 3)
exact7 <- round(6 / 36, 3)
est7; exact7''',
  [("est7", "est7", 3)],
  "<code>set.seed(2026)</code> で2個のサイコロを10,000回投げ、和が 7 になる確率の推定値 <code>est7</code>（小数第3位）を求めてください（d1 → d2 の順に <code>sample()</code>）。",
  "2つのベクトルを足すと、1回ごとの和のベクトルになります。",
  "推定値 {est7}、正確な値は 6/36 ≈ 0.167。"),
Q(4, 4, "Product returns", "返品の確率（シナリオ1）",
  "An online shop had 2,500 orders last month and 175 were returned (made-up data). Estimate the probability and the odds of a return, and the expected returns among the next 400 orders.",
  "", '''# 1. Probability of a return (3 decimals)
# 2. Odds of a return (3 decimals)
# 3. Expected number of returns in 400 orders
# 4. Conclusion (comment):
''',
  '''orders <- 2500; returns <- 175
p_return <- round(returns / orders, 3)
odds_return <- round(returns / (orders - returns), 3)
expected_400 <- 400 * returns / orders
p_return; odds_return; expected_400
# Conclusion: about 7% of orders come back, so plan for about 28 returns per 400 orders.''',
  [("p_return", "p_return", 3), ("odds_return", "odds_return", 3), ("expected_400", "expected_400", 0)],
  "2,500件中175件が返品でした（架空）。返品の確率 <code>p_return</code>・オッズ <code>odds_return</code>（小数第3位）と、次の400件での返品の期待数 <code>expected_400</code> を求めてください。",
  "確率は ÷ 全体、オッズは ÷ 失敗（返品されなかった数）。",
  "確率 {p_return}、オッズ {odds_return}、400件中の期待数 {expected_400} 件。"),
Q(5, 5, "Law of large numbers", "大数の法則（シナリオ2）",
  "With `set.seed(550)`, flip a coin 10,000 times. Report the running proportion of heads after 10, 100, 1,000 and 10,000 flips, the absolute error after 10,000 flips, and plot the running proportion. Write 3 sentences.",
  "", '''# 1. flips <- sample(c(0, 1), 10000, replace = TRUE)   (1 = heads)
# 2. running proportion: cumsum(flips) / seq_along(flips)
# 3. values after 10, 100, 1000, 10000 flips
# 4. absolute error after 10000 flips (4 decimals)
# 5. plot with a red line at 0.5
# 6. Report (3 sentences as comments):
''',
  '''set.seed(550)
flips <- sample(c(0, 1), 10000, replace = TRUE)
running <- cumsum(flips) / seq_along(flips)
round(running[c(10, 100, 1000, 10000)], 4)
err_10000 <- round(abs(running[10000] - 0.5), 4)
err_10000
plot(running, type = "l", ylim = c(0, 1), xlab = "Flips", ylab = "Proportion of heads")
abline(h = 0.5, col = "red", lty = 2)
# With few flips the proportion jumps around a lot.
# As the number of flips grows it settles close to 0.5.
# This is the law of large numbers: long-run relative frequency approaches the probability.''',
  [("p_after_100", "running[100]", 2), ("err_10000", "err_10000", 4)],
  "<code>set.seed(550)</code> で <code>sample(c(0, 1), 10000, replace = TRUE)</code> を実行し、100回時点の表の割合 <code>p_after_100</code>（小数第2位）と、10,000回時点の 0.5 との差の絶対値 <code>err_10000</code>（小数第4位）を求めてください。",
  "<code>cumsum(flips) / seq_along(flips)</code> が「その時点までの割合」。",
  "100回で {p_after_100}、10,000回での誤差は {err_10000}。回数が増えるほど 0.5 に近づきます。"),
]

B = [
Q(6, 1, "Union with the addition rule", "加法定理（見本）",
  "Use the shop table (made-up data) to find P(Bought ∪ Phone) with the general addition rule.",
  SHOP, "",
  '''# === Complete example — read and run ===
addmargins(shop)
n <- sum(shop)
p_B  <- sum(shop[, "Bought"]) / n
p_Ph <- sum(shop["Phone", ]) / n
p_B_and_Ph <- shop["Phone", "Bought"] / n
p_union <- p_B + p_Ph - p_B_and_Ph   # subtract the overlap once
p_union''',
  [("p_union", "p_union", 2)],
  "ショップの二元表（架空）で、加法定理から P(購入 ∪ スマホ) <code>p_union</code>（小数第2位）を求めてください（見本を実行）。",
  "P(A ∪ B) = P(A) + P(B) − P(A ∩ B)。",
  "P(購入 ∪ スマホ) = {p_union}。重なり（スマホで購入した人）を1回引いています。"),
Q(7, 2, "Conditional probabilities", "条件付き確率（穴埋め）",
  "Find P(Bought | Phone) and P(Bought | Computer) from the shop table.",
  SHOP, '''p_b_phone <- shop["Phone", "___"] / sum(shop["___", ])
p_b_comp  <- shop["Computer", "Bought"] / sum(shop[___, ])
round(c(p_b_phone, p_b_comp), 3)
round(proportions(shop, margin = ___), 3)   # all row proportions''',
  '''p_b_phone <- shop["Phone", "Bought"] / sum(shop["Phone", ])
p_b_comp  <- shop["Computer", "Bought"] / sum(shop["Computer", ])
round(c(p_b_phone, p_b_comp), 3)
round(proportions(shop, margin = 1), 3)   # all row proportions''',
  [("p_b_phone", "p_b_phone", 3), ("p_b_comp", "p_b_comp", 3)],
  "ショップの表から P(購入 | スマホ) <code>p_b_phone</code> と P(購入 | パソコン) <code>p_b_comp</code>（小数第3位）を求めてください。",
  "条件（| の後ろ）の行の合計が分母。",
  "スマホ {p_b_phone}、パソコン {p_b_comp}。端末によって購入率が違います。"),
Q(8, 3, "Gym renewals", "ジムの更新（自由記述）",
  "A gym (made-up data) has 240 members: 90 annual-plan members (72 renewed) and 150 monthly-plan members (84 renewed). Build the table, find P(renew), P(renew | annual) and decide whether plan and renewal are independent.",
  "", '''# Write all your code here
# Hint: matrix(c(72, 18, 84, 66), nrow = 2, byrow = TRUE, dimnames = ...)
''',
  '''gym <- matrix(c(72, 18, 84, 66), nrow = 2, byrow = TRUE,
              dimnames = list(plan = c("Annual", "Monthly"), renewed = c("Yes", "No")))
addmargins(gym)
p_renew <- round(sum(gym[, "Yes"]) / sum(gym), 3)
p_renew_annual <- round(gym["Annual", "Yes"] / sum(gym["Annual", ]), 3)
p_renew; p_renew_annual
# Not independent: P(renew | annual) is not equal to P(renew).''',
  [("p_renew", "p_renew", 3), ("p_renew_annual", "p_renew_annual", 3)],
  "会員240人（年間プラン90人中72人更新、月額プラン150人中84人更新、架空）。P(更新) <code>p_renew</code> と P(更新 | 年間) <code>p_renew_annual</code>（小数第3位）を求め、独立か判断してください。",
  "独立なら P(更新 | 年間) = P(更新)。",
  "P(更新) = {p_renew}、P(更新 | 年間) = {p_renew_annual}。等しくないので独立ではありません。"),
Q(9, 4, "At least one defect", "少なくとも1個の不良（シナリオ1）",
  "Each part is defective with probability 0.04, independently. In a box of 5 parts, what is P(at least one defect)? How many parts can a box hold before P(at least one defect) exceeds 0.5?",
  "", '''# 1. P(no defect in 5) and P(at least one) using the complement
# 2. Try n = 1:30 and find the first n where P(at least one) > 0.5
# 3. Conclusion (comment):
''',
  '''p_none5 <- (1 - 0.04)^5
p_atleast1 <- round(1 - p_none5, 4)
p_atleast1
n <- 1:30
probs <- 1 - (1 - 0.04)^n
first_n <- min(n[probs > 0.5])
first_n
# Conclusion: with 17 or more parts, a defect is more likely than not.''',
  [("p_atleast1", "p_atleast1", 4), ("first_n", "first_n", 0)],
  "不良率 0.04（独立）の部品5個の箱で、少なくとも1個不良の確率 <code>p_atleast1</code>（小数第4位）と、その確率が初めて 0.5 を超える個数 <code>first_n</code> を求めてください。",
  "「少なくとも1個」の余事象は「1個もない」＝ (1 − 0.04)^n。",
  "5個で {p_atleast1}。{first_n} 個以上で 0.5 を超えます。"),
Q(10, 5, "Bayes and a screening test", "ベイズと検査（シナリオ2）",
  "A condition affects 2% of people. A test detects 90% of true cases and gives a false positive for 8% of healthy people (made-up numbers). Find P(condition | positive). Then repeat for a high-risk group with 20% prevalence. Write a 3-sentence note for a clinic.",
  "", '''# 1. Store prior, sensitivity, false-positive rate
# 2. P(positive) by the law of total probability
# 3. Posterior P(condition | positive)  (3 decimals)
# 4. Repeat with prior = 0.20
# 5. Note (3 sentences as comments):
''',
  '''posterior <- function(prior, sens = 0.90, fpr = 0.08) {
  p_pos <- sens * prior + fpr * (1 - prior)
  sens * prior / p_pos
}
post_low  <- round(posterior(0.02), 3)
post_high <- round(posterior(0.20), 3)
post_low; post_high
# In the general population most positives are false positives.
# In the high-risk group a positive result is far more convincing.
# Always consider the base rate before telling a patient what a positive means.''',
  [("post_low", "post_low", 3), ("post_high", "post_high", 3)],
  "有病率 2%、検出率 90%、偽陽性率 8%（架空）の検査で、陽性のとき本当に該当する確率 <code>post_low</code> と、有病率 20% の集団での同じ確率 <code>post_high</code>（小数第3位）を求めてください。",
  "P(陽性) = 0.90 × 事前 + 0.08 × (1 − 事前)。事後 = 0.90 × 事前 ÷ P(陽性)。",
  "有病率 2% では {post_low}、20% では {post_high}。基準率が低いと陽性の多くは偽陽性です。"),
]

C = [
Q(11, 1, "Binomial: coupon emails", "二項分布：クーポンメール（見本）",
  "12 customers each use a coupon with probability 0.2. Use the binomial functions.",
  "", "",
  '''# === Complete example — read and run ===
p3     <- dbinom(3, size = 12, prob = 0.2)                     # exactly 3
p_le3  <- pbinom(3, size = 12, prob = 0.2)                     # at most 3
p_ge4  <- pbinom(3, size = 12, prob = 0.2, lower.tail = FALSE) # 4 or more
med    <- qbinom(0.5, size = 12, prob = 0.2)                   # median
round(c(p3, p_le3, p_ge4), 4); med
plot(0:12, dbinom(0:12, 12, 0.2), type = "h", lwd = 5, xlab = "Coupons used", ylab = "P")''',
  [("p3", "p3", 4)],
  "X ~ B(12, 0.2) で、ちょうど 3 人がクーポンを使う確率 <code>p3</code>（小数第4位）を入力してください（見本を実行）。",
  "「ちょうど」は d。",
  "P(X = 3) = {p3}。「以下」は p、「以上」は p(k − 1, lower.tail = FALSE)。"),
Q(12, 2, "Binomial: at least / mean", "二項分布：以上と平均（穴埋め）",
  "For X ~ B(20, 0.35), find P(X ≥ 8) and the mean np.",
  "", '''p_ge8 <- pbinom(___, size = 20, prob = 0.35, lower.tail = ___)
mean_x <- ___ * ___
round(p_ge8, 4); mean_x''',
  '''p_ge8 <- pbinom(7, size = 20, prob = 0.35, lower.tail = FALSE)
mean_x <- 20 * 0.35
round(p_ge8, 4); mean_x''',
  [("p_ge8", "p_ge8", 4), ("mean_x", "mean_x", 1)],
  "X ~ B(20, 0.35) で P(X ≥ 8) <code>p_ge8</code>（小数第4位）と、平均 np <code>mean_x</code>（小数第1位）を求めてください。",
  "「8 以上」は q = 7 で <code>lower.tail = FALSE</code>。",
  "P(X ≥ 8) = {p_ge8}、平均は {mean_x}。"),
Q(13, 3, "Poisson: help desk", "ポアソン：サポート窓口（自由記述）",
  "A help desk gets 4 calls per hour on average. Find P(exactly 2 calls in an hour), P(more than 6 calls in an hour) and P(no calls in 30 minutes) (4 decimals).",
  "", '''# Write all your code here
''',
  '''p2 <- round(dpois(2, lambda = 4), 4)
p_gt6 <- round(ppois(6, lambda = 4, lower.tail = FALSE), 4)
p0_30 <- round(dpois(0, lambda = 4 * 30 / 60), 4)
p2; p_gt6; p0_30''',
  [("p2", "p2", 4), ("p_gt6", "p_gt6", 4), ("p0_30", "p0_30", 4)],
  "1時間に平均4件の問い合わせ。ちょうど2件 <code>p2</code>、6件より多い <code>p_gt6</code>、30分で0件 <code>p0_30</code> の確率（小数第4位）を求めてください。",
  "区間を変えたら λ も比例させる：30分なら λ = 2。",
  "P(2件) = {p2}、P(6件超) = {p_gt6}、P(30分で0件) = {p0_30}。"),
Q(14, 4, "Geometric: sales calls", "幾何分布：営業電話（シナリオ1）",
  "A salesperson closes a sale on 10% of calls (independent). Find P(first sale on call 5) and P(no sale in the first 10 calls). How many calls are expected until the first sale?",
  "", '''# 1. P(first success on call 5) — remember R counts failures before success
# 2. P(no sale in the first 10 calls)
# 3. Expected number of calls until the first sale (1/p)
# 4. Conclusion (comment):
''',
  '''p <- 0.1
p_call5 <- round(dgeom(4, prob = p), 4)
p_none10 <- round(pgeom(9, prob = p, lower.tail = FALSE), 4)   # 10+ failures
expected_calls <- 1 / p
p_call5; p_none10; expected_calls
# Conclusion: going 10 calls without a sale happens about 35% of the time, so it is not unusual.''',
  [("p_call5", "p_call5", 4), ("p_none10", "p_none10", 4), ("expected_calls", "expected_calls", 0)],
  "成約率 10% の営業電話で、5本目で初めて成約する確率 <code>p_call5</code>、最初の10本で1件も成約しない確率 <code>p_none10</code>（小数第4位）、初成約までの期待本数 <code>expected_calls</code> を求めてください。",
  "R の <code>dgeom(x)</code> は「成功の前の失敗の数」。5本目 → x = 4。",
  "5本目で初成約 {p_call5}、10本連続で不成約 {p_none10}、期待本数 {expected_calls}。"),
Q(15, 5, "Quality control", "品質管理（シナリオ2）",
  "Parts are defective with p = 0.03. In a sample of 50, find P(at most 2 defects) exactly (binomial), with a simulation (`set.seed(1)`, 10,000 samples) and with a Poisson approximation (λ = np). Write 3 sentences comparing them.",
  "", '''# 1. Exact: pbinom
# 2. Simulation: rbinom(10000, 50, 0.03), proportion <= 2
# 3. Poisson approximation with lambda = 50 * 0.03
# 4. Report (3 sentences as comments):
''',
  '''exact <- round(pbinom(2, size = 50, prob = 0.03), 4)
set.seed(1)
sim <- round(mean(rbinom(10000, size = 50, prob = 0.03) <= 2), 4)
pois <- round(ppois(2, lambda = 50 * 0.03), 4)
exact; sim; pois
# The simulation lands close to the exact binomial value.
# The Poisson approximation is also close because n is large and p is small.
# A box with 3 or more defects happens only about 1 time in 5.''',
  [("exact", "exact", 4), ("sim", "sim", 4), ("pois", "pois", 4)],
  "不良率 3% の部品50個で「不良 2 個以下」の確率を、正確な二項 <code>exact</code>、シミュレーション <code>sim</code>（<code>set.seed(1)</code>、<code>rbinom(10000, 50, 0.03)</code>）、ポアソン近似 <code>pois</code>（λ = np）で求めてください（小数第4位）。",
  "ポアソン近似は n が大きく p が小さいときに使えます。",
  "正確 {exact}、シミュレーション {sim}、ポアソン {pois}。3つとも近い値になります。"),
]

D = [
Q(16, 1, "Normal probabilities", "正規分布の確率（見本）",
  "Delivery time ~ N(30, 5) minutes (made-up). Use pnorm() and qnorm().",
  "", "",
  '''# === Complete example — read and run ===
p_le25 <- pnorm(25, mean = 30, sd = 5)                     # 25 min or less
p_ge40 <- pnorm(40, mean = 30, sd = 5, lower.tail = FALSE) # 40 min or more
p_28_35 <- pnorm(35, 30, 5) - pnorm(28, 30, 5)             # between
q95 <- qnorm(0.95, mean = 30, sd = 5)                      # 95th percentile
round(c(p_le25, p_ge40, p_28_35, q95), 4)''',
  [("p_28_35", "p_28_35", 4)],
  "配達時間 ~ N(30, 5) で、28〜35分に届く確率 <code>p_28_35</code>（小数第4位）を入力してください（見本を実行）。",
  "あいだ＝大きい方の累積 − 小さい方の累積。",
  "P(28 ≤ X ≤ 35) = {p_28_35}。連続分布では「ちょうど」の確率は 0 なので dnorm は使いません。"),
Q(17, 2, "Exam scores", "試験の得点（穴埋め）",
  "Scores ~ N(500, 100). Find the share scoring above 650 and the score needed for the top 10%.",
  "", '''p_above650 <- pnorm(___, mean = 500, sd = 100, lower.tail = ___)
cutoff_top10 <- qnorm(___, mean = 500, sd = 100)
round(p_above650, 4); round(cutoff_top10, 1)''',
  '''p_above650 <- pnorm(650, mean = 500, sd = 100, lower.tail = FALSE)
cutoff_top10 <- qnorm(0.90, mean = 500, sd = 100)
round(p_above650, 4); round(cutoff_top10, 1)''',
  [("p_above650", "p_above650", 4), ("cutoff_top10", "cutoff_top10", 1)],
  "得点 ~ N(500, 100) で、650 点を超える割合 <code>p_above650</code>（小数第4位）と、上位 10% に入る最低点 <code>cutoff_top10</code>（小数第1位）を求めてください。",
  "上位 10% ＝ 下から 90%。",
  "650 点超は {p_above650}、上位 10% の境目は {cutoff_top10} 点。"),
Q(18, 3, "Normal approximation to the binomial", "二項の正規近似（自由記述）",
  "For X ~ B(100, 0.4), check the conditions np ≥ 10 and n(1 − p) ≥ 10, then compare the exact P(X ≤ 45) with the normal approximation using the continuity correction (4 decimals).",
  "", '''# Write all your code here
''',
  '''n <- 100; p <- 0.4
c(n * p, n * (1 - p))                     # both >= 10
exact45 <- round(pbinom(45, n, p), 4)
approx45 <- round(pnorm(45.5, mean = n * p, sd = sqrt(n * p * (1 - p))), 4)
exact45; approx45''',
  [("exact45", "exact45", 4), ("approx45", "approx45", 4)],
  "X ~ B(100, 0.4) の P(X ≤ 45) を、正確な値 <code>exact45</code> と、連続性補正つきの正規近似 <code>approx45</code>（平均 np、SD √(np(1 − p))、45.5 を使う）で求めてください（小数第4位）。",
  "正規近似は <code>pnorm(45.5, n*p, sqrt(n*p*(1-p)))</code>。",
  "正確 {exact45}、近似 {approx45}。np = 40、n(1 − p) = 60 でどちらも 10 以上なので近似がよく合います。"),
Q(19, 4, "t critical values", "t の臨界値（シナリオ1）",
  "A researcher has n = 12 observations. Find the t critical value for a 95% two-sided interval and compare it with z. Then find P(T > 2.5) for df = 20.",
  "", '''# 1. df for one sample of 12
# 2. t* = qt(0.975, df) and z* = qnorm(0.975)  (3 decimals)
# 3. P(T > 2.5) with df = 20  (4 decimals)
# 4. Conclusion (comment): why is t* larger than z*?
''',
  '''df <- 12 - 1
t_star <- round(qt(0.975, df = df), 3)
z_star <- round(qnorm(0.975), 3)
p_t25 <- round(pt(2.5, df = 20, lower.tail = FALSE), 4)
t_star; z_star; p_t25
# Conclusion: t has heavier tails, so it must go further out to leave 2.5% in each tail.''',
  [("t_star", "t_star", 3), ("p_t25", "p_t25", 4)],
  "n = 12 のとき、両側 95% の t 臨界値 <code>t_star</code>（小数第3位）と、df = 20 で T &gt; 2.5 となる確率 <code>p_t25</code>（小数第4位）を求めてください。",
  "df = n − 1 = 11。右側の確率は <code>lower.tail = FALSE</code>。",
  "t* = {t_star}（z* = 1.960 より大きい）、P(T &gt; 2.5) = {p_t25}。"),
Q(20, 5, "Chi-square and F", "χ² と F（シナリオ2）",
  "Find P(χ² ≥ 9.5) for df = 4 and P(F ≥ 4.5) for F(3, 8). Then, with `set.seed(550)`, simulate 5,000 values of z1² + z2² + z3² and check that their mean is close to df = 3. Write 3 sentences.",
  "", '''# 1. pchisq(9.5, df = 4, lower.tail = FALSE)   (4 decimals)
# 2. pf(4.5, df1 = 3, df2 = 8, lower.tail = FALSE)   (4 decimals)
# 3. chi3 <- rnorm(5000)^2 + rnorm(5000)^2 + rnorm(5000)^2 ; mean(chi3)
# 4. hist(chi3) with curve(dchisq(x, 3), add = TRUE)
# 5. Report (3 sentences as comments):
''',
  '''p_chi <- round(pchisq(9.5, df = 4, lower.tail = FALSE), 4)
p_f   <- round(pf(4.5, df1 = 3, df2 = 8, lower.tail = FALSE), 4)
set.seed(550)
chi3 <- rnorm(5000)^2 + rnorm(5000)^2 + rnorm(5000)^2
mean_chi3 <- round(mean(chi3), 2)
hist(chi3, breaks = 50, freq = FALSE, col = "lightblue")
curve(dchisq(x, df = 3), add = TRUE, col = "red", lwd = 2)
p_chi; p_f; mean_chi3
# Both chi-square and F are right-skewed and non-negative, so we look at the right tail.
# A chi-square of 9.5 (df = 4) and an F of 4.5 (3, 8) are both fairly rare, about 5% or less.
# The simulated sum of 3 squared normals has a mean close to 3, as the theory says (mean = df).''',
  [("p_chi", "p_chi", 4), ("p_f", "p_f", 4), ("mean_chi3", "mean_chi3", 2)],
  "df = 4 の χ² で 9.5 以上の確率 <code>p_chi</code>、F(3, 8) で 4.5 以上の確率 <code>p_f</code>（小数第4位）、<code>set.seed(550)</code> で作った z1² + z2² + z3²（各 <code>rnorm(5000)</code> を順に）の平均 <code>mean_chi3</code>（小数第2位）を求めてください。",
  "χ²・F は右側の面積なので <code>lower.tail = FALSE</code>。",
  "P(χ² ≥ 9.5) = {p_chi}、P(F ≥ 4.5) = {p_f}、シミュレーションの平均 {mean_chi3}（理論値 df = 3）。"),
]

CARD = '''╔══════════════════════════════════════════════════════╗
║  M3 QUICK REFERENCE                                  ║
║  sample(x, size, replace = TRUE)   set.seed(n)       ║
║  probability = success / total   odds = s / f        ║
║  P(A or B) = P(A) + P(B) - P(A and B)                ║
║  P(A | B) = P(A and B) / P(B)   independent: = P(A)  ║
║  proportions(table, margin = 1)  addmargins(table)   ║
║  Bayes: P(H|D) = P(D|H) P(H) / P(D)                  ║
║  r d p q :  random / exactly / at most / percentile  ║
║  dbinom pbinom qbinom   (at least k: q = k - 1,      ║
║                          lower.tail = FALSE)         ║
║  dpois ppois   dgeom (failures before 1st success)   ║
║  pnorm qnorm   pt qt   pchisq   pf                   ║
║  normal approx: np >= 10 and n(1-p) >= 10            ║
╚══════════════════════════════════════════════════════╝'''

MOD = dict(key="m3", short="550 M3", name_ja="確率と分布",
           title="550 M3 — Probability & Probability Distributions: R Coding Practice (20 Questions)",
           file="m3_practice_v1.Rmd", folder=SRC + "/Module 3", wd=SRC + "/Module 3",
           data_note="No data files are needed: every data set is made up or simulated.",
           data_note_ja="📂 データファイルは不要です（すべて架空のデータかシミュレーション）。<code>set.seed()</code> の値と <code>sample()</code> を呼ぶ順番をノートブックと同じにすると、同じ答えになります。",
           lessons_ja='<a href="m3_prob.html">確率の基本</a>（Topic A）・<a href="m3_cond.html">条件付き確率・独立</a>／<a href="m3_bayes.html">頻度論とベイズ</a>（B）・<a href="m3_discrete.html">二項・幾何・ポアソン</a>（C）・<a href="m3_normal.html">正規分布</a>／<a href="m3_tchif.html">t・χ²・F</a>（D）',
           topics=[("Probability & Simulation", A), ("Conditional Probability, Independence & Bayes", B),
                   ("Discrete Distributions", C), ("Continuous Distributions", D)],
           card=CARD, web="ex_550_m3_prob.html")
MOD["questions"] = A + B + C + D
