"""550 M2: 記述統計 — 5 lessons (donors data, real R output)."""
from lib550 import *
from c_m1 import r4ds

MOD = "550 M2"
LOAD = 'donors <- read.csv("donors.csv")\ndonors1_20 <- donors[1:20, ]'

# =============================================================== 1. center
def m2_center(P):
    L = dict(slug="m2_center", mod=MOD, icon="🎯", title="中心の指標：平均・中央値・トリム平均・最頻値",
             tag="M2 · Measures of Center — Mean, Statistics vs Parameters, Median, Trimmed Mean &amp; Mode",
             lead="データの「真ん中」を1つの数で表す方法を比べます。<strong>平均</strong>と <code>na.rm = TRUE</code>、<strong>統計量と母数</strong>（標本と母集団）、外れ値に強い<strong>中央値</strong>、その中間の<strong>トリム平均</strong>、形を示す<strong>最頻値</strong>です。",
             video="The Donors Dataset ／ Measures of Center: The Mean ／ Statistics vs Parameters &amp; Samples vs Populations ／ The Median ／ The Trimmed Mean &amp; Mode",
             unav=["① 平均と NA", "② 統計量と母数", "③ 中央値と頑健性", "④ トリム平均と最頻値"],
             terms=[("descriptive statistics", "記述統計", "データを要約して描写する数値・グラフ。"),
                    ("inferential statistics", "推測統計", "標本から母集団について推論する（信頼区間・検定）。"),
                    ("mean (x̄, μ)", "平均", "合計 ÷ 個数。標本は x̄、母集団は μ。"),
                    ("na.rm = TRUE", "欠損を除く", "NA を除いて計算する引数。"),
                    ("statistic / parameter", "統計量／母数", "標本から計算した値／母集団の真の値。"),
                    ("median", "中央値", "並べたときの真ん中の値。"),
                    ("resistant", "頑健（外れ値に強い）", "極端な値にあまり動かされない性質。"),
                    ("trimmed mean", "トリム平均", "両端を一定割合切り捨てた平均。"),
                    ("mode", "最頻値", "いちばん多く出る値。二峰性は bimodal。")],
             tip="平均は<strong>てこの釣り合う点</strong>、中央値は<strong>面積を半分に分ける点</strong>。外れ値や長い裾があると、平均だけが裾の方へ引っぱられる。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>① The Donors Dataset ／ Measures of Center: The Mean</li><li>② Statistics vs Parameters &amp; Sample vs Populations</li><li>③ Measures of Center: The Median</li><li>④ The Trimmed Mean &amp; the Mode</li></ul>')]
    b.append(unit(1, "平均と NA", "R が「計算しない」のは親切", f'''
  <p><strong>記述統計（descriptive statistics）</strong>は、データを数値やグラフで<strong>要約・描写</strong>することです。データを調べ始める段階は<strong>探索的データ分析（EDA）</strong>とも呼ばれます。まず <code>donors</code> の最初の20人を取り出します。</p>
  {P.R(LOAD + '\ndonors1_20$age')}
  <p><strong>平均（mean）</strong>は「合計 ÷ 個数」です。式で書くと <span style="white-space:nowrap">x̄ = Σxᵢ / n</span>。ところが <code>mean()</code> をそのまま使うと…</p>
  {P.R('mean(donors1_20$age)\nmean(donors1_20$age, na.rm = TRUE)')}
  <p>年齢に <code>NA</code>（欠損）が混じっているので、R は <code>NA</code> を返します。「データがまだきれいではない」と教えてくれているのです。<code>na.rm = TRUE</code>（NA を remove）で、欠損を除いた12人の平均 <strong>60.5 歳</strong>が出ます。</p>
  {warn('<code>length(donors1_20$age)</code> は NA を含めて 20 を返します。手計算するときは「合計 ÷ 20」ではなく「合計 ÷ <strong>NA でない個数</strong>（12）」です。<code>sum(!is.na(x))</code> で NA でない個数を数えられます。')}
'''))
    b.append(unit(2, "統計量と母数、標本と母集団", "x̄ で μ を推定する", f'''
  <p>最初の20人は<strong>標本（sample）</strong>、95,412人全体を<strong>母集団（population）</strong>と考えてみます。</p>
  {table(["", "標本 sample", "母集団 population"], [["計算した値の名前", "<strong>統計量</strong> statistic", "<strong>母数</strong> parameter"], ["平均の記号", "x̄（エックスバー）", "μ（ミュー）"], ["ふつうは", "手元にある", "わからない（推定したい）"]])}
  {P.R('mean(donors1_20$age, na.rm = TRUE)   # 統計量 x-bar\nmean(donors$age, na.rm = TRUE)       # 母数 mu')}
  <p>x̄ = 60.5、μ ≈ 61.61 で近い値です。ただしこれは<strong>運が良かった</strong>だけかもしれません。「最初の20行」は便宜的に選んだだけで、母集団を代表する保証がないからです。<strong>ランダム標本</strong>なら代表的になりやすいです。</p>
  {P.R('set.seed(550)\nrand20 <- donors[sample(nrow(donors), 20), ]\nmean(rand20$age, na.rm = TRUE)')}
  {note('📚 統計学の2本柱：<strong>記述統計</strong>（データを描写する）と<strong>推測統計</strong>（標本から母集団を推測する：信頼区間・仮説検定。M4 以降）。')}
'''))
    b.append(unit(3, "中央値と「外れ値への強さ」", "平均と中央値がずれるとき", f'''
  <p><strong>中央値（median）</strong>は、値を<strong>小さい順に並べた真ん中</strong>です。個数が偶数なら真ん中2つの平均です。</p>
  {P.R('median(c(1, 5, 7, 10, 12))\nmedian(c(1, 5, 7, 10))')}
  <p>最初の20人の寄付総額で、平均と中央値を比べます。</p>
  {P.R('mean(donors1_20$totalGivingAmount)\nmedian(donors1_20$totalGivingAmount)')}
  <p>平均 97.65 に対して中央値 62.5。大きく違うのは、200ドル超の寄付者が数人いるからです。<strong>ドットプロット</strong>（R では <code>stripchart()</code>）で見てみます。</p>
  {P.R('x <- donors1_20$totalGivingAmount\nstripchart(x, method = "stack", pch = 16, cex = 1.4, ylim = c(0, 3),\n           xlab = "Total $ given (first 20 donors)")\nabline(v = mean(x), col = "red", lwd = 2)       # mean\nabline(v = median(x), col = "darkgreen", lwd = 2) # median', plot=True, h=300)}
  <p>平均（赤）は右の大きな値に<strong>引っぱられ</strong>、中央値（緑）は多数派の近くにとどまります。平均は外れ値に<strong>敏感（sensitive）</strong>、中央値は<strong>頑健（resistant）</strong>です。</p>
  {simple("10人のうち1人が大金持ちだと、平均年収はぐっと上がるけど、真ん中の人の年収（中央値）はほとんど変わらない。")}
'''))
    b.append(unit(4, "トリム平均と最頻値", "平均と中央値のあいだ", f'''
  <p><strong>トリム平均（trimmed mean）</strong>は、上下の端を一定割合<strong>切り捨ててから</strong>平均をとります。平均より頑健で、中央値より多くのデータを使います。よく使うのは 10% トリム（上10%・下10% を除く）です。</p>
  {P.R('mean(donors$totalGivingAmount)\nmean(donors$totalGivingAmount, trim = 0.10)\nmean(donors$totalGivingAmount, trim = 0.25)\nmedian(donors$totalGivingAmount)')}
  <p>切る割合を増やすほど、値は中央値（78）に近づきます（<code>trim = 0.5</code> にすると中央値と同じ）。</p>
  <h3>最頻値（mode）</h3>
  <p>いちばん多く現れる値です。量的・質的どちらにも使えますが、R に組み込みの関数はありません。<code>table()</code> で数えて最大のものを探します。山が2つあれば<strong>二峰性（bimodal）</strong>で、「中心」より<strong>形</strong>の情報として役立ちます。</p>
  {P.R('bimodal_data <- c(rep(0, 9), 1, 3, 4, 5, 6, 8, rep(10, 9))\ntable(bimodal_data)\nmean(bimodal_data); median(bimodal_data)', show_code=True)}
  {warn('この二峰性データは平均も中央値も 5 前後ですが、<strong>実際に 5 付近の値はほとんどありません</strong>。中心の指標だけで要約すると誤解を生むことがあるので、必ずグラフも見ましょう。')}
  {practice("p-m2ct-u4", "3つの中心を比べる", "<code>donors$numberGifts</code>（寄付回数）の<strong>平均・中央値・10%トリム平均</strong>を求めてください。",
             ["mean", "median", "trim", "numberGifts"], 'mean(donors$numberGifts)\nmedian(donors$numberGifts)\nmean(donors$numberGifts, trim = 0.1)', "平均 9.6、中央値 7、10%トリム平均 8.3（その間）。平均 &gt; 中央値なので右に裾が長い分布と予想できる（次の回でヒストグラムで確認）。")}
'''))
    b.append(teal('➡️ <strong>次の講義へ：</strong>数値だけでは形がわかりません。次の <a href="m2_graphs.html">基本のグラフ</a>で、ヒストグラムや棒グラフを描きます。'))
    q = [("mean(x) returns NA. What is the most likely reason?", "x contains missing values", ["x is stored as a data frame", "x has too many observations", "x contains negative numbers"], "Any NA in the data makes mean() return NA. Add na.rm = TRUE to ignore missing values."),
         ("A number calculated from a sample, used to estimate a population value, is called a…", "statistic", ["parameter", "census", "residual"], "Statistics come from samples; parameters describe populations. x̄ estimates μ."),
         ("Which symbol stands for the population mean?", "μ (Greek mu)", ["x̄ (x-bar)", "s (sample SD)", "n (count)"], "μ is the population mean; x̄ is the sample mean."),
         ("A data set has a few very large values. Which measure of center is most resistant to them?", "The median", ["The mean", "The maximum", "The range"], "The median depends only on the middle position, so extreme values barely move it."),
         ("For right-skewed data, which is usually true?", "The mean is larger than the median", ["The median is larger than the mean", "The mean and median are always equal", "The mean is always zero"], "The long right tail pulls the mean toward the large values, above the median."),
         ("What does mean(x, trim = 0.10) do?", "Drops 10% from each end first", ["Drops only the largest 10% first", "Rounds the mean to one decimal", "Uses only the first 10% of x"], "A 10% trimmed mean removes 10% from each end and averages the rest, so it is more resistant than the mean.")]
    return L, "\n".join(b), q

# =============================================================== 2. graphs
def m2_graphs(P):
    L = dict(slug="m2_graphs", mod=MOD, icon="📊", title="基本のグラフ：ヒストグラム・ドット／幹葉・棒グラフ",
             tag="M2 · Basic Graphs — Describing Shape with Histograms, Dotplots &amp; Stemplots, Barplots for Categorical Data",
             lead="グラフの選び方は<strong>データの種類</strong>で決まります。量的データには<strong>ヒストグラム・ドットプロット・幹葉図</strong>、カテゴリには<strong>度数表と棒グラフ</strong>。分布の<strong>形（右に歪む・左に歪む・左右対称）</strong>の読み方も学びます。",
             video="Describing Shape with Histograms ／ Dotplots &amp; Stemplots ／ Graphs for Categorical Data: Barplots",
             unav=["① ヒストグラムと形", "② ドットプロットと幹葉図", "③ カテゴリのグラフ", "④ 2つのカテゴリ"],
             terms=[("histogram", "ヒストグラム", "量的データを区間（bin）に分けた度数の柱。"),
                    ("right-skewed", "右に歪んだ", "右に長い裾。平均 > 中央値。positive skew。"),
                    ("left-skewed", "左に歪んだ", "左に長い裾。平均 < 中央値。negative skew。"),
                    ("symmetric", "左右対称", "中央で折ると重なる形。平均 ≈ 中央値。"),
                    ("unimodal / bimodal", "単峰／二峰", "山が1つ／2つ。"),
                    ("dotplot (stripchart)", "ドットプロット", "1つの値を1つの点で積む。少量データ向き。"),
                    ("stemplot", "幹葉図", "幹（十の位）と葉（一の位）で値を並べる。"),
                    ("barplot", "棒グラフ", "カテゴリの度数・割合の棒。順番や間隔に意味はない。"),
                    ("two-way table", "二元表（クロス表）", "2つのカテゴリ変数の組み合わせの度数。")],
             tip="ヒストグラムは「量的」、棒グラフは「カテゴリ」。棒グラフに<strong>中心</strong>や<strong>歪み</strong>はない（並べ替えれば形が変わるから）。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>① Describing Shape with Histograms</li><li>② Dotplots &amp; Stemplots</li><li>③④ Graphs for Categorical Data: Barplots</li></ul>')]
    b.append(unit(1, "ヒストグラムで形を見る", "右に歪む・左に歪む・左右対称", f'''
  <p><strong>ヒストグラム</strong>は量的データを<strong>区間（bin）</strong>に分けて、各区間の個数を柱にしたグラフです。たくさんのデータの<strong>形</strong>をつかむのに向いています（個々の値は見えなくなる）。</p>
  {P.R(LOAD + '\npar(mfrow = c(1, 3))\nhist(donors$totalGivingAmount[donors$totalGivingAmount < 600], main = "Right-skewed",\n     xlab = "Total $ given (< 600)", col = "lightblue")\nhist(donors$wealthRating, main = "Left-skewed", xlab = "Wealth rating", col = "lightblue")\nhist(donors$incomeRating, main = "Roughly symmetric", xlab = "Income rating", col = "lightblue")\npar(mfrow = c(1, 1))', plot=True, w=900, h=330)}
  <p>（寄付総額は最大 9,485 まであり柱がつぶれるので、600 未満だけを描いています。）</p>
  {table(["形", "見た目", "平均と中央値"], [["右に歪む（right / positive skew）", "裾が<strong>右</strong>に長い", "平均 &gt; 中央値"], ["左に歪む（left / negative skew）", "裾が<strong>左</strong>に長い", "平均 &lt; 中央値"], ["ほぼ左右対称", "真ん中で折ると重なる", "平均 ≈ 中央値"]])}
  {P.R('c(mean = mean(donors$wealthRating, na.rm = TRUE), median = median(donors$wealthRating, na.rm = TRUE))')}
  <p>wealthRating は平均が中央値より小さく、左に歪んでいることと一致します。ほかに、山の数（<strong>単峰・二峰</strong>）や、どの値もほぼ同じ高さの<strong>一様（uniform）</strong>という形もあります。</p>
  {warn('歪みの向きは<strong>裾（tail）がある側</strong>で呼びます。山が右に寄っていると「右に歪んでいる」と言いたくなりますが、それは<strong>左に歪んだ</strong>分布です。')}
'''))
    b.append(unit(2, "ドットプロットと幹葉図", "少ないデータなら値まで見える", f'''
  <p>データが少ないときは、<strong>1つ1つの値が見える</strong>グラフが便利です。</p>
  {P.R('stripchart(donors1_20$age, method = "stack", pch = 16, cex = 2,\n           ylim = c(0, 3), xlab = "Age (first 20 donors)")', plot=True, h=260)}
  <p><strong>幹葉図（stemplot）</strong>は、十の位を<strong>幹</strong>、一の位を<strong>葉</strong>として並べます。横に倒したヒストグラムに、実際の値が書き込まれたものです。</p>
  {P.R('stem(donors1_20$age)')}
  <p>読み方：「<code>3 | 8</code>」は 38 歳、「<code>7 | 00258</code>」は 70, 70, 72, 75, 78 歳です。</p>
  {table(["", "ドットプロット・幹葉図"], [["良い点", "実際の値が見える／形がわかる／すき間（gap）やかたまり（cluster）が見える"], ["弱い点", "データが多いと使えない／幹葉図は読みにくい（上司への報告には不向き）"]])}
'''))
    b.append(unit(3, "カテゴリのグラフ：度数表と棒グラフ", "ヒストグラムは使えない", f'''
  <p><code>urbanicity</code>（都市度）のようなカテゴリ変数に、<code>hist()</code> や <code>stripchart()</code> は使えません。</p>
  {P.R('hist(donors$urbanicity)')}
  <p>カテゴリはまず<strong>数えます</strong>。<code>table()</code> で度数、<code>proportions()</code> で割合です。</p>
  {P.R('table(donors$urbanicity)\nround(proportions(table(donors$urbanicity)), 3) * 100')}
  <p>棒グラフは<strong>表を作ってから</strong> <code>barplot()</code> に渡します。</p>
  {P.R('barplot(table(donors$urbanicity), las = 1, ylab = "Count",\n        main = "How do we increase the number of urban donors?",\n        col = c(rep("gray", 4), "red"))', plot=True, h=360)}
  {warn('棒グラフには「中心」も「歪み」もありません。カテゴリの<strong>並び順は自由</strong>なので、並べ替えれば形が変わるからです。また<strong>ヒストグラムは棒グラフではない</strong>（柱が接していて、横軸は数直線）。')}
  {note('🥧 <strong>円グラフ</strong>はよく見かけますが、人は角度から量を読み取るのが苦手で、棒の長さのほうが比べやすいです。カテゴリが互いに重ならず合計100% になる場合にしか使えない点にも注意。')}
'''))
    b.append(unit(4, "2つのカテゴリ変数", "二元表と積み上げ棒グラフ", f'''
  <p>「住んでいる地域」と「郵送に反応したか」の関係を見るには、<strong>二元表（two-way table）</strong>を作ります。</p>
  {P.R('table(donors$urbanicity, donors$respondedMailing)\nround(proportions(table(donors$urbanicity, donors$respondedMailing), margin = 1), 3)')}
  <p><code>margin = 1</code> は「<strong>行ごと</strong>に割合を出す」指定です。各地域のうち何割が反応したかを比べられます。</p>
  {P.R('barplot(table(donors$respondedMailing, donors$urbanicity), legend.text = c("No", "Yes"),\n        las = 1, ylab = "Count", main = "Responded to mailing, by urbanicity")', plot=True, h=360)}
  {r4ds("Ch.5 Exploratory Data Analysis", "EDA は「データについて問いを立て、図と変換で答えを探し、答えから次の問いを作る」くり返し。まず<strong>1つの変数のばらつき（variation）</strong>を見て、次に<strong>2つの変数がいっしょに変わるか（covariation）</strong>を見る。カテゴリ×カテゴリなら度数の表、カテゴリ×量なら箱ひげ図が出発点。")}
  {practice("p-m2gr-u4", "カテゴリの度数と割合", "<code>donors$socioEconomicStatus</code> の<strong>度数表</strong>と、<strong>割合（%・小数第1位）</strong>を求め、棒グラフを描いてください。",
             ["table", "proportions", "socioEconomicStatus", "barplot"], 't <- table(donors$socioEconomicStatus)\nt\nround(proportions(t) * 100, 1)\nbarplot(t)', "average が約52%、highest が約31%、lowest が約17%（NA を除く）。順序のあるカテゴリなので、lowest → average → highest に並べ替えると読みやすい：<code>t[c(\"lowest\", \"average\", \"highest\")]</code>。")}
'''))
    b.append(teal('➡️ <strong>次の講義へ：</strong>中心だけでなく<strong>ばらつき</strong>も要約しましょう。次の <a href="m2_spread.html">5数要約・箱ひげ図・IQR</a>へ。'))
    q = [("Which graph is best for showing the shape of 90,000 donors' ages?", "A histogram", ["A stemplot", "A pie chart", "A barplot"], "Histograms group many numeric values into bins, so the shape is clear even for large data sets."),
         ("A histogram has a long tail to the right. How is it described?", "Right-skewed", ["Left-skewed", "Evenly spread", "Bell-shaped"], "Skew is named after the side with the tail, so a long right tail means right (positive) skew."),
         ("In a left-skewed distribution, how do the mean and median usually compare?", "The mean is below the median", ["The mean is above the median", "They are always identical", "The median is undefined"], "The long left tail pulls the mean down toward the small values."),
         ("Why can't hist() be used for the urbanicity variable?", "It is a categorical variable", ["It has too many rows to plot", "It contains no missing values", "It is already sorted by R"], "Histograms need numbers on a number line. For categories, count them with table() and use barplot()."),
         ("In a stemplot with stems in tens, what does '7 | 25' show?", "The values 72 and 75", ["The values 7, 2 and 5", "The value 725", "The values 27 and 57"], "The stem is the tens digit and each leaf is a ones digit, so 7 | 25 means 72 and 75."),
         ("What must you pass to barplot() for a categorical variable?", "A table of counts", ["The raw text column", "A numeric vector", "A histogram object"], "barplot() draws bar heights from counts, so make the table first: barplot(table(x)).")]
    return L, "\n".join(b), q

# =============================================================== 3. spread
def m2_spread(P):
    L = dict(slug="m2_spread", mod=MOD, icon="📦", title="5数要約・箱ひげ図・範囲と IQR・外れ値",
             tag="M2 · Measures of Spread — Five-Number Summary, Boxplots, Range &amp; IQR, Outliers with 1.5(IQR)",
             lead="平均が同じでも、ばらつきが違えば別のデータです。<strong>5数要約</strong>と<strong>四分位数</strong>、それを絵にした<strong>箱ひげ図</strong>、ばらつきの指標<strong>範囲と IQR</strong>、そして<strong>1.5×IQR ルール</strong>で外れ値を決める方法を学びます。",
             video="The Five-Number Summary ／ Boxplots ／ Measures of Variability: Range &amp; IQR ／ Calculating Outliers with 1.5(IQR)",
             unav=["① 5数要約", "② 箱ひげ図", "③ 範囲と IQR", "④ 1.5×IQR の外れ値"],
             terms=[("five-number summary", "5数要約", "最小・Q1・中央値・Q3・最大。"),
                    ("percentile", "パーセンタイル", "その値より下にデータの何%があるか。"),
                    ("Q1 / Q3", "第1／第3四分位数", "25／75パーセンタイル。"),
                    ("boxplot", "箱ひげ図", "5数要約と外れ値を描いた図。"),
                    ("range", "範囲", "最大 − 最小。1つの数。"),
                    ("IQR", "四分位範囲", "Q3 − Q1。真ん中50%の幅。頑健。"),
                    ("fence", "フェンス（境界）", "Q1 − 1.5IQR と Q3 + 1.5IQR。"),
                    ("outlier", "外れ値", "フェンスの外側の値。"),
                    ("comparative boxplot", "比較箱ひげ図", "y ~ group でグループごとに並べる。")],
             tip="外れ値の判定は<strong>「1.5 × IQR を Q1 から引き、Q3 に足す」</strong>。1.5 は経験上の目安で、数学的な理由はない。外れ値を見つけたら、まず<strong>なぜその値なのか</strong>を調べる。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>① The Five-Number Summary</li><li>② Boxplots</li><li>③ Measures of Variability: Range &amp; IQR</li><li>④ Calculating Outliers with 1.5(IQR)</li></ul>')]
    b.append(unit(1, "5数要約とパーセンタイル", "min・Q1・median・Q3・max", f'''
  <p>中心の指標だけでは、データの広がりがわかりません。<strong>5数要約（five-number summary）</strong>は、データを4等分する5つの値です。</p>
  {P.R(LOAD + '\nmin(donors$age, na.rm = TRUE)\nquantile(donors$age, probs = c(0.25, 0.50, 0.75), na.rm = TRUE)\nmax(donors$age, na.rm = TRUE)')}
  {table(["値", "意味", "donors の年齢"], [["最小 min", "いちばん小さい値", "1"], ["Q1（25パーセンタイル）", "25% がこれより下", "48"], ["中央値（50パーセンタイル）", "半分がこれより下", "62"], ["Q3（75パーセンタイル）", "75% がこれより下", "75"], ["最大 max", "いちばん大きい値", "98"]])}
  <p>解釈の例：「寄付者の<strong>4人に1人は48歳以下</strong>、<strong>半数は62歳以上</strong>」。<code>summary()</code> なら平均と NA の数もまとめて出ます。</p>
  {P.R('summary(donors$age)')}
  {warn('最小値が <strong>1 歳</strong>？ 寄付者として不自然です。入力ミスかもしれません。要約の数値は、<strong>データの品質チェック</strong>にも使えます。')}
'''))
    b.append(unit(2, "箱ひげ図", "5数要約を絵にする", f'''
  {P.R('boxplot(donors$age, horizontal = TRUE, pch = 16, col = "lightblue",\n        xlab = "Age", main = "Half of our donors are over 60 years old")', plot=True, h=300)}
  <p>箱の左端が <strong>Q1</strong>、中の太線が<strong>中央値</strong>、右端が <strong>Q3</strong>。ひげは外れ値でない範囲の最小・最大まで伸び、その外側の点が<strong>外れ値</strong>です。タイトルに<strong>結論</strong>を書くと伝わりやすいグラフになります。</p>
  <h3>比較箱ひげ図：量 ~ グループ</h3>
  <p><code>boxplot(量 ~ カテゴリ, data = df)</code> で、グループごとの分布を並べて比べられます。</p>
  {P.R('boxplot(incomeRating ~ gender, data = donors, col = "lightblue", las = 1,\n        main = "Income rating by gender")', plot=True, h=330)}
  {table(["", "箱ひげ図"], [["良い点", "最小・最大・中央値がすぐわかる／大きなデータでも使える／グループ比較に強い／外れ値が見える／形（歪み）のヒント"], ["弱い点", "何人分かわからない／すき間や山（二峰性）が隠れる／外れ値が多いと読みにくい"]])}
  {warn('両方とも量的な変数（例：最小寄付額 ~ 最大寄付額）で箱ひげ図を描くと、何百ものグループができて意味のない図になります。量×量には<strong>散布図</strong>（M6）を使います。')}
'''))
    b.append(unit(3, "ばらつきの指標：範囲と IQR", "平均が同じでも違うデータ", f'''
  {P.R('data1 <- c(0, 50, 100)\ndata2 <- c(50, 50, 50)\nc(mean(data1), mean(data2))')}
  <p>どちらも平均 50 ですが、ばらつきはまったく違います。これを数で表すのが<strong>ばらつきの指標（measures of variability / spread）</strong>です。</p>
  <h3>範囲（range）＝ 最大 − 最小</h3>
  {P.R('range(donors$age, na.rm = TRUE)\ndiff(range(donors$age, na.rm = TRUE))')}
  {warn('R の <code>range()</code> は<strong>最小と最大の2つ</strong>を返します。統計の「範囲」は<strong>1つの数</strong>（差）なので、<code>diff(range(x))</code> か <code>max(x) - min(x)</code> で求めます。範囲は2つの値しか使わず、外れ値で簡単にふくらむのが弱点。')}
  <h3>四分位範囲（IQR）＝ Q3 − Q1</h3>
  <p>IQR は<strong>真ん中50%のデータの幅</strong>です。端の値を使わないので<strong>頑健</strong>です。</p>
  {P.R('IQR(donors$age, na.rm = TRUE)\nIQR(donors1_20$age, na.rm = TRUE)')}
  <p>母集団の IQR は 27（＝75 − 48）、最初の20人の IQR は 24.5。標本の値は母集団の値の<strong>推定</strong>です。ばらつきの指標にはほかに、平均絶対偏差や<strong>標準偏差</strong>（次の回）があります。</p>
'''))
    b.append(unit(4, "1.5 × IQR ルールで外れ値を決める", "フェンスを計算する", f'''
  <p>箱ひげ図の点は、次の<strong>フェンス（境界）</strong>の外側にある値です。</p>
  <div class="note-box">📐 <strong>下のフェンス</strong> ＝ Q1 − 1.5 × IQR　　<strong>上のフェンス</strong> ＝ Q3 + 1.5 × IQR</div>
  {P.R('my_IQR <- IQR(donors$age, na.rm = TRUE)\nmy_Q1  <- quantile(donors$age, 0.25, na.rm = TRUE)\nmy_Q3  <- quantile(donors$age, 0.75, na.rm = TRUE)\nlower_fence <- my_Q1 - 1.5 * my_IQR\nupper_fence <- my_Q3 + 1.5 * my_IQR\nc(lower_fence, upper_fence)\nsum(donors$age < lower_fence, na.rm = TRUE)\nsum(donors$age > upper_fence, na.rm = TRUE)')}
  <p>7.5 歳未満が外れ値（20人）、115.5 歳を超える人はいないので上の外れ値はなし。箱ひげ図の左側の点と一致します。年齢が7歳以下の寄付者は、入力ミスの可能性を調べる価値があります。</p>
  {r4ds("Ch.5 Exploratory Data Analysis（Unusual Values）", "外れ値は<strong>入力ミス</strong>のこともあれば、<strong>重要な新事実</strong>のこともある。外れ値を除いた分析と含めた分析の両方を行い、結果が大きく変わるなら、除いた理由を必ず説明する。理由なく消してはいけない。")}
  {practice("p-m2sp-u4", "寄付総額の外れ値フェンス", "<code>donors$totalGivingAmount</code> の <strong>IQR</strong> と <strong>上のフェンス</strong>を求め、上のフェンスを超える人数を数えてください。",
             ["IQR", "quantile", "1.5", "sum"], 'q3 <- quantile(donors$totalGivingAmount, 0.75)\niqr <- IQR(donors$totalGivingAmount)\nupper <- q3 + 1.5 * iqr\nupper\nsum(donors$totalGivingAmount > upper)', "Q3 = 131、IQR = 91 なので上のフェンスは 267.5。右に長い裾をもつ分布なので、上の外れ値がたくさんある。")}
'''))
    b.append(teal('➡️ <strong>次の講義へ：</strong>もっともよく使うばらつきの指標が<strong>標準偏差</strong>です。次の <a href="m2_sd_normal.html">標準偏差と正規分布</a>へ。'))
    q = [("Which five values make up the five-number summary?", "Min, Q1, median, Q3, max", ["Min, mean, median, mode, max", "Mean, SD, IQR, range, median", "Q1, Q2, Q3, mean, SD"], "The five-number summary splits the data into quarters: minimum, first quartile, median, third quartile and maximum."),
         ("The 25th percentile of donor age is 48. What does this mean?", "About 25% are 48 or under", ["The average donor is 48", "25 donors are exactly age 48", "About 48% are under 25"], "A percentile tells you the share of the data below a value: about a quarter of donors are at or below 48."),
         ("In a boxplot, what does the line inside the box show?", "The median", ["The mean", "The maximum", "The range"], "The box runs from Q1 to Q3 and the line inside it marks the median."),
         ("Why is the IQR more resistant to outliers than the range?", "It ignores the extreme quarters", ["It uses only the largest values", "It always equals zero", "It squares every distance"], "IQR = Q3 − Q1 only uses the middle 50% of the data, so extreme values do not affect it."),
         ("Q1 = 48, Q3 = 75 and IQR = 27. What is the upper fence?", "115.5", ["102.0", "88.5", "121.5"], "Upper fence = Q3 + 1.5 × IQR = 75 + 40.5 = 115.5."),
         ("In R, what does range(x) return?", "Both the minimum and the maximum", ["Only the difference max minus min", "The middle 50% of the data", "The standard deviation of x"], "range() returns two numbers. Use diff(range(x)) to get the statistical range (one number).")]
    return L, "\n".join(b), q

# =============================================================== 4. sd & normal
def m2_sd_normal(P):
    L = dict(slug="m2_sd_normal", mod=MOD, icon="🔔", title="標準偏差・正規分布・経験則・歪度と尖度",
             tag="M2 · The Standard Deviation, Normal Distributions &amp; the Empirical Rule, Connecting Center &amp; Spread, Kurtosis &amp; Skew",
             lead="もっとも重要なばらつきの指標<strong>標準偏差</strong>を、手順を追って計算します（<strong>母集団と標本</strong>で割る数が違う理由も）。次に<strong>正規分布</strong>と <strong>68-95-99.7 の経験則</strong>、中心とばらつきから形を推理する方法、<strong>歪度・尖度</strong>を学びます。",
             video="Measures of Variability: The Standard Deviation ／ Normal Distributions &amp; the Empirical Rule ／ Connecting Center, Spread, &amp; Shape ／ Kurtosis &amp; Skew",
             unav=["① 標準偏差を手で計算", "② 正規分布と経験則", "③ 中心・ばらつき・形", "④ 歪度と尖度"],
             terms=[("deviation", "偏差", "各値 − 平均。"),
                    ("variance", "分散", "偏差の2乗の平均。単位が2乗になる。"),
                    ("standard deviation (s, σ)", "標準偏差", "分散の平方根。値は平均から典型的にどれだけ離れるか。"),
                    ("n − 1", "標本の割る数", "標本分散・標本標準偏差は n − 1 で割る（R の sd()）。"),
                    ("normal distribution", "正規分布", "平均 μ と標準偏差 σ で決まる左右対称の釣鐘型。"),
                    ("empirical rule", "経験則", "±1σ に約68%、±2σ に約95%、±3σ に約99.7%。"),
                    ("Chebyshev's theorem", "チェビシェフの定理", "どんな分布でも ±kσ の外は 1/k² 以下。"),
                    ("skewness", "歪度", "非対称の度合い。負＝左、0＝対称、正＝右。"),
                    ("kurtosis", "尖度", "裾の重さ・とがり具合。正規分布は3（超過尖度0）。")],
             tip="標準偏差は「<strong>ふつうの値が平均からどれくらい離れているか</strong>」。0 が最小（全部同じ値）で、負にはならない。外れ値や歪みに<strong>敏感</strong>。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>① Measures of Variability: The Standard Deviation</li><li>② Normal Distributions &amp; the Empirical Rule</li><li>③ Connecting Center, Spread, &amp; Shape</li><li>④ Kurtosis &amp; Skew</li></ul>')]
    b.append(unit(1, "標準偏差を手順どおりに計算する", "平均からのずれの「典型的な大きさ」", f'''
  {P.R('donors <- read.csv("donors.csv")\nmy_data <- c(0, 5, 5, 5, 10, 50)\nmy_mean <- mean(my_data)\ndev <- my_data - my_mean       # 1. 平均からのずれ（偏差）\ndev\ndev^2                          # 2. 2乗する\nsum(dev^2)                     # 3. 合計する\nmy_var <- sum(dev^2) / length(my_data)   # 4. 個数で割る＝分散\nmy_var\nsqrt(my_var)                   # 5. 平方根＝標準偏差')}
  <p>偏差をそのまま足すと必ず 0 になるので、<strong>2乗してから</strong>平均します（分散）。分散は単位が2乗（ドル²）で解釈しにくいので、<strong>平方根</strong>で元の単位に戻したものが標準偏差です。</p>
  <h3>R の <code>sd()</code> と値が違う？</h3>
  {P.R('var(my_data)\nsd(my_data)')}
  {table(["", "母集団 σ", "標本 s（R の sd()）"], [["割る数", "n", "<strong>n − 1</strong>"], ["使う場面", "全体のデータがある", "標本から母集団を推定する（ふつうはこちら）"]])}
  <p>上の手計算は <strong>n で割った母集団の標準偏差</strong>（17.0）、R の <code>sd()</code> は <strong>n − 1 で割った標本標準偏差</strong>（18.64）です。標本では平均を標本から計算したぶん、ばらつきを小さく見積もりがちなので、n − 1 で割って補正します。</p>
  <p>解釈：「このデータの値は、<strong>平均からおよそ 18.6 離れているのが典型的</strong>」。</p>
  {P.R('sd(c(0, 0, 50, 100, 100))\nsd(c(50, 50, 50, 50, 50))')}
  {warn('標準偏差の最小は <strong>0</strong>（全部同じ値）で、<strong>負にはなりません</strong>。また平均と同じく外れ値に<strong>敏感</strong>です。上の <code>my_data</code> の 50 を 500 にすると、sd は 200 を超えます。')}
'''))
    b.append(unit(2, "正規分布と 68-95-99.7 の経験則", "平均と標準偏差だけで決まる形", f'''
  <p><strong>正規分布（normal distribution）</strong>は、単峰で左右対称の<strong>釣鐘型</strong>の分布です。<strong>平均 μ と標準偏差 σ の2つ</strong>で形が決まり、X ~ Normal(μ, σ) と書きます。知能指数（IQ）は平均 100・標準偏差 15 のほぼ正規分布になるよう作られています。</p>
  {P.R('curve(dnorm(x, 100, 15), from = 40, to = 160, lwd = 2, xlab = "IQ", ylab = "",\n      main = "The Empirical Rule: 68-95-99.7")\nabline(v = c(85, 115), col = "red", lwd = 2)\nabline(v = c(70, 130), col = "blue", lwd = 2)\nabline(v = c(55, 145), col = "darkgreen", lwd = 2)', plot=True, h=340)}
  {table(["範囲", "割合（約）", "IQ ~ N(100, 15)"], [["μ ± 1σ", "68%", "85〜115"], ["μ ± 2σ", "95%", "70〜130"], ["μ ± 3σ", "99.7%", "55〜145"]])}
  <p>この数字はどこから来るのでしょう。正規分布の面積を R で計算すると確かめられます（<code>pnorm()</code> は M3 で詳しく）。</p>
  {P.R('pnorm(1) - pnorm(-1)\npnorm(2) - pnorm(-2)\npnorm(3) - pnorm(-3)')}
  {warn('経験則は<strong>正規分布（に近い）データ専用</strong>です。右に歪んだデータには使えません。どんな分布でも使える保証は<strong>チェビシェフの定理</strong>：「平均から k 標準偏差の外にあるのは多くても 1/k²」（k = 2 なら最大25%）。')}
'''))
    b.append(unit(3, "中心・ばらつき・形をつなげる", "数字から形を推理する", f'''
  <p>平均・中央値・標準偏差がわかれば、グラフがなくても形をある程度推理できます。</p>
  {table(["分布", "平均", "中央値", "SD", "推理"], [["A", "20", "20", "5", "平均 ≈ 中央値 → ほぼ対称"], ["B", "20", "15", "5", "平均 &gt; 中央値 → 右に歪む"], ["C", "10", "10", "8", "最小値が 0 なら、平均から 3SD 左（−14）まで伸ばせない → 正規分布ではありえない"], ["D", "30", "30", "6", "30 − 3×6 = 12 &gt; 0 → 正規分布の可能性あり"]])}
  {note('🔍 <strong>正規分布の可能性チェック</strong>（値が 0 以上の量の場合）：平均から<strong>左右に 3 標準偏差</strong>の余地があるか？ 平均 − 3SD が 0 より小さくなるなら、左右対称の正規分布にはなれません（右に歪んでいるはず）。寄付総額（平均 104.5、SD 約 119）も同じ理由で正規分布ではありません。')}
  {P.R('c(mean = mean(donors$totalGivingAmount), sd = sd(donors$totalGivingAmount))\nmean(donors$totalGivingAmount) - 3 * sd(donors$totalGivingAmount)')}
'''))
    b.append(unit(4, "歪度と尖度", "形を数で表す", f'''
  <p><strong>歪度（skewness）</strong>は非対称の度合いです。<strong>負なら左に歪む、0 なら対称、正なら右に歪む</strong>。<strong>尖度（kurtosis）</strong>は正規分布と比べた<strong>裾の重さ・とがり具合</strong>で、正規分布の尖度は 3 です（3 を引いた「超過尖度」で 0 と表す流儀もあります）。</p>
  {table(["尖度", "名前", "特徴"], [["3 より大きい", "急尖（leptokurtic）", "中心がとがり、<strong>裾が重い</strong>（極端な値が出やすい）"], ["3", "正規（mesokurtic）", "正規分布と同じ"], ["3 より小さい", "緩尖（platykurtic）", "中心が平ら、<strong>裾が軽い</strong>"]])}
  <p>パッケージ（<code>psych</code> の <code>describe()</code> など）でも出せますが、定義どおり計算することもできます。</p>
  {P.R('skew <- function(x) { x <- x[!is.na(x)]; mean((x - mean(x))^3) / sd(x)^3 }\nkurt <- function(x) { x <- x[!is.na(x)]; mean((x - mean(x))^4) / sd(x)^4 }\nround(c(skew_total = skew(donors$totalGivingAmount), skew_wealth = skew(donors$wealthRating),\n        kurt_total = kurt(donors$totalGivingAmount)), 2)')}
  <p>寄付総額は歪度が大きく正（強く右に歪む）、wealthRating は負（左に歪む）。ヒストグラムの見た目と一致します。寄付総額の尖度は 3 を大きく上回り、裾が非常に重い（極端な高額寄付がある）ことを示します。</p>
  {note('📝 歪度・尖度は計算式が何種類かあり、ソフトによって値が少し違います。報告で見かけたら意味がわかれば十分で、この授業で頻繁に使うものではありません。')}
  {practice("p-m2sd-u4", "標本標準偏差を2通りで", "<code>x &lt;- c(2, 4, 4, 4, 5, 5, 7, 9)</code> の標準偏差を、（1）<code>sd()</code> で、（2）<code>sqrt(sum((x - mean(x))^2) / (length(x) - 1))</code> で求め、一致を確かめてください。",
             ["sd", "sqrt", "sum", "length"], 'x <- c(2, 4, 4, 4, 5, 5, 7, 9)\nsd(x)\nsqrt(sum((x - mean(x))^2) / (length(x) - 1))', "どちらも 2.138。n で割ると 2.0（母集団の標準偏差）になる。")}
'''))
    b.append(teal('➡️ <strong>次の講義へ：</strong>平均と標準偏差がわかれば、<strong>単位の違うデータどうし</strong>を比べられます。次の <a href="m2_z.html">z スコア</a>へ。'))
    q = [("Why are the deviations squared before averaging them?", "Raw deviations always sum to zero", ["Squaring makes units easier to read", "R cannot add negative numbers", "It removes all of the outliers"], "Positive and negative deviations cancel out, so they are squared before being averaged."),
         ("R's sd() gives a larger value than your hand calculation that divided by n. Why?", "sd() divides by n − 1", ["sd() rounds every value first", "sd() ignores the largest value", "sd() uses the median, not the mean"], "sd() is the sample standard deviation, which divides by n − 1 instead of n."),
         ("What is the smallest possible standard deviation?", "It is 0", ["It is 1", "It is −1", "It is 0.5"], "SD is a square root of an average of squares, so it cannot be negative; it is 0 when all values are equal."),
         ("IQ ~ Normal(100, 15). About what share of adults have an IQ between 70 and 130?", "About 95%", ["About 68%", "About 99%", "About 50%"], "70 and 130 are 2 standard deviations from the mean, and about 95% of a normal distribution lies within ±2σ."),
         ("A variable has minimum 0, mean 10 and SD 8. Why can it not be normal?", "Mean − 3 SD falls below zero", ["Its mean is too small to be normal", "Its SD is smaller than its mean", "A normal mean must be zero"], "A normal shape needs room for about 3 SDs on both sides; 10 − 24 = −14 is impossible here, so the data must be right-skewed."),
         ("A distribution has negative skewness. Which shape is it?", "Left-skewed", ["Right-skewed", "Symmetric", "Bell-shaped"], "Negative skewness means the long tail is on the left side.")]
    return L, "\n".join(b), q

# =============================================================== 5. z
def m2_z(P):
    L = dict(slug="m2_z", mod=MOD, icon="⚖️", title="z スコア：単位の違うデータを比べる",
             tag="M2 · Standardized Scores (z-scores), Using z-scores &amp; Descriptive Statistics Conclusion",
             lead="点数の満点も単位も違うテストで、どちらが「良かった」かを比べるには<strong>標準化</strong>が必要です。<strong>z スコア</strong>の計算と解釈、データ全体の標準化、そして「<strong>記述統計は描写してこそ</strong>」というまとめで M2 を締めくくります。",
             video="Standardized Scores: z-scores ／ Using z-scores ／ Descriptive Statistics Conclusion ／ Model Talk",
             unav=["① z スコアとは", "② donors で計算", "③ 世代・試験をまたいだ比較", "④ 標準化と記述統計のまとめ"],
             terms=[("standardized score", "標準化得点", "平均と標準偏差で単位をそろえた値。"),
                    ("z-score", "z スコア", "(値 − 平均) ÷ 標準偏差。平均から何 SD 離れているか。"),
                    ("z = 0", "ゼロ", "ちょうど平均。"),
                    ("standard normal", "標準正規分布", "平均 0・標準偏差 1 の正規分布 N(0, 1)。"),
                    ("scale()", "標準化関数", "ベクトル全体を z スコアに変換する R の関数。"),
                    ("test statistic", "検定統計量", "推測統計で使う標準化された値（M4）。")],
             tip="z スコアの符号は「平均より上か下か」を示すだけ。<strong>ゴルフのスコアやマラソンのタイム</strong>のように、低いほど良いものでは負の z が「良い」成績。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>①② Standardized Scores: z-scores</li><li>③ Using z-scores &amp; the MLB</li><li>④ Descriptive Statistics Conclusion ／ Model Talk</li></ul>')]
    b.append(unit(1, "z スコアとは", "平均から何 SD 離れているか", f'''
  <p>英語のテストで 82 点（クラス平均 70、標準偏差 8）、数学で 90 点（平均 85、標準偏差 4）でした。どちらが<strong>クラスの中で</strong>良い成績でしょうか。素点だけでは比べられません。</p>
  <div class="note-box">📐 <strong>z スコア</strong> ＝（値 − 平均）÷ 標準偏差　　→「平均から<strong>標準偏差いくつ分</strong>離れているか」</div>
  {P.R('(82 - 70) / 8   # English\n(90 - 85) / 4   # Math')}
  <p>英語は平均より <strong>1.5 SD 上</strong>、数学は <strong>1.25 SD 上</strong>。素点は数学の方が高いですが、<strong>相対的には英語の方が良い</strong>成績です。</p>
  {table(["z", "意味"], [["0", "ちょうど平均"], ["+2", "平均より 2 SD 上（正規分布なら上位約2.5%）"], ["−1", "平均より 1 SD 下"]])}
  {simple("z スコアは「クラスの中での位置」をそろえるものさし。満点や単位が違うテストでも、同じものさしで比べられる。")}
'''))
    b.append(unit(2, "donors で z スコアを計算する", "1人の寄付者を2つの面から見る", f'''
  <p>最初の寄付者は、<strong>寄付回数 31 回</strong>、<strong>平均寄付額 7.74 ドル</strong>でした。それぞれ全体の中でどのくらいの位置でしょうか。</p>
  {P.R('donors <- read.csv("donors.csv")\nmean_gifts <- mean(donors$numberGifts)\nsd_gifts   <- sd(donors$numberGifts)\n(31 - mean_gifts) / sd_gifts\nmean_amount <- mean(donors$averageGiftAmount)\nsd_amount   <- sd(donors$averageGiftAmount)\n(7.74 - mean_amount) / sd_amount')}
  <p>寄付回数は平均より約 <strong>2.5 SD 上</strong>（とても多い）、平均寄付額は約 <strong>0.52 SD 下</strong>（やや少ない）。「<strong>少額をこまめに寄付する人</strong>」という人物像が見えてきます。</p>
  {warn('負の z スコアが必ずしも「悪い」わけではありません。<strong>ゴルフのスコア</strong>や<strong>マラソンのタイム</strong>は低いほど良いので、平均より下（負の z）が良い成績です。符号は「上か下か」だけを表します。')}
'''))
    b.append(unit(3, "時代や試験をまたいで比べる", "同じ基準で「すごさ」を測る", f'''
  <p>時代によって平均やばらつきが違うデータも、z スコアなら比べられます。架空の営業成績の例で考えます。</p>
  {P.R('sales <- data.frame(\n  person = c("Aoki (2015)", "Baker (2020)", "Chen (2025)"),\n  units  = c(120, 150, 160),\n  mean   = c(80, 110, 130),\n  sd     = c(15, 20, 10))\nsales$z <- round((sales$units - sales$mean) / sales$sd, 2)\nsales')}
  <p>販売数は Chen がいちばん多いのに、z スコアで見ると<strong>同じ年の同僚と比べて最も突出していたのは Chen（z = 3.0）</strong>、次が Aoki（2.67）、Baker（2.0）です。平均も標準偏差も年によって違うので、素点の比較は公平ではありません。</p>
  {note('⚾ 講義では、野球の歴代ホームラン王（ルース・マリス・マグワイア・ボンズ・ジャッジ）を、それぞれの年のリーグ平均と標準偏差で標準化して比べています。考え方は上と同じです。')}
'''))
    b.append(unit(4, "データ全体の標準化と、記述統計のまとめ", "scale() と「描写する」こと", f'''
  <p><code>scale()</code> を使うと、ベクトル全体を一度に z スコアにできます。標準化したデータは<strong>平均 0・標準偏差 1</strong> になります。</p>
  {P.R('non_norm <- c(0, 0, 0, 10, 20)\nz <- as.vector(scale(non_norm))\nround(z, 3)\nc(mean = round(mean(z), 10), sd = sd(z))')}
  {warn('平均 0・SD 1 の<strong>正規分布</strong>を<strong>標準正規分布</strong> N(0, 1) と呼びますが、<strong>標準化しても形は変わりません</strong>。上のデータは標準化後も右に歪んだままで、「標準正規」にはなりません。')}
  <h3>記述統計のまとめ：「描写的」であること</h3>
  <p>M2 で学んだ数値（中心・ばらつき・形・z スコア）とグラフは、データを<strong>人に伝わる物語</strong>にするための道具です。数値を並べるだけでは不十分で、「<strong>寄付者の半数は62歳以上、寄付額は少数の高額寄付者に強く引っぱられた右に歪んだ分布</strong>」のように、<strong>文章で描写</strong>してはじめて意味を持ちます（Navarro, <em>Learning Statistics with R</em>, Ch.5 の結びより趣旨）。</p>
  {practice("p-m2z-u4", "z スコアで比べる", "あるマラソン大会のタイム（分）は平均 240、標準偏差 30。別の大会は平均 210、標準偏差 20。Aさんは1つ目で 195 分、Bさんは2つ目で 175 分でした。それぞれの z スコアを求め、相対的に速いのはどちらか考えてください。",
             ["195", "240", "175", "210"], '(195 - 240) / 30   # A\n(175 - 210) / 20   # B', "A は −1.5、B は −1.75。タイムは低いほど良いので、より負の大きい <strong>B</strong> の方が相対的に速い。")}
'''))
    b.append(teal('➡️ <strong>次のモジュールへ：</strong>データを描写できたら、次は<strong>偶然</strong>を数で扱う番です。<a href="m3_prob.html">550 M3 確率と分布</a>へ進みましょう。'))
    q = [("What does a z-score tell you?", "SDs between a value and the mean", ["The percentage of values below it", "How far a value is from the median", "The number of values in the data set"], "z = (value − mean) / SD, so it counts standard deviations above (+) or below (−) the mean."),
         ("A test has mean 70 and SD 8. What is the z-score for a score of 82?", "1.5", ["12", "0.67", "−1.5"], "(82 − 70) / 8 = 12 / 8 = 1.5."),
         ("English: z = 1.5. Math: z = 1.25. Which result is better relative to the class?", "The English test", ["The math test", "Both are equal", "Cannot be judged"], "The larger z-score is further above its class mean, so English is the better relative result."),
         ("For marathon times, a runner has z = −1.2. What does this mean?", "The runner was faster than average", ["The runner was slower than average", "The runner finished exactly average", "The time was recorded wrongly"], "Lower times are better, so a negative z-score (below the mean time) means a faster than average runner."),
         ("After converting data with scale(), what are the new mean and SD?", "Mean 0 and SD 1", ["Mean 1 and SD 0", "Mean 100 and SD 15", "They stay the same"], "Standardizing subtracts the mean and divides by the SD, giving mean 0 and SD 1."),
         ("Right-skewed data are standardized into z-scores. What is their shape now?", "Still right-skewed", ["Standard normal", "Left-skewed", "Perfectly symmetric"], "Standardizing only shifts and rescales the values; it does not change the shape of the distribution.")]
    return L, "\n".join(b), q

LESSONS = [m2_center, m2_graphs, m2_spread, m2_sd_normal, m2_z]
