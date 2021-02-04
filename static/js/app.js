const burger = document.querySelector(".hamburger");
let nav = document.querySelector(".nav-links");
let cancel = document.querySelector(".cancel");
let navShow = document.querySelector(".nav-show");
let navCircle = document.querySelector(".nav-circle");
let navBar = document.querySelector("header");


if (window.outerWidth > 768) {
  window.addEventListener("scroll", function () {
    if (window.pageYOffset > 70) {
      navBar.classList.add("nav");
    } else {
      navBar.classList.remove("nav");
    }
  });
}


burger.onclick = () => {
  nav.classList.toggle("nav-mobile");
  cancel.classList.toggle("cancel-view");
  navShow.classList.toggle("cancel");
};

navCircle.onclick = () => {
  navCircle.classList.toggle("active");
};
