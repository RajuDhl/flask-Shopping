const navs = document.getElementsByClassName('nav-link');
    for (let i = 0; i < navs.length; i++) {
        if (navs[i].href === window.location.href) {
            navs[i].style.color = 'white';
        }
    }