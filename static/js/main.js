// main.js - nav, active link highlight, mobile menu
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        const mobileBtn = document.getElementById('mobileMenuBtn');
        const navLinks = document.getElementById('navLinks');
        if (mobileBtn) mobileBtn.addEventListener('click', () => navLinks.classList.toggle('active'));

        const navbar = document.querySelector('.navbar');
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) navbar.classList.add('scrolled'); else navbar.classList.remove('scrolled');
        });

        // Active link highlight by data-page
        const path = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
        const map = {
            'index.html': 'home',
            '': 'home',
            'form.html': 'form',
            'signup.html': 'signup',
            'login.html': 'login'
        };
        const current = map[path] || (path.indexOf('index') >= 0 ? 'home' : path.replace('.html', ''));
        document.querySelectorAll('[data-page]').forEach(el => {
            if (el.dataset.page === current) el.classList.add('active');
            else el.classList.remove('active');
        });

        // close mobile menu when link clicked
        document.querySelectorAll('.nav-links a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('active')));
    });
})();
