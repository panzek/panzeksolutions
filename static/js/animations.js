import Alpine from 'alpinejs';
import { gsap } from 'gsap';

window.Alpine = Alpine;
Alpine.start();

// Example GSAP animation

const fadeIn = (solutioncard, delay = 0) => {
    gsap.from(solutioncard, { 
        opacity: 0,
        y: 20, 
        duration: 0.8,
        delay,
        ease: "power2.out",
    });
};

window.fadeIn = fadeIn;

