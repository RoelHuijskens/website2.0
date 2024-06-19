<template>
    <div  @click="scroll_to_card('my-info-holder')" class="header">
        <p class="typing-text">{{ typedText }}</p><span id="prompt-cursor"></span>
    </div>
</template>

<script>
export default {
    data() {
        return {
            typedText: "",
            fullText: "Roel Huijskens, software, devops and data engineer. Ask me anything or click here for more info about me.",
            typingSpeed: 70, // Adjust the typing speed (in milliseconds) here
        };
    },
    mounted() {
        this.startTypingAnimation();
    },
    methods: {
        async startTypingAnimation() {
            await this.delay()
            let currentIndex = 0;
            const typingInterval = setInterval(() => {
                this.typedText += this.fullText[currentIndex];
                currentIndex++;
                if (currentIndex === this.fullText.length) {
                    clearInterval(typingInterval);
                }
            }, this.typingSpeed);
        },
        delay() {
            console.log("delaying this bitch")
            return new Promise((resolve) => setTimeout(resolve, 2000));
        },



        scroll_to_card(id) {
        console.log("Scrolling to card with label:", id)
        // Assuming each life stage element has an id corresponding to its label
        const elementId = `#${id}`;
        const element = document.querySelector(elementId);

        if (element) {
        // Scroll to the element
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }


}



    },
};
</script>

<style>
.header {
    display: flex;
    align-items: center;
    justify-content: left;
    font-family: monospace;

}

@keyframes blinking{
    0%{opacity: 0;}
    50%{opacity: 1;}
    100%{opacity: 0;}
    
}


#prompt-start {
    margin: 0 0.3rem;
    
}

#prompt-cursor {
  margin: 0 0 0 0.3rem;
  width: 0.4rem;
  height:1rem;
  background-color: white;
  animation: blinking 1s 5;
  opacity: 0;
}
.typing-text {
    animation: typing-animation 1s steps(40, end);
    font-size: 1.2rem;
}

@keyframes typing-animation {
    from {
        width: 0;
    }
}
</style>