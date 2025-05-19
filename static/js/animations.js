// No imports needed

// GSAP animation
const fadeIn = (solutioncard, delay = 0) => {
    gsap.from(solutioncard, { 
        opacity: 0,
        y: 20, 
        duration: 0.8,
        delay,
        ease: "power2.out",
    }); // gsap is global
};

window.fadeIn = fadeIn;

