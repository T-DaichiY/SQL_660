/* code-editor.js — turns the practice textareas (.code-editor) into a real code editor:
   R / SQL / Python syntax highlighting (chosen from the site folder), autocomplete, Tab indent / Shift-Tab dedent, auto-close brackets.
   Built on CodeMirror 5 (cdnjs). The original <textarea> is kept in sync, so practice.js
   (checkPractice reads textarea.value) keeps working unchanged. */
(function () {
  var CM = 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/';
  if (document.querySelector('script[src*="sql-engine"]')) return; // those pages have their own editor
  var areas = Array.prototype.filter.call(document.querySelectorAll('textarea.code-editor'),
    function (a) { return !a.closest('.editor-wrap'); });
  if (!areas.length) return;
  var path = location.pathname;
  var LANG = /\/python5[28]0\//.test(path) ? 'python' : /\/(stats|r650)\//.test(path) ? 'r' : 'sql';
  var WORDCH = LANG === 'r' ? /[\w.]/ : /\w/;
  var MODE = { r: 'r', python: 'python', sql: 'text/x-sql' }[LANG];
  var MODEFILE = { r: 'r/r', python: 'python/python', sql: 'sql/sql' }[LANG];

  function css(href) {
    var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = href; document.head.appendChild(l);
  }
  function js(src, cb) {
    var s = document.createElement('script'); s.src = src; s.onload = cb;
    s.onerror = function () { /* offline: leave plain textareas */ };
    document.head.appendChild(s);
  }
  function chain(list, done) {
    if (!list.length) return done();
    js(list[0], function () { chain(list.slice(1), done); });
  }

  var style = document.createElement('style');
  style.textContent =
    '.CodeMirror.cm-r{height:auto;min-height:130px;border-radius:10px;background:#1e293b;color:#e5e7eb;' +
    "font-family:'JetBrains Mono','SF Mono',Consolas,Monaco,monospace;font-size:1rem;line-height:1.6;}" +
    '.cm-r .CodeMirror-scroll{min-height:130px;padding:.35rem 0;}' +
    '.cm-r .CodeMirror-gutters{background:#172033;border-right:1px solid #2b3a55;}' +
    '.cm-r .CodeMirror-linenumber{color:#64748b;}' +
    '.cm-r .CodeMirror-cursor{border-left:2px solid #e5e7eb;}' +
    '.cm-r .CodeMirror-selected{background:rgba(147,197,253,.25);}' +
    '.cm-r .CodeMirror-focused .CodeMirror-selected{background:rgba(147,197,253,.32);}' +
    '.cm-r .CodeMirror-activeline-background{background:rgba(255,255,255,.04);}' +
    '.cm-r .cm-keyword,.cm-r .cm-builtin{color:#93c5fd;}' +
    '.cm-r .cm-atom{color:#fca5a5;}' +
    '.cm-r .cm-number{color:#fca5a5;}' +
    '.cm-r .cm-string,.cm-r .cm-string-2{color:#86efac;}' +
    '.cm-r .cm-comment{color:#94a3b8;font-style:italic;}' +
    '.cm-r .cm-variable-2,.cm-r .cm-variable-3{color:#e5e7eb;}' +
    '.cm-r .cm-operator{color:#fcd34d;}' +
    '.cm-r .CodeMirror-matchingbracket{color:#fff!important;background:rgba(147,197,253,.35);}' +
    '.CodeMirror-hints{background:#0f172a;border:1px solid #334155;border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.35);' +
    "font-family:'JetBrains Mono','SF Mono',Consolas,monospace;font-size:.92rem;z-index:10000;max-height:14rem;}" +
    '.CodeMirror-hint{color:#cbd5e1;padding:2px 10px;border-radius:5px;}' +
    'li.CodeMirror-hint-active{background:#334155;color:#fff;}' +
    '.cm-r-hint-kind{float:right;margin-left:1.2rem;color:#64748b;font-size:.75rem;}';
  document.head.appendChild(style);

  // vocabulary used in the course (functions / keywords), shown in the completion list
  var VOCAB = ('abs all any anova aov apply as.character as.factor as.numeric barplot binom.test boxplot c cat ceiling ' +
    'chisq.test cor cor.test cumsum cut data.frame dbinom dnorm dpois dunif exp factor floor for function geom_bar ' +
    'geom_boxplot geom_histogram geom_point geom_smooth ggplot aes head hist if ifelse is.na legend length levels lines lm log ' +
    'log10 mean median min max names nchar ncol nrow pbinom pchisq pnorm points ppois pt punif qbinom qchisq qnorm qt quantile ' +
    'rbinom read.csv rep return rev rnorm round rowSums sample sapply scale sd seq set.seed shapiro.test sort sqrt str ' +
    'subset sum summary t.test table tail tapply unique var which while wilcox.test with write.csv xtabs abline plot ' +
    'par pairs predict residuals coef confint anova mutate filter select arrange group_by summarise library install.packages ' +
    'TRUE FALSE NULL NA Inf NaN na.rm breaks col main xlab ylab horizontal probs lower.tail df data').split(/\s+/);
  var PY = ('abs all any append astype bool dict dropna enumerate fillna float for from groupby head if import in int isna items ' +
    'join keys len list loc iloc map max mean median merge min ndarray np numpy open pd pandas plt pivot_table plot print range ' +
    'read_csv rename reshape return round set shape sort_values sorted std str sum tolist transpose type unique value_counts ' +
    'values zip arange linspace zeros ones random matplotlib hist scatter xlabel ylabel title show subplots figure legend ' +
    'DataFrame Series True False None def class else elif while with as lambda not and or').split(/\s+/);
  var SQLW = ('SELECT FROM WHERE GROUP BY ORDER HAVING JOIN INNER LEFT RIGHT FULL OUTER ON AS AND OR NOT IN LIKE BETWEEN IS NULL ' +
    'DISTINCT LIMIT OFFSET UNION INTERSECT EXCEPT CASE WHEN THEN ELSE END COUNT SUM AVG MIN MAX INSERT INTO VALUES UPDATE SET ' +
    'DELETE CREATE TABLE ALTER DROP PRIMARY KEY FOREIGN REFERENCES INDEX VIEW WITH ASC DESC COALESCE CAST ROUND LENGTH UPPER LOWER ' +
    'SUBSTR TRIM REPLACE ABS EXISTS ANY ALL OVER PARTITION CROSS NATURAL USING').split(/\s+/);
  if (LANG === 'python') VOCAB = PY; else if (LANG === 'sql') VOCAB = SQLW;
  var KEYWORDS = { 'if': 1, 'else': 1, 'for': 1, 'while': 1, 'function': 1, 'return': 1, 'TRUE': 1, 'FALSE': 1, 'NULL': 1, 'NA': 1 };

  function hint(cm) {
    var cur = cm.getCursor(), line = cm.getLine(cur.line);
    var start = cur.ch, end = cur.ch;
    while (start && WORDCH.test(line.charAt(start - 1))) --start;
    var word = line.slice(start, end);
    var seen = {}, list = [];
    function add(w, kind) {
      if (w === word || seen[w] || w.toLowerCase().indexOf(word.toLowerCase()) !== 0) return;
      seen[w] = 1; list.push({ text: w, kind: kind });
    }
    VOCAB.forEach(function (w) { add(w, KEYWORDS[w] ? 'keyword' : (LANG === 'sql' ? 'SQL' : LANG === 'python' ? 'Python' : 'R')); });
    // names the student already typed (variables, column names)
    (cm.getValue().match(/[A-Za-z_.][\w.]*/g) || []).forEach(function (w) { add(w, 'ここで使用'); });
    list.sort(function (a, b) { return a.text.length - b.text.length || (a.text < b.text ? -1 : 1); });
    return {
      list: list.slice(0, 40).map(function (x) {
        return {
          text: x.text,
          render: function (el) {
            el.appendChild(document.createTextNode(x.text));
            var k = document.createElement('span'); k.className = 'cm-r-hint-kind'; k.textContent = x.kind; el.appendChild(k);
          }
        };
      }),
      from: CodeMirror.Pos(cur.line, start), to: CodeMirror.Pos(cur.line, end)
    };
  }

  function upgrade(ta) {
    var cm = CodeMirror.fromTextArea(ta, {
      mode: MODE, theme: 'r', lineNumbers: true, indentUnit: 2, tabSize: 2, indentWithTabs: false,
      lineWrapping: false, matchBrackets: true, autoCloseBrackets: true, styleActiveLine: true,
      viewportMargin: Infinity,
      extraKeys: {
        Tab: function (e) {
          if (e.somethingSelected()) e.indentSelection('add');
          else e.replaceSelection('  ', 'end');
        },
        'Shift-Tab': function (e) { e.indentSelection('subtract'); },
        'Ctrl-Space': function (e) { e.showHint({ hint: hint, completeSingle: false }); },
        Enter: function (e) { e.execCommand('newlineAndIndent'); }
      }
    });
    cm.getWrapperElement().classList.add('cm-r');
    cm.on('change', function () { cm.save(); });
    cm.on('inputRead', function (e, ch) {
      if (ch.origin === '+input' && WORDCH.test(ch.text[0]) && !e.state.completionActive) {
        var c = e.getCursor(), l = e.getLine(c.line), s = c.ch;
        while (s && WORDCH.test(l.charAt(s - 1))) --s;
        if (c.ch - s >= 2) e.showHint({ hint: hint, completeSingle: false });
      }
    });
    ta._cm = cm;
    return cm;
  }

  css(CM + 'codemirror.min.css');
  css(CM + 'addon/hint/show-hint.min.css');
  chain([
    CM + 'codemirror.min.js',
    CM + 'mode/' + MODEFILE + '.min.js',
    CM + 'addon/edit/matchbrackets.min.js',
    CM + 'addon/edit/closebrackets.min.js',
    CM + 'addon/selection/active-line.min.js',
    CM + 'addon/hint/show-hint.min.js'
  ], function () {
    areas.forEach(upgrade);
    window.PracticeEditors = areas;
  });
})();
