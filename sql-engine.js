/* ===== M6 Practice Arena — shared SQL engine, editor, and grading logic =====
   Loads sql.js (real SQLite compiled to WASM) from cdnjs, seeds an in-memory
   University DB + Banking DB, and exposes helpers each m6_practice_*.html
   page uses to render its 15 practice cards (5 basic / 5 intermediate / 5 advanced). */

var SQL_ENGINE = (function () {
  var SQLlib = null;
  var pristineBytes = null;
  var readyPromise = null;

  var SEED_SQL = [
    "CREATE TABLE department (dept_name TEXT PRIMARY KEY, building TEXT, budget NUMERIC);",
    "CREATE TABLE instructor (instructor_id INTEGER PRIMARY KEY, name TEXT, dept_name TEXT REFERENCES department(dept_name), salary NUMERIC);",
    "CREATE TABLE student (student_id INTEGER PRIMARY KEY, name TEXT, dept_name TEXT REFERENCES department(dept_name), tot_cred INTEGER);",
    "CREATE TABLE course (course_id TEXT PRIMARY KEY, title TEXT, dept_name TEXT REFERENCES department(dept_name), credits INTEGER);",
    "CREATE TABLE section (course_id TEXT REFERENCES course(course_id), section_id INTEGER, semester TEXT, year INTEGER, building TEXT, room_number TEXT, PRIMARY KEY (course_id, section_id, semester, year));",
    "CREATE TABLE takes (student_id INTEGER REFERENCES student(student_id), course_id TEXT, section_id INTEGER, semester TEXT, year INTEGER, grade TEXT, PRIMARY KEY (student_id, course_id, section_id, semester, year));",
    "CREATE TABLE teaches (instructor_id INTEGER REFERENCES instructor(instructor_id), course_id TEXT, section_id INTEGER, semester TEXT, year INTEGER, PRIMARY KEY (instructor_id, course_id, section_id, semester, year));",
    "CREATE TABLE advisor (student_id INTEGER REFERENCES student(student_id), instructor_id INTEGER REFERENCES instructor(instructor_id), PRIMARY KEY (student_id));",
    "CREATE TABLE prereq (course_id TEXT REFERENCES course(course_id), prereq_id TEXT REFERENCES course(course_id), PRIMARY KEY (course_id, prereq_id));",

    "INSERT INTO department VALUES ('Comp. Sci.','Taylor',100000),('Physics','Watson',70000),('Math','Chandler',80000),('History','Painter',50000),('Biology','Watson',90000),('Elec. Eng.','Taylor',85000),('Finance','Painter',120000),('Accounting','Painter',95000);",
    "INSERT INTO instructor VALUES (10101,'Brandt','Comp. Sci.',98000),(10102,'Katz','Comp. Sci.',75000),(15151,'Bourikas','Comp. Sci.',90000),(22222,'Kim','Elec. Eng.',80000),(33333,'Srinivasan','Finance',65000),(45565,'Chen','Physics',94000),(58583,'Wu','Math',90000),(76543,'Singh','Biology',80000);",
    "INSERT INTO student VALUES (101,'Zhang','Comp. Sci.',102),(102,'Shankar','Comp. Sci.',102),(128,'Levy','Physics',46),(133,'Brown','Comp. Sci.',58),(139,'Aoi','Elec. Eng.',60),(141,'Chavez','Finance',110),(145,'Okada','Math',34),(148,'Wright','History',22),(150,'Nakamura','Biology',15),(155,'Silva','Comp. Sci.',96),(160,'Patel','Elec. Eng.',88),(165,'Kobayashi','Finance',12),(170,'Garcia','Math',72),(175,'Suzuki','History',95),(180,'Novak','Biology',54),(185,'Lindgren','Comp. Sci.',28),(190,'Petrov','Physics',66),(195,'Costa','Accounting',101),(200,'Ueda','Accounting',40),(205,'Volkov','Music',20);",
    "INSERT INTO course VALUES ('CS-101','Intro. to Computer Science','Comp. Sci.',4),('CS-190','Game Design','Comp. Sci.',4),('CS-315','Robotics','Comp. Sci.',3),('CS-347','Database System Concepts','Comp. Sci.',3),('EE-181','Intro. to Digital Systems','Elec. Eng.',3),('PHY-101','Physics I','Physics',4),('MAT-201','Calculus II','Math',4),('HIS-351','World History','History',3),('BIO-101','Intro. to Biology','Biology',4),('FIN-201','Corporate Finance','Finance',3),('ACC-101','Financial Accounting','Accounting',3);",
    "INSERT INTO prereq VALUES ('CS-190','CS-101'),('CS-315','CS-101'),('CS-347','CS-101'),('EE-181','PHY-101');",
    "INSERT INTO section VALUES ('CS-101',1,'Fall',2023,'Taylor','101'),('CS-101',1,'Spring',2024,'Taylor','101'),('CS-190',1,'Spring',2024,'Taylor','102'),('CS-315',1,'Fall',2023,'Taylor','103'),('CS-347',1,'Fall',2023,'Taylor','104'),('CS-347',1,'Spring',2024,'Taylor','104'),('EE-181',1,'Fall',2023,'Taylor','201'),('PHY-101',1,'Fall',2023,'Watson','100'),('MAT-201',1,'Spring',2024,'Chandler','50'),('HIS-351',1,'Fall',2023,'Painter','20'),('BIO-101',1,'Spring',2024,'Watson','10'),('FIN-201',1,'Fall',2023,'Painter','30'),('ACC-101',1,'Spring',2024,'Painter','31');",
    "INSERT INTO teaches VALUES (10101,'CS-101',1,'Fall',2023),(10101,'CS-347',1,'Fall',2023),(10102,'CS-101',1,'Spring',2024),(15151,'CS-315',1,'Fall',2023),(15151,'CS-190',1,'Spring',2024),(15151,'CS-347',1,'Spring',2024),(22222,'EE-181',1,'Fall',2023),(45565,'PHY-101',1,'Fall',2023),(58583,'MAT-201',1,'Spring',2024),(76543,'BIO-101',1,'Spring',2024),(33333,'FIN-201',1,'Fall',2023);",
    "INSERT INTO advisor VALUES (101,10101),(102,10101),(133,10101),(141,10102),(139,33333),(145,33333);",
    "INSERT INTO takes VALUES (101,'CS-101',1,'Fall',2023,'A'),(101,'CS-347',1,'Fall',2023,'A-'),(102,'CS-101',1,'Fall',2023,'B+'),(102,'CS-315',1,'Fall',2023,'A'),(133,'CS-101',1,'Fall',2023,'B'),(133,'CS-190',1,'Spring',2024,'A'),(155,'CS-101',1,'Spring',2024,'A'),(155,'CS-347',1,'Spring',2024,'B+'),(185,'CS-101',1,'Spring',2024,'C'),(139,'EE-181',1,'Fall',2023,'A-'),(160,'EE-181',1,'Fall',2023,'B'),(190,'PHY-101',1,'Fall',2023,'A'),(145,'MAT-201',1,'Spring',2024,'B'),(170,'MAT-201',1,'Spring',2024,'A-'),(148,'HIS-351',1,'Fall',2023,'A'),(175,'HIS-351',1,'Fall',2023,'B+'),(150,'BIO-101',1,'Spring',2024,'B'),(180,'BIO-101',1,'Spring',2024,'A'),(141,'FIN-201',1,'Fall',2023,'A'),(165,'FIN-201',1,'Fall',2023,'C+'),(195,'ACC-101',1,'Spring',2024,'A'),(200,'ACC-101',1,'Spring',2024,'B');",

    "CREATE TABLE branch (branch_name TEXT PRIMARY KEY, branch_city TEXT, assets NUMERIC);",
    "CREATE TABLE customer (customer_id TEXT PRIMARY KEY, customer_name TEXT, customer_street TEXT, customer_city TEXT);",
    "CREATE TABLE account (account_number TEXT PRIMARY KEY, branch_name TEXT REFERENCES branch(branch_name), balance NUMERIC);",
    "CREATE TABLE depositor (customer_id TEXT REFERENCES customer(customer_id), account_number TEXT REFERENCES account(account_number), PRIMARY KEY (customer_id, account_number));",
    "CREATE TABLE loan (loan_number TEXT PRIMARY KEY, branch_name TEXT REFERENCES branch(branch_name), amount NUMERIC);",
    "CREATE TABLE borrower (customer_id TEXT REFERENCES customer(customer_id), loan_number TEXT REFERENCES loan(loan_number), PRIMARY KEY (customer_id, loan_number));",

    "INSERT INTO branch VALUES ('Brooklyn Bank','Brooklyn',9000000),('Brooklyn Bridge Bank','Brooklyn',3700000),('Midtown Bank','Manhattan',5000000),('Downtown Bank','Manhattan',4200000),('Bronx Central Bank','Bronx',2100000);",
    "INSERT INTO customer VALUES ('10001','Alex Johnson','Grand Concourse','Bronx'),('10002','Hank Irwin','River Ave','Bronx'),('10003','Maria Chen','Grand Concourse','Bronx'),('10004','Sara Johnson','Ocean Pkwy','Brooklyn'),('10005','Wei Tanaka','Flatbush Ave','Brooklyn'),('10006','Omar Diaz','5th Ave','Manhattan'),('10007','Priya Nair','Broadway','Manhattan'),('10008','Liam Byrne','Grand Concourse','Bronx');",
    "INSERT INTO account VALUES ('A-101','Brooklyn Bank',42000),('A-102','Brooklyn Bank',38656),('A-103','Brooklyn Bridge Bank',51000),('A-104','Midtown Bank',15000),('A-105','Midtown Bank',27000),('A-106','Downtown Bank',9000),('A-107','Bronx Central Bank',12000),('A-108','Brooklyn Bank',60000);",
    "INSERT INTO depositor VALUES ('10001','A-101'),('10002','A-102'),('10003','A-103'),('10004','A-108'),('10005','A-104'),('10006','A-105'),('10007','A-106'),('10008','A-107');",
    "INSERT INTO loan VALUES ('L-201','Brooklyn Bank',15000),('L-202','Brooklyn Bridge Bank',9000),('L-203','Midtown Bank',22000),('L-204','Downtown Bank',5000);",
    "INSERT INTO borrower VALUES ('10002','L-201'),('10002','L-202'),('10003','L-201'),('10006','L-203');"
  ].join("\n");

  function init() {
    if (readyPromise) return readyPromise;
    readyPromise = initSqlJs({
      locateFile: function (file) {
        return "https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.14.2/" + file;
      }
    }).then(function (SQL) {
      SQLlib = SQL;
      var db = new SQL.Database();
      db.run(SEED_SQL);
      pristineBytes = db.export();
      db.close();
      return true;
    });
    return readyPromise;
  }

  // Runs `sql` against a fresh copy of the seeded DB. Never mutates shared state.
  function runQuery(sql) {
    if (!SQLlib || !pristineBytes) {
      return { error: "SQLエンジンを読み込み中です。少し待ってからもう一度お試しください。" };
    }
    var db = new SQLlib.Database(pristineBytes);
    try {
      var res = db.exec(sql);
      db.close();
      if (res.length === 0) return { columns: [], rows: [] };
      return { columns: res[0].columns, rows: res[0].values };
    } catch (e) {
      db.close();
      return { error: e.message };
    }
  }

  function normalizeRows(rows) {
    return rows.map(function (r) {
      return r.map(function (v) { return v === null ? "∅" : String(v); });
    });
  }

  function gradeQuery(studentSql, solutionSql, orderSensitive) {
    var student = runQuery(studentSql);
    if (student.error) {
      return { pass: false, studentError: student.error, student: null, expected: null };
    }
    var expected = runQuery(solutionSql);
    if (expected.error) {
      // Should never happen if solutions were validated, but fail safe.
      return { pass: false, studentError: null, engineError: expected.error, student: student, expected: null };
    }
    var a = normalizeRows(student.rows);
    var b = normalizeRows(expected.rows);
    if (!orderSensitive) {
      a = a.map(function (r) { return r.join("\u0001"); }).sort();
      b = b.map(function (r) { return r.join("\u0001"); }).sort();
    } else {
      a = a.map(function (r) { return r.join("\u0001"); });
      b = b.map(function (r) { return r.join("\u0001"); });
    }
    var pass = JSON.stringify(a) === JSON.stringify(b);
    return { pass: pass, student: student, expected: expected };
  }

  return { init: init, runQuery: runQuery, gradeQuery: gradeQuery };
})();

/* ===== Live syntax highlighting (textarea-over-pre overlay, SQL tokenizer) ===== */

var SQL_KEYWORDS = ["SELECT","FROM","WHERE","JOIN","INNER","LEFT","RIGHT","FULL","OUTER","CROSS",
  "ON","USING","GROUP","BY","ORDER","HAVING","AS","AND","OR","NOT","IN","IS","NULL","NULLS",
  "UNION","ALL","INTERSECT","EXCEPT","DISTINCT","CASE","WHEN","THEN","ELSE","END","WITH",
  "LIMIT","ASC","DESC","BETWEEN","LIKE","EXISTS","CAST","COUNT","SUM","AVG","MIN","MAX",
  "INSERT","INTO","VALUES","UPDATE","SET","DELETE","CREATE","TABLE","PRIMARY","KEY",
  "FOREIGN","REFERENCES","CHECK","DEFAULT","UNIQUE"];
var SQL_TYPES = ["INTEGER","INT","TEXT","NUMERIC","REAL","VARCHAR","CHAR","DATE","BOOLEAN","MONEY"];

/* Table/column names available for autocomplete — must match SEED_SQL above. */
var SCHEMA_INFO = {
  department: ["dept_name", "building", "budget"],
  instructor: ["instructor_id", "name", "dept_name", "salary"],
  student: ["student_id", "name", "dept_name", "tot_cred"],
  course: ["course_id", "title", "dept_name", "credits"],
  section: ["course_id", "section_id", "semester", "year", "building", "room_number"],
  takes: ["student_id", "course_id", "section_id", "semester", "year", "grade"],
  teaches: ["instructor_id", "course_id", "section_id", "semester", "year"],
  advisor: ["student_id", "instructor_id"],
  prereq: ["course_id", "prereq_id"],
  branch: ["branch_name", "branch_city", "assets"],
  customer: ["customer_id", "customer_name", "customer_street", "customer_city"],
  account: ["account_number", "branch_name", "balance"],
  depositor: ["customer_id", "account_number"],
  loan: ["loan_number", "branch_name", "amount"],
  borrower: ["customer_id", "loan_number"]
};
var SCHEMA_TABLES = Object.keys(SCHEMA_INFO);
var SCHEMA_COLUMNS = (function () {
  var seen = {}, list = [];
  SCHEMA_TABLES.forEach(function (t) {
    SCHEMA_INFO[t].forEach(function (c) {
      if (!seen[c]) { seen[c] = true; list.push(c); }
    });
  });
  return list;
})();

function escapeHtmlSQL(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function highlightSQLLine(line) {
  var out = "", i = 0;
  while (i < line.length) {
    var rest = line.slice(i);
    if (rest.slice(0, 2) === "--") {
      out += '<span class="cm">' + escapeHtmlSQL(rest) + "</span>";
      break;
    }
    var m = rest.match(/^'[^']*'/) || rest.match(/^"[^"]*"/);
    if (m) {
      out += '<span class="st">' + escapeHtmlSQL(m[0]) + "</span>";
      i += m[0].length;
      continue;
    }
    m = rest.match(/^-?\d+(\.\d+)?/);
    if (m) {
      out += '<span class="nm">' + escapeHtmlSQL(m[0]) + "</span>";
      i += m[0].length;
      continue;
    }
    m = rest.match(/^[A-Za-z_]\w*/);
    if (m) {
      var w = m[0], up = w.toUpperCase();
      if (SQL_KEYWORDS.indexOf(up) !== -1 || SQL_TYPES.indexOf(up) !== -1) {
        out += '<span class="kw">' + escapeHtmlSQL(w) + "</span>";
      } else {
        out += escapeHtmlSQL(w);
      }
      i += w.length;
      continue;
    }
    out += escapeHtmlSQL(rest[0]);
    i += 1;
  }
  return out;
}

function highlightSQL(code) {
  return code.split("\n").map(highlightSQLLine).join("\n");
}

/* ===== Autocomplete (keywords + table/column names) ===== */

var AC = { open: false, editorId: null, items: [], active: 0, dropdownEl: null };

function acGetWordRangeAtCaret(editor) {
  var pos = editor.selectionStart, val = editor.value;
  var start = pos;
  while (start > 0 && /[A-Za-z0-9_]/.test(val[start - 1])) start--;
  return { start: start, end: pos, word: val.slice(start, pos) };
}

// Classic "mirror div" technique: clone the textarea's box/font metrics onto an
// offscreen div containing the text up to the caret, then read where that text
// ends to know the caret's on-screen pixel position.
function acGetCaretCoordinates(textarea, position) {
  var mirror = document.createElement("div");
  var style = getComputedStyle(textarea);
  ["boxSizing", "width", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft",
   "borderTopWidth", "borderRightWidth", "borderBottomWidth", "borderLeftWidth",
   "fontFamily", "fontSize", "fontWeight", "lineHeight", "letterSpacing", "whiteSpace"]
    .forEach(function (p) { mirror.style[p] = style[p]; });
  mirror.style.position = "absolute";
  mirror.style.visibility = "hidden";
  mirror.style.top = "0";
  mirror.style.left = "-9999px";
  document.body.appendChild(mirror);
  mirror.textContent = textarea.value.substring(0, position);
  var span = document.createElement("span");
  span.textContent = textarea.value.substring(position) || ".";
  mirror.appendChild(span);
  var coords = { top: span.offsetTop, left: span.offsetLeft, height: span.offsetHeight || parseInt(style.lineHeight, 10) || 18 };
  document.body.removeChild(mirror);
  return coords;
}

function acGetDropdown() {
  if (!AC.dropdownEl) {
    AC.dropdownEl = document.createElement("div");
    AC.dropdownEl.className = "autocomplete-dropdown";
    AC.dropdownEl.hidden = true;
    document.body.appendChild(AC.dropdownEl);
  }
  return AC.dropdownEl;
}

function acHide() {
  AC.open = false;
  AC.editorId = null;
  if (AC.dropdownEl) AC.dropdownEl.hidden = true;
}

function acCandidateTag(word) {
  var up = word.toUpperCase();
  if (SQL_TYPES.indexOf(up) !== -1) return "type";
  if (SQL_KEYWORDS.indexOf(up) !== -1) return "keyword";
  if (SCHEMA_TABLES.indexOf(word) !== -1) return "table";
  return "column";
}

function acUpdate(editorId) {
  var editor = document.getElementById("ed-" + editorId);
  var range = acGetWordRangeAtCaret(editor);
  if (range.word.length < 1) { acHide(); return; }
  var upper = range.word.toUpperCase();
  var lower = range.word.toLowerCase();
  var kwMatches = SQL_KEYWORDS.concat(SQL_TYPES).filter(function (k) {
    return k.indexOf(upper) === 0;
  });
  var nameMatches = SCHEMA_TABLES.concat(SCHEMA_COLUMNS).filter(function (n) {
    return n.toLowerCase().indexOf(lower) === 0;
  });
  var seen = {};
  var items = [];
  kwMatches.concat(nameMatches).forEach(function (text) {
    if (seen[text]) return;
    seen[text] = true;
    items.push({ text: text, tag: acCandidateTag(text) });
  });
  items = items.slice(0, 8);
  if (items.length === 0 || (items.length === 1 && items[0].text.toLowerCase() === lower)) { acHide(); return; }
  AC.open = true;
  AC.editorId = editorId;
  AC.items = items;
  AC.active = 0;
  acRender(editor, range);
}

var AC_TAG_LABEL = { keyword: "keyword", type: "type", table: "table", column: "column" };

function acRender(editor, range) {
  var dd = acGetDropdown();
  dd.innerHTML = "";
  AC.items.forEach(function (item, idx) {
    var el = document.createElement("div");
    el.className = "autocomplete-item" + (idx === AC.active ? " active" : "");
    el.innerHTML = "<span>" + escapeHtmlSQL(item.text) + '</span><span class="ac-tag">' + AC_TAG_LABEL[item.tag] + "</span>";
    el.addEventListener("mousedown", function (e) {
      e.preventDefault();
      acApply(idx);
    });
    dd.appendChild(el);
  });
  var coords = acGetCaretCoordinates(editor, range.end);
  var rect = editor.getBoundingClientRect();
  dd.style.left = (rect.left + window.scrollX + coords.left - editor.scrollLeft) + "px";
  dd.style.top = (rect.top + window.scrollY + coords.top + coords.height - editor.scrollTop) + "px";
  dd.hidden = false;
}

function acApply(idx) {
  if (!AC.open || !AC.editorId) return;
  var editor = document.getElementById("ed-" + AC.editorId);
  var range = acGetWordRangeAtCaret(editor);
  var chosen = AC.items[idx !== undefined ? idx : AC.active];
  if (!chosen) return;
  var before = editor.value.slice(0, range.start), after = editor.value.slice(range.end);
  editor.value = before + chosen.text + after;
  var newPos = before.length + chosen.text.length;
  editor.selectionStart = editor.selectionEnd = newPos;
  editor.dispatchEvent(new Event("input"));
  acHide();
  editor.focus();
}

document.addEventListener("scroll", function () { if (AC.open) acHide(); }, true);
document.addEventListener("mousedown", function (e) {
  if (AC.open && AC.dropdownEl && !AC.dropdownEl.contains(e.target)) acHide();
});

/* ===== Result table rendering ===== */

function renderResultTable(result) {
  if (result.error) {
    return '<div class="sql-error">⚠️ ' + escapeHtmlSQL(result.error) + "</div>";
  }
  if (!result.rows || result.rows.length === 0) {
    return '<div class="sql-empty">（結果は0行でした）</div>';
  }
  var html = '<div class="result-wrap"><table class="result-table"><thead><tr>';
  result.columns.forEach(function (c) { html += "<th>" + escapeHtmlSQL(c) + "</th>"; });
  html += "</tr></thead><tbody>";
  result.rows.slice(0, 50).forEach(function (row) {
    html += "<tr>";
    row.forEach(function (v) {
      html += "<td>" + (v === null ? '<span class="null-val">NULL</span>' : escapeHtmlSQL(String(v))) + "</td>";
    });
    html += "</tr>";
  });
  html += "</tbody></table>";
  if (result.rows.length > 50) {
    html += '<div class="sql-empty">（' + result.rows.length + "行中、先頭50行のみ表示）</div>";
  }
  html += "</div>";
  return html;
}

/* ===== Practice card rendering + wiring ===== */

function buildPracticeCard(p) {
  var card = document.createElement("div");
  card.className = "practice-card sql-practice-card";
  card.innerHTML =
    '<div class="ptitle">' + escapeHtmlSQL(p.title) + ' <span class="ptier">' + p.tier + "</span></div>" +
    '<p class="ptask">' + p.scenario + "</p>" +
    '<p class="pconcept">🎯 <strong>スキル:</strong> ' + escapeHtmlSQL(p.concept) + "</p>" +
    '<div class="editor-wrap">' +
      '<pre class="code-highlight" id="hl-' + p.id + '" aria-hidden="true"><code></code></pre>' +
      '<textarea class="code-editor" id="ed-' + p.id + '" spellcheck="false" wrap="off"></textarea>' +
    "</div>" +
    '<div class="practice-toolbar">' +
      '<button class="run-btn" type="button" data-id="' + p.id + '">▶ 実行</button>' +
      '<button class="check-btn" type="button" data-id="' + p.id + '">✅ 採点</button>' +
      '<button class="hint-btn" type="button" data-id="' + p.id + '">💡 ヒントを見る</button>' +
      '<button class="reveal-btn" type="button" data-id="' + p.id + '">🔑 答えを見る</button>' +
    "</div>" +
    '<div class="check-result" id="result-' + p.id + '"></div>' +
    '<p class="phint" id="hint-' + p.id + '" hidden>💡 <strong>ヒント:</strong> ' + escapeHtmlSQL(p.hint) + "</p>" +
    '<div class="answer-reveal" id="answer-' + p.id + '" hidden>' +
      '<pre class="code-block"><code id="answer-code-' + p.id + '"></code></pre>' +
    "</div>";
  return card;
}

function wirePracticeCard(p) {
  var editor = document.getElementById("ed-" + p.id);
  var hl = document.getElementById("hl-" + p.id);
  var hlCode = hl.querySelector("code");
  editor.value = p.starter;

  function sync() {
    hlCode.innerHTML = highlightSQL(editor.value) + "\n";
  }
  sync();
  editor.addEventListener("input", function () {
    sync();
    acUpdate(p.id);
  });
  editor.addEventListener("scroll", function () {
    hl.scrollTop = editor.scrollTop;
    hl.scrollLeft = editor.scrollLeft;
    if (AC.open && AC.editorId === p.id) acHide();
  });
  editor.addEventListener("blur", function () {
    // Small delay so a mousedown on a dropdown item still registers as a click
    // before we hide it (blur fires before the item's own click otherwise).
    setTimeout(function () { if (AC.editorId === p.id) acHide(); }, 150);
  });
  editor.addEventListener("keydown", function (e) {
    if (AC.open && AC.editorId === p.id) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        AC.active = (AC.active + 1) % AC.items.length;
        acRender(editor, acGetWordRangeAtCaret(editor));
        return;
      }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        AC.active = (AC.active - 1 + AC.items.length) % AC.items.length;
        acRender(editor, acGetWordRangeAtCaret(editor));
        return;
      }
      if (e.key === "Tab" || e.key === "Enter") {
        e.preventDefault();
        acApply();
        return;
      }
      if (e.key === "Escape") {
        e.preventDefault();
        acHide();
        return;
      }
    }
    if (e.key === "Tab") {
      e.preventDefault();
      var s = editor.selectionStart, en = editor.selectionEnd;
      editor.value = editor.value.slice(0, s) + "  " + editor.value.slice(en);
      editor.selectionStart = editor.selectionEnd = s + 2;
      editor.dispatchEvent(new Event("input"));
    }
  });

  var runBtn = document.querySelector('.run-btn[data-id="' + p.id + '"]');
  var checkBtn = document.querySelector('.check-btn[data-id="' + p.id + '"]');
  var hintBtn = document.querySelector('.hint-btn[data-id="' + p.id + '"]');
  var revealBtn = document.querySelector('.reveal-btn[data-id="' + p.id + '"]');
  var resultEl = document.getElementById("result-" + p.id);
  var hintEl = document.getElementById("hint-" + p.id);
  var answerEl = document.getElementById("answer-" + p.id);
  var answerCodeEl = document.getElementById("answer-code-" + p.id);
  answerCodeEl.innerHTML = highlightSQL(p.solution);

  runBtn.addEventListener("click", function () {
    var res = SQL_ENGINE.runQuery(editor.value);
    resultEl.innerHTML = '<div class="result-label">▶ 実行結果</div>' + renderResultTable(res);
  });

  checkBtn.addEventListener("click", function () {
    // Strip line comments (the starter text always begins with a "-- ..." prompt)
    // before checking whether the student actually wrote any SQL yet.
    var withoutComments = editor.value.replace(/--[^\n]*/g, "").trim();
    if (withoutComments === "") {
      resultEl.innerHTML = '<div class="check-result-msg fail">✍️ まずSQLを入力してから採点してください。</div>';
      return;
    }
    var g = SQL_ENGINE.gradeQuery(editor.value, p.solution, !!p.orderSensitive);
    var html = "";
    if (g.studentError) {
      html += '<div class="check-result-msg fail">❌ SQLエラー: ' + escapeHtmlSQL(g.studentError) + "</div>";
    } else if (g.pass) {
      html += '<div class="check-result-msg pass">✅ 正解です！結果が模範解答と一致しました。</div>';
      html += '<div class="result-label">▶ 実行結果</div>' + renderResultTable(g.student);
    } else {
      html += '<div class="check-result-msg fail">❌ 結果が模範解答と一致しません。もう一度見直してみましょう。</div>';
      html += '<div class="result-label">▶ あなたの実行結果</div>' + renderResultTable(g.student);
    }
    resultEl.innerHTML = html;
  });

  hintBtn.addEventListener("click", function () {
    hintEl.hidden = !hintEl.hidden;
    hintBtn.textContent = hintEl.hidden ? "💡 ヒントを見る" : "🙈 ヒントを隠す";
  });

  revealBtn.addEventListener("click", function () {
    answerEl.hidden = !answerEl.hidden;
    revealBtn.textContent = answerEl.hidden ? "🔑 答えを見る" : "🙈 答えを隠す";
  });
}

/* ===== Schema reference panel (which tables/columns exist) ===== */

var UNIVERSITY_TABLES = ["department", "instructor", "student", "course", "section", "takes", "teaches", "advisor", "prereq"];
var BANKING_TABLES = ["branch", "customer", "account", "depositor", "loan", "borrower"];

function schemaTableRow(t) {
  return '<div class="schema-table"><span class="schema-tname">' + escapeHtmlSQL(t) + "</span>" +
    '<span class="schema-cols">' + escapeHtmlSQL(SCHEMA_INFO[t].join(", ")) + "</span></div>";
}

function buildSchemaRefHTML() {
  return '<div class="schema-ref" id="schemaRef">' +
    '<button type="button" class="schema-ref-toggle" id="schemaRefToggle">📋 テーブル構成（列一覧）を見る ▾</button>' +
    '<div class="schema-ref-body" id="schemaRefBody" hidden>' +
      '<div class="schema-group"><h3>🎓 University DB</h3>' + UNIVERSITY_TABLES.map(schemaTableRow).join("") + "</div>" +
      '<div class="schema-group"><h3>🏦 Banking DB</h3>' + BANKING_TABLES.map(schemaTableRow).join("") + "</div>" +
    "</div>" +
  "</div>";
}

function wireSchemaReference() {
  var toggle = document.getElementById("schemaRefToggle");
  var body = document.getElementById("schemaRefBody");
  if (!toggle || !body) return;
  toggle.addEventListener("click", function () {
    body.hidden = !body.hidden;
    toggle.textContent = body.hidden ? "📋 テーブル構成（列一覧）を見る ▾" : "🙈 テーブル構成を隠す ▴";
  });
}

function renderPracticeArena(problems, containers) {
  var intro = document.querySelector(".arena-intro");
  if (intro && !document.getElementById("schemaRef")) {
    intro.insertAdjacentHTML("afterend", buildSchemaRefHTML());
    wireSchemaReference();
  }
  var byTier = { basic: containers.basicsEl, intermediate: containers.intermediateEl, advanced: containers.advancedEl };
  problems.forEach(function (p) {
    var target = byTier[p.tier];
    if (!target) return;
    var card = buildPracticeCard(p);
    target.appendChild(card);
  });
  problems.forEach(wirePracticeCard);

  SQL_ENGINE.init().then(function () {
    document.querySelectorAll(".sql-engine-status").forEach(function (el) {
      el.textContent = "✅ SQLエンジンの準備ができました。実際にクエリを実行できます。";
      el.className = "sql-engine-status ready";
    });
  }).catch(function (err) {
    document.querySelectorAll(".sql-engine-status").forEach(function (el) {
      el.textContent = "⚠️ SQLエンジンの読み込みに失敗しました。インターネット接続を確認して再読み込みしてください。";
      el.className = "sql-engine-status error";
    });
  });
}
