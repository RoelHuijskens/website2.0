<script setup>
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faLinkedin } from '@fortawesome/free-brands-svg-icons'
import { faGithub } from '@fortawesome/free-brands-svg-icons'
import Logo from './Logo.vue'

library.add(faLinkedin, faGithub)
</script>



<template>
    <div class="top-banner">
        <span class = "banner-item" style="color:white">placholder</span>
        <span class = "banner-item">
            <Logo/>
        </span>
        <span class="links banner-item">
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
    background-color: #f8f8f8;
    top: 0;
    width: 100vw;
    box-shadow: 0px 5px 5px gray;
    z-index: 20;
    visibility: hidden;
    display: flex;
    justify-content: space-between;
    flex-direction: row;
}

.banner-item {
    width: 15rem;
}

.logo {
    height: 7rem;
    width: 7rem;
}

.links {
    top:0;
    right: 0;
    z-index:20;
    display: flex;
    justify-content: space-around;
    margin: 2rem 2.5rem 2rem 0;
    height:100%;
}

.link {
    transition: top ease 0.3s;
    position:relative;
    width:3rem;
    height:3rem;
    color: #213547;
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