"""550 M1: R入門 & 測定水準 — 5 lessons."""
from lib550 import *

MOD = "550 M1"
R4DS = '📗 <strong>R4DS（Wickham &amp; Grolemund, <em>R for Data Science</em>）より：</strong>'

def r4ds(ch, t):
    return f'<div class="teal-box">{R4DS}{t}<br><span style="font-size:.85rem">出典: R4DS {ch}（内容を要約・日本語で再構成）</span></div>'

# =============================================================== 1. levels
def m1_levels(P):
    L = dict(slug="m1_levels", mod=MOD, icon="📏", title="測定水準：名義・順序・間隔・比率",
             tag="M1 · Levels of Measurement — Nominal, Ordinal, Interval, Ratio &amp; Continuity",
             lead="統計の手法は、データが<strong>どんな種類の値</strong>かで選び方が変わります。最初に<strong>4つの測定水準</strong>（名義・順序・間隔・比率）と、<strong>数字で書かれたカテゴリ</strong>のわな、<strong>離散と連続</strong>の違いを整理します。",
             video="Overall Types ／ Nominal ／ Ordinal ／ Interval ／ Ratio ／ Non-Numeric Coded as Numeric ／ Continuity",
             unav=["① 質的と量的", "② 名義と順序", "③ 間隔と比率", "④ 数字のカテゴリ・連続性"],
             terms=[("categorical (qualitative)", "質的変数", "グループやラベルを表す値。"),
                    ("quantitative", "量的変数", "量として計算に意味がある数値。"),
                    ("nominal", "名義尺度", "順序のないカテゴリ（州・性別）。"),
                    ("ordinal", "順序尺度", "順序はあるが間隔が等しいとは限らない（満足度）。"),
                    ("interval", "間隔尺度", "差に意味があるが、真のゼロがない（摂氏温度）。"),
                    ("ratio", "比率尺度", "真のゼロがあり、比（2倍など）に意味がある（年齢・金額）。"),
                    ("true zero", "真のゼロ", "「その量がまったくない」を意味する0。"),
                    ("discrete", "離散", "数えられる、飛び飛びの値（人数）。"),
                    ("continuous", "連続", "区間内のどの値もとりうる（時間・体重）。")],
             tip="判定は<strong>3つの質問</strong>で：①順序はある？ ②差（間隔）は等しい？ ③0は「何もない」を意味する？ 全部 No なら名義、①だけ Yes なら順序、②まで Yes なら間隔、③まで Yes なら比率。")
    b = []
    b.append(teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>① Overall Types</li><li>② Nominal Data ／ Ordinal Data</li><li>③ Interval Data ／ Ratio Data</li><li>④ Non-Numeric Coded as Numeric ／ Continuity</li></ul>'))
    b.append(unit(1, "データの大きな2分類：質的と量的", "「計算して意味があるか」で分ける", f'''
  <p>データの列（変数）は、まず大きく<strong>質的変数（categorical / qualitative）</strong>と<strong>量的変数（quantitative）</strong>に分かれます。見分ける質問は1つ、「<strong>その値で平均を計算して意味があるか？</strong>」です。</p>
  {table(["分類", "中身", "例（donors データ）"], [["質的（カテゴリ）", "グループ・ラベル", "<code>state</code>（州）、<code>gender</code>、<code>urbanicity</code>（都市度）"], ["量的", "量・測定値", "<code>age</code>（年齢）、<code>totalGivingAmount</code>（寄付総額）"]])}
  <p>このコースでよく使う <code>donors.csv</code>（退役軍人団体の寄付データ）で、列の種類を確かめてみます。<code>str()</code> は各列の<strong>型</strong>を表示します。</p>
  {P.R('donors <- read.csv("donors.csv")\nstr(donors[, c("age", "incomeRating", "state", "urbanicity", "socioEconomicStatus", "totalGivingAmount")])')}
  <p><code>int</code>・<code>num</code> は数値、<code>chr</code> は文字です。ただし<strong>R の型は測定水準そのものではありません</strong>。<code>incomeRating</code> は <code>int</code>（整数）ですが、中身は「1〜7の所得ランク」というカテゴリです（④で詳しく）。</p>
  {simple("質的＝「どのグループ？」に答える値、量的＝「どれくらい？」に答える値。平均を出して意味があるなら量的。")}
'''))
    b.append(unit(2, "名義尺度と順序尺度", "カテゴリにも2種類ある", f'''
  <h3>名義尺度（nominal）</h3>
  <p><strong>名前をつけるだけ</strong>のカテゴリです。並べる順番に意味はありません。州（IL, CA, …）、性別、好きな色など。できる計算は<strong>数える（度数・割合）</strong>ことと<strong>最頻値</strong>くらいです。</p>
  {P.R('table(donors$urbanicity)')}
  <p><code>city</code> と <code>rural</code> のどちらが「上」ということはありません。だから<strong>名義</strong>です。</p>
  <h3>順序尺度（ordinal）</h3>
  <p>カテゴリに<strong>自然な順番</strong>があるものです。<code>socioEconomicStatus</code>（low → average → highest）、アンケートの「とても不満〜とても満足」、メダルの金銀銅など。</p>
  {P.R('table(donors$socioEconomicStatus)')}
  {warn('<strong>順序尺度の落とし穴：</strong>順番はあっても、<strong>段階どうしの間隔が等しいとは限りません</strong>。「不満→普通」と「普通→満足」が同じ幅である保証はないので、順序データの平均は慎重に扱います。中央値や度数のほうが安全です。')}
  {note('🏅 <strong>例：</strong>マラソンの<strong>順位</strong>（1位・2位・3位）は順序尺度。1位と2位の差が1秒でも、2位と3位の差が10分でも、順位は同じ「1つ違い」です。')}
'''))
    b.append(unit(3, "間隔尺度と比率尺度", "「ゼロ」の意味で分かれる", f'''
  <p>どちらも<strong>量的</strong>で、<strong>差（間隔）が等しい</strong>数値です。違いは<strong>0 が「何もない」を意味するか</strong>です。</p>
  {table(["", "間隔尺度 interval", "比率尺度 ratio"], [["差に意味", "ある", "ある"], ["真のゼロ", "<strong>ない</strong>（0は目盛りの1点）", "<strong>ある</strong>（0＝まったくない）"], ["比（2倍）", "意味がない", "意味がある"], ["例", "摂氏・華氏の温度、西暦年、IQ", "年齢、身長、金額、寄付回数、ケルビン温度"]])}
  <p>摂氏 20℃ は 10℃ の「2倍暑い」わけではありません。0℃ は「熱がない」ではなく、水が凍る点に付けた目盛りだからです。一方、寄付総額 \\$200 は \\$100 の<strong>ちょうど2倍</strong>で、\\$0 は「寄付ゼロ」を意味します。</p>
  {P.R('c(mean(donors$totalGivingAmount), max(donors$totalGivingAmount) / min(donors$totalGivingAmount))')}
  <p>寄付総額は比率尺度なので、平均も「最大は最小の何倍か」も意味があります。</p>
  {simple("温度（摂氏）は「差」はOKだけど「何倍」はNG＝間隔。お金や年齢は0が「なし」なので「何倍」もOK＝比率。")}
'''))
    b.append(unit(4, "数字で書かれたカテゴリと、離散・連続", "見た目の数字にだまされない", f'''
  <h3>Non-numeric coded as numeric（数字でコード化されたカテゴリ）</h3>
  <p>郵便番号、背番号、「1=男性, 2=女性」のようなコード、<code>incomeRating</code>（1〜7）は、<strong>数字で書かれていても計算の意味が薄い</strong>ことがあります。郵便番号の平均は無意味です。</p>
  {P.R('summary(donors$incomeRating)\ntable(donors$incomeRating)')}
  <p><code>summary()</code> は平均（Mean）まで出してくれますが、R は<strong>意味まではわかりません</strong>。所得ランクは<strong>順序尺度</strong>として度数で見るのが基本です。</p>
  {warn('R が <code>int</code> や <code>num</code> と表示しても、それだけで量的とは言えません。<strong>測定水準を判断するのはあなた</strong>です。カテゴリとして扱いたいときは <code>factor()</code> に変換します（M5 以降で使います）。')}
  <h3>離散（discrete）と連続（continuous）</h3>
  <p>量的変数はさらに、<strong>数える</strong>値（離散）と<strong>測る</strong>値（連続）に分かれます。</p>
  {table(["", "離散 discrete", "連続 continuous"], [["イメージ", "数える（0, 1, 2, …）", "測る（区間内のどの値も）"], ["例", "寄付回数、子どもの人数、サイト訪問者数", "時間、体重、気温、寄付の平均額"]])}
  {note('🔍 年齢は本来は連続（生まれてからの時間）ですが、データでは整数に丸めて記録されることが多いです。<strong>記録の仕方</strong>と<strong>本来の性質</strong>を分けて考えましょう。')}
  {practice("p-m1lv-u4", "変数の種類を R で確かめる", "<code>donors</code> の <code>numberGifts</code>（寄付回数）について、<strong>型</strong>を <code>class()</code> で、<strong>値の種類の数</strong>を <code>length(unique())</code> で調べてください。",
             ["class", "numberGifts", "unique", "length"], 'class(donors$numberGifts)\nlength(unique(donors$numberGifts))',
             "整数（integer）で、とりうる値の種類も限られる → 数える量なので<strong>離散</strong>の<strong>比率尺度</strong>（0回＝寄付なし）。")}
'''))
    b.append(teal('➡️ <strong>次の講義へ：</strong>データの種類がわかったら、次は R 自体の操作です。<a href="m1_rbasics.html">R の基本</a>で、電卓としての使い方と変数（オブジェクト）を学びます。'))
    q = [("Which level of measurement is a list of U.S. states (IL, CA, TX, …)?", "Nominal", ["Ordinal", "Interval", "Ratio"], "States are labels with no natural order, so they are nominal."),
         ("Customer satisfaction is recorded as Very unhappy, Unhappy, Neutral, Happy, Very happy. What is it?", "Ordinal", ["Nominal", "Interval", "Ratio"], "The categories have a natural order, but the gaps between them are not guaranteed to be equal, so the data are ordinal."),
         ("Why is temperature in degrees Celsius an interval (not ratio) variable?", "0 °C does not mean no heat at all", ["Its values can be negative numbers", "It is measured with a thermometer", "Its values always have decimals"], "Interval data have equal differences but no true zero; 0 °C is just a point on the scale, so 20 °C is not twice as hot as 10 °C."),
         ("Which variable is measured on a ratio scale?", "Total dollars donated", ["Year a donor was born", "A donor's postal ZIP code", "Income rank from 1 to 7"], "Money has a true zero ($0 means nothing donated), so ratios such as 'twice as much' make sense."),
         ("incomeRating is stored by R as an integer from 1 to 7. What is the best way to treat it?", "As ordinal categories", ["As a ratio variable", "As a continuous variable", "As an interval variable"], "It is a numeric code for ordered income groups. R's data type does not decide the level of measurement."),
         ("Which variable is discrete rather than continuous?", "Number of gifts made", ["Time spent on a site", "Weight of a parcel, kg", "Average gift in dollars"], "Counts take separate whole-number values, so they are discrete. Time, weight and average amounts can take any value in an interval.")]
    return L, "\n".join(b), q

# =============================================================== 2. rbasics
def m1_rbasics(P):
    L = dict(slug="m1_rbasics", mod=MOD, icon="🧮", title="R の基本：電卓・代入・変数名",
             tag="M1 · R Introduction — RStudio, R as a Calculator, Assignment, Naming, Math Functions",
             lead="R と RStudio の役割分担から始めて、<strong>R を電卓として使う</strong>、<code>&lt;-</code> で<strong>値を保存する</strong>、<strong>変数名のルールと習慣</strong>、<code>sqrt()</code> や <code>round()</code> などの<strong>関数と引数</strong>までを学びます。",
             video="Getting Started with R and R Studio ／ R as a Calculator ／ The Assignment Operator ／ Naming Variables ／ More Math Operations ／ Autocomplete, Tab Completion, History",
             unav=["① R と RStudio", "② 電卓としての R", "③ 代入と変数名", "④ 関数と引数"],
             terms=[("R / RStudio", "言語／開発環境", "R が計算する本体、RStudio はそれを使いやすくする画面（IDE）。"),
                    ("console", "コンソール", "コードを1行ずつ実行する窓。"),
                    ("code chunk", "コードチャンク", "R Markdown／Notebook 内のコードの枠。"),
                    ("<-", "代入演算子", "右の値を左の名前に保存する。「gets」と読む。"),
                    ("object / variable", "オブジェクト／変数", "名前をつけて保存した値。Environment に表示される。"),
                    ("snake_case", "スネークケース", "単語を _ でつなぐ命名法（my_sales）。"),
                    ("function / argument", "関数／引数", "round(x, digits = 2) の round が関数、x と digits が引数。"),
                    ("NaN", "非数", "Not a Number。sqrt(-9) などの結果。")],
             tip="エラーの多くは<strong>タイプミス</strong>です。大文字・小文字、スペース、閉じかっこを最初に疑う。<code>+</code> が出て止まったら、かっこか引用符が閉じていないサイン（Esc で中断）。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>① Notes-Getting Started ／ Getting Started with R and R Studio</li><li>② R as a Calculator</li><li>③ The Assignment Operator ／ Naming Variables: Rules &amp; Conventions</li><li>④ More Math Operations ／ Autocomplete, Tab Completion, History</li></ul>')]
    b.append(unit(1, "R と RStudio", "エンジンと運転席", f'''
  <p><strong>R</strong> は統計計算をする<strong>プログラミング言語（エンジン）</strong>、<strong>RStudio</strong> は R を快適に使うための<strong>画面（運転席）</strong>です。両方をインストールし、普段は RStudio を開いて作業します。</p>
  {table(["ペイン（窓）", "役割"], [["Source（ソース）", "Rmd／R スクリプトを書く場所。保存して何度でも実行できる"], ["Console（コンソール）", "1行ずつ実行し、結果がすぐ出る"], ["Environment（環境）", "保存したオブジェクトの一覧。History タブで過去のコマンドも見られる"], ["Files / Plots / Help", "ファイル、グラフ、ヘルプの表示"]])}
  <p>この授業では <strong>R Notebook（.Rmd）</strong> を使います。文章の中に<strong>コードチャンク</strong>を挟み、チャンク単位で実行します。</p>
  {table(["操作", "Mac", "Windows"], [["今の行／選択範囲を実行", "Cmd + Return", "Ctrl + Enter"], ["新しいチャンクを挿入", "Option + Cmd + I", "Ctrl + Alt + I"], ["<code>&lt;-</code> を入力", "Option + −", "Alt + −"]])}
  {note('💬 チャンクの<strong>中</strong>の <code>#</code> はコメント（R が無視する）、チャンクの<strong>外</strong>の <code>#</code> は見出しになり、アウトラインに表示されます。')}
'''))
    b.append(unit(2, "電卓としての R", "計算の順番とタイプミス", f'''
  <p>R は高機能な電卓です。コンソールに表示される <code>&gt;</code> は入力待ちの印なので、自分で打つ必要はありません。</p>
  {P.R('10 + 2\n10 - 2\n10 * 2\n10 / 2\n10 ^ 2')}
  <p>結果の前の <code>[1]</code> は「この行は<strong>1番目の要素</strong>から始まる」という意味です（ベクトルの回で再登場）。</p>
  <h3>計算の順番</h3>
  <p>かけ算・わり算はたし算より先（数学と同じ）。迷ったら<strong>かっこ</strong>で明示します。</p>
  {P.R('1 + 2 * 3\n(1 + 2) * 3')}
  <h3>タイプミスと空白</h3>
  <p>R は<strong>書いたとおり</strong>にしか動きません。<code>+</code> のつもりで <code>=</code> と打つとエラーになります。</p>
  {P.R('10 = 20')}
  <p>空白はある程度自由ですが、<strong>演算子の前後に1つずつ</strong>入れる書き方（<code>10 + 20</code>）が標準です。CodeGrade の課題でもこの書き方が求められます。</p>
  {warn('関数名の途中に空白を入れると動きません（<code>cit ation()</code> はエラー）。かっこを閉じ忘れると、R は続きを待って <code>+</code> を表示します。<strong>Esc</strong> で中断して書き直しましょう。')}
  {r4ds("Ch.2 Workflow: Basics", "R との間には「面倒な計算は R が引き受けるかわりに、指示は完全に正確に」という約束がある。<strong>タイプミスも大文字・小文字の違いも、すべて意味を持つ</strong>。")}
'''))
    b.append(unit(3, "代入（&lt;-）と変数名のルール", "値に名前をつけて保存する", f'''
  <p><code>&lt;-</code> は<strong>代入演算子</strong>です。「右の値を、左の名前に保存する」と読みます。保存しただけでは表示されないので、名前を打つか <code>print()</code> で確認します。</p>
  {P.R('sales <- 350\nroyalty <- 7\nrevenue <- sales * royalty\nrevenue')}
  <p><code>=</code> でも代入できますが、R では <code>&lt;-</code> が慣習です。また<strong>同じ名前に代入し直すと、前の値は上書き</strong>されます。</p>
  {P.R('revenue <- revenue + 550\nrevenue')}
  <h3>変数名のルール（守らないとエラー）</h3>
  {table(["ルール", "OK", "エラー"], [["使える文字は英字・数字・<code>.</code>・<code>_</code>", "<code>my.sales</code>, <code>my_sales</code>", "<code>sales?</code>"], ["空白は使えない", "<code>my.sales</code>", "<code>my sales</code>"], ["数字や <code>_</code> で始められない", "<code>sales1718</code>", "<code>1718sales</code>, <code>_sales</code>"], ["予約語は使えない", "<code>my_break</code>", "<code>break</code>, <code>TRUE</code>, <code>NA</code>, <code>if</code>"]])}
  {P.R('1718sales <- 2000')}
  <p>大文字と小文字は<strong>別の名前</strong>です。<code>sales</code> と <code>Sales</code> は別のオブジェクトになります。</p>
  <h3>変数名の習慣（守ると読みやすい）</h3>
  <ul><li><strong>意味がわかる名前</strong>：<code>sales</code>、<code>revenue</code>（<code>var1</code> は ✗）</li><li><strong>短く</strong>：長すぎる名前は打つのも読むのも大変</li><li><strong>スタイルを統一</strong>：<code>my_new_salary</code>（snake_case）、<code>myNewSalary</code>（camelCase）、<code>my.new.salary</code>（dot.case）。<code>my-new-salary</code> は R では使えない</li><li>CodeGrade 課題では<strong>指定された名前（Q1, Q2 …）</strong>を使う</li></ul>
  {practice("p-m1rb-u3", "代入して計算する", "1冊 \\$12 の本が 85 冊売れました。単価を <code>price</code>、冊数を <code>books</code> に代入し、売上 <code>total</code> を計算して表示してください。",
             ["price", "books", "total", "<-"], 'price <- 12\nbooks <- 85\ntotal <- price * books\ntotal', "<code>total</code> は 1020。代入は表示されないので、最後に名前だけの行を置いて確認する。")}
'''))
    b.append(unit(4, "関数と引数", "sqrt・abs・round と補完機能", f'''
  <p>R には計算用の<strong>関数</strong>がたくさんあります。<code>関数名(引数)</code> の形で使います。</p>
  {P.R('sqrt(225)\n225 ^ 0.5\nabs(-21)\nsqrt(1 + abs(-8))')}
  <p>R は実数で計算するので、負の数の平方根は <code>NaN</code>（Not a Number）になり、警告が出ます。</p>
  {P.R('sqrt(-9)')}
  <h3>引数の名前と順番</h3>
  <p><code>round()</code> には <code>x</code>（丸める数）と <code>digits</code>（小数点以下の桁数、既定値は 0）という引数があります。<strong>名前を書けば順番は自由</strong>、名前を省くと<strong>書いた順番</strong>で割り当てられます。</p>
  {P.R('round(3.14159)\nround(3.14159, 2)\nround(digits = 2, x = 3.14159)\nround(2, 3.14159)')}
  {warn('最後の <code>round(2, 3.14159)</code> は「2 を小数第3位で丸める」と解釈され、結果は 2 です。<strong>名前なしのときは順番が意味を決める</strong>ので注意。また引数の中で <code>&lt;-</code> を使う（<code>round(x &lt;- 3.14)</code>）のは避けます。')}
  <h3>補完と履歴</h3>
  <ul><li><strong>Tab</strong>：関数名・引数名・保存した変数名を補完（打ち間違いが減る）</li><li><strong>↑ キー</strong>（コンソール）：過去のコマンドを呼び出す。Environment ペインの <strong>History</strong> タブでも見られる</li><li>わからない関数は <code>?round</code> でヘルプを開く</li></ul>
'''))
    b.append(teal('➡️ <strong>次の講義へ：</strong>1つの値だけでなく、たくさんの値をまとめて扱うのが R の強みです。次の <a href="m1_vectors.html">ベクトル</a>で、まとめて計算・取り出す方法を学びます。'))
    q = [("In RStudio, which pane lists the objects you have saved, such as sales and revenue?", "The Environment pane", ["The Source editor pane", "The Console output pane", "The Files and Plots pane"], "The Environment pane shows every object you have created; its History tab also lists past commands."),
         ("What does R return for 1 + 2 * 3?", "It returns 7", ["It returns 9", "It returns 6", "It returns 13"], "Multiplication comes before addition, so R computes 2 * 3 = 6 first and then adds 1."),
         ("After running sales <- 350, why does nothing appear in the output?", "Assignment saves without printing", ["R needs = instead of <- to show it", "The value is too large to display", "350 is not a valid number in R"], "An assignment only saves the value. Type the name (sales) or use print(sales) to see it."),
         ("Which of these is a valid R variable name?", "sales_2024", ["2024_sales", "sales 2024", "_sales2024"], "Names must start with a letter (or a period) and cannot contain spaces, so only sales_2024 works."),
         ("What does round(2, 3.14159) return?", "It returns 2", ["It returns 3.14", "It returns 3", "It returns 3.142"], "Without names, arguments are matched by position: x = 2 and digits = 3.14159, so the result is 2."),
         ("Why does sqrt(-9) give NaN?", "R uses real numbers by default", ["The square root needs the ^ symbol", "Negative numbers must be in quotes", "sqrt only accepts whole numbers"], "There is no real square root of a negative number, so R returns NaN (Not a Number) with a warning.")]
    return L, "\n".join(b), q

# =============================================================== 3. vectors
def m1_vectors(P):
    L = dict(slug="m1_vectors", mod=MOD, icon="🔢", title="ベクトル：まとめて計算・型・取り出し",
             tag="M1 · R Introduction — Vectors, Vectorized Operations, Data Types &amp; Indexing",
             lead="R の基本単位は<strong>ベクトル</strong>（同じ型の値の並び）です。<code>c()</code> で作り、<strong>まとめて計算（ベクトル化演算）</strong>し、<strong>文字・論理値</strong>も扱い、<code>[ ]</code> で<strong>番号や条件で取り出す</strong>ところまで進みます。",
             video="Vectorized Operations ／ Vectors &amp; Other Data Types ／ Indexing Vectors",
             unav=["① ベクトルを作る", "② ベクトル化演算", "③ 文字と論理値", "④ 添字で取り出す"],
             terms=[("vector", "ベクトル", "同じ型の値を並べたもの。c() で作る。"),
                    ("c()", "combine", "値をつなげてベクトルにする関数。"),
                    ("index", "添字（インデックス）", "要素の番号。R は 1 から数える。"),
                    ("vectorized operation", "ベクトル化演算", "全要素に同じ計算を一度に行う。"),
                    ("character", "文字型", "\"hello\" のような文字列。"),
                    ("logical", "論理型", "TRUE / FALSE（と NA）。"),
                    ("==, !=, <, <=", "比較演算子", "結果は論理値。= は代入なので比較に使えない。"),
                    ("logical indexing", "論理添字", "x[x > 0] のように条件で取り出す。"),
                    ("coercion", "型の強制変換", "型が混ざると、より一般的な型にそろえられる。")],
             tip="<code>x[x &gt; 0]</code> は「x のうち 0 より大きい<strong>値</strong>」、<code>months[x &gt; 0]</code> は「x が 0 より大きい<strong>位置の月名</strong>」。<strong>角かっこの外側</strong>が何を返すかを決める。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>①② Vectorized Operations</li><li>③ Vectors &amp; Other Data Types</li><li>④ Indexing Vectors</li></ul>')]
    b.append(unit(1, "ベクトルを作る", "c() で値を並べる", f'''
  <p>ある本の月別販売数が、1月 0冊、2月 100冊、3月 200冊、4月 50冊、あとは 0冊だったとします。12個の値を1つの名前で持つには <code>c()</code>（combine）を使います。</p>
  {P.R('sales.by.month <- c(0, 100, 200, 50, 0, 0, 0, 0, 0, 0, 0, 0)\nsales.by.month\nlength(sales.by.month)')}
  <p>要素は <code>[番号]</code> で取り出せます。<strong>R の番号は 1 から</strong>始まります（Python は 0 から）。</p>
  {P.R('sales.by.month[2]\nsales.by.month[7:12]')}
  <p><code>7:12</code> は 7, 8, …, 12 の連番を作る書き方です。要素の値を書き換えることもできます。存在しない番号を指定すると <code>NA</code>（欠損）が返ります。</p>
  {P.R('sales.by.month[5] <- 25\nsales.by.month\nsales.by.month[13]')}
'''))
    b.append(unit(2, "ベクトル化演算", "ループなしで全部に計算", f'''
  <p>ベクトルに計算をすると、<strong>すべての要素に同時に</strong>適用されます。1冊の利益が \\$7 なら、月ごとの利益は1行で出ます。</p>
  {P.R('profit <- sales.by.month * 7\nprofit')}
  <p>同じ長さのベクトルどうしなら、<strong>同じ位置どうし</strong>で計算されます。月ごとの1日あたり利益を出してみます。</p>
  {P.R('days.per.month <- c(31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)\nround(profit / days.per.month, 2)')}
  {r4ds("Ch.16 Vectors（Recycling）", "長さの違うベクトルで計算すると、R は<strong>短い方をくり返して（recycling）</strong>長さをそろえる。<code>sales.by.month * 7</code> は「7」を12回くり返した計算と同じ。長さが割り切れないと警告が出るので、意図しない recycling に注意。")}
  {P.R('c(1, 2, 3, 4) + c(10, 20)\nc(1, 2, 3) + c(10, 20)')}
'''))
    b.append(unit(3, "文字と論理値", "数値以外の型", f'''
  <h3>文字型（character）</h3>
  <p>文字は <code>"…"</code> または <code>'…'</code> で囲みます。</p>
  {P.R('months <- c("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")\nmonths[2:5]\nlength(months)\nnchar("hello")')}
  <p><code>length()</code> は<strong>要素の数</strong>、<code>nchar()</code> は<strong>文字数</strong>です。混同しやすいので注意。</p>
  <h3>論理型（logical）と比較</h3>
  <p>比較の結果は <code>TRUE</code> か <code>FALSE</code> です。等しいかどうかは <code>==</code>（<code>=</code> は代入）。</p>
  {P.R('2 + 2 == 4\nsqrt(25) == 5\n100 < 100\n100 <= 100\n25 != 30')}
  <p>論理値は計算すると <code>TRUE = 1</code>、<code>FALSE = 0</code> として扱われます。だから <code>sum()</code> で「TRUE の個数」が数えられます。</p>
  {P.R('x <- c(TRUE, TRUE, FALSE)\nsum(x)\nmean(x)')}
  {r4ds("Ch.16 Vectors（Coercion）", "1つのベクトルには<strong>1つの型</strong>しか入らない。型を混ぜると、<strong>logical → integer → double → character</strong> の順に、より一般的な型へ自動でそろえられる（暗黙の型変換）。数値の列に文字が1つでも混じると、列全体が文字になるのはこのため。")}
  {P.R('c(1, "a", TRUE)\nclass(c(1, 2.5, TRUE))')}
'''))
    b.append(unit(4, "添字で取り出す", "番号で・条件で", f'''
  <h3>複数の番号で取り出す</h3>
  <p>複数の要素は<strong>番号のベクトル</strong>で指定します。<strong><code>c()</code> を忘れやすい</strong>ので注意。</p>
  {P.R('sales.by.month[c(2, 7, 12)]\nsales.by.month[4:2]\nsales.by.month[2, 7, 12]')}
  <p><code>[2, 7, 12]</code> は「2次元以上の表の位置」と解釈され、ベクトルには使えずエラーになります。</p>
  <h3>論理添字（条件で取り出す）</h3>
  <p>「販売数が 0 より大きい月」を数百万行のデータで目で探すのは無理です。<strong>条件</strong>を角かっこに入れます。</p>
  {P.R('sales.by.month > 0\nsales.by.month[sales.by.month > 0]\nmonths[sales.by.month > 0]')}
  {warn('<strong>何を返したいか</strong>で角かっこの外側を選びます。販売数そのものが欲しいなら <code>sales.by.month[...]</code>、月の名前が欲しいなら <code>months[...]</code>。条件（中身）は同じでも答えが変わります。')}
  {practice("p-m1vc-u4", "条件に合う要素を取り出す", "<code>scores &lt;- c(72, 95, 58, 88, 64)</code> から、<strong>70 点以上の点数</strong>を取り出し、さらにその<strong>人数</strong>を <code>sum()</code> で数えてください。",
             ["scores", ">=", "70", "sum"], 'scores <- c(72, 95, 58, 88, 64)\nscores[scores >= 70]\nsum(scores >= 70)', "<code>scores[scores &gt;= 70]</code> は 72, 95, 88。<code>scores &gt;= 70</code> は論理値なので、<code>sum()</code> で TRUE の数＝3人が出る。")}
'''))
    b.append(teal('➡️ <strong>次の講義へ：</strong>コードが増えてきたら、ファイルの置き場所や作業環境の管理が大切です。次の <a href="m1_workflow.html">作業ディレクトリ・パッケージ</a>へ。'))
    q = [("In R, what is the index of the first element of a vector?", "Index 1", ["Index 0", "Index -1", "Index 12"], "R counts from 1, so x[1] is the first element (Python starts from 0)."),
         ("sales has 12 numbers. What does sales * 7 return?", "12 values, each multiplied by 7", ["One number: total sales times 7", "An error, as 7 is not a vector", "Just the first value times 7"], "Arithmetic on a vector is vectorized: R applies it to every element at once."),
         ("What does sum(c(TRUE, FALSE, TRUE, TRUE)) return?", "It returns 3", ["It returns 4", "It returns NA", "It returns 1"], "TRUE is treated as 1 and FALSE as 0, so the sum counts the TRUE values."),
         ("What is the type of c(1, \"a\", TRUE)?", "character", ["numeric", "logical", "a mixture"], "A vector holds one type only. Mixing types coerces everything to the most general type, which is character here."),
         ("Why does sales.by.month[2, 7, 12] give an error?", "Several positions need c() around them", ["Vectors cannot hold more than 10 values", "Index 12 is outside the vector", "Square brackets only accept one number"], "Commas inside [ ] mean extra dimensions. Use sales.by.month[c(2, 7, 12)] to pick several elements."),
         ("Which code returns the names of the months that had positive sales?", "months[sales.by.month > 0]", ["sales.by.month[months > 0]", "sum(sales.by.month > 0)", "months > sales.by.month"], "The condition goes inside the brackets; the vector outside the brackets (months) decides what is returned.")]
    return L, "\n".join(b), q

# =============================================================== 4. workflow
def m1_workflow(P):
    L = dict(slug="m1_workflow", mod=MOD, icon="🗂️", title="作業ディレクトリ・コメント・パッケージ・環境の整理",
             tag="M1 · R Introduction — Working Directory, Comments, Packages &amp; Cleaning Your Environment",
             lead="R が<strong>どのフォルダを見ているか</strong>（作業ディレクトリ）、未来の自分のための<strong>コメント</strong>、機能を追加する<strong>パッケージ</strong>の「インストール」と「読み込み」の違い、そして<strong>環境の掃除</strong>を学びます。",
             video="Set Working Directory ／ Comments ／ Installing &amp; Loading Packages ／ Cleaning your Environment",
             unav=["① 作業ディレクトリ", "② コメント", "③ パッケージ", "④ 環境の整理"],
             terms=[("working directory", "作業ディレクトリ", "R がファイルを探し、保存するフォルダ。"),
                    ("getwd() / setwd()", "確認／変更", "作業ディレクトリを表示／設定する。"),
                    ("list.files()", "ファイル一覧", "作業ディレクトリ内のファイルを表示。"),
                    ("absolute / relative path", "絶対／相対パス", "ルートからの完全な道順／今いる場所からの道順。"),
                    ("comment (#)", "コメント", "# 以降は R が無視する説明文。"),
                    ("package", "パッケージ", "関数やデータのまとまり（Python のライブラリに相当）。"),
                    ("install.packages()", "インストール", "パッケージを PC に入れる。1回だけ。"),
                    ("library()", "読み込み", "パッケージを今のセッションで使えるようにする。毎回。"),
                    ("rm()", "削除", "環境からオブジェクトを消す。rm(list = ls()) で全部。")],
             tip="パッケージは<strong>電球</strong>のたとえで：<code>install.packages()</code> は電球を<strong>取り付ける</strong>（1回）、<code>library()</code> は<strong>スイッチを入れる</strong>（使うたび）。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>① Set Working Directory</li><li>② Comments</li><li>③ Installing &amp; Loading Packages</li><li>④ Cleaning your Environment</li></ul>')]
    b.append(unit(1, "作業ディレクトリ", "R はどこのファイルを見ている？", f'''
  <p><strong>作業ディレクトリ（working directory）</strong>は、R がファイルを<strong>読み込むときに探し</strong>、<strong>保存するときに置く</strong>フォルダです。<code>read.csv("donors.csv")</code> が「ファイルが見つからない」と言うとき、原因のほとんどはここです。</p>
  {P.R('"donors.csv" %in% list.files()')}
  <p><code>getwd()</code> を実行すると、今のフォルダのパス（例：<code>"/Users/you/Documents/DTSC550"</code>）が表示されます。上のコードは「donors.csv がそのフォルダにあるか」を TRUE/FALSE で確かめています。</p>
  {table(["関数", "役割"], [["<code>getwd()</code>", "今の作業ディレクトリを表示"], ["<code>list.files()</code>", "そのフォルダにあるファイルの一覧"], ["<code>setwd(\"パス\")</code>", "作業ディレクトリを変更"]])}
  <p>RStudio では <strong>Tools → Global Options → General → Default working directory</strong> で既定のフォルダを決められます。いちばん簡単なのは、<strong>.Rmd と CSV を同じフォルダに置く</strong>ことです（Notebook はそのフォルダを作業ディレクトリとして実行されます）。</p>
  {r4ds("Ch.6 Workflow: Projects", "スクリプトの中に <code>setwd(\"/Users/…\")</code> のような<strong>絶対パス</strong>を書くと、他の人の PC では動かない。分析ごとにフォルダ（RStudio Project）を作り、その中で<strong>相対パス</strong>を使うのが長く使えるやり方。パスの区切りは Windows でも <code>/</code> を使うのが安全（<code>\\\\</code> は R で特別な意味を持つ）。")}
  {warn('パスの書き方は Mac（<code>/Users/name/Desktop</code>）と Windows（<code>C:/Users/name/Desktop</code>）で違います。CSV を Excel や Numbers で開いて上書き保存すると形式が変わることがあるので、<strong>開かずにそのまま</strong>使いましょう。')}
'''))
    b.append(unit(2, "コメント", "未来の自分とチームのために", f'''
  <p><code>#</code> から行末までは R が無視します。短いコードでも「何のための計算か」を書いておくと、あとで読むあなたと同僚が助かります。</p>
  {P.R('seeker <- 3.1415          # 1つ目の変数を作る\nlover  <- 2.7183          # 2つ目の変数を作る\nkeeper <- seeker * lover  # 2つを掛けて3つ目を作る\nprint(keeper)             # keeper の値を表示')}
  {note('✍️ 良いコメントは「<strong>何をしているか</strong>」より「<strong>なぜそうするか</strong>」を書きます。例：<code># 欠損があるので na.rm = TRUE</code>。')}
  {r4ds("Ch.6 Workflow: Projects", "長い目で見れば、Environment に残った結果ではなく<strong>スクリプト（とデータ）を「本物の記録」</strong>と考えるべき。スクリプトがあれば環境は再現できるが、逆は難しい。だから RStudio の「終了時にワークスペースを保存しない」設定が勧められている。")}
'''))
    b.append(unit(3, "パッケージ：インストールと読み込み", "2段階を区別する", f'''
  <p><strong>パッケージ</strong>は関数・データのまとまりです（Python の NumPy や pandas のような「ライブラリ」）。R に最初から入っているものもありますが、多くはインターネットから入れます。</p>
  {table(["段階", "関数", "頻度", "電球のたとえ"], [["① インストール", "<code>install.packages(\"dplyr\")</code>", "PC ごとに<strong>1回</strong>", "電球を取り付ける"], ["② 読み込み", "<code>library(dplyr)</code>", "セッション（Notebook）ごとに<strong>毎回</strong>", "スイッチを入れる"]])}
  <p>インストールだけして読み込み忘れると、関数が「見つからない」と言われます。インストールしていないパッケージを読み込もうとしても同じくエラーです。</p>
  {P.R('library(notARealPackage)')}
  {warn('<code>install.packages()</code> は<strong>引用符あり</strong>（<code>"dplyr"</code>）、<code>library()</code> は<strong>引用符なし</strong>でも動く（<code>library(dplyr)</code>）。インストールの行は Notebook に残すと毎回実行されてしまうので、コンソールで1回だけ実行するか <code>#</code> でコメントアウトしておきます。')}
  <p>入っているパッケージの確認・更新は、RStudio の <strong>Packages</strong> ペインが簡単です（チェックが入っているのが読み込み済み）。Windows で「Rtools が必要」という警告が出ても、この授業では無視して大丈夫です。</p>
'''))
    b.append(unit(4, "環境の整理", "rm() とほうきボタン", f'''
  <p>作業を続けると Environment にオブジェクトがたまります。古い値が残っていると、<strong>消したはずの変数が実は生きていて結果が変わる</strong>といった事故の原因になります。</p>
  {P.R('a <- 1\nb <- 2\nls()\nrm(a)\nls()\nrm(list = ls())\nls()')}
  <ul><li><code>ls()</code>：今ある名前の一覧</li><li><code>rm(名前)</code>：1つ削除</li><li><code>rm(list = ls())</code>：全部削除</li><li>RStudio の Environment／Console にある<strong>ほうきアイコン</strong>でも削除できる</li></ul>
  {note('🔁 提出前のチェック：環境を空にしてから <strong>Run All</strong>（すべてのチャンクを上から実行）。エラーなく最後まで動けば、他の人の PC でも再現できる可能性が高くなります。')}
  {practice("p-m1wf-u4", "パッケージを読み込んで環境を空にする", "（1）<code>stats</code> パッケージを読み込み、（2）<code>x &lt;- 5</code> を作ってから、（3）環境のオブジェクトを<strong>すべて</strong>削除するコードを書いてください。",
             ["library", "stats", "rm", "ls"], 'library(stats)\nx <- 5\nrm(list = ls())', "<code>stats</code> は R に最初から入っているので install は不要。<code>rm(list = ls())</code> で全オブジェクトを削除。")}
'''))
    b.append(teal('➡️ <strong>次の講義へ：</strong>準備は整いました。次の <a href="m1_dataframe.html">データフレーム</a>で、表の形のデータを作り、CSV から読み込んで調べます。'))
    q = [("read.csv(\"donors.csv\") says the file cannot be found. What should you check first?", "If it is in the working folder", ["If the file has far too many rows", "If R was updated recently", "If the file uses commas"], "R looks for the file in the working directory. Check with getwd() and list.files()."),
         ("Which function shows the current working directory?", "getwd()", ["setwd()", "dir()", "ls()"], "getwd() gets the working directory; setwd() changes it, dir() lists its files and ls() lists objects."),
         ("How often do you need to run install.packages(\"psych\") on one computer?", "Once", ["Every time you open a notebook", "Every time you use a function", "Never; packages are built in"], "Installing puts the package on the computer once. Loading with library() is done in every session."),
         ("You installed dplyr yesterday. Today its functions are 'not found'. Why?", "It was not loaded with library()", ["You must reinstall it every day", "dplyr only works in the console", "The package was deleted overnight"], "A package must be loaded in each new session before its functions can be used."),
         ("What does rm(list = ls()) do?", "Removes every object in the environment", ["Lists every object in the environment", "Removes only the last object created", "Deletes all files in the working folder"], "ls() returns the names of all objects, and rm(list = ...) removes all of them. Files on disk are not touched."),
         ("Why do experts avoid setwd(\"/Users/me/Desktop/project\") inside a script?", "Other computers use other paths", ["setwd() is slower than read.csv()", "Absolute paths only work on Windows", "R cannot read files on the Desktop"], "An absolute path only exists on your machine, so the script breaks when someone else runs it.")]
    return L, "\n".join(b), q

# =============================================================== 5. dataframe
def m1_dataframe(P):
    L = dict(slug="m1_dataframe", mod=MOD, icon="🧾", title="データフレーム：作る・取り出す・調べる・CSV を読む",
             tag="M1 · Data Frames in R — Intro, Accessing Data, Analyzing a Data Frame &amp; Loading a CSV",
             lead="ばらばらのベクトルを1つの表にまとめるのが<strong>データフレーム</strong>です。<code>data.frame()</code> で作り、<code>$</code> と <code>[行, 列]</code> で取り出し、<code>dim()</code>・<code>str()</code>・<code>summary()</code> で調べ、最後に <code>read.csv()</code> で <strong>donors.csv</strong> を読み込みます。",
             video="Intro to Data Frames ／ Accessing Data in Data Frames ／ Analyzing a Data Frame ／ The donors.csv file ／ Loading a CSV into R",
             unav=["① データフレームを作る", "② 列と行を取り出す", "③ 中身を調べる", "④ CSV を読み込む"],
             terms=[("data frame", "データフレーム", "列＝変数、行＝ケースの表。列ごとに型が違ってよい。"),
                    ("$", "ドル記号", "df$列名 で1列をベクトルとして取り出す。"),
                    ("df[行, 列]", "角かっこ添字", "行と列を番号や名前で指定する。空欄は「全部」。"),
                    ("dim() / nrow() / ncol()", "大きさ", "行数と列数。"),
                    ("names()", "列名", "列の名前の一覧。colnames() と同じ。"),
                    ("str()", "構造", "各列の型と先頭の値を表示。"),
                    ("summary()", "要約", "数値列は5数要約と平均、NA の数も表示。"),
                    ("read.csv()", "CSV 読み込み", "CSV ファイルをデータフレームにする。"),
                    ("CSV", "カンマ区切り", "表を文字で保存する形式。")],
             tip="<code>df$age</code> は<strong>ベクトル</strong>、<code>df[1]</code> や <code>df[\"age\"]</code> は<strong>データフレーム</strong>が返る。平均など計算に使うのは <code>$</code> の方。")
    b = [teal('📖 <strong>講義動画との対応</strong><ul style="margin:.4rem 0 0 1.2rem"><li>① Intro to Data Frames</li><li>② Accessing Data in Data Frames</li><li>③ Analyzing a Data Frame</li><li>④ The donors.csv file ／ Loading a CSV into R</li></ul>')]
    b.append(unit(1, "データフレームを作る", "ばらばらのベクトルを1つの表に", f'''
  <p>ある実験で9人の参加者のデータを取りました。4つのベクトルに分けて保存すると、R には「これらが同じ人たちのデータだ」という関係がわかりません。</p>
  {P.R('group  <- c(1, 1, 1, 2, 2, 2, 3, 3, 3)\ngender <- c("male", "male", "male", "male", "male", "female", "female", "female", "female")\nage    <- c(17, 19, 21, 37, 18, 19, 47, 18, 19)\nscore  <- c(12, 10, 11, 15, 16, 14, 25, 21, 29)\nexpt <- data.frame(age, gender, group, score)\nexpt')}
  <p><code>data.frame()</code> に入れると、<strong>同じ行＝同じ参加者</strong>として1つの表になります。列（変数）ごとに型が違ってもかまいません（数値と文字が並んでいる）。</p>
  {simple("データフレーム＝エクセルの表のようなもの。縦の列が「何を測ったか」、横の行が「誰（何）のデータか」。")}
'''))
    b.append(unit(2, "列と行を取り出す", "$ と [行, 列]", f'''
  <h3>列を取り出す</h3>
  {P.R('expt$score\nexpt[1]\nclass(expt$score)\nclass(expt[1])')}
  <p><code>$</code> は<strong>ベクトル</strong>、<code>[1]</code> は<strong>1列のデータフレーム</strong>を返します。平均などを計算するときは <code>$</code> を使います。</p>
  <h3>行と列を同時に指定する <code>[行, 列]</code></h3>
  <p>カンマの<strong>左が行、右が列</strong>です。空欄は「すべて」を意味します。</p>
  {P.R('expt[1, ]\nexpt[3:7, 3:4]\nexpt[3:7, c("score", "age")]')}
  {warn('<code>expt[1, ]</code> の<strong>カンマを忘れる</strong>と <code>expt[1]</code>（1列目）になってしまいます。「1行目」と「1列目」は全然違うので、行がほしいときはカンマを必ず書きましょう。')}
  <p>条件で行を選ぶこともできます。ベクトルの論理添字と同じ考え方です。</p>
  {P.R('expt[expt$score > 20, ]')}
'''))
    b.append(unit(3, "データフレームを調べる", "dim・names・str・summary", f'''
  <p>知らないデータを受け取ったら、まず<strong>大きさ・列名・型・要約</strong>を確認します。</p>
  {P.R('dim(expt)\nnrow(expt)\nnames(expt)\nstr(expt)\nsummary(expt)')}
  <ul><li><code>str()</code>：行数・列数、各列の<strong>型</strong>（<code>num</code>, <code>chr</code>）と先頭の値</li><li><code>summary()</code>：数値列は<strong>最小・第1四分位・中央値・平均・第3四分位・最大</strong>。文字列は長さや種類の数など（R 4.5 以降の表示）</li></ul>
  {note('🧪 CodeGrade の課題では <code>ls.str()</code> を使う指示が出ることがあります。環境にあるオブジェクトの構造をまとめて表示する関数です。')}
'''))
    b.append(unit(4, "CSV を読み込む：donors.csv", "read.csv() と最初のチェック", f'''
  <p>実際のデータは <strong>CSV（カンマ区切り）</strong>ファイルで渡されることが多いです。この授業の <code>donors.csv</code> は、退役軍人団体がダイレクトメールで寄付を募ったときの見込み寄付者のデータ（Nwanganga &amp; Chapple, <em>Practical Machine Learning in R</em>）です。</p>
  <p>CSV を <strong>.Rmd と同じフォルダ</strong>に置き、<code>read.csv()</code> で読み込みます。課題で名前が指定されていれば、その名前で保存します。</p>
  {P.R('donors <- read.csv("donors.csv")\ndim(donors)\nnames(donors)[1:8]')}
  <p>9万行以上・22列の大きなデータです。全部を表示せず、<code>head()</code> と <code>summary()</code> で様子を見ます。</p>
  {P.R('head(donors[, 1:6], 3)\nsummary(donors$age)')}
  {warn('<code>summary()</code> の <strong>NA\'s</strong> に注目。<code>age</code> には欠損値が2万件以上あります。このままでは <code>mean(donors$age)</code> が <code>NA</code> になるので、M2 では <code>na.rm = TRUE</code> を使います。')}
  {table(["read.csv で失敗する原因", "対処"], [["ファイルが作業ディレクトリにない", "<code>list.files()</code> で確認、同じフォルダに置く"], ["ファイル名のつづり・大文字小文字", "<code>\"donors.csv\"</code> を正確に"], ["引用符や <code>.csv</code> を忘れた", "<code>read.csv(\"donors.csv\")</code> の形を守る"]])}
  {practice("p-m1df-u4", "読み込んだデータを調べる", "<code>donors</code> の<strong>行数</strong>を求め、<code>totalGivingAmount</code>（寄付総額）の <code>summary()</code> を表示してください。",
             ["nrow", "donors", "summary", "totalGivingAmount"], 'nrow(donors)\nsummary(donors$totalGivingAmount)', "行数は 95412。寄付総額は中央値が 78 なのに最大は 9,485 もある、右に長い分布（M2 で詳しく扱う）。")}
'''))
    b.append(teal('➡️ <strong>次のモジュールへ：</strong>データを読み込めたら、次は数字で要約する番です。<a href="m2_center.html">550 M2 記述統計</a>で、平均・中央値とグラフを学びます。'))
    q = [("Why put the vectors age, gender, group and score into one data frame?", "So each row is one participant", ["So R can store more than 100 values", "So the vectors become one vector", "So all columns become the same type"], "A data frame tells R that values in the same row belong to the same case. Columns can still have different types."),
         ("What does expt$score return?", "A numeric vector", ["A one-column data frame", "The first row of expt", "The column name as text"], "The $ operator extracts one column as a plain vector, which you can pass to mean() or sum()."),
         ("Which code returns only the first ROW of the data frame expt?", "expt[1, ]", ["expt[1]", "expt[, 1]", "expt$1"], "Inside [row, column], the number before the comma picks rows. expt[1] and expt[, 1] give the first column."),
         ("Which function shows each column's data type and its first few values?", "str()", ["dim()", "head()", "nrow()"], "str() shows the structure: dimensions, column types (num, chr, int) and the first values."),
         ("summary(donors$age) shows NA's 23665. What does this tell you?", "Many ages are missing", ["Many donors are aged 0", "The mean age is 23,665", "Age is stored as text"], "NA's counts missing values. Functions such as mean() need na.rm = TRUE to ignore them."),
         ("You run read.csv(\"Donors.csv\") but the file is named donors.csv. What happens?", "R cannot find the file", ["R loads the file anyway", "R creates an empty file", "R renames the file for you"], "File names must match exactly, including upper- and lower-case letters.")]
    return L, "\n".join(b), q

LESSONS = [m1_levels, m1_rbasics, m1_vectors, m1_workflow, m1_dataframe]
