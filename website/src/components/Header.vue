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
            fullText: "Roel Huijskens, software, devops and data engineer... Ask me anyting.",
            typingSpeed: 100, // Adjust the typing speed (in milliseconds) here
        };
    },
    mounted() {
        this.startTypingAnimation();
    },
    methods: {
        startTypingAnimation() {
            let currentIndex = 0;
            const typingInterval = setInterval(() => {
                this.typedText += this.fullText[currentIndex];
                currentIndex++;
                if (currentIndex === this.fullText.length) {
                    clearInterval(typingInterval);
                }
            }, this.typingSpeed);
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
  animation: blinking 1s infinite;
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