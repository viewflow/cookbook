window.addEventListener('turbo:render', function() {
    const toggleNavSidebar = document.getElementById('toggle-nav-sidebar');
    if (toggleNavSidebar !== null) {
        const navSidebar = document.getElementById('nav-sidebar');
        const main = document.getElementById('main');
        let navSidebarIsOpen = localStorage.getItem('django.admin.navSidebarIsOpen');
        if (navSidebarIsOpen === null) {
            navSidebarIsOpen = 'true';
        }
        main.classList.toggle('shifted', navSidebarIsOpen === 'true');
        navSidebar.setAttribute('aria-expanded', navSidebarIsOpen);

        toggleNavSidebar.addEventListener('click', function() {
            if (navSidebarIsOpen === 'true') {
                navSidebarIsOpen = 'false';
            } else {
                navSidebarIsOpen = 'true';
            }
            localStorage.setItem('django.admin.navSidebarIsOpen', navSidebarIsOpen);
            main.classList.toggle('shifted');
            navSidebar.setAttribute('aria-expanded', navSidebarIsOpen);
        });
    }
    window.initSidebarQuickFilter();
})

const originalAddEventListener = window.addEventListener;

window.addEventListener = function(event, listener, options) {
  if (event === 'load') {
    originalAddEventListener.call(this, 'turbo:render', listener, options);
  }

  originalAddEventListener.call(this, event, listener, options);
};


const originalDocAddEventListener = document.addEventListener;

document.addEventListener = function(event, listener, options) {
  if (event === 'DOMContentLoaded') {
    originalDocAddEventListener.call(this, 'turbo:render', listener, options);
  }

  originalDocAddEventListener.call(this, event, listener, options);
};


