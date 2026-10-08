# SQL_660 学習サイトの作り方 (BUILD_GUIDE)

リポジトリ: `T-DaichiY/SQL_660` (branch `main`) / 場所: `Eastern/660 - SQL/Lesson_website/`
新しいモジュール(M8 など)を足すときの手順書。

## 0. フォルダ・リンク集

| 何 | 場所 |
|---|---|
| サイト本体(このフォルダ) | `/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern/660 - SQL/Lesson_website/` |
| 科目フォルダ(教科書PDF・各Mの素材) | `/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern/660 - SQL/` |
| M7 ソース(script) | `/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern/660 - SQL/M7/M7 script.docx` |
| GitHub リポジトリ | https://github.com/T-DaichiY/SQL_660 |
| Whisper skill | `~/.claude/skills/lecture-transcriber/` |
| 文字起こしの作業フォルダ(M7分) | `~/Downloads/M7_audio/`(不要なら削除可) |
| Voice Memos 録音の保存先 | `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/` |
| 過去の会話ログ(詳細確認用) | `~/.claude/projects/-Users-apple-Library-CloudStorage-GoogleDrive-daichi-yamamoto-sisbschool-com-My-Drive-AY26-27/17956935-4b6e-435b-8b1f-c436cfd6b3f7.jsonl` |

## 1. 全体像

- **静的サイト**(HTML/CSS/JS のみ、ビルド不要)。ブラウザで `index.html` を開けば動く。
- 各モジュール(M1〜M7)は次の4種類で構成:
  1. **レッスンページ** `<topic>.html` と、やさしい版 `<topic>_easy.html`
  2. **「+」ページ** `mN_plus.html` — 講義では扱わなかった教科書だけの内容(`_easy` 付き)
  3. **演習アリーナ** `mN_practice_*.html` — ブラウザ内で SQL を実行して自動採点
  4. **ハブページ** `mN_practice.html` — 演習ページへのカード一覧
- `index.html` に全レッスン数・演習問題数のバッジとカードがある(現在: 全44レッスン / 演習210問)。

### 主なファイル

| ファイル | 役割 |
|---|---|
| `sql-engine.js` | 中核。sql.js(SQLite WASM)、シードデータ、採点、PG互換レイヤー、スキーマパネル |
| `practice.js` / `practice-arena.css` | 演習カードUI、構文ハイライト、オートコンプリート |
| `style.css` / `easy.css` | 全体スタイル / やさしい版スタイル |
| `nav.js` / `typewriter.js` | ナビ開閉 / 演出 |

## 2. 教材の元ネタ(ソース)

1. **授業録音の文字起こし** — 講師の授業が分かりにくいので、動画は見ずに文字起こし+教科書でガイドを作る。
2. **教科書** *Practical SQL, 2nd ed.* (PDF) — 講義で扱わなかった章を「+」ページにする。
3. **講師の script / rubric** (`M7/M7 script.docx` など) — 課題ページが最終権威。

### 文字起こし(Whisper)

Mac 標準の文字起こしは崩れる(特に2倍速)ので Whisper を使う。手順は **skill `lecture-transcriber`** に集約済み:

- 「この録音を文字起こしして」と言えば実行される。
- 中身: `~/.claude/skills/lecture-transcriber/`(`SKILL.md`, `assets/list_recordings.py`, `assets/transcribe_batch.sh`)。
- モデル `turbo`、`--language en`、`--initial_prompt` に SQL 用語を入れる。
- Voice Memos のフォルダ読み取りには VS Code の **フルディスクアクセス**が必要。ファイル名は日時なので**録音の長さ**で照合する。
- 末尾が無音のファイルは最後にゴミ文字が出る(無視してよい)。
- 録音は 1x〜1.5x 推奨。

## 3. 1モジュールを作る流れ

1. **ソース収集**: 文字起こし(Whisper)+ script/docx + 教科書該当章。
2. **計画**: レッスン単元の分割、「+」ページ用に教科書の未カバー範囲を洗い出す、演習の分量を決める。
3. **エンジン拡張が必要か判断**(新データセット、新関数、新しい採点方式)→ §5。
4. **レッスンHTML作成**: 既存ページ(例 `joins_types.html`)を骨格としてコピー。
   構成: `.site-header` / `.ch-banner` / `.page-layout` / `.unit`(単元ごと) / `.quiz-section` / `<aside>` / `<footer>`。
   便利なコンポーネント: `.simple-box`(要約) `.warn-box` `.teal-box` `.compare-table` `.code-block`。
   `_easy` 版は同内容を平易に。
5. **演習ページ作成**: 問題オブジェクト配列(§4)+ 共通の `practice.js`/`sql-engine.js` を読み込む。
6. **ナビ挿入**: 全HTMLへ新モジュールの行を追加(§6)。
7. **`index.html` 更新**: カード追加、バッジの数値更新。
8. **検証**(§7)→ **コミット**(§8)→ ユーザー承認後 push。

### クイズのルール

MCQ は**正解が常に一番長い選択肢にならないよう**にする(長さバイアス禁止)。

## 4. 演習問題の書式

各ページに `SQL_PROBLEMS` 配列。主なフィールド:

```js
{
  title, scenario,          // 問題文
  starter,                  // エディタの初期文
  solution,                 // 模範解答 SQL
  hint,
  orderSensitive: false,    // 行順を採点に含めるか
  // 更新系(UPDATE/ALTER/DROP…)は mutate モード:
  mode: "mutate",           // 省略時は "select"
  verify: "SELECT ... ORDER BY post_id",  // 変更後の状態を確認する SELECT
  requireKeywords: ["UPDATE"]             // 任意: 必須キーワード
}
```

- **select モード** (`gradeQuery`): 学生SQLと模範解答の結果行を比較。
- **mutate モード** (`gradeMutation`): 学生SQL/模範解答を**それぞれ新品DBで実行**し、同じ `verify` の結果を比較。
  スキーマ確認は `pragma_table_info('t')`、テーブル存在確認は `sqlite_master` を verify に使える。
- 更新系は実行しても結果表が出ないので、▶実行では `runMutationPreview` が verify 結果を見せる。

## 5. sql-engine.js のしくみ

- **sql.js 1.14.2**(cdnjs)で本物の SQLite をブラウザ内実行。DB は最初に作った**pristine のバイト列**から毎回 `new Database(pristineBytes)` で復元。
- **シードデータ**: 大学DB / 銀行DB / `ds_jobs`(M7、24行、意図的に汚したデータ)/ `ownership_map`。
- **公開API**: `{ init, runQuery, gradeQuery, runMutationPreview, gradeMutation }`。
- **PostgreSQL 互換(M7)**: ページ側で
  `window.ARENA_OPTS = { pgCompat: true, schemaGroups: ["ds_jobs"] }` を設定すると有効化。
  - シム関数: `left, right, split_part, strpos, initcap, lpad, rpad, regexp*` など。
    カスタム関数は `new Database` ごとに再登録。可変長は `Object.defineProperty(fn,"length",{value:-1})`。
  - SQLリライタ (`pgTokenize` / `pgRewrite`): `::` キャスト、`TRUNCATE`→`DELETE`、
    `ALTER COLUMN TYPE / NOT NULL` は `pgRebuild`(テーブル再作成)、複数アクションの ALTER 分割。
  - 変換できない構文(全文検索など)は「概念のみ」と明記し、演習には出さない。
- **スキーマパネル**: `SCHEMA_INFO` / `SCHEMA_TYPES` / `SCHEMA_GROUP_DEFS`。問題ごとに使うテーブルの列を右側に浮動表示(幅広、メインは左にシフト)。`[hidden]{display:none}` を明示すること。
- **キャッシュバスティング**: `<script src="sql-engine.js?v=9">`。エンジンを変えたら全HTMLの `?v=` を上げる。

## 6. ナビ伝播

全ページ(現在104枚)の共通ナビに各モジュールの行がある。新モジュール追加時は
**固定文字列の `str.replace` を `glob("*.html")` に対して回す Python スクリプト**で挿入(冪等にする=既に入っていたらスキップ)。
新規ページを作り終えてから実行し、新規ページにもナビを入れる。`.nav-groups.open{max-height:380px}` など行数が増えたら CSS の高さも確認。

## 7. 検証チェックリスト

1. **Node ハーネス**: 実際の `sql-engine.js` を読み込み、全問題について
   - 模範解答がエラーなく動く、行数・形が問題文と合う
   - mutate は解答→verify を2回回して結果が同一(非決定性チェック)
   - 「解答 vs 解答」は PASS、「解答 vs わざと間違い」は FAIL(採点が識別できているか)
2. **ヘッドレス Chrome**: cdnjs の WASM 版で実際に動くか(Node版と別配布のため)。スクリーンショットで見た目も確認。
3. **Python チェック**: リンク切れ、`<div>` の開閉バランス、`index.html` のカウント整合。
4. **既存モジュールの回帰**: 前モジュールの問題数が変わっていないこと(M6=135問など)。
5. レッスン内容の**数値・コード文字列**は文字起こしと教科書で照合(崩れた文字起こしは信用しない)。

## 8. Git ルール

- `git add -A` / `git add .` は**禁止**。必ずファイルを明示してステージ。
- `.docx` のソース2つ(`M3 and M4 .docx`, `m1_rest and M2.doc.docx`)は**未追跡のまま**。
- コミットメッセージ末尾: `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`
- push はユーザーが「push」「yes」等で承認してから。

## 8.5 M8（統計・CTE）で追加したもの
- **データ**: `bikes`（講義の配布データそのまま：`M8/Lesson data set/` の `create_bikes_table.sql` と同じ列 `cross_date, high_temp, low_temp, precip, brooklyn, manhattan, williamsburg, queensboro, total`、210行。CSV自体が4月1〜30日の30日分を7回繰り返している。id・曜日の列は無い）、`departments/employees/employee_projects`（架空・5部署20人）、銀行DB。`M8/bikes.csv`・`M8/M8_transcripts_whisper.txt` に素材を保存。
- **統計関数**: sql.js は集計関数を自作できないので `pgRewriteStats` が `corr / regr_slope / regr_intercept / regr_r2 / var_* / stddev_* / covar_*` を `SUM(CASE…)` の式に書き換える（NULLの組は無視＝PostgreSQLと同じ）。`pg_sqrt` を登録。講義の数値（0.74 / 370.18 / −7891.03 / 0.55 / 125.06 / 11.18）がそのまま再現される。
- **採点**: 小数は有効10桁で比較（`normalizeRows`）。CTE・ウィンドウ関数はSQLite標準で動く。`percentile_cont` / crosstab / LATERAL は未対応＝概念のみ。
- **注意**: SQLiteは整数÷整数が切り捨て（`::numeric` でも直らない）→ `* 100.0` を先に掛ける。
- **ナビ**: M8 の行は `M8 統計・CTE`（クラス `nav-row m7`）。ページ名は m8_stats_intro / m8_regression / m8_variance / m8_cte / m8_cte_multi / m8_plus / m8_practice(_stats/_regression/_cte/_m8_plus)。
- 並列エージェントは**自分専用の一時ファイル（タグ付き）**を使うこと。共有の一時HTMLだと互いの結果を上書きする。

## 9. ハマりどころ(過去の不具合)

| 症状 | 原因 / 対策 |
|---|---|
| パネル本文が隠れない | `hidden` 属性がCSSに負ける → `[hidden]{display:none}` を追加 |
| 関数の引数個数が合わない | `create_function` は後勝ち、引数は `fn.length` → 可変長は `variadic()` ヘルパ |
| 厳密CASTチェックの誤判定 | CAST後の値でなく内側の式を検査 |
| 行数を手で書いて間違える | ブリーフにも実測値を入れる。自動チェックで確認 |
| `sleep` 連鎖が拒否される | Monitor の until ループで待つ |
| Voice Memos が Operation not permitted | フルディスクアクセスを付与(再起動が必要な場合あり。後で外れることもある) |
| Whisper が末尾で幻覚 | 無音で終わる録音の仕様。無視 |

## 10. 並列化のコツ

大きい作業(複数ページの執筆)は、共通ブリーフ(骨格ファイル、CSSクラス、問題書式、採点ルール、検証手順)を渡して Sonnet サブエージェントに分担させ、統合後に §7 を通す。
