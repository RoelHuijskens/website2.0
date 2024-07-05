<script setup>  
import { ref } from 'vue';
import APG from './lifestage_info/APG.vue'
import UU from './lifestage_info/UU.vue'
import VU from './lifestage_info/VU.vue'


const infoText = {
  APG,
  UU,
  VU
}


</script>

<script>
export default {
  props:['title','content','tag', 'index'],
  data(){
    return {
      id: this.translate_name_to_id(this.title),
      full_view: false,
      tag: this.tag.toLowerCase(),
      full_view_component: ref(this.tag)
    }
  },
  computed: {
    allign_content_left() {
      return this.index%2 == 0 
    },
    imgDivStyle() {
      const image_path = 'https://raw.githubusercontent.com/RoelHuijskens/Website2.0/master/website/src/assets/imgs/' + this.tag + '.jpg'
      return {
        backgroundImage: `url(${image_path})`,
      }
    }
  },
  methods: {
    translate_name_to_id(name) {
      return name.toLowerCase().replace(/\s/g, "-");
    },
    set_full_view() {
      console.log("Setting full view")
      this.full_view = !this.full_view;
  },
}
}

</script>

<template>
  <div class="life-section-holder" @click="set_full_view" :class="{ section_holder_full_view: full_view }" >
    <!-- <div v-bind:class="" :style="imgDivStyle"> -->
      <div v-bind:class="{'life-picture-holder': true}" :style="imgDivStyle">
        <div v-bind:class="{'card-holder':true, 'card-holder-left':allign_content_left, 'card-holder-right':!allign_content_left}">
      <div class="card-format">
        <div class="title-card-holder">
          <h2 style="max-width:20rem">{{title}}</h2>
          </div>
        <p >{{content}}</p><u>More</u>
      </div>
    </div>
  </div>
  </div>
  <div v-if="full_view" @click="set_full_view" class="life-section-holder-full-view">
    <div class='life-picture-holder-full-view' :style="imgDivStyle">
      <component v-bind:is="infoText[full_view_component]"/>
      <p>{{ infoText[tag] }}</p>
    </div>
  </div>
  
</template>

<style>
.card-format{
  width:40%;
  height:120%;
  background-color: white;
  box-shadow: rgb(38, 57, 77) 0px 20px 30px -10px;
  border-radius: 10px;
  padding: 2rem 2rem;
  position: relative;
  text-align: left;
  opacity: 0.95;
}



.card-holder-left{
  justify-content: flex-start;
}
.card-holder-right{
  justify-content: flex-end;
}

.card-holder-full-view{
  padding: 6rem 4rem;
  justify-content: center;
}

.card-holder{
  padding: 5rem 6rem;
  display: flex;
  min-width: 40rem;
}


.life-section-holder{
  width: 100%;
  display: flex;
  justify-content: center;
  position: relative;
  font-size: 1rem;
}

.life-section-holder-full-view{
  width: 100vw;
  height: 100vh;
  justify-content: center;
  padding: 3rem 0;
  position: fixed;
  left:0;
  top:0;
  z-index: 100;
  background-color: rgb(0,0,0,0.6);
  animation: full-view-apperance 0.5s;
}

@keyframes full-view-apperance {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
} 

#card-initial{
  margin-top: 0;
}

.card-appear{
  animation-name: full-view-card-appereance;
  margin-top: -10rem;
}

@keyframes full-view-card-appereance {
  0% {
    opacity: 0;
    transform: translateY(100%);
  }

  40% {
    opacity: 0;
    transform: translateY(100%);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}



.life-section-holder-full-view-disabled{
  visibility: hidden;
  width: 0;
  height: 0;
  z-index: -100;
}

.life-picture-holder{
  background-attachment: fixed;
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
  width:60vw;
  height:75vh;
  min-height: 500px;
  margin: -3rem auto;
  border-radius: 9px;
  box-shadow: rgba(50, 50, 93, 0.25) 0px 13px 27px -5px, rgba(0, 0, 0, 0.3) 0px 8px 16px -8px;
  max-width:80rem;
  min-width: 60rem;
  max-height: 50rem;
  position: relative;
  top: 0;
  transition: top ease 0.3s;
}


.life-picture-holder:hover {
  top: -1rem;
}


.life-picture-holder-full-view{
  width: 80%;
  height: 75%;
  margin: auto;
  border-radius: 9px;
  box-shadow: rgba(50, 50, 93, 0.25) 0px 13px 27px -5px, rgba(0, 0, 0, 0.3) 0px 8px 16px -8px;
  overflow-y: scroll;
  padding: 4rem 0;
  background-size: cover;
}

.title-card-holder{
  text-align: center;
  font-size: 1.2rem;
}

.title-card-holder-full{
  text-align: center;
}

</style>
