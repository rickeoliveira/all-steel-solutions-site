const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');
menuToggle?.addEventListener('click', () => {
  const isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
  menuToggle.setAttribute('aria-expanded', String(!isOpen));
  menuToggle.setAttribute('aria-label', isOpen ? 'Abrir menu' : 'Fechar menu');
  nav.classList.toggle('open', !isOpen);
});
nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  nav.classList.remove('open');
  menuToggle?.setAttribute('aria-expanded', 'false');
  menuToggle?.setAttribute('aria-label', 'Abrir menu');
}));

document.querySelectorAll('.carousel-arrow').forEach(button => {
  button.addEventListener('click', () => {
    const track = document.getElementById(button.dataset.carousel);
    const card = track?.querySelector(':scope > article:not([hidden])');
    if (!track || !card) return;
    const gap = parseFloat(getComputedStyle(track).columnGap) || 20;
    const direction = Number(button.dataset.direction);
    track.scrollBy({ left: direction * (card.getBoundingClientRect().width + gap), behavior: 'smooth' });
  });
});

const productTrack = document.getElementById('product-track');
document.querySelectorAll('.category').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.category').forEach(tab => {
      const selected = tab === button;
      tab.classList.toggle('active', selected);
      tab.setAttribute('aria-pressed', String(selected));
    });
    productTrack.querySelectorAll('.product-card').forEach(card => {
      card.hidden = button.dataset.filter !== 'todos' && card.dataset.category !== button.dataset.filter;
    });
    productTrack.scrollTo({ left: 0, behavior: 'smooth' });
  });
});

document.getElementById('year').textContent = new Date().getFullYear();
