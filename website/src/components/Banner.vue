<script setup>
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faLinkedin } from '@fortawesome/free-brands-svg-icons'
import { faGithub } from '@fortawesome/free-brands-svg-icons'
import Logo from './Logo.vue'

library.add(faLinkedin, faGithub)
</script>


<script>

export default {

    data () {
        return {
            privacy: "",
            privacy_placholder: "Privacy",
            privacy_text: "All questions are sent to the OpenAI API as asked. Questions are visible to me for helping me curate my knowledge base. I do not store any ip information or any other user information not provided in the questions.",
            run_animation: false
        }
    },

    mounted() {
    this.run_animation = false
    this.privacy = this.privacy_placholder
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
            this.run_animation = true
        } else {
            console.log("hiding logo")
            document.querySelector(".top-banner").style.visibility = "hidden"
            this.run_animation = false
        }
    
    },
    seePrivacy() {
        if (this.privacy == this.privacy_placholder){
            this.privacy = this.privacy_text
        } else {
            this.privacy = this.privacy_placholder
        }
    }

}
}

</script>


<template>
    <div class="top-banner">
        <span class = "banner-item" style="color:white">placholder</span>
        <span class = "banner-item">
            <Logo :run_animation="run_animation"/>
        </span>
        <span class="links banner-item">
            <a href="https://www.linkedin.com/in/roel-huijskens/"><font-awesome-icon class="link" icon="fa-brands fa-linkedin" /></a>
            <a href="https://github.com/RoelHuijskens"><font-awesome-icon class="link" icon="fa-brands fa-github" /></a>
            <a href="https://github.com/RoelHuijskens/website2.0/blob/master/website/src/assets/docs/Resume_eng.pdf"><b class="link">CV</b></a>
        </span>
        
    </div>
    <div @click="seePrivacy" class="top-banner-chat">
        <div class="chat-disclaimer">
            <p>{{ privacy }}</p>
        </div>
    </div>
</template>




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
    margin: 3rem 2.5rem 2rem 0;
    height:100%;
}

.link {
    transition: top ease 0.3s;
    position:relative;
    width:2rem;
    height:2rem;
    color: #213547;
    font-size: 1.5rem;
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



.top-banner-chat {
    font-size: 0.8rem;
    position: fixed;
    bottom: 0;
    width: 100%;
    display: flex;
    justify-content: flex-end;
    z-index: 100;
    visibility: visible;
}

.chat-disclaimer {
    background-color: rgb(248,248,248,1);
    padding: 0 1.5rem;
    border-radius: 20px 20px 0 0;
    box-shadow: 0px 5px 8px black;
    max-width: 20rem;
    margin: 0 3rem;
}

</style>