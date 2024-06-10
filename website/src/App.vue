<script setup lang="ts">
import LifeStage from './components/LifeStage.vue'
import AMA from './components/AMA.vue'





</script>

<template>
  <div class="app-holder">
  <Header/>
  <AMA :image="'me.jpg'"/>
  <div id="padding"/>
  <LifeStage :title="'APG AM'" :content="'I am currently working at APG Asset Management as a devops engineer in the Self Service & Data Science team. Here i support our business with data analytics tooling such as posit, R, Python.'" :image="'apg.jpg'" :index="1" />
  <LifeStage :title="'Utrecht University'" :content="'I have completed my Masters degree in Applied Statistics at the Utrecht University. Providing met with a strong data foundation and analytical skills, and completed my thesis at Statistics Netherlands.'" :image="'UU.jpg'" :index="2" />
  <LifeStage :title="'Vrije Universiteit Amsterdam'" :content="'I did my bachelor studies in pyschology at the Vrije universiteit Amsterdam, i initially chose psychology due to my interest in neuro science. Along the way i got hooked by statistics and programming. '" :image="'VU.jpg'" :index="3" />
 </div>
</template>

<style scoped>

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
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
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

</style>

