// reveal elements on scroll
(function () {
    const check = () => {
        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.top < (window.innerHeight || document.documentElement.clientHeight) - 80) el.classList.add('animated');
        });
    };
    window.addEventListener('scroll', check);
    window.addEventListener('load', check);
})();
