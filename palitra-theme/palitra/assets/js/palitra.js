/* Палитра: mobile drawer + keyboard-friendly mega menu. */
(function () {
	'use strict';

	var drawer = document.getElementById('pl-drawer');
	var burger = document.querySelector('.pl-burger');
	if (drawer && burger) {
		var closeBtn = drawer.querySelector('.pl-drawer__close');
		var open = function () {
			drawer.hidden = false;
			requestAnimationFrame(function () { drawer.classList.add('is-open'); });
			burger.setAttribute('aria-expanded', 'true');
			document.documentElement.classList.add('pl-no-scroll');
			if (closeBtn) { closeBtn.focus(); }
		};
		var close = function () {
			drawer.classList.remove('is-open');
			burger.setAttribute('aria-expanded', 'false');
			document.documentElement.classList.remove('pl-no-scroll');
			setTimeout(function () { drawer.hidden = true; }, 250);
			burger.focus();
		};
		burger.addEventListener('click', open);
		if (closeBtn) { closeBtn.addEventListener('click', close); }
		drawer.addEventListener('click', function (e) { if (e.target === drawer) { close(); } });
		document.addEventListener('keydown', function (e) {
			if (e.key === 'Escape' && !drawer.hidden) { close(); }
		});
	}

	// Close an open mega menu with Escape (desktop keyboard users).
	document.addEventListener('keydown', function (e) {
		if (e.key !== 'Escape') { return; }
		var item = document.activeElement && document.activeElement.closest('.pl-nav__item');
		if (item) {
			var link = item.querySelector('.pl-nav__link');
			item.classList.add('is-closed');
			if (link) { link.focus(); }
		}
	});
	document.querySelectorAll('.pl-nav__item').forEach(function (item) {
		item.addEventListener('mouseleave', function () { item.classList.remove('is-closed'); });
		item.addEventListener('focusout', function (e) {
			if (!item.contains(e.relatedTarget)) { item.classList.remove('is-closed'); }
		});
	});
})();
