// Collapses/expands the fixed sidebar on pages that have one.
// Persists the user's choice so it stays collapsed across pages.
document.addEventListener('DOMContentLoaded', function () {
  var btn = document.getElementById('sidebarToggle');
  var sidebar = document.querySelector('.sidebar');
  var main = document.querySelector('.main');
  if (!btn || !sidebar || !main) return;

  function apply(collapsed) {
    sidebar.classList.toggle('collapsed', collapsed);
    main.classList.toggle('sidebar-collapsed', collapsed);
  }

  var saved = localStorage.getItem('powersense-sidebar') === 'collapsed';
  apply(saved);

  btn.addEventListener('click', function () {
    var collapsed = !sidebar.classList.contains('collapsed');
    apply(collapsed);
    localStorage.setItem('powersense-sidebar', collapsed ? 'collapsed' : 'expanded');
  });
});
