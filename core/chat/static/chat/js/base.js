

const switcher = document.getElementById('flexSwitchCheckDefault');
switcher.addEventListener('change', validate, false);
const navbar = document.getElementById('navbar')
const moon = document.getElementById('moon')
const offcanvas = document.getElementById('offcanvasNavbar')
const usernameLink = document.getElementById('usernameLink')



function validate() {
  let checked = switcher.checked;
  if (checked) {
    localStorage.dark = true;
    darkMode();
  }

  else {
    delete localStorage.dark;
    lightMode();
  }
}

function darkMode() {
  var element = document.body;
  element.className = "dark-mode";
  navbar.classList.remove('bg-light');
  navbar.classList.add('bg-dark');
  navbar.classList.add('navbar-dark');
  moon.style.color = 'white';
  offcanvas.classList.add('text-bg-dark');
  usernameLink.className = 'text-white';
}

function lightMode() {
  var element = document.body;
  element.className = "light-mode";
  navbar.classList.remove('bg-dark');
  navbar.classList.add('bg-light');
  navbar.classList.remove('navbar-dark');
  moon.style.color = 'black';
  offcanvas.classList.remove('text-bg-dark');
  usernameLink.className = 'text-black';

}

if (localStorage.dark) {
  switcher.checked = true;
  darkMode();
}