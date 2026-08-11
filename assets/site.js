const menu = document.querySelector('.menu');
const nav = document.querySelector('.main-nav');
if(menu && nav){
  menu.addEventListener('click',()=>{
    nav.classList.toggle('open');
    menu.setAttribute('aria-expanded', nav.classList.contains('open') ? 'true' : 'false');
  });
}

const year = document.querySelector('[data-current-year]');
if(year) year.textContent = new Date().getFullYear();

// Legacy static articles used a text-only organizational byline.
// Link it to the publication author page without altering named-author bylines.
document.querySelectorAll('.byline span:first-child').forEach((node)=>{
  if(node.querySelector('a')) return;
  const text = node.textContent.trim();
  if(text === 'By Pickleball Cosmos Editorial'){
    node.innerHTML = 'By <a class="source-link" href="/editorial/">Pickleball Cosmos Editorial</a>';
  }
});
