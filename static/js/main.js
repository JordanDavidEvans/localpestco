document.addEventListener('DOMContentLoaded', () => {
  const elements = document.querySelectorAll('p, h1, h2, h3, img, .fade-in-element');
  elements.forEach(el => {
    el.classList.add('fade-in-element');
  });

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in-element').forEach(el => {
    observer.observe(el);
  });

  const menuToggle = document.querySelector('.menu-toggle');
  const mainNav = document.querySelector('.main-nav');
  if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', () => {
      mainNav.classList.toggle('open');
    });
  }
});
