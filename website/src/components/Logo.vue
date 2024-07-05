<script setup>
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faLinkedin } from '@fortawesome/free-brands-svg-icons'
import { faGithub } from '@fortawesome/free-brands-svg-icons'

library.add(faLinkedin, faGithub)
</script>



<template>
    <div class="top-banner">
        <span class="logo">
            <p @click="scroll_to_card('utrecht-university')"> Thisis my logo</p>
        </span>
        <span class="links">
            <a href="https://www.linkedin.com/in/roel-huijskens/"><font-awesome-icon class="link" icon="fa-brands fa-linkedin" /></a>
            <a href="https://github.com/RoelHuijskens"><font-awesome-icon class="link" icon="fa-brands fa-github" /></a>
        </span>
        
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
            document.querySelector(".top-banner").style.visibility = "visible"
        } else {
            console.log("hiding logo")
            document.querySelector(".top-banner").style.visibility = "hidden"
        }
    
    }

}
}

</script>


<style>
.top-banner {
    position: fixed;
    background-color: rgb(255, 255, 255);
    top: 0;
    width: 100vw;
    box-shadow: 0px 5px 5px gray;
    z-index: 10;

}

.logo {
    padding: 1.5rem;
    transition: 0.3s;
}

.links {
    position:fixed;
    top:0;
    right: 0;
    z-index:20;
    width: 10rem;
    display: flex;
    justify-content: space-around;
    padding: 1.5rem;

}

.link {
    transition: top ease 0.3s;
    position:relative;
    width:2rem;
    height:2rem;
}

.link:hover {
    top:-0.2rem;
}

.logo:hover {
    width: 100%;
}

@keyframes top-banner-fade-in {
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