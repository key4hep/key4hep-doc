(function () {
  var overview = document.getElementById('algorithm-overview');
  if (!overview) return;

  var totalItems = parseInt(overview.dataset.total, 10);
  var totalPackages = parseInt(overview.dataset.packages, 10);

  var searchInput = document.getElementById('alg-search');
  var statsEl = document.getElementById('alg-stats');

  // Toggle package group collapse/expand
  overview.querySelectorAll('.alg-package-header').forEach(function (header) {
    header.addEventListener('click', function () {
      header.closest('.alg-package-group').classList.toggle('collapsed');
    });
  });

  // Toggle card expand/collapse
  overview.querySelectorAll('.alg-card-header').forEach(function (header) {
    header.addEventListener('click', function () {
      header.closest('.alg-card').classList.toggle('expanded');
    });
  });

  function debounce(fn, delay) {
    var timer;
    return function () {
      clearTimeout(timer);
      timer = setTimeout(fn, delay);
    };
  }

  function updateStats(visibleCards, visiblePackages) {
    statsEl.textContent =
      'Showing ' + visibleCards + ' of ' + totalItems +
      ' algorithms in ' + visiblePackages + ' packages';
  }

  function filterCards() {
    var query = searchInput.value.trim().toLowerCase();
    var visibleCards = 0;

    overview.querySelectorAll('.alg-card').forEach(function (card) {
      if (!query) {
        card.style.display = '';
        visibleCards++;
        return;
      }
      var name = (card.dataset.name || '').toLowerCase();
      var lib  = (card.dataset.lib  || '').toLowerCase();
      var pkg  = (card.dataset.package || '').toLowerCase();
      var matches = name.indexOf(query) !== -1 ||
                    lib.indexOf(query)  !== -1 ||
                    pkg.indexOf(query)  !== -1;
      card.style.display = matches ? '' : 'none';
      if (matches) visibleCards++;
    });

    var visiblePackages = 0;
    overview.querySelectorAll('.alg-package-group').forEach(function (group) {
      var anyVisible = false;
      group.querySelectorAll('.alg-card').forEach(function (c) {
        if (c.style.display !== 'none') anyVisible = true;
      });
      group.style.display = anyVisible ? '' : 'none';
      if (anyVisible) visiblePackages++;
    });

    updateStats(visibleCards, visiblePackages);
  }

  searchInput.addEventListener('input', debounce(filterCards, 200));

  // URL hash deep-linking: #Name expands and scrolls to that card
  function handleHash() {
    var hash = decodeURIComponent(window.location.hash.slice(1));
    if (!hash) return;
    var target = null;
    overview.querySelectorAll('.alg-card').forEach(function (c) {
      if (c.dataset.name === hash) target = c;
    });
    if (!target) return;
    var group = target.closest('.alg-package-group');
    if (group) group.classList.remove('collapsed');
    target.classList.add('expanded');
    setTimeout(function () {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  }

  window.addEventListener('hashchange', handleHash);
  handleHash();

  updateStats(totalItems, totalPackages);
})();
