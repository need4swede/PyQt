
// HOME SCROLL ANIMATION
if (window.screen.width > 425){ // != MOBILE
  // INITIALIZE SCROLL DIRECTION
  let up = 0; let down = 0;
  // ON SCROLL...
  window.addEventListener('wheel', function(event)
  {
    // GET ELEMENTS
    let demoImages = document.querySelectorAll(".fadeup")
    let mouse = document.querySelector(".scroll-down");
  if (event.deltaY < 0) // ON UP SCROLLS
  {
    up +=1;
    down = 0;
    if (up === 1){
      // REVEAL SCROLL ANIMATION AND HIDE IMAGES
      demoImages.forEach(el => {
        el.classList.remove("active");
      })
      mouse.classList.add("fadeIn");
      mouse.classList.remove("fadeOut");
    }
    return
  }
  else if (event.deltaY > 0) // ON DOWN SCROLLS
  {
    down +=1
    up = 0;
    if (down === 1){
      // HIDE SCROLL ANIMATION AND REVEAL IMAGES
      demoImages.forEach(el => {
        el.classList.add("active");
      })
      mouse.classList.add("fadeOut");
      mouse.classList.remove("fadeIn");
    }
    return
  }});
} else { // MOBILE
  function reveal() {
    // COLLECT ELEMENTS TO FADE UP
    let reveals = document.querySelectorAll(".fadeup");
    for (let i = 0; i < reveals.length; i++) {
      // WINDOW PROPERTIES
      let windowHeight = window.innerHeight;
      let elementTop = reveals[i].getBoundingClientRect().top;
      let elementVisible = 150;
      // REVEAL ELEMENTS ON SCROLL DOWN
      if (elementTop < windowHeight - elementVisible) {
        reveals[i].classList.add("active");
      } else { // HIDE ELEMENTS ON SCROLL UP
        reveals[i].classList.remove("active");
      }
    }
  }
  window.addEventListener("scroll", reveal);
}

// HOME DOWNLOAD BUTTON
function addBokeh() {
	document.getElementById("bokeh").className = "blur";
	document.getElementById("canvas").className = "blur-less";
	document.getElementById("modal").className = "visible";
};
function removeBokeh() {
	document.getElementById("bokeh").className = document.getElementById("bokeh").className.replace(/(?:^|\s)blur(?!\S)/g , '');
	document.getElementById("canvas").className = document.getElementById("canvas").className.replace(/(?:^|\s)blur-less(?!\S)/g , '');
	document.getElementById("modal").className = document.getElementById("modal").className.replace(/(?:^|\s)visible(?!\S)/g , '');
};
document.getElementById("launch").addEventListener( 'click' , addBokeh );
document.getElementById("modal").addEventListener( 'click' , removeBokeh );

// LISTENS FOR KEY PRESSES
document.addEventListener('keydown', function (event) {
	
})

// CONSOLE MESSAGE
console.log('%cWelcome to Rename!\nIf you have any questions, please reach out', 'color:cyan;');
console.log(`%cView my portfolion: \nhttps://www.mafshari.work`, 'color:lightgreen;');