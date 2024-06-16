<template>
    <div class="header">
        <p class="typing-text">{{ typedText }}</p><span id="prompt-cursor"></span>
    </div>
</template>

<script>
export default {
    data() {
        return {
            typedText: "",
            fullText: "Roel Huijskens, software, devops and data engineer... ask me anything.",
            typingSpeed: 100, // Adjust the typing speed (in milliseconds) here
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