// Nested dropdown submenu ("Past projects") toggle: works on touch and desktop.
document.addEventListener('DOMContentLoaded', function () {
    var toggles = document.querySelectorAll('.dropdown-submenu > .dropdown-toggle');

    toggles.forEach(function (toggle) {
        toggle.addEventListener('click', function (event) {
            event.preventDefault();
            event.stopPropagation();

            var submenu = toggle.nextElementSibling;
            if (!submenu) {
                return;
            }

            var isOpen = submenu.classList.toggle('show');
            toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });
    });

    // Collapse submenus whenever their parent dropdown closes.
    document.querySelectorAll('.nav-item.dropdown').forEach(function (dropdown) {
        dropdown.addEventListener('hide.bs.dropdown', function () {
            dropdown.querySelectorAll('.dropdown-submenu > .dropdown-menu.show').forEach(function (submenu) {
                submenu.classList.remove('show');
                var toggle = submenu.previousElementSibling;
                if (toggle) {
                    toggle.setAttribute('aria-expanded', 'false');
                }
            });
        });
    });
});
