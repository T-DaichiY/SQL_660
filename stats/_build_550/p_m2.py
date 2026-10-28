"""M2 practice: center, graphs & categorical data, spread, normal & z-scores (donors data)."""
from practice_gen import Q, SRC

LOAD = 'donors <- read.csv("donors.csv")\ndonors1_20 <- donors[1:20, ]'

A = [
Q(1, 1, "Mean of the first 20 donors", "最初の20人の平均（見本）",
  "Compute the sample mean age of the first 20 donors and compare it with the population mean.",
  LOAD, "",
  '''# === Complete example — read and run ===
mean(donors1_20$age)                       # NA: there are missing ages
xbar <- mean(donors1_20$age, na.rm = TRUE) # sample statistic
mu   <- mean(donors$age, na.rm = TRUE)     # population parameter
round(xbar, 2)
round(mu, 2)
sum(!is.na(donors1_20$age))                # how many ages were used''',
  [("xbar", "xbar", 2), ("mu", "mu", 2)],
  "<code>donors</code> の最初の20人の平均年齢 x̄ と、全体の平均年齢 μ（どちらも小数第2位）を求めてください（見本を実行）。",
  "NA があるので <code>na.rm = TRUE</code>。",
  "x̄ = {xbar}、μ = {mu}。標本（最初の20人）の統計量で母集団の母数を推定しています。"),
Q(2, 2, "Three measures of center", "3つの中心（穴埋め）",
  "Find the mean, median and 10% trimmed mean of `numberGifts`.",
  "", '''m  <- ___(donors$numberGifts)
md <- ___(donors$numberGifts)
tm <- mean(donors$numberGifts, trim = ___)
round(c(m, md, tm), 2)''',
  '''m  <- mean(donors$numberGifts)
md <- median(donors$numberGifts)
tm <- mean(donors$numberGifts, trim = 0.10)
round(c(m, md, tm), 2)''',
  [("mean", "m", 2), ("median", "md", 2), ("trimmed", "tm", 2)],
  "寄付回数 <code>numberGifts</code> の平均・中央値・10% トリム平均（小数第2位）を求めてください。",
  "トリム平均は <code>trim = 0.10</code>（上下 10% ずつ除く）。",
  "平均 {mean}、中央値 {median}、トリム平均 {trimmed}。平均 &gt; トリム平均 &gt; 中央値の順は、右に歪んだ分布のサインです。"),
Q(3, 3, "Random sample vs first 20 rows", "無作為標本と最初の20行（自由記述）",
  "With `set.seed(10)`, draw a random sample of 100 donors. Compare the sample mean of `totalGivingAmount` with the population mean (2 decimals) and compute the difference.",
  "", '''# Write all your code here
''',
  '''set.seed(10)
srs <- donors[sample(nrow(donors), 100), ]
samp_mean <- round(mean(srs$totalGivingAmount), 2)
pop_mean  <- round(mean(donors$totalGivingAmount), 2)
gap <- round(samp_mean - pop_mean, 2)
samp_mean; pop_mean; gap''',
  [("samp_mean", "samp_mean", 2), ("gap", "gap", 2)],
  "<code>set.seed(10)</code> のあと、<code>donors</code> から100人を無作為抽出し、寄付総額の標本平均 <code>samp_mean</code> と、母平均との差 <code>gap</code>（小数第2位）を求めてください。",
  "<code>donors[sample(nrow(donors), 100), ]</code> で100行を重複なく選べます。",
  "標本平均 {samp_mean}、差 {gap}。種（seed）を変えると標本平均も変わります＝標本変動。"),
Q(4, 4, "Salaries with an outlier", "外れ値のある給与（シナリオ1）",
  "A small company's 9 salaries (in $1,000) include the CEO. Compare mean and median with and without the CEO and recommend which center to report.",
  "salary <- c(42, 45, 47, 48, 50, 52, 55, 58, 410)   # last value is the CEO",
  '''# 1. Mean and median of all 9 salaries (2 decimals)
# 2. Mean without the CEO
# 3. Which measure changed more? Why?
# 4. Recommendation (comment): which center should HR report?
''',
  '''mean_all <- round(mean(salary), 2)
median_all <- median(salary)
mean_no_ceo <- round(mean(salary[-9]), 2)
mean_all; median_all; mean_no_ceo
# The mean drops a lot without the CEO; the median hardly moves.
# Recommendation: report the median, because it is resistant to the outlier.''',
  [("mean_all", "mean_all", 2), ("median_all", "median_all", 0), ("mean_no_ceo", "mean_no_ceo", 2)],
  "CEO を含む9人の給与（千ドル）です。全員の平均 <code>mean_all</code>（小数第2位）、中央値 <code>median_all</code>、CEO を除いた平均 <code>mean_no_ceo</code>（小数第2位）を求めてください。",
  "<code>salary[-9]</code> は9番目を除いたベクトル。",
  "平均 {mean_all} → CEO なしで {mean_no_ceo}、中央値は {median_all}。報告には外れ値に強い中央値が適切です。"),
Q(5, 5, "Average gift amount report", "平均寄付額のレポート（シナリオ2）",
  "Summarise `averageGiftAmount`: mean, median, 5% and 25% trimmed means. Decide the shape from these numbers and write a 3-sentence report for the fundraising team.",
  "", '''# 1. Mean and median (2 decimals)
# 2. Trimmed means with trim = 0.05 and trim = 0.25
# 3. Shape: compare mean vs median
# 4. Report (3 sentences as comments):
''',
  '''g <- donors$averageGiftAmount
avg_mean <- round(mean(g), 2)
avg_median <- round(median(g), 2)
tr05 <- round(mean(g, trim = 0.05), 2)
tr25 <- round(mean(g, trim = 0.25), 2)
avg_mean; avg_median; tr05; tr25
# Report: the typical (median) average gift is smaller than the mean.
# Trimming pulls the center down toward the median, so a few large gifts inflate the mean.
# The distribution is right-skewed; use the median when describing a typical donor.''',
  [("avg_mean", "avg_mean", 2), ("avg_median", "avg_median", 2), ("tr25", "tr25", 2)],
  "<code>averageGiftAmount</code> の平均 <code>avg_mean</code>・中央値 <code>avg_median</code>・25% トリム平均 <code>tr25</code>（小数第2位）を求め、形を判断してください。",
  "トリムの割合を増やすほど中央値に近づきます。",
  "平均 {avg_mean}、中央値 {avg_median}、25% トリム平均 {tr25}。平均 &gt; 中央値なので右に歪んでいます。"),
]

B = [
Q(6, 1, "Counts and proportions", "度数と割合（見本）",
  "Make a frequency table, a percentage table and a barplot of `urbanicity`.",
  "", "",
  '''# === Complete example — read and run ===
t_urban <- table(donors$urbanicity)
t_urban
pct <- round(proportions(t_urban) * 100, 1)
pct
pct_urban <- pct[["urban"]]
barplot(t_urban, las = 1, ylab = "Count", main = "Donors by urbanicity")''',
  [("pct_urban", "pct_urban", 1)],
  "<code>urbanicity</code> の度数表と割合（%）を作り、urban の割合 <code>pct_urban</code>（小数第1位）を入力してください（見本を実行）。",
  "<code>proportions(table(x)) * 100</code>。",
  "urban は {pct_urban}%。棒グラフは表を作ってから <code>barplot()</code> に渡します。"),
Q(7, 2, "Response rate by area", "地域ごとの反応率（穴埋め）",
  "Make a two-way table of urbanicity × respondedMailing and find the response rate in the suburbs.",
  "", '''tab <- table(donors$___, donors$respondedMailing)
rates <- round(proportions(tab, margin = ___), 3)
rates
suburb_rate <- rates["suburb", "___"]
suburb_rate''',
  '''tab <- table(donors$urbanicity, donors$respondedMailing)
rates <- round(proportions(tab, margin = 1), 3)
rates
suburb_rate <- rates["suburb", "TRUE"]
suburb_rate''',
  [("suburb_rate", "suburb_rate", 3)],
  "urbanicity × respondedMailing の二元表を作り、<strong>行ごと</strong>の割合から郊外（suburb）の反応率 <code>suburb_rate</code>（小数第3位）を求めてください。",
  "<code>margin = 1</code> は行ごとの割合。列名は \"TRUE\"（文字）で指定します。",
  "郊外の反応率は {suburb_rate}。行ごとの割合にすると、地域の人数の違いに左右されずに比べられます。"),
Q(8, 3, "Ages in their 70s", "70代の寄付者（自由記述）",
  "Draw a histogram of donor ages, then count how many donors are aged 70–79 and what percentage of donors with a known age that is (1 decimal).",
  "", '''# Write all your code here
''',
  '''hist(donors$age, col = "lightblue", main = "Donor ages", xlab = "Age")
n_70s <- sum(donors$age >= 70 & donors$age < 80, na.rm = TRUE)
pct_70s <- round(n_70s / sum(!is.na(donors$age)) * 100, 1)
n_70s; pct_70s''',
  [("n_70s", "n_70s", 0), ("pct_70s", "pct_70s", 1)],
  "年齢のヒストグラムを描き、70〜79歳の人数 <code>n_70s</code> と、年齢がわかる人に占める割合 <code>pct_70s</code>（%・小数第1位）を求めてください。",
  "2つの条件は <code>&amp;</code> でつなぎます。NA があるので <code>na.rm = TRUE</code>。",
  "70代は {n_70s} 人（{pct_70s}%）。"),
Q(9, 4, "Response rate by gender", "性別ごとの反応率（シナリオ1）",
  "The team wants to know whether women or men responded more often. Compute the response rate for female and male donors (3 decimals) and conclude.",
  "", '''# 1. Two-way table of gender x respondedMailing
# 2. Row proportions
# 3. Response rate for female and male
# 4. Conclusion (comment):
''',
  '''g_tab <- table(donors$gender, donors$respondedMailing)
g_rates <- round(proportions(g_tab, margin = 1), 3)
g_rates
female_rate <- g_rates["female", "TRUE"]
male_rate   <- g_rates["male", "TRUE"]
female_rate; male_rate
# Conclusion: the two response rates are very close (about 5% each).''',
  [("female_rate", "female_rate", 3), ("male_rate", "male_rate", 3)],
  "性別×反応の二元表から、女性の反応率 <code>female_rate</code> と男性の反応率 <code>male_rate</code>（小数第3位）を求めてください。",
  "Q7 と同じく <code>proportions(…, margin = 1)</code>。",
  "女性 {female_rate}、男性 {male_rate}。差はとても小さく、性別による違いはほぼ見られません（差が偶然かどうかは M5 の χ² 検定で）。"),
Q(10, 5, "Dotplot, stemplot and shape", "ドット・幹葉図と形（シナリオ2）",
  "For the 20 first donors, draw a dotplot and a stemplot of `totalGivingAmount`. Then compute mean − median for the 20 donors and for all donors, and explain what the sign tells you about shape.",
  "", '''# 1. stripchart(..., method = "stack") of the 20 donors
# 2. stem() of the 20 donors
# 3. mean - median for the 20 donors and for all donors (2 decimals)
# 4. Report (3 sentences as comments): shape, which center to use, why
''',
  '''x20 <- donors1_20$totalGivingAmount
stripchart(x20, method = "stack", pch = 16, xlab = "Total $ given")
stem(x20)
gap20  <- round(mean(x20) - median(x20), 2)
gapall <- round(mean(donors$totalGivingAmount) - median(donors$totalGivingAmount), 2)
gap20; gapall
# Both gaps are positive: the mean sits above the median.
# A few large totals form a long right tail, so the distribution is right-skewed.
# The median is the better "typical" value for these donors.''',
  [("gap20", "gap20", 2), ("gapall", "gapall", 2)],
  "最初の20人の寄付総額で、平均 − 中央値 <code>gap20</code>、全員での平均 − 中央値 <code>gapall</code>（どちらも小数第2位）を求めてください。",
  "正なら平均が中央値より大きい＝右に歪んでいる目安。",
  "最初の20人で {gap20}、全体で {gapall}。どちらも正なので右に歪んだ分布です。"),
]

C = [
Q(11, 1, "Five-number summary and fences", "5数要約とフェンス（見本）",
  "Compute the five-number summary of age, the IQR and the 1.5·IQR fences.",
  "", "",
  '''# === Complete example — read and run ===
summary(donors$age)
q1 <- quantile(donors$age, 0.25, na.rm = TRUE)
q3 <- quantile(donors$age, 0.75, na.rm = TRUE)
iqr <- IQR(donors$age, na.rm = TRUE)
lower_fence <- q1 - 1.5 * iqr
upper_fence <- q3 + 1.5 * iqr
c(lower_fence, upper_fence)
boxplot(donors$age, horizontal = TRUE, col = "lightblue", xlab = "Age")''',
  [("iqr", "iqr", 0), ("lower_fence", "lower_fence", 1)],
  "年齢の IQR と下のフェンス（Q1 − 1.5 × IQR、小数第1位）を求めてください（見本を実行）。",
  "<code>IQR()</code> と <code>quantile()</code> にも <code>na.rm = TRUE</code>。",
  "IQR = {iqr}、下のフェンス = {lower_fence}。箱ひげ図の左側の点が、このフェンスより下の外れ値です。"),
Q(12, 2, "Outliers in total giving", "寄付総額の外れ値（穴埋め）",
  "Find Q3, the IQR, the upper fence and the number of high outliers in `totalGivingAmount`.",
  "", '''x <- donors$totalGivingAmount
q3  <- quantile(x, ___)
iqr <- ___(x)
upper <- q3 + ___ * iqr
n_high <- sum(x ___ upper)
upper; n_high''',
  '''x <- donors$totalGivingAmount
q3  <- quantile(x, 0.75)
iqr <- IQR(x)
upper <- q3 + 1.5 * iqr
n_high <- sum(x > upper)
upper; n_high''',
  [("upper", "upper", 1), ("n_high", "n_high", 0)],
  "寄付総額の上のフェンス <code>upper</code>（小数第1位）と、それを超える外れ値の数 <code>n_high</code> を求めてください。",
  "上のフェンス = Q3 + 1.5 × IQR。",
  "上のフェンスは {upper}、外れ値は {n_high} 件。右に長い裾のため上の外れ値がたくさんあります。"),
Q(13, 3, "Standard deviation by hand", "標準偏差を手で（自由記述）",
  "For `x <- c(4, 8, 6, 5, 3, 10)`, compute the population SD (divide by n) and the sample SD (divide by n − 1) step by step, and check the second one with `sd()`. Round to 3 decimals.",
  "", '''# Write all your code here
''',
  '''x <- c(4, 8, 6, 5, 3, 10)
dev <- x - mean(x)
pop_sd  <- round(sqrt(sum(dev^2) / length(x)), 3)
samp_sd <- round(sqrt(sum(dev^2) / (length(x) - 1)), 3)
pop_sd; samp_sd
round(sd(x), 3)''',
  [("pop_sd", "pop_sd", 3), ("samp_sd", "samp_sd", 3)],
  "<code>x &lt;- c(4, 8, 6, 5, 3, 10)</code> の母集団の標準偏差 <code>pop_sd</code>（n で割る）と標本標準偏差 <code>samp_sd</code>（n − 1 で割る）を小数第3位まで求めてください。",
  "偏差 → 2乗 → 合計 → 割る → 平方根。R の <code>sd()</code> は n − 1。",
  "母集団 {pop_sd}、標本 {samp_sd}（= <code>sd(x)</code>）。"),
Q(14, 4, "Which machine is more consistent?", "どちらの機械が安定？（シナリオ1）",
  "Two machines fill 500 ml bottles. Compare their means, SDs and IQRs and decide which machine is more consistent.",
  "machine_a <- c(498, 502, 501, 499, 500, 503, 497, 500, 501, 499)\nmachine_b <- c(490, 510, 505, 495, 500, 512, 488, 503, 497, 500)",
  '''# 1. Mean of each machine
# 2. SD of each machine (2 decimals)
# 3. IQR of each machine
# 4. Side-by-side boxplot
# 5. Conclusion (comment):
''',
  '''c(mean(machine_a), mean(machine_b))
sd_a <- round(sd(machine_a), 2)
sd_b <- round(sd(machine_b), 2)
c(IQR(machine_a), IQR(machine_b))
boxplot(machine_a, machine_b, names = c("A", "B"), ylab = "ml")
sd_a; sd_b
# Conclusion: both average 500 ml, but A has a much smaller spread, so A is more consistent.''',
  [("sd_a", "sd_a", 2), ("sd_b", "sd_b", 2)],
  "500 ml を目標に充填する2台の機械です。機械 A と B の標準偏差 <code>sd_a</code>・<code>sd_b</code>（小数第2位）を求め、どちらが安定しているか判断してください。",
  "平均が同じでも、ばらつき（SD・IQR）で品質は変わります。",
  "どちらも平均 500 ml。SD は A が {sd_a}、B が {sd_b} で、A の方が安定しています。"),
Q(15, 5, "Gifts by area", "地域ごとの寄付回数（シナリオ2）",
  "Compare `numberGifts` across urbanicity groups with a comparative boxplot and `tapply()`. Report the median and IQR for urban and rural donors and write a 3-sentence summary.",
  "", '''# 1. boxplot(numberGifts ~ urbanicity, data = donors)
# 2. Median of numberGifts in each group with tapply()
# 3. IQR in each group with tapply()
# 4. Summary (3 sentences as comments):
''',
  '''boxplot(numberGifts ~ urbanicity, data = donors, las = 1, col = "lightblue")
meds <- tapply(donors$numberGifts, donors$urbanicity, median)
iqrs <- tapply(donors$numberGifts, donors$urbanicity, IQR)
meds; iqrs
med_urban <- meds[["urban"]]
med_rural <- meds[["rural"]]
iqr_urban <- iqrs[["urban"]]
# Summary: the groups have similar medians and spreads.
# Every group has many high outliers (very frequent givers).
# Urbanicity alone does not separate frequent and infrequent donors much.''',
  [("med_urban", "med_urban", 0), ("med_rural", "med_rural", 0), ("iqr_urban", "iqr_urban", 0)],
  "<code>tapply()</code> で地域ごとの寄付回数の中央値と IQR を求め、urban の中央値 <code>med_urban</code>、rural の中央値 <code>med_rural</code>、urban の IQR <code>iqr_urban</code> を入力してください。",
  "<code>tapply(値, グループ, 関数)</code> でグループごとに計算できます。",
  "中央値は urban {med_urban}、rural {med_rural}、urban の IQR は {iqr_urban}。地域による差は小さめです。"),
]

D = [
Q(16, 1, "The empirical rule", "経験則（見本）",
  "Check the 68-95-99.7 rule for IQ ~ N(100, 15) with `pnorm()`.",
  "", "",
  '''# === Complete example — read and run ===
within1 <- pnorm(115, 100, 15) - pnorm(85, 100, 15)
within2 <- pnorm(130, 100, 15) - pnorm(70, 100, 15)
within3 <- pnorm(145, 100, 15) - pnorm(55, 100, 15)
round(c(within1, within2, within3), 4)
curve(dnorm(x, 100, 15), from = 40, to = 160, xlab = "IQ", ylab = "")
abline(v = c(85, 115), col = "red")''',
  [("within1", "within1", 4)],
  "IQ ~ N(100, 15) で 85〜115 に入る割合 <code>within1</code>（小数第4位）を求めてください（見本を実行）。",
  "区間の確率は「上の累積 − 下の累積」。",
  "±1σ に {within1}（約 68%）。±2σ は約 95%、±3σ は約 99.7% です。"),
Q(17, 2, "Comparing two tests with z", "z で2つのテストを比べる（穴埋め）",
  "English: 82 (mean 70, SD 8). Math: 90 (mean 85, SD 4). Which result is better relative to the class?",
  "", '''z_eng  <- (82 - ___) / ___
z_math <- (___ - 85) / ___
c(z_eng, z_math)''',
  '''z_eng  <- (82 - 70) / 8
z_math <- (90 - 85) / 4
c(z_eng, z_math)''',
  [("z_eng", "z_eng", 2), ("z_math", "z_math", 2)],
  "英語 82 点（平均 70、SD 8）と数学 90 点（平均 85、SD 4）の z スコア <code>z_eng</code>・<code>z_math</code>（小数第2位）を求めてください。",
  "z = (値 − 平均) ÷ SD。",
  "英語 {z_eng}、数学 {z_math}。素点は数学が高いが、相対的には英語の方が良い成績です。"),
Q(18, 3, "Unusually frequent donors", "とても多く寄付する人（自由記述）",
  "Compute the z-score of a donor with 31 gifts, then count how many donors have |z| > 3 for `numberGifts`.",
  "", '''# Write all your code here
''',
  '''m <- mean(donors$numberGifts); s <- sd(donors$numberGifts)
z31 <- round((31 - m) / s, 2)
z_all <- (donors$numberGifts - m) / s
n_extreme <- sum(abs(z_all) > 3)
z31; n_extreme''',
  [("z31", "z31", 2), ("n_extreme", "n_extreme", 0)],
  "寄付回数 31 回の人の z スコア <code>z31</code>（小数第2位）と、|z| &gt; 3 の人数 <code>n_extreme</code> を求めてください。",
  "ベクトル全体を一度に標準化できます：<code>(x - m) / s</code>。",
  "31 回は z = {z31}。|z| &gt; 3 は {n_extreme} 人。"),
Q(19, 4, "Marathon times", "マラソンのタイム（シナリオ1）",
  "Runner A ran 195 min in a race with mean 240 and SD 30. Runner B ran 175 min in a race with mean 210 and SD 20. Lower times are better. Who did better relative to their race?",
  "", '''# 1. z-score for each runner (2 decimals)
# 2. Which z is better here? (lower time = better)
# 3. Conclusion (comment):
''',
  '''z_a <- round((195 - 240) / 30, 2)
z_b <- round((175 - 210) / 20, 2)
z_a; z_b
# Conclusion: B's z is more negative, so B was relatively faster.''',
  [("z_a", "z_a", 2), ("z_b", "z_b", 2)],
  "ランナー A（平均 240・SD 30 の大会で 195 分）と B（平均 210・SD 20 の大会で 175 分）の z スコア <code>z_a</code>・<code>z_b</code>（小数第2位）を求めてください。",
  "タイムは低いほど良いので、より負の z が良い成績。",
  "A は {z_a}、B は {z_b}。B の方が相対的に速いです。"),
Q(20, 5, "Is numberGifts normal?", "寄付回数は正規分布？（シナリオ2）",
  "Standardize `numberGifts` with `scale()`. Check the new mean and SD, compute the share within ±1 SD and compare it with the empirical rule's 68%. Write 3 sentences on whether the variable is normal.",
  "", '''# 1. z <- as.vector(scale(...))
# 2. mean and sd of z (round)
# 3. proportion with |z| <= 1 (3 decimals)
# 4. histogram of z
# 5. Report (3 sentences as comments):
''',
  '''z <- as.vector(scale(donors$numberGifts))
round(c(mean(z), sd(z)), 3)
within_1sd <- round(mean(abs(z) <= 1), 3)
within_1sd
hist(z, breaks = 50, col = "lightblue", main = "Standardized numberGifts")
# Standardizing gives mean 0 and SD 1 but does not change the shape.
# The share within 1 SD differs from 68% and the histogram has a long right tail.
# numberGifts is right-skewed, so the empirical rule should not be used for it.''',
  [("within_1sd", "within_1sd", 3)],
  "<code>scale()</code> で寄付回数を標準化し、|z| ≤ 1 に入る割合 <code>within_1sd</code>（小数第3位）を求め、経験則の 68% と比べてください。",
  "<code>mean(abs(z) &lt;= 1)</code> で割合が出ます。",
  "±1SD に {within_1sd}。68% とずれ、ヒストグラムも右に歪んでいるので正規分布ではありません（標準化しても形は変わらない）。"),
]

CARD = '''╔══════════════════════════════════════════════════════╗
║  M2 QUICK REFERENCE                                  ║
║  mean(x, na.rm = TRUE)  median(x)  mean(x, trim=.1)  ║
║  table(x)  proportions(table(x))  barplot(table(x))  ║
║  proportions(table(a, b), margin = 1)   row %        ║
║  hist(x)  stripchart(x, method='stack')  stem(x)     ║
║  summary(x)  quantile(x, .25)  IQR(x)  range(x)      ║
║  fences: Q1 - 1.5*IQR   Q3 + 1.5*IQR                 ║
║  boxplot(y ~ group, data = df)  tapply(y, g, median) ║
║  sd(x) (n-1)   var(x)                                ║
║  pnorm(q, mean, sd)  68-95-99.7 within 1/2/3 SD      ║
║  z = (x - mean) / sd     scale(x)                    ║
╚══════════════════════════════════════════════════════╝'''

MOD = dict(key="m2", short="550 M2", name_ja="記述統計",
           title="550 M2 — Descriptive Statistics: R Coding Practice (20 Questions)",
           file="m2_practice_v1.Rmd", folder=SRC + "/Module ２", wd=SRC + "/Module ２",
           data_note="Uses `donors.csv` (Brightspace). Save it in the same folder as this notebook and run Q1 first.",
           data_note_ja="📂 <code>donors.csv</code>（Brightspace で配布）を使います。ノートブックと同じフォルダに置き、最初に Q1 のデータ読み込みを実行してください。",
           lessons_ja='<a href="m2_center.html">平均・中央値</a>（Topic A）・<a href="m2_graphs.html">基本のグラフ</a>（B）・<a href="m2_spread.html">箱ひげ図・IQR</a>／<a href="m2_sd_normal.html">標準偏差</a>（C）・<a href="m2_sd_normal.html">正規分布</a>／<a href="m2_z.html">z スコア</a>（D）',
           topics=[("Measures of Center", A), ("Graphs & Categorical Data", B),
                   ("Measures of Spread", C), ("Normal Distribution & z-scores", D)],
           card=CARD, web="ex_550_m2.html")
MOD["questions"] = A + B + C + D
