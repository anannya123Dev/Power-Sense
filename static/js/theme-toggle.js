// Applies saved theme immediately (avoids flash), then wires up the
// #themeToggle icon button once the page has loaded, if present.
(function () {
  var saved = localStorage.getItem('powersense-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
})();

document.addEventListener('DOMContentLoaded', function () {
  var btn = document.getElementById('themeToggle');
  if (!btn) return;

  function updateIcon() {
    var t = document.documentElement.getAttribute('data-theme');
    btn.textContent = t === 'light' ? '☀️' : '🌙';
  }
  updateIcon();

  btn.addEventListener('click', function () {
    var cur = document.documentElement.getAttribute('data-theme');
    var next = cur === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('powersense-theme', next);
    updateIcon();
  });
});
