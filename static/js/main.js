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
        const canvas = document.getElementById('flag');
        if (canvas) {
          const ctx = canvas.getContext('2d');
          const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
          };
          resize();
          window.addEventListener('resize', resize);
          let phase = 0;
          let split = 0;
          let yellowAlpha = 1;
          let showWelcome = true;
          const draw = () => {
            const w = canvas.width;
            const h = canvas.height;
            ctx.clearRect(0, 0, w, h);
            if (phase === 0) {
              ctx.fillStyle = '#000';
              ctx.fillRect(0, 0, w, h / 2);
              ctx.fillStyle = '#c60000';
              ctx.fillRect(0, h / 2, w, h / 2);
            } else {
              ctx.fillStyle = '#000';
              ctx.fillRect(-split, 0, w, h / 2);
              ctx.fillStyle = '#c60000';
              ctx.fillRect(split, h / 2, w, h / 2);
            }
            ctx.fillStyle = `rgba(255,255,0,${yellowAlpha})`;
            ctx.beginPath();
            ctx.arc(w / 2, h / 2, Math.min(w, h) / 4, 0, Math.PI * 2);
            ctx.fill();
            if (showWelcome) {
              ctx.fillStyle = '#fff';
              ctx.font = `${Math.min(w, h) / 12}px sans-serif`;
              ctx.textAlign = 'center';
              ctx.fillText('Welcome', w / 2, h / 2 + Math.min(w, h) / 24);
            }
            requestAnimationFrame(draw);
          };
          const startSplit = () => {
            phase = 1;
            const splitTimer = setInterval(() => {
              split += 8;
              if (split >= canvas.width / 2) clearInterval(splitTimer);
            }, 30);
            setTimeout(() => {
              showWelcome = false;
              const fadeTimer = setInterval(() => {
                yellowAlpha -= 0.02;
                if (yellowAlpha <= 0) clearInterval(fadeTimer);
              }, 30);
            }, 1500);
          };
          draw();
          setTimeout(startSplit, 1000);
        }
        setTimeout(() => {
          splash.classList.add('hide');
        }, 4500);
        setTimeout(() => {
          splash.remove();
        }, 6500);
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
