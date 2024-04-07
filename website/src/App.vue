<script setup lang="ts">
import LifeStage from './components/LifeStage.vue'
import AMA from './components/AMA.vue'
</script>

<template>
  <div class="app-holder">
  <Header/>
  <AMA :image="'me.jpg'"/>
  <LifeStage :title="'APG AM'" :content="'Time At APG Asset Management.'" :image="'apg.jpg'" :index="1" />
  <LifeStage :title="'Utrecht University'" :content="'Time At the UU'" :image="'UU.jpg'" :index="2" />
  <LifeStage :title="'Vrije Universiteit Amsterdam'" :content="'Time At the vu.'" :image="'VU.jpg'" :index="3" />
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
  width:100%;
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




</style>
