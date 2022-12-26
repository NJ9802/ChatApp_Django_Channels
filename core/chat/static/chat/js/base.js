
// Index
const switcher = document.getElementById('flexSwitchCheckDefault');
switcher.addEventListener('change', validate, false);
const navbar = document.getElementById('navbar');
const moon = document.getElementById('moon');
const offcanvas = document.getElementById('offcanvasNavbar');
const searchModal = document.getElementById('search-modal');
const dropdownOptionsNavbar = document.getElementById('dropdown-options-navbar');
let navTabs = document.getElementById('nav-tabs');
let chatLink = document.getElementById('chat-link');
let groupLink = document.getElementById('group-link');

// Chat
let dropdownOptions = document.getElementById('dropdown-options');
let profileInfoModal = document.getElementById('profile-info-modal');
let backgroundModal = document.getElementById('background-modal');
let wallpaperInput = document.getElementById('wallpaper');

let fixedChatDiv = document.getElementById('fixed-div');
let backLink = document.getElementById('back-link');
let profileInfoButton = document.getElementById('profile-info-button');

// Contacts
let newGroupLink = document.getElementById('new-group-link');

// New Group
let groupNameInput = document.getElementById('id_name');
let contactsList = document.querySelectorAll('[id=contacts-list]');



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
  navbar.classList.add('bg-dark', 'navbar-dark');
  moon.style.color = 'white';
  offcanvas.classList.add('text-bg-dark');
  searchModal.classList.add('bg-dark');
  dropdownOptionsNavbar.classList.add('dropdown-menu-dark');
  navTabs.classList.remove('bg-light');
  navTabs.classList.add('bg-dark');
  chatLink.classList.remove('text-black');
  chatLink.classList.add('text-white');
  groupLink.classList.remove('text-black');
  groupLink.classList.add('text-white');

  dropdownOptions.classList.add('dropdown-menu-dark');
  profileInfoModal.classList.add('bg-dark');
  backgroundModal.classList.add('bg-dark');
  wallpaperInput.classList.add('bg-dark', 'text-white');
  fixedChatDiv.classList.remove('bg-light');
  fixedChatDiv.classList.add('bg-dark');
  backLink.classList.remove('text-black');
  backLink.classList.add('text-white');
  profileInfoButton.style.color = 'white';
  newGroupLink.style.color = 'white';
  groupNameInput.classList.add('bg-dark', 'text-white', 'border-0');
  for (let i = 0; i < contactsList.length; i++) {
    contactsList[i].classList.add('bg-dark', 'text-white');
  };





}

function lightMode() {
  var element = document.body;
  element.className = "light-mode";
  navbar.classList.remove('bg-dark', 'navbar-dark');
  navbar.classList.add('bg-light');
  moon.style.color = 'black';
  offcanvas.classList.remove('text-bg-dark');
  searchModal.classList.remove('bg-dark');
  dropdownOptionsNavbar.classList.remove('dropdown-menu-dark');
  navTabs.classList.remove('bg-dark');
  navTabs.classList.add('bg-light');
  chatLink.classList.remove('text-white');
  chatLink.classList.add('text-dark');
  groupLink.classList.remove('text-white');
  groupLink.classList.add('text-dark');


  // dropdownOptions.classList.remove('dropdown-menu-dark');
  // profileInfoModal.classList.remove('bg-dark');
  // fixedChatDiv.classList.remove('bg-dark');
  // fixedChatDiv.classList.add('bg-light');
  // backLink.classList.remove('text-white');
  // backLink.classList.add('text-black');
  // profileInfoButton.style.color = 'black';
  // newGroupLink.style.color = 'black';
  // groupNameInput.classList.remove('bg-dark');
  // groupNameInput.classList.remove('text-white');



};

if (localStorage.dark) {
  switcher.checked = true;
  darkMode();
};

let contactsUl = document.getElementById('contacts-ul');
contactsUl.addEventListener('click', check, false);
let contactsInput = document.querySelectorAll('.contact-input');

function check() {
  let totalUsers = JSON.parse(document.getElementById('total-users').textContent);

  let participantsDiv = document.getElementById('participants');
  let count = 0;
  for (let i = 0; i < contactsInput.length; i++) {
    if (contactsInput[i].checked === true) {
      count = count + 1;
    };
  };

  if (count === 0) {
    participantsDiv.innerHTML = 'Add participants';
  }

  else {
    participantsDiv.innerHTML = count + ' of ' + totalUsers + ' participants';
  };
};