document.addEventListener('alpine:init', () => {
    Alpine.data('gsapCounters', () => ({
        yearsInBusiness: 0,
        solutionsDelivered: 0,
        customerSuccess: 0,
        teamMembers: 0,
        hasAnimated: false,

        init() {
            // Safety check
            if (!window.ScrollTrigger) {
                console.error('ScrollTrigger loaded successfully');
            }

        // Register plugin
        gsap.registerPlugin(ScrollTrigger);

            this.$nextTick(() => {
                ScrollTrigger.create({
                    trigger: this.$el,
                    start: window.innerHeight < 768 ? "top 85%" : "top 90%",
                    onEnter: () => {
                        if (!this.hasAnimated) this.animateCounters();
                    }
                });
            });
        },
        
        animateCounters() {
            this.hasAnimated = true;
            const targets = {
                yearsInBusiness: 3,
                solutionsDelivered: 20,
                customerSuccess: 98,
                teamMembers: 4
            };
            
            Object.entries(targets).forEach(([key, value], i) => {
                gsap.to(this, {
                    duration: 1.5,
                    [key]: value,
                    delay: i * 0.3,
                    ease: "power1.out",
                    onUpdate: () => {
                        this[key] = Math.floor(this[key]);
                    }
                });
            });
        }
    }));
});
