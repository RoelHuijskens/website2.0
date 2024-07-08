<script setup lang="ts">
import LifeStage from './components/LifeStage.vue'
import AMA from './components/AMA.vue'
import Logo from './components/Logo.vue'
import Me from './components/Me.vue'
import Connector from './components/lifestage_info/timeline_Connecter.vue'


</script>

<template>
  <div class="app-holder">
  <Logo/>
  <AMA :image="'me.jpg'"/>
  <Me/>
  <div class="timeline-end"></div>
  <div class="timeline-background">
  <Connector position="start" text="2021-Now"></Connector>
  <LifeStage :title="'APG Asset Management'" :content="'I am currently working at APG Asset Management as a devops engineer in the Self Service & Data Science team. Here I support our business with data analytics tooling such as Posit, R, Python.'" :tag="'APG'" :index="1" />
  <Connector position="" text="2018-2020"></Connector>
  <LifeStage :title="'Utrecht University'" :content="'I have completed my Masters degree in Applied Statistics at the Utrecht University. Providing met with a strong data foundation and analytical skills, and completed my thesis at Statistics Netherlands.'" :tag="'UU'" :index="2" />
  <Connector position="" text="2015-2018"></Connector>
  <LifeStage :title="'Vrije Universiteit Amsterdam'" :content="'I did my bachelor studies in pyschology at the Vrije universiteit Amsterdam, I initially chose psychology due to my interest in neuroscience. Along the way i got hooked by statistics and programming. '" :tag="'VU'" :index="3" />
  <Connector position="end" text="1996-2015"></Connector>
  <div class="timeline-filler"></div>  
  </div>
  <div class="timeline-end"></div>
 </div>
</template>

<style>

* {
  font-family: 'Code Next', Verdana, sans-serif;
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

.timeline-background {
  background-color: #213547;
  width: 3px;
  margin: 0 auto;
  padding: 5rem 0;
  z-index: -14;
}

.timeline-end {
  border-width: 3px;
  border-radius: 50%;
  border-style: solid;
  border-color: #213547;
  width: 1.5rem;
  height: 1.5rem;
  margin: 0 auto;
}

.timeline-filler {
  height: 50vh;
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
  background: rgb(0,0,0,0)        /* color of the tracking area */
}

body::-webkit-scrollbar-thumb {
  background-color: black;    /* color of the scroll thumb */
  border-radius: 20px;       /* roundness of the scroll thumb */
  border: 3px solid white;  /* creates padding around scroll thumb */
}


div::-webkit-scrollbar {
  width: 15px;               /* width of the entire scrollbar */
}

div::-webkit-scrollbar-track {
  background: rgb(0,0,0,0)        /* color of the tracking area */
}

div::-webkit-scrollbar-thumb {
  background-color: black;    /* color of the scroll thumb */
  border-radius: 20px;       /* roundness of the scroll thumb */
  border: 3px solid white;  /* creates padding around scroll thumb */
}



</style>

