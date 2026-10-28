"""550 M3: 確率と分布 — 6 lessons. All examples are original (no course-note text or data reused)."""
from lib550 import *
from c_m1 import r4ds

MOD = "550 M3"
SHOP = '''shop <- matrix(c(90, 30, 60, 20,
                 110, 90, 40, 60), nrow = 2, byrow = TRUE,
               dimnames = list(device = c("Phone", "Computer"),
                               result = c("Bought", "Browsed", "Cart", "Left")))'''

# =============================================================== 1. probability basics
def m3_prob(P):
    L = dict(slug="m3_prob", mod=MOD, icon="🎲", title="確率の基本：標本空間・事象・確率とオッズ",
             tag="M3 · Probability — Probability Terms, Probability &amp; Odds, the Law of Large Numbers",
             lead="確率の言葉（<strong>ランダムな試行・標本空間・事象</strong>）を R の <code>sample()</code> で体験し、<strong>確率</strong>と<strong>オッズ</strong>の違い、たくさんくり返すと割合が確率に近づく<strong>大数の法則</strong>を学びます。",
             video="Notes: Intro to Probability ／ Probability Terms ／ Probability &amp; Odds",
             unav=["① 試行・標本空間・事象", "② R でシミュレーション", "③ 確率とオッズ", "④ 大数の法則"],
             terms=[("random experiment", "ランダムな試行", "結果が偶然で決まる手続き（コイン投げ・営業電話）。"),
                    ("sample space (S)", "標本空間", "起こりうる結果すべての集まり。"),
                    ("outcome", "結果", "標本空間の1つの要素。"),
                    ("event", "事象", "結果の集まり（例：奇数が出る＝{1, 3, 5}）。"),
                    ("simple event", "根元事象", "結果1つだけからなる事象。"),
                    ("probability", "確率", "成功数 ÷ 全体。0 以上 1 以下。"),
                    ("odds", "オッズ", "成功数 ÷ 失敗数（成功:失敗）。"),
                    ("law of large numbers", "大数の法則", "くり返すほど相対度数が確率に近づく。"),
                    ("set.seed()", "乱数の種", "乱数の結果を再現できるようにする。")],
             tip="<strong>確率＝成功 ÷ 全体</strong>、<strong>オッズ＝成功 ÷ 失敗</strong>。確率 1/6 のオッズは 1:5。オッズ 1:3 の確率は 1/4。分母の違いを意識する。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>①② 550_Notes_Intro to Probability ／ Probability Terms</li><li>③④ Probability &amp; Odds</li></ul>')]
    b.append(unit(1, "ランダムな試行・標本空間・事象", "確率の言葉をそろえる", f'''
  <p><strong>ランダムな試行（random experiment）</strong>は、結果がはっきり決まっていて、どれになるかは<strong>偶然</strong>で決まる手続きです。コイン投げ、サイコロ、Web 広告のクリック（する／しない）、株価の1年後（上がる／下がる／変わらない）など。</p>
  {table(["用語", "意味", "サイコロ1個の例"], [["標本空間 S", "起こりうる結果すべて", "S = {1, 2, 3, 4, 5, 6}"], ["結果 outcome", "S の要素1つ", "4"], ["事象 event", "結果の集まり", "偶数 E = {2, 4, 6}"], ["根元事象 simple event", "結果1つだけの事象", "{6}"]])}
  <p>コインを2回投げると、S = {{(表,表), (表,裏), (裏,表), (裏,裏)}} の<strong>4通り</strong>です。「(表,裏)」と「(裏,表)」は別の結果であることに注意しましょう。</p>
  {simple("標本空間＝くじ箱の中身全部、事象＝その中で「当たり」と決めたくじの集まり。")}
'''))
    b.append(unit(2, "R でランダムな試行をシミュレーションする", "sample() と set.seed()", f'''
  <p><code>sample(候補, size = 回数, replace = TRUE)</code> で、候補から無作為に選べます。<code>replace = TRUE</code> は<strong>復元抽出</strong>（選んだものを戻す＝サイコロをくり返し振る）です。</p>
  {P.R('die <- 1:6\nset.seed(2026)\nsample(die, size = 10, replace = TRUE)')}
  <p>乱数は実行のたびに変わります。<code>set.seed()</code> で<strong>種</strong>を決めると、同じ結果を再現できます（レポートや課題で大切）。</p>
  {P.R('sample(die, size = 6, replace = FALSE)\nsample(die, size = 7, replace = FALSE)')}
  {warn('<code>replace = FALSE</code>（<strong>非復元抽出</strong>）では、一度選んだものは戻らないので、候補の数（6）より多くは選べずエラーになります。名簿から重複なく人を選ぶときは FALSE、サイコロのようにくり返すときは TRUE。')}
'''))
    b.append(unit(3, "確率とオッズ", "分母が違う2つの表し方", f'''
  <div class="note-box">📐 <strong>確率</strong> P(A) ＝ A に当てはまる結果の数 ÷ 全部の結果の数（すべて同じ確からしさのとき）<br>📐 <strong>オッズ</strong> ＝ 成功の数 ÷ 失敗の数（「成功:失敗」とも書く）</div>
  <p>サイコロで偶数が出る確率は 3/6 = 0.5、オッズは 3:3 = 1:1。6 が出る確率は 1/6、オッズは 1:5 です。</p>
  <p>データから確率を<strong>推定</strong>することもできます。あるオンラインショップの1か月の注文 2,500 件のうち、返品が 175 件だったとします（架空のデータ）。</p>
  {P.R('orders <- 2500\nreturns <- 175\nreturns / orders                  # probability of a return\nreturns / (orders - returns)      # odds of a return')}
  <p>「無作為に1件選ぶと、約 7% の確率で返品」「長い目で見ると約 7% が返品」と解釈します。オッズは約 0.075（≒ 1:13）。</p>
  {warn('R に <code>175 / 2,500</code> とカンマ付きで書くとエラーです。また <code>a + b + c / total</code> は「c だけを total で割ってから足す」計算になります。<strong>分子全体をかっこで囲む</strong>：<code>(a + b + c) / total</code>。')}
  {table(["", "範囲", "例"], [["確率 probability", "0〜1（0＝起こらない、1＝必ず起こる）", "0.07"], ["百分率 percentage", "0%〜100%", "7%"], ["割合 proportion", "確率と同じ数値。ただし「偶然」の意味は含まない", "全注文の 7% が返品"]])}
'''))
    b.append(unit(4, "大数の法則", "くり返すほど確率に近づく", f'''
  <p>コインを投げた回数が少ないと、表の割合は 0.5 から大きくずれます。回数を増やすと、割合はだんだん 0.5 に近づきます。これが<strong>大数の法則（law of large numbers）</strong>で、確率を「<strong>長い目で見た相対度数</strong>」と解釈する根拠です。</p>
  {P.R('set.seed(550)\nflips <- sample(c("H", "T"), size = 2000, replace = TRUE)\nprop_heads <- cumsum(flips == "H") / seq_along(flips)\nprop_heads[c(10, 100, 1000, 2000)]\nplot(prop_heads, type = "l", ylim = c(0, 1), las = 1,\n     xlab = "Number of flips", ylab = "Proportion of heads")\nabline(h = 0.5, col = "red", lty = 2)', plot=True, h=330)}
  {warn('大数の法則は「<strong>長い目で見ると</strong>」の話です。「表が5回続いたから次は裏が出やすい」という考えは<strong>ギャンブラーの誤謬</strong>。コインに記憶はなく、次の1回の確率は 0.5 のままです。')}
  {practice("p-m3pr-u4", "サイコロの大数の法則", "<code>set.seed(1)</code> のあと、サイコロを <strong>6000 回</strong>振るシミュレーションをして、<strong>6 が出た割合</strong>を求めてください（理論値は 1/6 ≈ 0.167）。",
             ["set.seed", "sample", "replace = TRUE", "mean"], 'set.seed(1)\nrolls <- sample(1:6, size = 6000, replace = TRUE)\nmean(rolls == 6)', "<code>rolls == 6</code> は TRUE/FALSE のベクトル。<code>mean()</code> を取ると TRUE の割合になる。結果は 1/6 に近い値になる。")}
'''))
    b.append(teal('➡️ <strong>次の講義へ：</strong>事象を組み合わせると、「AかつB」「AまたはB」「Bのときの A」の確率が考えられます。次の <a href="m3_cond.html">余事象・加法定理・条件付き確率・独立</a>へ。'))
    q = [("What is the sample space for tossing a coin twice?", "HH, HT, TH, TT", ["HH, HT, TT", "H, T", "0, 1 or 2 heads"], "There are four equally likely outcomes; HT and TH are different outcomes."),
         ("What does set.seed(2026) do before sample()?", "Makes random results repeatable", ["Makes the results more random", "Removes duplicates from the sample", "Sorts the sampled values for you"], "Fixing the seed lets you (and others) reproduce the same random numbers."),
         ("sample(1:6, size = 7, replace = FALSE) gives an error. Why?", "Only six values exist to draw", ["size must be smaller than five", "replace must always be TRUE", "1:6 is not a valid vector"], "Without replacement each value can be drawn once, so you cannot draw 7 from 6 values."),
         ("The probability of an event is 1/4. What are the odds?", "1:3", ["1:4", "3:1", "4:1"], "Probability 1/4 means 1 success for every 3 failures, so the odds are 1:3."),
         ("175 of 2,500 orders were returned. What is the estimated probability of a return?", "0.07", ["0.075", "0.175", "0.93"], "175 / 2500 = 0.07; 0.075 is the odds (175 / 2325)."),
         ("A fair coin lands heads 5 times in a row. What is P(heads) on the next toss?", "0.5", ["Less than 0.5", "More than 0.5", "0"], "Tosses are independent, so the probability stays 0.5. Expecting tails is the gambler's fallacy.")]
    return L, "\n".join(b), q

# =============================================================== 2. combining events
def m3_cond(P):
    L = dict(slug="m3_cond", mod=MOD, icon="🔗", title="余事象・和と積・加法定理・条件付き確率・独立",
             tag="M3 · Probability — Complements, Intersections &amp; Unions, the General Addition Rule, Conditional Probability, Independent Events",
             lead="架空のオンラインショップの<strong>二元表</strong>を使って、<strong>余事象</strong>、<strong>積（かつ）と和（または）</strong>、<strong>加法定理</strong>、<strong>排反</strong>、<strong>条件付き確率</strong>、<strong>独立</strong>を順に計算します。最後に「排反」と「独立」の違いを整理します。",
             video="Complements, Intersections, and Unions ／ The General Addition Rule ／ Conditional Probability ／ Independent Events: Using Technology ／ Using Formulas",
             unav=["① 余事象", "② 積・和と加法定理", "③ 条件付き確率", "④ 独立と排反"],
             terms=[("complement (Aᶜ)", "余事象", "A でないこと。P(A) + P(Aᶜ) = 1。"),
                    ("intersection (A ∩ B)", "積事象", "A かつ B。同時確率。"),
                    ("union (A ∪ B)", "和事象", "A または B（両方も含む）。"),
                    ("general addition rule", "加法定理", "P(A∪B) = P(A) + P(B) − P(A∩B)。"),
                    ("mutually exclusive", "排反", "同時に起こらない。P(A∩B) = 0。"),
                    ("two-way table", "二元表", "2つのカテゴリ変数のクロス集計。"),
                    ("conditional probability", "条件付き確率", "P(A | B)：B が起きたときの A の確率。"),
                    ("independent", "独立", "P(A | B) = P(A)。B を知っても A の確率は変わらない。"),
                    ("addmargins()", "周辺合計", "表に行・列の合計を追加する R の関数。")],
             tip="条件付き確率は<strong>「given の後ろ」が分母</strong>。P(購入 | スマホ) なら、分母は<strong>スマホの合計</strong>。まず条件の行（列）だけを見る。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>① Complements, Intersections, and Unions</li><li>② The General Addition Rule</li><li>③ Conditional Probability</li><li>④ Independent Events — Using Technology ／ Using Formulas</li></ul>')]
    b.append(unit(1, "余事象", "「〜でない」から計算する", f'''
  <p>事象 A の<strong>余事象（complement）</strong> Aᶜ は「<strong>A でない</strong>」結果すべてです。すべての結果の確率の合計は 1 なので：</p>
  <div class="note-box">📐 P(A) + P(Aᶜ) = 1　　→　P(A) = 1 − P(Aᶜ)</div>
  <p>サイコロ2個の和が 2 になる確率は 1/36 なので、「和が 2 <strong>以外</strong>」の確率は 1 − 1/36 = 35/36。35通りを数えるより速いです。</p>
  {P.R('1 - 1/36\n# P(at least one 6 in 4 rolls) = 1 - P(no 6 in 4 rolls)\n1 - (5/6)^4')}
  {warn('「<strong>少なくとも1つ</strong>」の余事象は「<strong>1つもない</strong>」です。「少なくとも2人」の余事象は「0人または1人」。境目を間違えないように、0, 1, 2, … と書き出して確認しましょう。')}
'''))
    b.append(unit(2, "積（かつ）・和（または）と加法定理", "二元表で数える", f'''
  <p>架空のショップで、ある日の訪問者 500 人を<strong>端末</strong>と<strong>行動</strong>で分けた二元表です。</p>
  {P.R(SHOP + '\naddmargins(shop)')}
  <p>B = 購入（Bought）、Ph = スマホ（Phone）とします。</p>
  {table(["表現", "意味", "人数", "確率"], [["B ∩ Ph（積・かつ）", "スマホで購入", "90", "90/500 = 0.18"], ["B ∪ Ph（和・または）", "購入した、またはスマホ（両方も含む）", "200 + 200 − 90 = 310", "0.62"]])}
  <p>和を数えるとき、「スマホで購入」の 90 人は<strong>購入者にもスマホ利用者にも入っている</strong>ので、そのまま足すと<strong>2回数えて</strong>しまいます。そこで重なりを1回引きます。</p>
  <div class="note-box">📐 <strong>加法定理</strong>：P(A ∪ B) = P(A) + P(B) − P(A ∩ B)</div>
  {P.R('n <- sum(shop)\np_B  <- sum(shop[, "Bought"]) / n\np_Ph <- sum(shop["Phone", ]) / n\np_B_and_Ph <- shop["Phone", "Bought"] / n\np_B + p_Ph - p_B_and_Ph')}
  <p>確率の「または」は<strong>両方を含む</strong>（inclusive OR）意味です。「ケーキかアイス、どっちにする？」の日常の「または」（どちらか一方）とは違います。</p>
  <h3>排反（mutually exclusive）</h3>
  <p>「購入（Bought）」と「途中離脱（Left）」は1人が同時に当てはまりません。このように<strong>共通部分がない</strong>事象を<strong>排反</strong>といい、P(A ∩ B) = 0 なので加法定理の引き算が不要になります。</p>
  {P.R('(sum(shop[, "Bought"]) + sum(shop[, "Left"])) / n')}
'''))
    b.append(unit(3, "条件付き確率", "条件で分母が変わる", f'''
  <p><strong>条件付き確率</strong> P(A | B) は、「<strong>B が起きたと分かっているとき</strong>の A の確率」です。縦棒 | は「given（〜のとき）」と読みます。</p>
  <div class="note-box">📐 P(A | B) = P(A ∩ B) ÷ P(B)　　表で数えるなら：<strong>B の行（列）の中で A の人数 ÷ B の合計</strong></div>
  {P.R('# P(Bought | Phone): only look at the Phone row\nshop["Phone", "Bought"] / sum(shop["Phone", ])\n# P(Phone | Bought): only look at the Bought column\nshop["Phone", "Bought"] / sum(shop[, "Bought"])')}
  <p>P(購入 | スマホ) = 90/200 = 0.45、P(スマホ | 購入) = 90/200 = 0.45。この表ではたまたま同じですが、<strong>一般には違う値</strong>です（分母が違うから）。</p>
  <p><code>proportions(表, margin = 1)</code> を使うと、<strong>各行の中での割合</strong>（行を条件とした条件付き分布）が一度に出ます。</p>
  {P.R('round(proportions(shop, margin = 1), 3)')}
  <p>スマホ利用者の購入率は 0.45、パソコン利用者は 0.367。端末によって購入の確率が違う、つまり<strong>端末と購入は関連している（独立でない）</strong>ように見えます。</p>
  {warn('「<strong>A のとき B</strong>」と「<strong>B のとき A</strong>」を取り違えるのは、医療や AI でも起こる典型的なミスです。条件（given の後ろ）を先に見つけ、その合計を分母にしましょう。機械学習の<strong>混同行列</strong>（偽陽性率など）も条件付き確率です。')}
'''))
    b.append(unit(4, "独立と排反", "似ているようで正反対", f'''
  <p>2つの事象が<strong>独立（independent）</strong>とは、片方が起きたと知っても、もう片方の確率が<strong>変わらない</strong>ことです。</p>
  <div class="note-box">📐 A と B が独立 ⇔ P(A | B) = P(A)　（同じことだが P(A | B) = P(A | Bᶜ)、P(A ∩ B) = P(A) × P(B)）</div>
  {P.R('p_B                                               # P(Bought) overall\nshop["Phone", "Bought"] / sum(shop["Phone", ])    # P(Bought | Phone)\np_B * p_Ph; p_B_and_Ph                            # product rule check')}
  <p>全体の購入率 0.40 に対して、スマホ利用者では 0.45。等しくないので、この標本では「購入」と「スマホ」は<strong>独立ではありません</strong>（関連がある）。</p>
  {note('🤔 「0.45 と 0.40 くらいの差で関連があると言えるの？」という疑問はもっともです。偶然の差かどうかは、M5 の<strong>カイ二乗独立性検定</strong>で判定します。')}
  <h3>排反と独立はちがう</h3>
  <p>排反な事象（同時に起こらない）は、片方が起きたら<strong>もう片方は確率 0</strong> になります。つまり片方の情報がもう片方の確率を大きく変える＝<strong>独立ではない</strong>のです（どちらかの確率が 0 の場合を除く）。</p>
  {table(["", "排反 mutually exclusive", "独立 independent"], [["意味", "同時に起こらない", "片方を知っても確率が変わらない"], ["式", "P(A ∩ B) = 0", "P(A ∩ B) = P(A) × P(B)"], ["例", "購入と途中離脱（同じ人）", "2回のコイン投げの表"]])}
  {warn('独立を<strong>安易に仮定しない</strong>こと。実際には関連している出来事を独立として確率を掛け合わせると、とても小さな（間違った）確率が出て、重大な誤判断につながることがあります。')}
  {practice("p-m3cd-u4", "条件付き確率を表から求める", "上の <code>shop</code> 表で、<strong>P(Left | Computer)</strong>（パソコン利用者のうち途中離脱した割合）と、全体の <strong>P(Left)</strong> を求め、独立かどうか判断してください。",
             ["shop", "Computer", "Left", "sum"], 'shop["Computer", "Left"] / sum(shop["Computer", ])\nsum(shop[, "Left"]) / sum(shop)', "P(Left | Computer) = 60/300 = 0.20、P(Left) = 80/500 = 0.16。等しくないので独立ではない（パソコン利用者の方が離脱しやすい）。")}
'''))
    b.append(teal('➡️ <strong>次の講義へ：</strong>そもそも「確率」とは何を意味するのでしょう。次の <a href="m3_bayes.html">頻度論とベイズ</a>で、2つの考え方を比べます。'))
    q = [("P(A) = 0.3. What is P(not A)?", "0.70", ["0.30", "1.30", "0.03"], "Complements add to 1, so P(Aᶜ) = 1 − 0.3 = 0.7."),
         ("What is the complement of 'at least one defect' in a batch?", "No defects at all", ["Exactly one defect", "At most one defect", "Two or more defects"], "'At least one' covers 1, 2, 3, …, so its complement is 0 defects."),
         ("Why do we subtract P(A ∩ B) in P(A ∪ B) = P(A) + P(B) − P(A ∩ B)?", "Outcomes in both were counted twice", ["Unions must be smaller than one event", "Intersections are always negative", "It converts odds into probability"], "Cases in both A and B appear in P(A) and in P(B), so we remove the overlap once."),
         ("In the shop table, which is the denominator of P(Bought | Phone)?", "Phone visitors (200)", ["All buyers (200 people)", "All 500 of the visitors", "Phone buyers only (90)"], "The condition after the bar (Phone) defines the group, so divide by the Phone total."),
         ("P(Bought) = 0.40 and P(Bought | Phone) = 0.45. What can you say?", "Buying and Phone are not independent", ["Buying and Phone are mutually exclusive", "Buying and Phone are certainly causal", "The two probabilities must add to one"], "Independence requires P(A | B) = P(A). The probabilities differ, so the events are associated."),
         ("Two events with non-zero probabilities are mutually exclusive. Are they independent?", "No, never", ["Yes, always", "Only if both are rare", "Only for coin tosses"], "If one happens the other has probability 0, so knowing one changes the other: they are dependent.")]
    return L, "\n".join(b), q

# =============================================================== 3. bayes
def m3_bayes(P):
    L = dict(slug="m3_bayes", mod=MOD, icon="🧠", title="頻度論とベイズ：確率の2つの考え方",
             tag="M3 · Probability — The Frequentist Approach, the Bayesian Approach, Frequentist vs. Bayesian in A/B Testing",
             lead="確率には<strong>2つの解釈</strong>があります。長い目で見た相対度数とみなす<strong>頻度論</strong>と、信念の度合いとみなす<strong>ベイズ</strong>です。それぞれの長所・短所と、<strong>ベイズの定理</strong>の計算（検査の陽性の例）を学びます。",
             video="The Frequentist Approach to Probability ／ The Bayesian Approach to Probability ／ Frequentist vs. Bayesian Probability in A/B Testing",
             unav=["① 頻度論", "② ベイズ", "③ ベイズの定理を計算", "④ A/B テストでの違い"],
             terms=[("frequentist", "頻度論", "確率＝長い目で見た相対度数。客観的・固定。"),
                    ("Bayesian", "ベイズ", "確率＝ある人の信念の度合い。新しい情報で更新。"),
                    ("prior", "事前確率", "データを見る前の確率 P(H)。"),
                    ("likelihood", "尤度", "仮説のもとでデータが得られる確率 P(D | H)。"),
                    ("posterior", "事後確率", "データを見た後の確率 P(H | D)。"),
                    ("Bayes' theorem", "ベイズの定理", "P(H | D) = P(D | H) P(H) / P(D)。"),
                    ("base rate", "基準率", "そもそもの頻度（有病率など）。無視すると誤る。"),
                    ("A/B test", "A/B テスト", "2案を無作為に比べる実験。")],
             tip="ベイズの定理は「<strong>事前 × 尤度 → 事後</strong>」。陽性でも病気とは限らないのは、<strong>病気の人がそもそも少ない（基準率が低い）</strong>から。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>① The Frequentist Approach to Probability</li><li>②③ The Bayesian Approach to Probability</li><li>④ Frequentist vs. Bayesian Probability in A/B Testing</li></ul>')]
    b.append(unit(1, "頻度論：長い目で見た相対度数", "統計学の主流の考え方", f'''
  <p><strong>頻度論（frequentist）</strong>では、確率を「同じ試行を<strong>無限にくり返したときの相対度数</strong>」と定義します。前回の大数の法則がその土台です。この授業の信頼区間や仮説検定（M4 以降）は頻度論の考え方で組み立てられています。</p>
  {table(["長所", "短所"], [["世界の事実に根ざしている（客観的）", "無限のくり返しは現実には存在しない"], ["確率は固定で変わらない", "1回きりの出来事（明日の試合の勝率）に確率を付けにくい"], ["同じデータを見れば誰でも同じ答え", "2人の確率が違えば、どちらかが間違い"], ["", "仮定（例：正規分布）が外れると結論も崩れる"]])}
  {P.R('set.seed(7)\nsapply(c(10, 100, 10000), function(n) mean(sample(c(0, 1), n, replace = TRUE)))')}
  <p>コインを 10回・100回・1万回投げたときの表の割合です。回数が増えるほど 0.5 に近づく、これが頻度論の「確率」です。</p>
'''))
    b.append(unit(2, "ベイズ：信念の度合い", "新しい情報で確率を更新する", f'''
  <p><strong>ベイズ（Bayesian）</strong>の考え方では、確率は「ある人が、その出来事が本当だと<strong>どのくらい信じているか</strong>」の度合いです（主観確率）。18世紀のトーマス・ベイズにちなみます。</p>
  <p>「信念の度合い」は<strong>賭け</strong>で表せます。「このチームが勝てば 5 ドルもらえ、負ければ 5 ドル払う」賭けに乗るかどうかは、あなたが勝つ確率をどう見積もるかで決まります。90% だと思うなら喜んで乗るでしょう。</p>
  {table(["長所", "短所"], [["1回きりの出来事にも確率を付けられる", "完全に客観的にはなれない"], ["人によって確率が違っても合理的でいられる", "「誰の信念か」を決める必要がある"], ["事前の情報を使える／新しいデータで更新できる", "概念も計算も（事前分布・事後分布…）初心者には難しい"], ["機械学習など現代の応用が多い", ""]])}
  {note('⚖️ よく言われるまとめ：頻度論は<strong>狭すぎる</strong>（確率を付けたいものの多くを禁じる）、ベイズは<strong>広すぎる</strong>（観察者による違いを許しすぎる）。どちらが正しいというより、<strong>目的に合わせて使い分ける</strong>ものです。')}
'''))
    b.append(unit(3, "ベイズの定理を計算する", "陽性なら本当に病気？", f'''
  <div class="note-box">📐 <strong>ベイズの定理</strong>：P(H | D) = P(D | H) × P(H) ÷ P(D)<br>　H＝仮説（病気である）、D＝データ（検査が陽性）。P(H)＝<strong>事前確率</strong>、P(D | H)＝<strong>尤度</strong>、P(H | D)＝<strong>事後確率</strong>。</div>
  <p>ある病気の有病率は <strong>1%</strong>。検査は、病気の人の <strong>95%</strong> を陽性と判定し、病気でない人の <strong>5%</strong> も誤って陽性にします（架空の数値）。陽性と出た人が本当に病気である確率は？</p>
  {P.R('prior <- 0.01           # P(disease)\nsens  <- 0.95           # P(positive | disease)\nfalse_pos <- 0.05       # P(positive | no disease)\np_pos <- sens * prior + false_pos * (1 - prior)   # P(positive)\nposterior <- sens * prior / p_pos\nround(c(p_pos = p_pos, posterior = posterior), 3)')}
  <p>答えは約 <strong>16%</strong>。陽性でも、本当に病気なのは6人に1人ほどです。病気の人がもともと少ない（基準率 1%）ため、健康な多数の人から出る「偽陽性」の方が多くなるのです。</p>
  {P.R('# Same idea with counts: imagine 10,000 people\nsick <- 10000 * 0.01; healthy <- 10000 - sick\ntrue_pos <- sick * 0.95; false_pos_n <- healthy * 0.05\nc(true_pos = true_pos, false_pos = false_pos_n, share_sick = round(true_pos / (true_pos + false_pos_n), 3))')}
  {warn('「検査の精度 95%」から「陽性なら 95% 病気」と考えるのは、<strong>P(陽性 | 病気)</strong> と <strong>P(病気 | 陽性)</strong> の取り違えです（前回の条件付き確率の注意と同じ）。<strong>基準率の無視（base rate fallacy）</strong>と呼ばれます。')}
'''))
    b.append(unit(4, "A/B テストでの2つの見方", "同じ実験、違う問い", f'''
  <p>Web サイトのボタンを A 案・B 案で無作為に出し分け、クリック率を比べる<strong>A/B テスト</strong>を考えます。</p>
  {table(["", "頻度論のアプローチ", "ベイズのアプローチ"], [["問い", "「差がない」としたら、こんなに差が出る確率は？（p 値）", "データを見た今、B が A より良い確率は？"], ["事前の知識", "使わない", "過去のテスト結果などを事前分布として使う"], ["いつ判断？", "あらかじめ決めたサンプルサイズまで集める", "データが集まるたびに更新できる"], ["答えの形", "有意／有意でない", "「B が良い確率 92%」のような確率"]])}
  <p>この授業（M4〜M6）では、主に<strong>頻度論</strong>の道具（信頼区間・仮説検定・p 値）を学びます。ただし「p 値は帰無仮説が正しい確率ではない」など、ベイズの問いと混同しないことが大切です。</p>
  {practice("p-m3by-u4", "基準率を変えてみる", "上の検査の例で、有病率（prior）が <strong>10%</strong> の集団だったら、陽性の人が本当に病気である確率はいくつになるか計算してください。",
             ["prior", "0.1", "0.95", "0.05"], 'prior <- 0.10\np_pos <- 0.95 * prior + 0.05 * (1 - prior)\n0.95 * prior / p_pos', "約 0.679（68%）。基準率が上がると、同じ検査でも陽性の信頼度が大きく上がる。")}
'''))
    b.append(teal('➡️ <strong>次の講義へ：</strong>ここからは、偶然の結果を数で表す<strong>確率変数</strong>と、その<strong>分布</strong>です。次の <a href="m3_discrete.html">離散分布：一様・二項・幾何・ポアソン</a>へ。'))
    q = [("How does the frequentist view define probability?", "Long-run relative frequency", ["A person's degree of belief", "The odds offered by a bookmaker", "The number of possible outcomes"], "Frequentists define probability as the proportion of times an event occurs over very many repetitions."),
         ("Which is an advantage of the Bayesian view?", "It updates with new data", ["It is perfectly objective", "It never needs any assumptions", "It forbids subjective beliefs"], "Bayesians start from a prior and update it with data, and can assign probabilities to one-off events."),
         ("In Bayes' theorem, what is P(H) called?", "The prior probability", ["The posterior probability", "The likelihood of data", "The p-value of the test"], "P(H) is the probability of the hypothesis before seeing the data: the prior."),
         ("A disease affects 1% of people. A test has 95% sensitivity and a 5% false-positive rate. P(disease | positive) is about…", "16%", ["95%", "50%", "5%"], "Because the disease is rare, false positives from the healthy 99% outnumber true positives: 0.0095 / 0.059 ≈ 0.16."),
         ("Why is P(disease | positive) much lower than the test's 95% sensitivity here?", "The base rate of disease is low", ["The test was given incorrectly", "Sensitivity is always overstated", "Positive results are independent"], "With a low base rate, most positives come from the many healthy people (false positives)."),
         ("Which question fits a Bayesian A/B test?", "What is the chance B beats A?", ["Is the p-value below 0.05?", "How many visitors saw page A?", "Should α be 0.01 or 0.05?"], "A Bayesian analysis gives a direct probability that B is better, given the data and the prior.")]
    return L, "\n".join(b), q

# =============================================================== 4. discrete distributions
def m3_discrete(P):
    L = dict(slug="m3_discrete", mod=MOD, icon="🧮", title="確率変数と離散分布：一様・二項・幾何・ポアソン",
             tag="M3 · Probability Distributions — Random Variables, Uniform, Binomial Probabilities &amp; Distributions, Geometric, Poisson",
             lead="結果を数で表した<strong>確率変数</strong>（離散と連続）、R の分布関数の<strong>4つの接頭辞 r・d・p・q</strong>、そして<strong>一様・二項・幾何・ポアソン</strong>の4つの分布を、使える条件と R の計算でまとめます。",
             video="Random Variables ／ Uniform Distributions ／ Binomial Probabilities ／ Binomial Distributions ／ Geometric Distributions ／ Poisson Distribution",
             unav=["① 確率変数と r・d・p・q", "② 一様分布", "③ 二項分布", "④ 幾何分布とポアソン分布"],
             terms=[("random variable", "確率変数", "偶然の結果で値が決まる数。"),
                    ("discrete / continuous", "離散／連続", "数える値／測る値。"),
                    ("r d p q", "4つの接頭辞", "乱数・ちょうどの確率（密度）・以下の確率・パーセンタイル。"),
                    ("uniform", "一様分布", "どの値も同じ確からしさ。"),
                    ("binomial B(n, p)", "二項分布", "n 回中の成功数。成功/失敗・独立・回数固定・p 一定。"),
                    ("lower.tail", "下側", "TRUE なら「以下」、FALSE なら「より大きい」。"),
                    ("geometric", "幾何分布", "初めて成功するまでの回数（R は失敗の回数）。"),
                    ("Poisson (λ)", "ポアソン分布", "一定の時間・空間での発生回数。平均＝分散＝λ。"),
                    ("10% condition", "10% 条件", "非復元でも標本が母集団の10%以下なら独立とみなせる。")],
             tip="<strong>「ちょうど」→ d</strong>、<strong>「以下」→ p</strong>、<strong>「以上」→ 1 − p(k − 1)</strong> か <strong>p(k − 1, lower.tail = FALSE)</strong>。「4以上」は q = 3 を使うのがコツ。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>① 550_Probability Distributions ／ Random Variables</li><li>② Uniform Distributions</li><li>③ Binomial Probabilities ／ Binomial Distributions</li><li>④ Geometric Distributions ／ Poisson Distribution</li></ul>')]
    b.append(unit(1, "確率変数と、R の4つの接頭辞", "結果を数にする", f'''
  <p><strong>分布（distribution）</strong>は「変数がどんな値を、どのくらいの頻度でとるか」です。<strong>確率変数（random variable）</strong>は、ランダムな試行の結果で値が決まる<strong>数</strong>です。例：コインを2回投げたときの裏の回数 T（0, 1, 2 のどれか）。</p>
  {table(["", "離散 discrete", "連続 continuous"], [["値", "数直線上の飛び飛びの点", "ある区間のすべての値"], ["イメージ", "数える（購入数、不良品の数、来店者数）", "測る（冷凍庫の温度、重さ、滞在時間）"], ["グラフ", "棒（確率）", "密度曲線（下の面積が確率、全体で 1）"], ["この回の分布", "一様・二項・幾何・ポアソン", "一様・正規・t・χ²・F（次の回以降）"]])}
  <p>R の分布関数には、すべて<strong>同じ4つの接頭辞</strong>が付きます。二項分布なら <code>rbinom</code>・<code>dbinom</code>・<code>pbinom</code>・<code>qbinom</code>。</p>
  {table(["接頭辞", "意味", "問いの形"], [["r", "random：乱数を生成", "シミュレーションしたい"], ["d", "density：ちょうどその値の確率（連続なら密度）", "「ちょうど 3 人」"], ["p", "probability：その値<strong>以下</strong>の累積確率", "「3 人以下」"], ["q", "quantile：累積確率から値を逆算", "「50 パーセンタイルは何人？」"]])}
'''))
    b.append(unit(2, "一様分布", "どれも同じ確からしさ", f'''
  <p><strong>離散一様分布</strong>は、サイコロのように<strong>どの値も同じ確率</strong>の分布です。顧客 ID から無作為に調査対象を選ぶのも、離散一様分布からの抽出です。</p>
  {P.R('ids <- 50001:58000          # 8,000 customer IDs\nset.seed(42)\nchosen <- sample(ids, size = 800, replace = FALSE)\nhead(chosen, 8)\nhist(chosen, col = "lightblue", main = "Discrete uniform: sampled IDs", xlab = "ID")', plot=True, h=300)}
  <p>ヒストグラムはほぼ平ら（山がない）です。<strong>連続一様分布</strong>は、区間内の<strong>どの実数も</strong>同じ確からしさでとります。<code>runif()</code> で生成します。</p>
  {P.R('set.seed(42)\nround(runif(6, min = 2, max = 5), 2)\npunif(3, min = 2, max = 5)      # P(X <= 3)')}
  <p>2〜5 の一様分布で 3 以下になる確率は、区間の長さの比 (3 − 2)/(5 − 2) = 1/3 です。連続一様分布は、ベイズ統計の「情報のない事前分布」としても使われます。</p>
'''))
    b.append(unit(3, "二項分布", "n 回中の成功の数", f'''
  <p>ある通販会社がクーポン付きメールを <strong>12 人</strong>に送り、1人あたり <strong>20%</strong> の確率でクーポンが使われるとします（架空）。クーポンを使う人数 X は<strong>二項分布</strong> X ~ B(n = 12, p = 0.2) に従います。</p>
  <h3>二項分布の4条件（BINS）</h3>
  {table(["条件", "この例"], [["<strong>B</strong>inary：結果が成功／失敗の2つ", "使う／使わない"], ["<strong>I</strong>ndependent：試行どうしが独立", "人どうしは影響しない（母集団が標本の10倍以上なら非復元でも OK＝10% 条件）"], ["<strong>N</strong>umber：試行回数 n が固定", "12 人"], ["<strong>S</strong>ame：成功確率 p が一定", "全員 0.2"]])}
  {P.R('dbinom(3, size = 12, prob = 0.2)                     # exactly 3\nchoose(12, 3) * 0.2^3 * 0.8^9                        # same, by the formula\npbinom(3, size = 12, prob = 0.2)                     # at most 3\npbinom(3, size = 12, prob = 0.2, lower.tail = FALSE) # 4 or more\nqbinom(0.5, size = 12, prob = 0.2)                   # median number')}
  <p>公式は P(X = k) = ₙCₖ pᵏ (1 − p)ⁿ⁻ᵏ（<code>choose(n, k)</code> が ₙCₖ）。「ちょうど3人」は約 0.236、「3人以下」は約 0.795、「4人以上」は約 0.205 です。</p>
  {warn('「<strong>4 人以上</strong>」を求めるとき、<code>pbinom(4, …, lower.tail = FALSE)</code> と書くと「<strong>4 より大きい</strong>（5 人以上）」になってしまいます。離散分布では <strong>q = 3</strong> を使うのが正解です。')}
  {P.R('k <- 0:12\nplot(k, dbinom(k, 12, 0.2), type = "h", lwd = 5, las = 1, col = "steelblue",\n     xlab = "Number of customers who use the coupon", ylab = "Probability",\n     main = "X ~ B(12, 0.2)")', plot=True, h=320)}
  <p>シミュレーションでも確かめられます。大数の法則により、くり返しを増やすほど理論値に近づきます。</p>
  {P.R('set.seed(123)\nsims <- rbinom(10000, size = 12, prob = 0.2)\nmean(sims >= 4)')}
'''))
    b.append(unit(4, "幾何分布とポアソン分布", "「初めての成功まで」と「一定時間の回数」", f'''
  <h3>幾何分布：初めて成功するまで</h3>
  <p>営業電話の成約率が 0.1 のとき、<strong>初めて成約するのが何本目か</strong>は幾何分布に従います。条件は二項分布とほぼ同じ（成功/失敗・独立・p 一定）ですが、試行回数は決まっておらず「<strong>初めての成功</strong>」で止まります。右に歪んだ分布で、平均は 1/p（ここでは 10 本目）です。</p>
  {P.R('p <- 0.1\n# R counts FAILURES before the first success (X >= 0)\ndgeom(4, prob = p)                      # first success on call 5\np * (1 - p)^4                           # same by formula (trial-count version)\npgeom(19, prob = p, lower.tail = FALSE) # 20+ failures, i.e. success on call 21 or later')}
  {warn('R の <code>dgeom()</code> は「<strong>成功の前の失敗の数</strong>（0 から）」で数えます。「<strong>何本目</strong>で初めて成功するか（1 から）」で考えるときは、<strong>1 を引いて</strong>渡します（5本目 → <code>dgeom(4, …)</code>）。シミュレーションでは <code>rgeom(…) + 1</code>。')}
  <h3>ポアソン分布：一定の時間・空間での回数</h3>
  <p>サポート窓口に<strong>1時間あたり平均 4 件</strong>の問い合わせが来るとします。1時間の件数はポアソン分布 X ~ Poisson(λ = 4) で表せます。条件は、①同じ長さの区間なら発生確率が同じ、②区間どうしの発生が独立、の2つです。</p>
  {P.R('dpois(2, lambda = 4)                    # exactly 2 in an hour\n4^2 * exp(-4) / factorial(2)            # formula: lambda^x e^-lambda / x!\nppois(6, lambda = 4, lower.tail = FALSE) # more than 6 in an hour\nppois(0, lambda = 4 * 30 / 60)          # no calls in 30 minutes (lambda = 2)\nqpois(0.9, lambda = 4)                  # 90th percentile')}
  <p>区間の長さを変えるときは <strong>λ も比例させます</strong>（1時間 4 件 → 30分 2 件）。ポアソン分布は<strong>平均と分散がどちらも λ</strong> という特徴があります。</p>
  {practice("p-m3ds-u4", "二項とポアソンを使い分ける", "（1）不良率 3% の部品を 50 個検査したとき、不良品が <strong>2 個以下</strong>の確率。（2）1日平均 1.5 件起こるサーバー障害が、ある日 <strong>ちょうど 0 件</strong>の確率。",
             ["pbinom", "50", "0.03", "dpois"], 'pbinom(2, size = 50, prob = 0.03)\ndpois(0, lambda = 1.5)', "（1）は回数が決まった成功/失敗なので二項：約 0.811。（2）は一定時間の発生回数なのでポアソン：約 0.223。")}
'''))
    b.append(teal('➡️ <strong>次の講義へ：</strong>次はもっとも重要な連続分布、<a href="m3_normal.html">正規分布</a>です。<code>pnorm()</code> と <code>qnorm()</code> で確率とパーセンタイルを計算します。'))
    q = [("Which is a discrete random variable?", "Items in a shopping cart", ["Weight of a shopping cart in kg", "Time a shopper spends in a store", "Temperature inside a freezer"], "Counts take separate whole-number values; weight, time and temperature are measured (continuous)."),
         ("Which R prefix gives the probability of 'at most k'?", "p (pbinom)", ["d (dbinom)", "q (qbinom)", "r (rbinom)"], "p functions give the cumulative probability P(X ≤ k)."),
         ("Which situation is NOT binomial?", "Calls made until the first sale", ["12 emails, each opened with p = 0.2", "50 parts, each faulty with p = 0.03", "10 coin tosses counting heads"], "Binomial needs a fixed number of trials; 'until the first success' is geometric."),
         ("X ~ B(12, 0.2). Which code gives P(X ≥ 4)?", "pbinom(3, 12, 0.2, lower.tail = FALSE)", ["pbinom(4, 12, 0.2, lower.tail = FALSE)", "dbinom(4, 12, 0.2, lower.tail = FALSE)", "qbinom(4, 12, 0.2, lower.tail = TRUE)"], "lower.tail = FALSE gives P(X > q), so P(X ≥ 4) = P(X > 3) uses q = 3."),
         ("A help desk gets 4 calls per hour on average. What λ models a 15-minute period?", "λ = 1", ["λ = 4", "λ = 15", "λ = 60"], "Scale λ with the interval length: 4 × 15/60 = 1."),
         ("For a Poisson distribution with λ = 4, what is the variance?", "4.0", ["2.0", "16", "8.0"], "A Poisson distribution's mean and variance are both λ.")]
    return L, "\n".join(b), q

# =============================================================== 5. normal
def m3_normal(P):
    L = dict(slug="m3_normal", mod=MOD, icon="🔔", title="正規分布：pnorm・qnorm と二項／ポアソンの正規近似",
             tag="M3 · Probability Distributions — Normal Distributions, Modeling Binomial &amp; Poisson with Normal Curves",
             lead="連続分布の代表<strong>正規分布</strong>で、「〜以下」「〜以上」「〜の間」の確率を <code>pnorm()</code>、パーセンタイルを <code>qnorm()</code> で求めます。さらに、<strong>二項分布やポアソン分布を正規分布で近似</strong>できる条件と、<strong>標準正規分布</strong>を学びます。",
             video="Normal Distributions ／ Modeling Binomial &amp; Poisson with Normal Curves",
             unav=["① 正規分布の性質", "② pnorm で確率", "③ qnorm でパーセンタイル", "④ 正規近似と標準正規"],
             terms=[("normal N(μ, σ)", "正規分布", "単峰・左右対称の釣鐘型。平均＝中央値＝最頻値。"),
                    ("density curve", "密度曲線", "下の面積が確率。全体の面積は 1。"),
                    ("pnorm()", "累積確率", "その値以下の確率（下側の面積）。"),
                    ("qnorm()", "分位点", "累積確率からその値を求める。"),
                    ("dnorm()", "密度", "曲線の高さ。グラフ用で、確率ではない。"),
                    ("normal approximation", "正規近似", "条件を満たせば二項・ポアソンを正規分布で近似。"),
                    ("standard normal N(0, 1)", "標準正規分布", "平均 0、標準偏差 1。z の分布。")],
             tip="連続分布では「<strong>ちょうど 20</strong>」の確率は 0。だから正規分布の確率計算に <code>dnorm()</code> は使わない。<strong>面積＝確率</strong>で、<code>pnorm()</code> の差を取る。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>①②③ Normal Distributions</li><li>④ Modeling Binomial &amp; Poisson with Normal Curves</li></ul>')]
    b.append(unit(1, "正規分布の性質", "2つの母数で決まる釣鐘", f'''
  <p><strong>正規分布</strong>（ガウス分布）は、連続・単峰・左右対称の<strong>釣鐘型</strong>で、<strong>平均＝中央値＝最頻値</strong>です。身長、測定誤差、試験の得点などが近い形になります。信頼区間や多くの検定も、正規分布（に近い標本分布）を前提にしています。</p>
  <p>形を決めるのは<strong>平均 μ と標準偏差 σ</strong> の2つで、X ~ N(μ, σ) と書きます（分散 σ² で書く本もあるので注意）。</p>
  {P.R('curve(dnorm(x, mean = 30, sd = 5), from = 10, to = 50, lwd = 2, las = 1,\n      xlab = "Delivery time (minutes)", ylab = "Density", main = "X ~ N(30, 5)")\ncurve(dnorm(x, mean = 30, sd = 8), add = TRUE, lwd = 2, lty = 2, col = "red")\nlegend("topright", c("sd = 5", "sd = 8"), lty = c(1, 2), col = c("black", "red"), bty = "n")', plot=True, h=320)}
  <p>標準偏差が大きいほど、低く横に広い曲線になります。曲線の下の<strong>面積は常に 1</strong>（100%）です。</p>
'''))
    b.append(unit(2, "pnorm() で確率を求める", "以下・以上・あいだ", f'''
  <p>ある料理宅配の配達時間は、平均 <strong>30 分</strong>・標準偏差 <strong>5 分</strong>の正規分布に従うとします（架空）。</p>
  {P.R('pnorm(25, mean = 30, sd = 5)                      # P(X <= 25)\npnorm(40, mean = 30, sd = 5, lower.tail = FALSE)   # P(X >= 40)\npnorm(35, 30, 5) - pnorm(28, 30, 5)                # P(28 <= X <= 35)')}
  {table(["問い", "コード", "答え"], [["25分以内", "<code>pnorm(25, 30, 5)</code>", "約 0.159"], ["40分以上", "<code>pnorm(40, 30, 5, lower.tail = FALSE)</code>", "約 0.023"], ["28〜35分", "<code>pnorm(35, …) − pnorm(28, …)</code>", "約 0.497"]])}
  <p>「あいだ」は<strong>大きい方の累積 − 小さい方の累積</strong>です。図で確かめましょう。</p>
  {P.R('mu <- 30; sigma <- 5; lo <- 28; hi <- 35\nxs <- seq(lo, hi, length.out = 200)\ncurve(dnorm(x, mu, sigma), from = mu - 3.5 * sigma, to = mu + 3.5 * sigma,\n      las = 1, xlab = "Delivery time (minutes)", ylab = "Density")\npolygon(c(lo, xs, hi), c(0, dnorm(xs, mu, sigma), 0), col = "skyblue")\ntext(c(lo, hi), 0.002, c(lo, hi), col = "red")', plot=True, h=320)}
  {warn('連続分布では、ちょうど 1 点の確率は <strong>0</strong> です（面積がない）。そのため「以下」と「未満」の区別は気にしなくてよく、<code>dnorm()</code> は<strong>グラフを描くため</strong>に使い、確率の計算には使いません。（離散分布の二項・ポアソンとは違うので注意！）')}
'''))
    b.append(unit(3, "qnorm() でパーセンタイルを求める", "確率から値へ", f'''
  <p><code>qnorm()</code> は <code>pnorm()</code> の<strong>逆</strong>で、「下から何% の位置の値は？」に答えます。</p>
  {P.R('qnorm(0.75, mean = 30, sd = 5)     # third quartile (75th percentile)\nqnorm(0.95, mean = 30, sd = 5)     # 95% of deliveries are faster than this\npnorm(qnorm(0.95, 30, 5), 30, 5)   # round trip back to 0.95')}
  <p>第3四分位（Q3）は <strong>75 パーセンタイル</strong>なので約 33.4 分。「95% の配達がこの時間内に届く」は約 38.2 分です。お店の「○分以内にお届け」の約束を決めるのに使えます。</p>
  {practice("p-m3nm-u3", "正規分布の確率とパーセンタイル", "ある試験の得点が N(500, 100) に従うとします。（1）650 点以上の割合、（2）上位 10% に入るための最低点、を求めてください。",
             ["pnorm", "lower.tail = FALSE", "qnorm", "0.9"], 'pnorm(650, mean = 500, sd = 100, lower.tail = FALSE)\nqnorm(0.90, mean = 500, sd = 100)', "（1）約 0.067（6.7%）。（2）上位 10% ＝ 下から 90% なので <code>qnorm(0.90, …)</code> で約 628 点。")}
'''))
    b.append(unit(4, "正規近似と標準正規分布", "離散分布を曲線で表す", f'''
  <p>離散分布も、条件を満たせば<strong>正規分布で近似</strong>できます。</p>
  {table(["分布", "正規近似できる目安", "近似する正規分布"], [["二項 B(n, p)", "成功数 np と失敗数 n(1 − p) が<strong>どちらも 10 以上</strong>", "平均 np、SD √(np(1 − p))"], ["ポアソン(λ)", "λ が<strong>大きい</strong>（目安 10 以上）", "平均 λ、SD √λ"]])}
  {P.R('n <- 100; p <- 0.4\nk <- 0:n\nplot(k, dbinom(k, n, p), type = "h", lwd = 2, las = 1, col = "gray40",\n     xlab = "Number of successes", ylab = "Probability", xlim = c(20, 60),\n     main = "B(100, 0.4) and its normal approximation")\ncurve(dnorm(x, n * p, sqrt(n * p * (1 - p))), add = TRUE, col = "red", lwd = 2)', plot=True, h=320)}
  {P.R('pbinom(45, 100, 0.4)                          # exact\npnorm(45.5, mean = 40, sd = sqrt(100 * 0.4 * 0.6))   # normal approx. (+0.5 continuity correction)')}
  <p>np = 40、n(1 − p) = 60 で条件を満たし、正確な値（約 0.869）と近似（約 0.870）はほぼ一致します（離散を連続で近似するので 0.5 を足す<strong>連続性補正</strong>を使っています）。</p>
  <h3>標準正規分布 N(0, 1)</h3>
  <p>平均 0・標準偏差 1 の正規分布を<strong>標準正規分布</strong>といい、z スコアの分布です。<code>pnorm()</code> は <code>mean</code> と <code>sd</code> を省くと標準正規分布になります。</p>
  {P.R('pnorm(1.96)\nqnorm(0.975)')}
  {warn('標準化（z スコアに変換）しただけでは「標準<strong>正規</strong>」にはなりません。平均 0・SD 1 になるだけで、<strong>形は元のまま</strong>です（M2 の z スコアの回を参照）。')}
'''))
    b.append(teal('➡️ <strong>次の講義へ：</strong>推測統計でよく使う「正規分布の親戚」、<a href="m3_tchif.html">t 分布・χ² 分布・F 分布</a>へ。'))
    q = [("For a normal distribution, how are the mean, median and mode related?", "All three are equal", ["Mean > median > mode", "Mode > median > mean", "They differ at random"], "A normal curve is symmetric and unimodal, so the mean, median and mode are at the same point."),
         ("Delivery time ~ N(30, 5). Which code gives P(X ≥ 40)?", "pnorm(40, 30, 5, lower.tail = FALSE)", ["pnorm(40, 30, 5, lower.tail = TRUE)", "dnorm(40, 30, 5, lower.tail = FALSE)", "qnorm(40, 30, 5, lower.tail = FALSE)"], "pnorm gives areas; lower.tail = FALSE gives the area above 40."),
         ("Why don't we use dnorm() to find P(X = 20) for a normal variable?", "One point has zero probability", ["dnorm only works with N(0, 1)", "dnorm always returns exactly 1", "dnorm needs at least two values"], "For a continuous variable, probability is area; one point has no area. dnorm gives the curve's height."),
         ("Which code finds the 75th percentile of N(30, 5)?", "qnorm(0.75, 30, 5)", ["pnorm(0.75, 30, 5)", "dnorm(0.75, 30, 5)", "rnorm(0.75, 30, 5)"], "q functions turn a cumulative probability into a value: about 33.4 minutes."),
         ("When is B(n, p) approximately normal?", "If np and n(1 − p) are both ≥ 10", ["If n is less than 30 in total", "If p is exactly 0.5 for every trial", "If the trials are all dependent"], "With at least 10 expected successes and 10 expected failures, the binomial is close to normal."),
         ("What does pnorm(1.96) return (standard normal)?", "About 0.975", ["About 0.950", "About 0.025", "About 1.960"], "About 97.5% of the standard normal lies below z = 1.96, leaving 2.5% in the upper tail.")]
    return L, "\n".join(b), q

# =============================================================== 6. t, chi-square, F
def m3_tchif(P):
    L = dict(slug="m3_tchif", mod=MOD, icon="📐", title="t 分布・χ² 分布・F 分布",
             tag="M3 · Probability Distributions — T Distributions, Chi-square Distributions, F Distribution",
             lead="推測統計の主役になる3つの連続分布です。母標準偏差がわからないときの <strong>t 分布</strong>（自由度・重い裾・臨界値）、正規乱数の2乗和からできる <strong>χ² 分布</strong>、2つの χ² の比である <strong>F 分布</strong>を、R の <code>pt/qt</code>・<code>pchisq</code>・<code>pf</code> とシミュレーションで理解します。",
             video="T Distributions ／ Chi-square Distributions ／ F Distribution",
             unav=["① t 分布と自由度", "② t の臨界値", "③ χ² 分布", "④ F 分布"],
             terms=[("t distribution", "t 分布", "σ を s で推定するときに使う。対称で裾が重い。"),
                    ("degrees of freedom (df)", "自由度", "分布の形を決める母数。1標本の t なら n − 1。"),
                    ("heavier tails", "裾が重い", "中心から遠い値が出やすい。"),
                    ("critical value", "臨界値", "信頼区間・検定で使う境目の値（qt などで求める）。"),
                    ("chi-square χ²", "カイ二乗分布", "標準正規の2乗の和。0 以上、右に歪む。平均＝df。"),
                    ("F distribution", "F 分布", "2つの χ²（÷df）の比。df が2つ。ANOVA で使う。"),
                    ("pt / qt", "t の関数", "累積確率／分位点。"),
                    ("pchisq / pf", "χ²・F の関数", "累積確率（右側は lower.tail = FALSE）。")],
             tip="t は「<strong>正規分布の裾を重くしたもの</strong>」で df が増えると正規に近づく。χ² と F は<strong>0 以上・右に歪む</strong>ので、ふつう<strong>右側の面積</strong>（lower.tail = FALSE）を求める。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>①② T Distributions</li><li>③ Chi-square Distributions</li><li>④ F Distribution</li></ul>')]
    b.append(unit(1, "t 分布と自由度", "裾が重い正規分布の親戚", f'''
  <p>標本から平均を推測するとき、ふつうは<strong>母標準偏差 σ がわかりません</strong>。そこで標本標準偏差 s で代用しますが、その分の不確かさを反映した分布が <strong>t 分布</strong>（スチューデントの t 分布）です。</p>
  <p>標準正規分布と同じく<strong>連続・左右対称・平均 0</strong> ですが、形を決める母数は<strong>自由度（df）</strong>の1つだけです。</p>
  {P.R('curve(dnorm(x), from = -4, to = 4, lwd = 2, las = 1, ylab = "Density", xlab = "t",\n      main = "t distributions approach the normal as df grows")\ncols <- c("red", "orange", "darkgreen")\nfor (i in 1:3) curve(dt(x, df = c(1, 3, 10)[i]), add = TRUE, lwd = 2, lty = 2, col = cols[i])\nlegend("topright", c("normal", "df = 1", "df = 3", "df = 10"), lwd = 2,\n       lty = c(1, 2, 2, 2), col = c("black", cols), bty = "n")', plot=True, h=330)}
  <p>df が小さいほど<strong>山が低く、裾が重い（厚い）</strong>。df が大きくなるにつれて標準正規分布に近づきます。裾の重さは、右裾の面積で比べるとよくわかります。</p>
  {P.R('round(c(df1 = pt(2, df = 1, lower.tail = FALSE), df3 = pt(2, df = 3, lower.tail = FALSE),\n        df10 = pt(2, df = 10, lower.tail = FALSE), normal = pnorm(2, lower.tail = FALSE)), 4)')}
  <h3>なぜ df = n − 1？</h3>
  <p>5つのデータの平均が 20 と決まっているとき、4つまでは自由に選べますが、<strong>最後の1つは自動的に決まります</strong>（合計が 100 になるように）。標本平均を計算に使ったぶん、自由に動ける値が1つ減る、これが n − 1 です。</p>
  {P.R('known <- c(2, 5, 15, 60)\n5 * 20 - sum(known)   # the 5th value is forced')}
'''))
    b.append(unit(2, "t の臨界値", "qt() と qnorm() を比べる", f'''
  <p>t 分布は、<strong>平均（と回帰の傾き）</strong>の信頼区間や検定で、<strong>臨界値</strong>を求めるのに使います。たとえば標本サイズ 12 なら df = 11 で、97.5 パーセンタイル（両側 95% の境目）は：</p>
  {P.R('qt(0.975, df = 11)\nqnorm(0.975)\nqt(0.975, df = c(5, 30, 100, 1000))')}
  <p>t の臨界値（2.201）は z の臨界値（1.960）より<strong>大きい</strong>。裾が重いぶん、同じ 95% を確保するには遠くまで取る必要があるからです。df が増えると 1.96 に近づきます。</p>
  {note('🧰 t 分布では主に <code>pt()</code>（確率）と <code>qt()</code>（臨界値）を使います。<code>rt()</code>（乱数）や <code>dt()</code>（ちょうどの密度）はグラフやシミュレーション以外ではあまり使いません。M5 の t 検定・t 区間で本格的に登場します。')}
'''))
    b.append(unit(3, "χ²（カイ二乗）分布", "正規乱数の2乗を足すと", f'''
  <p>標準正規分布の値を<strong>2乗して k 個足す</strong>と、自由度 k の <strong>χ² 分布</strong>になります（「平方和」が鍵）。シミュレーションで作ってみます。</p>
  {P.R('set.seed(550)\nz1 <- rnorm(5000); z2 <- rnorm(5000); z3 <- rnorm(5000)\nchi3 <- z1^2 + z2^2 + z3^2\nc(mean = mean(chi3), var = var(chi3))\nhist(chi3, breaks = 50, freq = FALSE, col = "lightblue", las = 1,\n     main = "Sum of 3 squared normals vs chi-square (df = 3)", xlab = "Chi-square value")\ncurve(dchisq(x, df = 3), add = TRUE, lwd = 2, col = "red")', plot=True, h=330)}
  {table(["χ² 分布の性質", ""], [["値", "<strong>0 以上</strong>のみ（2乗の和だから）"], ["形", "<strong>右に歪む</strong>。df が増えると対称に近づく"], ["平均と分散", "平均 = df、分散 = 2 × df（上のシミュレーションでも約 3 と約 6）"], ["山の位置", "df − 2（df &gt; 2 のとき）"]])}
  <p>M5 の<strong>適合度検定・独立性検定</strong>で使います。たとえば、ある標本から χ² = 9.5（df = 4）が得られたとき、それ以上の値が出る確率は：</p>
  {P.R('pchisq(9.5, df = 4, lower.tail = FALSE)\nset.seed(1); mean(rchisq(10000, df = 4) >= 9.5)   # simulation check')}
  <p>約 5% なので、偶然にしては「やや珍しい」値です（詳しい判断は M4・M5 の仮説検定で）。</p>
'''))
    b.append(unit(4, "F 分布", "2つの χ² の比", f'''
  <p><strong>F 分布</strong>は、2つの χ²（それぞれ自由度で割ったもの）の<strong>比</strong>です。そのため自由度を<strong>2つ</strong>持ちます：分子の df₁ と分母の df₂。<strong>連続・単峰・右に歪む・0 以上・面積 1</strong>です。</p>
  {P.R('curve(df(x, df1 = 3, df2 = 8), from = 0, to = 6, lwd = 2, las = 1,\n      xlab = "F", ylab = "Density", main = "F distributions")\ncurve(df(x, df1 = 10, df2 = 30), add = TRUE, lwd = 2, lty = 2, col = "red")\nlegend("topright", c("F(3, 8)", "F(10, 30)"), lwd = 2, lty = c(1, 2),\n       col = c("black", "red"), bty = "n")', plot=True, h=320)}
  <p>M5 の <strong>ANOVA（分散分析）</strong>では、F 値が大きいほど「グループ間の差が偶然では説明しにくい」ことを意味します。F(3, 8) で F = 4.5 以上が出る確率は：</p>
  {P.R('pf(4.5, df1 = 3, df2 = 8, lower.tail = FALSE)\nset.seed(120); round(rf(10, df1 = 3, df2 = 8), 2)')}
  {r4ds("Ch.5 Exploratory Data Analysis", "分布の知識は、データの「典型的な値」と「珍しい値」を見分ける土台になる。EDA でヒストグラムを見るときも、ここで学んだ形（対称・右に歪む・裾の重さ）を思い浮かべると、どんなモデルや検定が合いそうか判断しやすい。")}
  {practice("p-m3tf-u4", "3つの分布の確率", "（1）df = 20 の t 分布で、t が <strong>2.5 より大きい</strong>確率。（2）df = 2 の χ² 分布で <strong>6 以上</strong>の確率。（3）F(2, 27) で <strong>3.35 以上</strong>の確率。",
             ["pt", "pchisq", "pf", "lower.tail = FALSE"], 'pt(2.5, df = 20, lower.tail = FALSE)\npchisq(6, df = 2, lower.tail = FALSE)\npf(3.35, df1 = 2, df2 = 27, lower.tail = FALSE)', "（1）約 0.011、（2）約 0.050、（3）約 0.050。どれも右側の面積なので <code>lower.tail = FALSE</code>。")}
'''))
    b.append(teal('➡️ <strong>次のモジュールへ：</strong>分布の道具がそろいました。<a href="m3_basics.html">550 M4 推測の基礎</a>で、データ収集と帰無仮説から仮説検定を組み立てていきます。'))
    q = [("When do we use a t distribution instead of the normal?", "When σ is estimated by the sample SD", ["When the data are categorical counts", "When the sample size is very large", "When the mean is known exactly"], "Replacing the unknown population SD with s adds uncertainty, which the t distribution accounts for."),
         ("Compared with the standard normal, a t distribution with df = 3 has…", "Heavier tails and a lower peak", ["Lighter tails and a taller peak", "A mean that is larger than zero", "Only positive possible values"], "Small df means more spread in the tails; as df grows, t approaches the normal."),
         ("A one-sample t procedure uses n = 12. What are the degrees of freedom?", "11", ["12", "13", "10"], "For one quantitative variable, df = n − 1 = 11."),
         ("Why is qt(0.975, df = 11) larger than qnorm(0.975)?", "The t curve has heavier tails", ["The t curve is not symmetric", "qt rounds to one decimal place", "df = 11 makes the mean larger"], "With more area in the tails, you must go further out to leave 2.5% in each tail."),
         ("Which statement about the chi-square distribution is true?", "Its mean equals its df", ["It can take negative values", "It is always left-skewed", "Its mean is always zero"], "A chi-square is a sum of squares, so it is non-negative and right-skewed, with mean = df."),
         ("How many degrees of freedom does an F distribution have?", "2", ["1", "3", "0"], "F is a ratio of two scaled chi-squares, so it has a numerator df and a denominator df.")]
    return L, "\n".join(b), q

LESSONS = [m3_prob, m3_cond, m3_bayes, m3_discrete, m3_normal, m3_tchif]
