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

    document.querySelectorAll('.workshop-content :is(.language-sh, .language-bash, .language-shell, .language-powershell, .language-zsh, .language-bat, .language-cmd, .language-copilot)')
        .forEach(function (block) {
            const code = block.matches('code') ? block : block.querySelector('pre code');
            if (!code) {
                return;
            }
            const contentName = code.classList.contains('language-copilot') ? 'prompt' : 'commands';
            if (block.matches('code')) {
                const pre = block.closest('pre');
                const wrapper = document.createElement('div');
                pre.before(wrapper);
                wrapper.append(pre);
                block = wrapper;
            }

            const status = document.createElement('span');
            status.className = 'code-copy-status visually-hidden';
            status.setAttribute('role', 'status');
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'code-copy-button';
            button.title = 'Copy ' + contentName;
            button.setAttribute('aria-label', 'Copy ' + contentName + ' to clipboard');
            button.innerHTML = '<svg class="code-copy-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>'
                + '<svg class="code-copied-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="m5 12 4 4L19 6"/></svg>';
            block.classList.add('code-copy-block');
            block.prepend(button);
            block.append(status);

            let resetTimer;
            button.addEventListener('click', async function () {
                clearTimeout(resetTimer);
                button.disabled = true;
                button.dataset.state = 'copying';
                button.title = 'Copying ' + contentName + '...';
                button.setAttribute('aria-busy', 'true');
                status.textContent = '';
                status.classList.add('visually-hidden');
                try {
                    if (!navigator.clipboard || !navigator.clipboard.writeText) {
                        throw new Error('Clipboard access is unavailable.');
                    }
                    await navigator.clipboard.writeText(code.textContent);
                    button.dataset.state = 'copied';
                    button.title = 'Copied';
                    status.textContent = 'Copied to clipboard.';
                    resetTimer = setTimeout(function () {
                        delete button.dataset.state;
                        button.title = 'Copy ' + contentName;
                    }, 2000);
                } catch (error) {
                    button.dataset.state = 'error';
                    button.title = 'Retry copying ' + contentName;
                    status.classList.remove('visually-hidden');
                    status.textContent = 'Clipboard access failed. Select and copy the text manually.';
                    console.warn('Could not copy workshop text:', error);
                } finally {
                    button.disabled = false;
                    button.removeAttribute('aria-busy');
                }
            });
        });
});
