document.addEventListener('DOMContentLoaded', () => {
  const textEls = document.querySelectorAll('p, h1, h2, h3');
  textEls.forEach(el => {
    el.classList.add('scroll-fade-text');
    const text = el.textContent;
    el.textContent = '';
    text.split('').forEach((char, i) => {
      const span = document.createElement('span');
      span.textContent = char === ' ' ? '\u00A0' : char;
      span.style.transitionDelay = `${i * 0.05}s`;
      el.appendChild(span);
    });
  });

  const elements = document.querySelectorAll('img, .fade-in-element, .scroll-fade-text');
  elements.forEach(el => {
    if (!el.classList.contains('scroll-fade-text')) {
      el.classList.add('fade-in-element');
    }
  });

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in-element, .scroll-fade-text').forEach(el => {
    observer.observe(el);
  });

  const menuToggle = document.querySelector('.menu-toggle');
  const mobileNav = document.querySelector('.mobile-nav');
  const closeMenu = document.querySelector('.close-menu');
  if (menuToggle && mobileNav) {
    menuToggle.addEventListener('click', () => {
      mobileNav.classList.toggle('open');
    });
  }
  if (closeMenu && mobileNav) {
    closeMenu.addEventListener('click', () => {
      mobileNav.classList.remove('open');
    });
  }

  const tfElement = document.querySelector('[data-tf-live]');
  if (tfElement) {
    const loadTypeform = () => {
      const s = document.createElement('script');
      s.src = '//embed.typeform.com/next/embed.js';
      s.defer = true;
      document.body.appendChild(s);
    };
    const formObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          loadTypeform();
          obs.disconnect();
        }
      });
    });
    formObserver.observe(tfElement);
  }

  document.querySelectorAll('.faq details').forEach(detail => {
    detail.addEventListener('toggle', function() {
      if (this.open) {
        document.querySelectorAll('.faq details').forEach(other => {
          if (other !== this) other.open = false;
        });
      }
    });
  });

  const splash = document.getElementById('splash-screen');
  if (splash) {
    const hasSeenSplash = document.cookie.split(';').some(c => c.trim() === 'splashSeen=true');
    if (hasSeenSplash) {
      splash.remove();
    } else {
      window.addEventListener('load', () => {
        document.cookie = 'splashSeen=true; path=/; max-age=31536000';
        setTimeout(() => {
          splash.classList.add('fade-english');
        }, 1000);
        setTimeout(() => {
          splash.classList.add('hide');
        }, 3000);
        splash.addEventListener('transitionend', () => {
          splash.remove();
        }, { once: true });
      });
    }
  }

  const header = document.querySelector('header');
  if (header) {
    const activateAt = 300;
    const handleScroll = () => {
      const { scrollY } = window;
      if (scrollY > activateAt) {
        header.classList.add('scrolled');
      } else if (scrollY <= 0) {
        header.classList.remove('scrolled');
      }
    };
    handleScroll();
    window.addEventListener('scroll', handleScroll);
  }
});
