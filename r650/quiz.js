// Shared quiz + scroll-reveal logic for all chapters
let score = 0, answered = 0, FEEDBACKS = {}, TOTAL = 5;

function setupQuiz(feedbacks) {
  FEEDBACKS = feedbacks;
  TOTAL = document.querySelectorAll('.quiz-q').length || 5;
  const sc = document.getElementById('score');
  if (sc) sc.textContent = '0 / ' + TOTAL;
}

function checkAnswer(btn, q) {
  const container = btn.closest('.quiz-q');
  const btns = container.querySelectorAll('.option-btn');
  if (btns[0].disabled) return;
  btns.forEach(b => b.disabled = true);
  const ok = btn.getAttribute('data-correct') === "true";
  const fb = document.getElementById('fb' + q);
  if (ok) {
    btn.classList.add('correct');
    score++;
    if (fb) { fb.textContent = "✅ " + (FEEDBACKS[q] || "Correct!"); fb.className = 'q-feedback show correct-fb'; }
  } else {
    btn.classList.add('wrong');
    btns.forEach(b => { if (b.getAttribute('data-correct') === "true") b.classList.add('correct'); });
    if (fb) { fb.textContent = "❌ Not quite. " + (FEEDBACKS[q] || "Review the section and check the highlighted correct answer."); fb.className = 'q-feedback show wrong-fb'; }
  }
  answered++;
  const sc = document.getElementById('score');
  if (sc) sc.textContent = score + ' / ' + TOTAL;
  const pb = document.getElementById('progressBar');
  if (pb) pb.style.width = (answered / TOTAL * 100) + '%';
}

// Scroll reveal for .unit blocks
const obs = new IntersectionObserver(e => {
  e.forEach(x => { if (x.isIntersecting) x.target.classList.add('visible'); });
}, { threshold: 0, rootMargin: '0px 0px -20px 0px' });
document.querySelectorAll('.unit').forEach(u => obs.observe(u));
setTimeout(() => { document.querySelectorAll('.unit:not(.visible)').forEach(u => u.classList.add('visible')); }, 600);
