/* ===== Stats practice arena: numeric / choice questions, graded in the browser =====
   Problem object:
   { id, tier:"basic|intermediate|advanced", title, scenario(HTML), concept, hint,
     type:"num" | "mcq",
     // num: answers:[{label, value, tol|relTol}]   (one or several numbers)
     // mcq: options:[...], correct:index
     explain(HTML), rcode: "R code ...\n# output" }
   Pages call: renderStatsArena(PROBLEMS, {basicsEl, intermediateEl, advancedEl}) */
(function () {
  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  var R_FUNCS = /^(library|lm|summary|cor|cov|mean|sd|var|median|sum|sqrt|abs|round|c|seq|rep|data\.frame|head|plot|abline|hist|boxplot|t\.test|aov|TukeyHSD|chisq\.test|pt|qt|pnorm|qnorm|pchisq|qchisq|pf|qf|predict|resid|residuals|coef|confint|anova|glm|exp|log|plogis|table|prop\.table|cat|print|cbind|rbind|matrix|nrow|ncol|length|min|max|which|sample|set\.seed|read\.csv|factor|as\.factor|relevel|vif|step|AIC|BIC|cooks\.distance|hatvalues|rstandard|shapiro\.test|bptest|ggplot|aes|geom_point|geom_smooth|pairwise\.t\.test|power\.t\.test|qqnorm|qqline|I|poly|scale|ifelse|paste|rnorm|runif)$/;
  function hlR(line) {
    var out = "", i = 0, m;
    while (i < line.length) {
      var rest = line.slice(i);
      if (rest[0] === "#") { out += '<span class="cm">' + esc(rest) + "</span>"; break; }
      if ((m = /^"(?:[^"\\]|\\.)*"|^'(?:[^'\\]|\\.)*'/.exec(rest))) { out += '<span class="st">' + esc(m[0]) + "</span>"; i += m[0].length; continue; }
      if ((m = /^\d+(?:\.\d+)?(?:[eE][-+]?\d+)?/.exec(rest)) && (i === 0 || !/[A-Za-z_.]/.test(line[i - 1]))) { out += '<span class="nm">' + m[0] + "</span>"; i += m[0].length; continue; }
      if ((m = /^[A-Za-z_.][A-Za-z0-9_.]*/.exec(rest))) { out += (R_FUNCS.test(m[0]) || /^(function|if|else|for|TRUE|FALSE|NULL|NA)$/.test(m[0])) ? '<span class="kw">' + esc(m[0]) + "</span>" : esc(m[0]); i += m[0].length; continue; }
      out += esc(rest[0]); i++;
    }
    return out;
  }
  function codeBlock(code) {
    return '<pre class="code-block">' + String(code).split("\n").map(function (l) { return '<span class="cl">' + hlR(l) + "</span>"; }).join("\n") + "</pre>";
  }
  function parseNum(s) {
    s = String(s || "").trim().replace(/[,\s]/g, "").replace(/×10\^?/g, "e").replace(/−/g, "-").replace(/%$/, "");
    if (/^-?\d+\/\d+$/.test(s)) { var p = s.split("/"); return +p[0] / +p[1]; }
    return s === "" ? NaN : Number(s);
  }
  function numOk(x, a) {
    if (!isFinite(x)) return false;
    var abs = a.tol != null ? a.tol : 0, rel = a.relTol != null ? a.relTol : 0;
    if (a.tol == null && a.relTol == null) abs = Math.max(0.005, Math.abs(a.value) * 0.005);
    return Math.abs(x - a.value) <= Math.max(abs, rel * Math.abs(a.value)) + 1e-12;
  }
  var KEY = "statsArena:" + location.pathname, solved = {}, total = 0, chip = null;
  try { solved = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { solved = {}; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(solved)); } catch (e) {} }
  function updateChip() { if (chip) chip.textContent = "✅ 正解 " + Object.keys(solved).length + " / " + total; }

  function card(p) {
    var el = document.createElement("div");
    el.className = "practice-card sql-practice-card";
    el.id = p.id;
    var h = '<div class="ptitle">' + esc(p.title) + ' <span class="ptier">' + esc(p.tier) + "</span>" + (solved[p.id] ? '<span class="done-badge">✓ 正解済み</span>' : "") + "</div>" +
      '<p class="ptask">' + p.scenario + "</p>" + (p.concept ? '<p class="pconcept">🎯 <strong>スキル:</strong> ' + esc(p.concept) + "</p>" : "");
    if (p.type === "mcq") {
      h += '<div class="choice-list" id="ch-' + p.id + '">' + p.options.map(function (o, i) {
        return '<label><input type="radio" name="q-' + p.id + '" value="' + i + '"><span>' + o + "</span></label>"; }).join("") + "</div>";
    } else {
      h += '<div class="ans-row">' + p.answers.map(function (a, i) {
        return "<label>" + esc(a.label || "答え") + ' <input class="ans-input" id="in-' + p.id + "-" + i + '" inputmode="decimal" autocomplete="off" placeholder="数値"></label>' + (a.unit ? "<span>" + esc(a.unit) + "</span>" : ""); }).join("") + "</div>";
    }
    h += '<div class="practice-toolbar"><button class="check-btn" type="button">✅ 採点</button><button class="hint-btn" type="button">💡 ヒントを見る</button><button class="reveal-btn" type="button">🔑 答えを見る</button></div>' +
      '<div class="check-result" id="res-' + p.id + '"></div>' +
      '<p class="phint" id="hint-' + p.id + '" hidden>💡 <strong>ヒント:</strong> ' + p.hint + "</p>" +
      '<div class="answer-reveal" id="ans-' + p.id + '" hidden>' + (p.rcode ? "<p><strong>Rでの解き方：</strong></p>" + codeBlock(p.rcode) : "") + '<div class="expl">' + (p.explain || "") + "</div></div>";
    el.innerHTML = h;
    var res = el.querySelector("#res-" + p.id);
    function say(ok, msg) { res.innerHTML = '<div class="check-result-msg ' + (ok ? "pass" : "fail") + '">' + msg + "</div>"; }
    el.querySelector(".hint-btn").onclick = function () { var x = el.querySelector("#hint-" + p.id); x.hidden = !x.hidden; };
    el.querySelector(".reveal-btn").onclick = function () {
      var x = el.querySelector("#ans-" + p.id); x.hidden = !x.hidden;
      if (!x.hidden && p.type === "mcq") {
        el.querySelectorAll(".choice-list label").forEach(function (l, i) { l.classList.toggle("right", i === p.correct); });
      }
      if (!x.hidden && p.type === "num") res.innerHTML = '<div class="check-result-msg fail">答え：' + p.answers.map(function (a) { return esc((a.label || "") + " = " + a.value); }).join(" ／ ") + "</div>";
    };
    el.querySelector(".check-btn").onclick = function () {
      var ok;
      if (p.type === "mcq") {
        var sel = el.querySelector('input[name="q-' + p.id + '"]:checked');
        if (!sel) { say(false, "選択肢を選んでから採点してください。"); return; }
        ok = +sel.value === p.correct;
        el.querySelectorAll(".choice-list label").forEach(function (l, i) {
          l.classList.remove("picked", "right", "wrong");
          if (i === +sel.value) l.classList.add(ok ? "right" : "wrong");
          if (!ok && false) l.classList.add("right");
        });
      } else {
        var vals = p.answers.map(function (a, i) { return parseNum(el.querySelector("#in-" + p.id + "-" + i).value); });
        if (vals.some(function (v) { return isNaN(v); })) { say(false, "数値を入力してください（例：0.74 ／ 8.06e-6）。"); return; }
        ok = p.answers.every(function (a, i) { return numOk(vals[i], a); });
      }
      if (ok) { solved[p.id] = 1; save(); updateChip(); var t = el.querySelector(".ptitle"); if (!t.querySelector(".done-badge")) t.insertAdjacentHTML("beforeend", '<span class="done-badge">✓ 正解済み</span>'); }
      say(ok, ok ? "🎉 正解です！「🔑 答えを見る」でRでの解き方を確認しましょう。" : "おしい！もう一度計算してみましょう。ヒントや、丸め方（小数第何位まで）を確認してください。");
    };
    return el;
  }
  window.renderStatsArena = function (problems, c) {
    total = problems.length;
    var host = (c.basicsEl || document.body).closest(".container") || document.body;
    chip = document.createElement("div"); chip.className = "score-chip";
    host.insertBefore(chip, host.firstChild); updateChip();
    problems.forEach(function (p) {
      var t = p.tier === "basic" ? c.basicsEl : p.tier === "intermediate" ? c.intermediateEl : c.advancedEl;
      t.appendChild(card(p));
    });
    if (location.hash) { var tgt = document.getElementById(decodeURIComponent(location.hash.slice(1))); if (tgt) tgt.scrollIntoView(); }
  };
})();
