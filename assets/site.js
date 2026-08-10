
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
