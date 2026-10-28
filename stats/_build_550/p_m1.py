"""M1 practice: R basics, vectors, data frames, CSV & levels of measurement."""
from practice_gen import Q, SRC

A = [
Q(1, 1, "Circumference of the Earth", "地球の円周（見本）",
  "Store the Earth's radius (3,963 miles) and compute the circumference and the surface area, rounded to 2 decimals.",
  "",
  "",
  '''# === Complete example — read and run ===
# Step 1: store values with <-
radius <- 3963
# Step 2: use the built-in constant pi
circumference <- 2 * pi * radius
area <- 4 * pi * radius^2
# Step 3: round and print
round(circumference, 2)
round(area, 2)''',
  [("circumference", "circumference", 2)],
  "地球の半径を 3,963 マイルとして、円周 <code>2 * pi * radius</code> を求め、小数第2位まで入力してください（ノートブックの見本を実行すれば出ます）。",
  "<code>pi</code> は R に組み込まれた円周率。<code>round(x, 2)</code> で丸めます。",
  "円周は {circumference} マイル。<code>&lt;-</code> で保存した値は名前で何度でも使えます。"),
Q(2, 2, "Order total with tax", "税込み合計（穴埋め）",
  "A notebook costs $12.50 and a school buys 40. Compute the subtotal and the total with 8% tax, rounded to 2 decimals.",
  "",
  '''price <- 12.50
qty   <- 40
subtotal <- ___ * ___
total    <- round(subtotal * ___, 2)   # add 8% tax
total''',
  '''price <- 12.50
qty   <- 40
subtotal <- price * qty
total    <- round(subtotal * 1.08, 2)   # add 8% tax
total''',
  [("total", "total", 2)],
  "1冊 \\$12.50 のノートを 40 冊買います。小計 <code>subtotal</code> と、8% の税を加えた合計 <code>total</code>（小数第2位）を求めてください。",
  "8% 加えるには 1.08 を掛けます。",
  "小計 500、合計 {total}。<code>___</code> を埋めるときも、演算子の前後に空白を入れる書き方を守りましょう。"),
Q(3, 3, "Fahrenheit to Celsius", "華氏を摂氏に（自由記述）",
  "Convert 98.6 °F to Celsius with C = (F − 32) × 5 / 9. Store it as `temp_c` and round to 1 decimal. Also compute `sqrt(abs(-50))` rounded to 3 decimals and store it as `root`.",
  "",
  '''# Write all your code here
''',
  '''temp_f <- 98.6
temp_c <- round((temp_f - 32) * 5 / 9, 1)
temp_c
root <- round(sqrt(abs(-50)), 3)
root''',
  [("temp_c", "temp_c", 1), ("root", "root", 3)],
  "98.6°F を摂氏に変換して <code>temp_c</code>（小数第1位）に保存し、<code>sqrt(abs(-50))</code> を小数第3位で <code>root</code> に保存してください。",
  "かっこを忘れると計算の順番が変わります：<code>(temp_f - 32) * 5 / 9</code>。",
  "temp_c = {temp_c}、root = {root}。関数は内側（abs）から先に計算されます。"),
Q(4, 4, "Café daily profit", "カフェの1日の利益（シナリオ1）",
  "A café sold 230 coffees at $4.25 and 85 cakes at $5.50 today. Costs are 35% of revenue. Compute revenue and profit (2 decimals).",
  "",
  '''# 1. Store prices and quantities in well-named variables
# 2. Compute revenue
# 3. Compute cost (35% of revenue) and profit
# 4. Conclusion (comment): what was today's profit?
''',
  '''coffee_price <- 4.25; coffee_qty <- 230
cake_price   <- 5.50; cake_qty   <- 85
revenue <- coffee_price * coffee_qty + cake_price * cake_qty
cost    <- 0.35 * revenue
profit  <- round(revenue - cost, 2)
revenue
profit
# Conclusion: revenue was $1,445 and today's profit was $939.25.''',
  [("revenue", "revenue", 2), ("profit", "profit", 2)],
  "コーヒー \\$4.25 を 230 杯、ケーキ \\$5.50 を 85 個売りました。費用は売上の 35%。売上 <code>revenue</code> と利益 <code>profit</code>（小数第2位）を求めてください。",
  "利益 = 売上 − 0.35 × 売上 = 0.65 × 売上。",
  "売上 {revenue}、利益 {profit}。変数名を意味のある名前にすると、あとで読み返しやすくなります。"),
Q(5, 5, "Compound vs simple interest", "複利と単利（シナリオ2）",
  "You invest $5,000 at 3.5% per year for 10 years. Compare compound interest A = P(1 + r)^n with simple interest P(1 + r·n). Report both and the difference (2 decimals) and write a 2-sentence recommendation.",
  "",
  '''# 1. Store P, r, n
# 2. Compute the compound amount
# 3. Compute the simple-interest amount
# 4. Compute the difference
# 5. Report (2 sentences as comments):
# Result:
# Recommendation:
''',
  '''P <- 5000; r <- 0.035; n <- 10
compound <- round(P * (1 + r)^n, 2)
simple   <- round(P * (1 + r * n), 2)
difference <- round(compound - simple, 2)
compound; simple; difference
# Result: after 10 years compound interest gives $7,052.99, simple gives $6,750.
# Recommendation: choose the compounding account; it earns about $303 more.''',
  [("compound", "compound", 2), ("difference", "difference", 2)],
  "\\$5,000 を年利 3.5% で 10 年運用します。複利 <code>P * (1 + r)^n</code> と単利 <code>P * (1 + r * n)</code> を計算し、複利の金額と差額（小数第2位）を入力してください。",
  "べき乗は <code>^</code>。<code>(1 + r)^n</code> のかっこを忘れずに。",
  "複利 {compound}、差額 {difference}。報告は「結果→おすすめ」の2文で、数字を入れて書きましょう。"),
]

B = [
Q(6, 1, "A week of temperatures", "1週間の気温（見本）",
  "Store 7 daily high temperatures in a vector and summarise them.",
  "temps <- c(24.5, 26.1, 23.8, 27.4, 28.0, 25.2, 22.9)\ndays  <- c(\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", \"Sat\", \"Sun\")",
  "",
  '''# === Complete example — read and run ===
length(temps)
mean(temps)
max(temps)
days[which.max(temps)]        # the hottest day
temps > 25                    # logical vector
hot_days <- sum(temps > 25)   # TRUE counts as 1
hot_days
days[temps > 25]              # names of the hot days''',
  [("hot_days", "hot_days", 0)],
  "7日分の最高気温のベクトルで、25℃ を超えた日数 <code>hot_days</code> を求めてください（見本を実行）。",
  "<code>sum(temps &gt; 25)</code> は TRUE の個数を数えます。",
  "25℃ 超えは {hot_days} 日。<code>days[temps &gt; 25]</code> で曜日名も取り出せます。"),
Q(7, 2, "Step counter", "歩数計（穴埋め）",
  "Find the weekend total (days 6–7) and how many days reached 8,000 steps.",
  "steps <- c(6500, 9200, 8100, 4300, 10050, 12000, 7300)",
  '''weekend_total <- sum(steps[___])
goal_days <- sum(steps ___ 8000)
weekend_total
goal_days''',
  '''weekend_total <- sum(steps[6:7])
goal_days <- sum(steps >= 8000)
weekend_total
goal_days''',
  [("weekend_total", "weekend_total", 0), ("goal_days", "goal_days", 0)],
  "1週間の歩数です。週末（6・7日目）の合計 <code>weekend_total</code> と、8,000 歩以上の日数 <code>goal_days</code> を求めてください。",
  "連番の添字は <code>6:7</code>、「以上」は <code>&gt;=</code>。",
  "週末の合計 {weekend_total} 歩、目標達成は {goal_days} 日。"),
Q(8, 3, "Quiz percentages", "小テストの得点率（自由記述）",
  "Ten quiz scores are out of 80. Convert them to percentages, then find how many students scored at least 70% and the mean percentage (1 decimal).",
  "scores <- c(56, 72, 64, 49, 80, 68, 59, 75, 61, 44)",
  '''# Write all your code here
''',
  '''pct <- scores / 80 * 100
n_pass <- sum(pct >= 70)
mean_pct <- round(mean(pct), 1)
n_pass
mean_pct''',
  [("n_pass", "n_pass", 0), ("mean_pct", "mean_pct", 1)],
  "80 点満点の小テスト10人分です。得点率（%）に変換し、70% 以上の人数 <code>n_pass</code> と平均得点率 <code>mean_pct</code>（小数第1位）を求めてください。",
  "ベクトル全体に <code>/ 80 * 100</code> を一度に適用できます（ベクトル化演算）。",
  "70% 以上は {n_pass} 人、平均は {mean_pct}%。"),
Q(9, 4, "Monthly revenue", "月別の売上（シナリオ1）",
  "A shop records units sold for 12 months and a price that rose in July. Compute monthly revenue, the total, and the months whose revenue is above the average.",
  "units <- c(120, 95, 130, 150, 160, 140, 110, 105, 170, 180, 200, 230)\nprice <- c(rep(15, 6), rep(17, 6))\nmonths <- month.abb",
  '''# 1. Compute the revenue for each month (vectorized)
# 2. Compute the total revenue
# 3. Which months are above the average revenue? How many?
# 4. Conclusion (comment):
''',
  '''revenue <- units * price
total_revenue <- sum(revenue)
above <- months[revenue > mean(revenue)]
n_above <- length(above)
total_revenue
above
# Conclusion: Sep-Dec are above average; total revenue was $28,840.''',
  [("total_revenue", "total_revenue", 0), ("n_above", "n_above", 0)],
  "12か月の販売数と、7月に値上げした単価のベクトルです。月別売上を作り、年間売上 <code>total_revenue</code> と、平均を上回った月の数 <code>n_above</code> を求めてください。",
  "<code>units * price</code> は同じ位置どうしで掛け算されます。<code>month.abb</code> は R 組み込みの月の略称。",
  "年間売上は {total_revenue}、平均を上回ったのは {n_above} か月。"),
Q(10, 5, "Survey answers and data types", "アンケートと型（シナリオ2）",
  "Survey answers arrive as text. Convert them to logical, find the proportion of 'yes', then explore what happens when types are mixed. Write a 2-sentence note on coercion.",
  "answers <- c(\"yes\", \"no\", \"yes\", \"yes\", \"no\", \"yes\", \"no\", \"yes\", \"yes\", \"no\")\nmixed <- c(10, \"20\", 30)",
  '''# 1. Convert answers to a logical vector (TRUE = "yes")
# 2. Proportion of yes (use mean on the logical vector)
# 3. What is class(mixed)? Why?
# 4. Convert mixed to numbers and sum them
# 5. Note (2 sentences as comments):
''',
  '''said_yes <- answers == "yes"
prop_yes <- mean(said_yes)
prop_yes
class(mixed)                 # "character": one text value coerces all
total_mixed <- sum(as.numeric(mixed))
total_mixed
# Note: a vector holds one type, so one "20" turned every value into text.
# Use as.numeric() to convert explicitly before calculating.''',
  [("prop_yes", "prop_yes", 1), ("total_mixed", "total_mixed", 0)],
  "文字で届いたアンケート回答です。\"yes\" を TRUE にした論理ベクトルの平均で賛成の割合 <code>prop_yes</code>（小数第1位）を、また <code>mixed</code> を数値に変換した合計 <code>total_mixed</code> を求めてください。",
  "<code>answers == \"yes\"</code> は論理ベクトル。<code>mean()</code> で TRUE の割合。<code>as.numeric()</code> で数値へ。",
  "賛成は {prop_yes}、合計は {total_mixed}。<code>class(mixed)</code> は \"character\"：1つの文字が混じると全体が文字になります（型の強制変換）。"),
]

C = [
Q(11, 1, "Build a data frame", "データフレームを作る（見本）",
  "Combine vectors into a data frame and inspect it.",
  "",
  "",
  '''# === Complete example — read and run ===
students <- data.frame(
  name  = c("Ana", "Ben", "Chen", "Dee", "Eli", "Fay"),
  class = c("A", "B", "A", "B", "A", "B"),
  score = c(78, 85, 62, 91, 70, 88),
  hours = c(3, 5, 1, 6, 2, 4))
str(students)
summary(students$score)
mean_score <- mean(students$score)
mean_score
students[students$hours > 3, ]     # rows: more than 3 hours of study''',
  [("mean_score", "mean_score", 2)],
  "6人の生徒のデータフレームを作り、点数の平均 <code>mean_score</code>（小数第2位）を求めてください（見本を実行）。",
  "<code>students$score</code> は列をベクトルとして取り出します。",
  "平均は {mean_score}。<code>[行, 列]</code> の行に条件を入れると、その条件の行だけ取り出せます。"),
Q(12, 2, "Product stock", "商品在庫（穴埋め）",
  "Select products that cost more than $100 and find their average stock.",
  "products <- data.frame(\n  item  = c(\"desk\", \"lamp\", \"chair\", \"shelf\", \"sofa\", \"rug\"),\n  price = c(220, 35, 140, 95, 650, 120),\n  stock = c(12, 40, 25, 18, 4, 9))",
  '''pricey <- products[products$___ > 100, ___]
n_pricey <- nrow(___)
mean_stock <- mean(pricey$___)
n_pricey
mean_stock''',
  '''pricey <- products[products$price > 100, ]
n_pricey <- nrow(pricey)
mean_stock <- mean(pricey$stock)
n_pricey
mean_stock''',
  [("n_pricey", "n_pricey", 0), ("mean_stock", "mean_stock", 2)],
  "価格 \\$100 超の商品を取り出し、その数 <code>n_pricey</code> と在庫の平均 <code>mean_stock</code>（小数第2位）を求めてください。",
  "行を条件で選び、列は空欄（すべて）：<code>products[条件, ]</code>。カンマを忘れずに。",
  "該当は {n_pricey} 商品、平均在庫 {mean_stock}。"),
Q(13, 3, "Exploring mtcars", "mtcars を調べる（自由記述）",
  "Use the built-in `mtcars` data: how many rows and columns? What is the mean mpg of 6-cylinder cars (2 decimals)? How many cars have a manual transmission (`am == 1`)?",
  "",
  '''# Write all your code here
''',
  '''dim(mtcars)
mpg6 <- round(mean(mtcars$mpg[mtcars$cyl == 6]), 2)
n_manual <- sum(mtcars$am == 1)
mpg6
n_manual''',
  [("mpg6", "mpg6", 2), ("n_manual", "n_manual", 0)],
  "組み込みデータ <code>mtcars</code> で、6気筒車の燃費（mpg）の平均 <code>mpg6</code>（小数第2位）と、マニュアル車（<code>am == 1</code>）の台数 <code>n_manual</code> を求めてください。",
  "列のベクトルに論理添字：<code>mtcars$mpg[mtcars$cyl == 6]</code>。",
  "6気筒の平均燃費は {mpg6} mpg、マニュアル車は {n_manual} 台（全 32 台・11 列）。"),
Q(14, 4, "Employee bonus", "社員のボーナス（シナリオ1）",
  "HR gives a 5% bonus. Build the data frame, add a `bonus` column, then report the mean salary in Sales and the total bonus cost.",
  "staff <- data.frame(\n  name   = c(\"Kim\", \"Lee\", \"Max\", \"Noa\", \"Oto\", \"Pia\", \"Ray\", \"Sam\"),\n  dept   = c(\"Sales\", \"IT\", \"Sales\", \"HR\", \"IT\", \"Sales\", \"HR\", \"IT\"),\n  salary = c(52000, 68000, 49000, 45000, 72000, 55000, 47000, 63000))",
  '''# 1. Add a new column bonus = 5% of salary
# 2. Mean salary of the Sales department
# 3. Total bonus cost
# 4. Conclusion (comment):
''',
  '''staff$bonus <- staff$salary * 0.05
sales_mean <- mean(staff$salary[staff$dept == "Sales"])
total_bonus <- sum(staff$bonus)
sales_mean
total_bonus
# Conclusion: the bonus costs $22,550 in total.''',
  [("sales_mean", "sales_mean", 0), ("total_bonus", "total_bonus", 0)],
  "社員8人のデータに、給与の 5% の <code>bonus</code> 列を追加します。営業部（Sales）の平均給与 <code>sales_mean</code> と、ボーナス総額 <code>total_bonus</code> を求めてください。",
  "新しい列は <code>staff$bonus &lt;- …</code> で作れます。",
  "営業部の平均給与は {sales_mean}、ボーナス総額は {total_bonus}。"),
Q(15, 5, "Air quality with missing values", "airquality と欠損値（シナリオ2）",
  "Use the built-in `airquality` data. Count the missing Ozone values, compute the mean Ozone (ignoring NA), the mean July temperature, and the number of days with Ozone above 100. Write a 3-sentence summary.",
  "",
  '''# 1. How many NA values are in Ozone?
# 2. Mean Ozone, ignoring NA (2 decimals)
# 3. Mean Temp in July (Month == 7), 2 decimals
# 4. How many days had Ozone > 100? (careful with NA!)
# 5. Summary (3 sentences as comments):
''',
  '''n_na <- sum(is.na(airquality$Ozone))
mean_ozone <- round(mean(airquality$Ozone, na.rm = TRUE), 2)
july_temp <- round(mean(airquality$Temp[airquality$Month == 7]), 2)
high_days <- sum(airquality$Ozone > 100, na.rm = TRUE)
n_na; mean_ozone; july_temp; high_days
# Summary: 37 of 153 Ozone values are missing, so we used na.rm = TRUE.
# Mean ozone was about 42 ppb; July averaged about 84 degrees F.
# Only 7 days had ozone above 100.''',
  [("n_na", "n_na", 0), ("mean_ozone", "mean_ozone", 2), ("high_days", "high_days", 0)],
  "組み込みデータ <code>airquality</code> で、Ozone の欠損数 <code>n_na</code>、欠損を除いた平均 <code>mean_ozone</code>（小数第2位）、Ozone が 100 を超えた日数 <code>high_days</code> を求めてください。",
  "<code>sum(is.na(x))</code> で NA の数。条件の合計にも <code>na.rm = TRUE</code> が必要です。",
  "欠損 {n_na} 件、平均 Ozone {mean_ozone}、100 超は {high_days} 日。NA があると <code>sum(x &gt; 100)</code> は NA になる点に注意。"),
]

D = [
Q(16, 1, "Load donors.csv", "donors.csv を読み込む（見本）",
  "Read the donors data and inspect its size and variable types.",
  "",
  "",
  '''# === Complete example — read and run ===
donors <- read.csv("donors.csv")   # the file must be in your working directory
n_rows <- nrow(donors)
n_rows
ncol(donors)
str(donors[, c("age", "state", "urbanicity", "incomeRating", "totalGivingAmount")])
table(donors$urbanicity)''',
  [("n_rows", "n_rows", 0)],
  "<code>donors.csv</code> を読み込み、行数 <code>n_rows</code> を確認してください（見本を実行）。",
  "<code>read.csv()</code> が失敗するときは、<code>getwd()</code> と <code>list.files()</code> で作業ディレクトリを確認。",
  "{n_rows} 行。<code>str()</code> で各列の型（int / chr / num）も確認しましょう。"),
Q(17, 2, "Missing ages", "年齢の欠損（穴埋め）",
  "Count the missing ages, compute the mean age without them, and the proportion of female donors.",
  "",
  '''n_missing <- sum(is.na(donors$___))
mean_age  <- round(mean(donors$age, na.rm = ___), 2)
prop_female <- round(mean(donors$gender == "___", na.rm = TRUE), 3)
n_missing; mean_age; prop_female''',
  '''n_missing <- sum(is.na(donors$age))
mean_age  <- round(mean(donors$age, na.rm = TRUE), 2)
prop_female <- round(mean(donors$gender == "female", na.rm = TRUE), 3)
n_missing; mean_age; prop_female''',
  [("n_missing", "n_missing", 0), ("mean_age", "mean_age", 2), ("prop_female", "prop_female", 3)],
  "<code>donors</code> の年齢の欠損数 <code>n_missing</code>、欠損を除いた平均年齢 <code>mean_age</code>（小数第2位）、性別が記録されている人のうち女性の割合 <code>prop_female</code>（小数第3位）を求めてください。",
  "論理ベクトルの <code>mean()</code> は TRUE の割合です。gender にも NA があるので <code>na.rm = TRUE</code> を付けます。",
  "欠損 {n_missing} 件、平均 {mean_age} 歳、女性の割合 {prop_female}。"),
Q(18, 3, "Levels of measurement in donors", "donors の測定水準（自由記述）",
  "For `state`, `socioEconomicStatus`, `age` and `incomeRating`, decide the level of measurement (write it as a comment). Then count the number of different states and the number of 'highest' socio-economic status donors.",
  "",
  '''# Write all your code here
# state:               (nominal / ordinal / interval / ratio?)
# socioEconomicStatus:
# age:
# incomeRating:
''',
  '''# state: nominal | socioEconomicStatus: ordinal | age: ratio | incomeRating: ordinal (coded 1-7)
n_states <- length(unique(donors$state))
n_highest <- sum(donors$socioEconomicStatus == "highest", na.rm = TRUE)
n_states
n_highest''',
  [("n_states", "n_states", 0), ("n_highest", "n_highest", 0)],
  "4つの変数の測定水準をコメントで書いたうえで、州の種類の数 <code>n_states</code> と、socioEconomicStatus が \"highest\" の人数 <code>n_highest</code> を求めてください。",
  "<code>length(unique(x))</code> で異なる値の数。incomeRating は数字でも順序尺度です。",
  "州は {n_states} 種類、highest は {n_highest} 人。state＝名義、socioEconomicStatus・incomeRating＝順序、age＝比率。"),
Q(19, 4, "Who responded to the mailing?", "郵送に反応した人（シナリオ1）",
  "How many donors responded to the mailing, what proportion is that, and do responders give more in total on average?",
  "",
  '''# 1. Number of donors with respondedMailing == TRUE
# 2. Proportion who responded (3 decimals)
# 3. Mean totalGivingAmount for responders and non-responders (2 decimals)
# 4. Conclusion (comment):
''',
  '''n_resp <- sum(donors$respondedMailing)
prop_resp <- round(mean(donors$respondedMailing), 3)
giving_yes <- round(mean(donors$totalGivingAmount[donors$respondedMailing]), 2)
giving_no  <- round(mean(donors$totalGivingAmount[!donors$respondedMailing]), 2)
n_resp; prop_resp; giving_yes; giving_no
# Conclusion: only about 5% responded; responders gave slightly more on average.''',
  [("n_resp", "n_resp", 0), ("prop_resp", "prop_resp", 3), ("giving_yes", "giving_yes", 2)],
  "郵送に反応した人数 <code>n_resp</code>、その割合 <code>prop_resp</code>（小数第3位）、反応した人の寄付総額の平均 <code>giving_yes</code>（小数第2位）を求めてください。",
  "<code>respondedMailing</code> はもともと論理型（TRUE/FALSE）。<code>!</code> で反転できます。",
  "反応 {n_resp} 人（{prop_resp}）。反応した人の平均寄付総額は {giving_yes}。"),
Q(20, 5, "incomeRating as an ordinal variable", "incomeRating を順序尺度として（シナリオ2）",
  "Treat `incomeRating` (1–7) as ordinal: make a frequency table, find the median rating, and the share of donors (with a rating) who are rated 5 or higher. Explain in 3 sentences why the mean is less meaningful here.",
  "",
  '''# 1. Frequency table of incomeRating
# 2. Median rating (ignore NA)
# 3. Proportion rated 5+ among donors with a rating (3 decimals)
# 4. Convert to an ordered factor with factor(..., ordered = TRUE) and check levels()
# 5. Explanation (3 sentences as comments):
''',
  '''table(donors$incomeRating)
med_rating <- median(donors$incomeRating, na.rm = TRUE)
rated <- donors$incomeRating[!is.na(donors$incomeRating)]
prop_high <- round(mean(rated >= 5), 3)
inc_f <- factor(donors$incomeRating, ordered = TRUE)
levels(inc_f)
med_rating; prop_high
# The numbers 1-7 are codes for ordered income groups.
# The gaps between groups are not known to be equal, so a mean of 3.9 has little meaning.
# Counts, proportions and the median describe an ordinal variable better.''',
  [("med_rating", "med_rating", 0), ("prop_high", "prop_high", 3)],
  "incomeRating（1〜7）を順序尺度として扱い、中央値 <code>med_rating</code> と、評価のある人のうち 5 以上の割合 <code>prop_high</code>（小数第3位）を求めてください。",
  "NA を先に除く：<code>rated &lt;- x[!is.na(x)]</code>。",
  "中央値は {med_rating}、5 以上は {prop_high}。順序尺度は段階の間隔が等しいとは限らないので、平均より中央値や割合で要約します。"),
]

CARD = '''╔══════════════════════════════════════════════════════╗
║  M1 QUICK REFERENCE                                  ║
║  x <- 5            assign        x            print  ║
║  round(x, 2)  sqrt(x)  abs(x)  pi  ^ (power)         ║
║  v <- c(1, 2, 3)   vector        v[2]  v[2:3]        ║
║  v[c(1, 3)]        several       v[v > 1]  logical   ║
║  length(v)  sum(v > 1)  mean(v)  which.max(v)        ║
║  as.numeric()  class()  (one type per vector)        ║
║  df <- data.frame(a, b)          df$a   df[1, ]      ║
║  df[df$a > 1, ]  rows by condition  nrow() ncol()    ║
║  str(df)  summary(df)  names(df)  head(df)           ║
║  read.csv(\\"file.csv\\")  getwd()  list.files()          ║
║  sum(is.na(x))   mean(x, na.rm = TRUE)               ║
║  install.packages(\\"pkg\\") once / library(pkg) each    ║
╚══════════════════════════════════════════════════════╝'''

MOD = dict(key="m1", short="550 M1", name_ja="R入門・データフレーム・測定水準",
           title="550 M1 — R Basics, Vectors, Data Frames & Levels of Measurement: R Coding Practice (20 Questions)",
           file="m1_practice_v1.Rmd", folder=SRC + "/Module 1", wd=SRC + "/Module ２",
           data_note="Topic D uses `donors.csv` (Brightspace). Save it in the same folder as this notebook.",
           data_note_ja="📂 Topic D（Q16〜Q20）は <code>donors.csv</code>（Brightspace で配布）を使います。ノートブックと同じフォルダに置いてください。Topic A〜C はデータ不要（R 組み込みデータと自分で作るベクトル）。",
           lessons_ja='<a href="m1_rbasics.html">R の基本</a>（Topic A）・<a href="m1_vectors.html">ベクトル</a>（B）・<a href="m1_dataframe.html">データフレーム</a>（C）・<a href="m1_levels.html">測定水準</a>／<a href="m1_workflow.html">作業ディレクトリ</a>（D）',
           topics=[("R as a Calculator & Assignment", A), ("Vectors & Indexing", B),
                   ("Data Frames", C), ("CSV Files & Levels of Measurement", D)],
           card=CARD, web="ex_550_m1.html")
MOD["questions"] = A + B + C + D
