let mainPosts = document.querySelectorAll(".main-post");
let posts = document.querySelectorAll(".post");

let i = 0;
let postIndex = 0;
let currentPost = posts[postIndex];
let currentMainPost = mainPosts[postIndex];

let progressInterval = setInterval(progress, 100); // 180

function progress() {
  if (i === 100) {
    i = -5;
    // reset progress bar
    currentPost.querySelector(".progress-bar__fill").style.width = 0;
    document.querySelector(
      ".progress-bar--primary .progress-bar__fill"
    ).style.width = 0;
    currentPost.classList.remove("post--active");

    postIndex++;

    currentMainPost.classList.add("main-post--not-active");
    currentMainPost.classList.remove("main-post--active");

    // reset postIndex to loop over the slides again
    if (postIndex === posts.length) {
      postIndex = 0;
    }

    currentPost = posts[postIndex];
    currentMainPost = mainPosts[postIndex];
  } else {
    i++;
    currentPost.querySelector(".progress-bar__fill").style.width = `${i}%`;
    document.querySelector(
      ".progress-bar--primary .progress-bar__fill"
    ).style.width = `${i}%`;
    currentPost.classList.add("post--active");

    currentMainPost.classList.add("main-post--active");
    currentMainPost.classList.remove("main-post--not-active");
  }
}
const navToggle = document.querySelector(".nav-menu_toggle"),
      navMenu = document.querySelector(".nav_menu"),
      navClose = document.querySelector(".nav-menu_close");



if(navToggle){
    navToggle.addEventListener("click", () => {
        navMenu.classList.add("show-menu")
    })
}

if(navClose){
    navClose.addEventListener("click", () => {
        navMenu.classList.remove("show-menu")
    })
}


// HEADER RIGHT

const rightHeader = document.querySelector(".right_header-toggle"),
      headerRightMenu = document.querySelector(".header-right"),
      rightClose = document.querySelector(".header-right_close");


if(rightHeader){
    rightHeader.addEventListener("click", () => {
        headerRightMenu.classList.add("show-right_menu")
    })
}

if(rightClose){
    rightClose.addEventListener("click", () => {
        headerRightMenu.classList.remove("show-right_menu")
    })
}

// SLIDER

// BACK TOP BTN

const backTopbtn = document.querySelector(".back-top-btn");

const showElemOnScroll = function (){
    if(window.scrollY > 150){
        backTopbtn.classList.add("active");
    }
    else{
        backTopbtn.classList.remove("active")
    }
}

window.addEventListener("scroll", showElemOnScroll);

 
