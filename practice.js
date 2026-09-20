// Lightweight self-check for the SQL code practice cards.
// Not a real SQL interpreter: it just checks that the required
// keywords/phrases appear in the student's typed query, then lets
// them reveal the model answer to compare for themselves.
function checkPractice(id, requiredKeywords) {
  var box = document.getElementById(id + '-input');
  var result = document.getElementById(id + '-result');
  if (!box || !result) return;
  var input = box.value.toUpperCase();
  var missing = requiredKeywords.filter(function (k) {
    return input.indexOf(k.toUpperCase()) === -1;
  });
  if (input.trim() === '') {
    result.className = 'check-result fail';
    result.textContent = '✍️ まずSQLを入力してから答え合わせしてください。';
    return;
  }
  if (missing.length === 0) {
    result.className = 'check-result pass';
    result.textContent = '✅ よくできました！必要なキーワードが揃っています。実際にpgAdminで実行して結果も確認してみましょう。';
  } else {
    result.className = 'check-result fail';
    result.textContent = '⚠️ 次のキーワード／要素がまだ見当たりません: ' + missing.join('、');
  }
}

function toggleAnswer(id, btn) {
  var ans = document.getElementById(id + '-answer');
  if (!ans) return;
  ans.hidden = !ans.hidden;
  if (btn) btn.textContent = ans.hidden ? '💡 答えを見る' : '🙈 答えを隠す';
}
