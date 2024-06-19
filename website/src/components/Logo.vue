<template>
    <div class="logo-holder">
        <div class="logo">
            <p @click="scroll_to_card('utrecht-university')"> Thisis my logo</p>
        </div>
    </div>
</template>

<script>

export default {

    mounted() {
    window.addEventListener("scroll", this.onScroll)
    },
    beforeDestroy() {
    window.removeEventListener("scroll", this.onScroll)
    },
    methods: {
    onScroll(e) {
        this.windowTop = window.top.scrollY /* or: e.target.documentElement.scrollTop */
        if (this.windowTop > 900) {
            console.log("showing logo")
            document.querySelector(".logo-holder").style.visibility = "visible"
        } else {
            console.log("hiding logo")
            document.querySelector(".logo-holder").style.visibility = "hidden"
        }
    
    }

}
}

</script>


<style>
.logo-holder {
    display: flex;
    justify-content: flex-end;
    visibility: hidden;
}

.logo {
    height: 3vh;
    padding: 1.5em;
    position: fixed;
    top: 0;
    width: 100vw;
    z-index: 10;
    background-color: rgb(255, 255, 255);
    box-shadow: 0px 5px 5px gray;
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