document.addEventListener('DOMContentLoaded', () => {

    const updateActiveState = () => {
        const currentPath = decodeURIComponent(window.location.pathname);

        const links = document.querySelectorAll('.nav-link, .dropdown-item');
        const triggers = document.querySelectorAll('.dropdown-trigger');
        const dropdowns = document.querySelectorAll('.dropdown');

        links.forEach(el => el.classList.remove('active'));
        triggers.forEach(el => el.classList.remove('active'));
        dropdowns.forEach(el => el.classList.remove('dropdown-open'));

        links.forEach(link => {
            if (link.tagName === 'A' && link.getAttribute('href')) {
                const linkHref = link.getAttribute('href');

                if (linkHref === currentPath) {
                    link.classList.add('active');

                    const parentDropdown = link.closest('.dropdown');
                    if (parentDropdown) {
                        const parentTrigger = parentDropdown.querySelector('.dropdown-trigger');
                        if (parentTrigger) parentTrigger.classList.add('active');

                        parentDropdown.classList.add('dropdown-open');
                    }
                }
            }
        });

        if (currentPath.toLowerCase().startsWith('/proyecto')) {
            dropdowns.forEach(dropdown => dropdown.classList.add('dropdown-open'));
            triggers.forEach(trigger => {
                if (trigger.textContent.includes('Proyecto')) {
                    trigger.classList.add('active');
                }
            });
        }
    };

    updateActiveState();

    const observer = new MutationObserver(() => {
        updateActiveState();
    });

    observer.observe(document.body, { childList: true, subtree: true });
});
