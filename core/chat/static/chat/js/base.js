

const switcher = document.getElementById('flexSwitchCheckDefault');
switcher.addEventListener('change', validate, false);

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
}

function lightMode() {
var element = document.body;
element.className = "light-mode";

}

if (localStorage.dark) {
  switcher.checked = true;
  darkMode();
}