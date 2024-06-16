<template>
    <div class="logo-holder">
        <div class="logo">
            <p @click="scroll_to_card('utrecht-university')"> Thisis my logo</p>
        </div>
    </div>
</template>

<script>
    export default {

    methods: {
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
    }
}
</script>


<style>
.logo-holder {
    display: flex;
    justify-content: center;
}

.logo {
    height: 3vh;
    padding: 1.5em;
    position: fixed;
    top: 0;
    width: 20vw;
    z-index: 10;
    background-color: rgb(255, 255, 255);
    box-shadow: 0px 5px 5px gray;
    border-radius: 0 0 12px 12px;
    transition: 0.3s;
    animation: logo-holder-fade-in 9s;
}

.logo:hover {
    width: 100%;
}

@keyframes logo-holder-fade-in {
    0% {
        opacity: 0;
        box-shadow: 0 0 0 0;
    }

    97% {
        opacity: 0;
        box-shadow: 0 0 0 0;
    }
    100% {
        opacity: 1;
        box-shadow: 0px 5px 5px gray;
    }
}

</style>