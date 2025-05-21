document.addEventListener("alpine:init", () => {
    Alpine.data("gsapCounters", () => ({
        yearsInBusiness: 0,
        solutionsDelivered: 0,
        teamMembers: 0,

        animateCounters() {
            gsap.to(this, {
                duration: 2,
                yearsInBusiness: 4,
                solutionsDelivered: 30,
                teamMembers: 4,
                ease: "power1.out",
                onUpdate: () => {
                    this.yearsInBusiness = Math.floor(this.yearsInBusiness);
                    this.solutionsDelivered = Math.floor(this.solutionsDelivered);
                    this.teamMembers = Math.floor(this.teamMembers);
                }
            });
        }
    }));
});