<script setup lang="ts">
import LifeStage from './components/LifeStage.vue'
import AMA from './components/AMA.vue'
import Logo from './components/Logo.vue'




</script>

<template>
  <div class="app-holder">
  <Logo/>
  <AMA :image="'me.jpg'"/>
  <LifeStage :title="'APG AM'" :content="'I am currently working at APG Asset Management as a devops engineer in the Self Service & Data Science team. Here i support our business with data analytics tooling such as Posit, R, Python.'" :image="'apg.jpg'" :index="1" />
  <LifeStage :title="'Utrecht University'" :content="'I have completed my Masters degree in Applied Statistics at the Utrecht University. Providing met with a strong data foundation and analytical skills, and completed my thesis at Statistics Netherlands.'" :image="'UU.jpg'" :index="2" />
  <LifeStage :title="'Vrije Universiteit Amsterdam'" :content="'I did my bachelor studies in pyschology at the Vrije universiteit Amsterdam, I initially chose psychology due to my interest in neuroscience. Along the way i got hooked by statistics and programming. '" :image="'VU.jpg'" :index="3" />
 </div>
</template>

<style>

* {
  font-family: 'Roboto', Times, sans-serif;
}

#app {
    margin: 0 0;
    padding:0 0;
}
.app-holder{
  left:0;
  top:0;
  position:absolute;
  width:99.35vw;
  height:100vh;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
#padding{
  height: 100vh;
}


body::-webkit-scrollbar {
  width: 15px;               /* width of the entire scrollbar */
}

body::-webkit-scrollbar-track {
  background: light-grey;        /* color of the tracking area */
}

body::-webkit-scrollbar-thumb {
  background-color: black;    /* color of the scroll thumb */
  border-radius: 20px;       /* roundness of the scroll thumb */
  border: 3px solid white;  /* creates padding around scroll thumb */
}

</style>

