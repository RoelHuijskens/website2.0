
<script setup>
import Header from './Header.vue'
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faChevronDown } from '@fortawesome/free-solid-svg-icons'
</script>
<script>
export default {
  data() {
   return{
      messages: []
   }
  },
  props:['image'],
  computed: {
    imgDivStyle() {
      const image_path = 'https://raw.githubusercontent.com/RoelHuijskens/Website2.0/master/website/src/assets/imgs/' + this.image
      return {
        backgroundImage: `url(${image_path})`,
        backgroundSize: 'cover', // Optional depending on your needs
        backgroundRepeat: 'no-repeat', // Optional depending on your needs
      }
    }
  },
  methods: {
    async addMessage(message, sender){
      this.messages.push({message: message, sender: sender})
      await new Promise(r => setTimeout(r, 1000));
      this.messages.push({message: {'questionText':'thinking...'}, sender: 'bot'})
      this.questionText = ''
      console.log(this.messages)
      const response = await axios.post(
        "http://127.0.0.1:8000/chat", 
        this.messages)
      this.messages.pop()
      this.messages.push(response.data)
    }
  },


}

</script>

<template>
  <div class="section-holder">
    <!-- <div v-bind:class="" :style="imgDivStyle"> -->
      <div v-bind:class="{'picture-holder': true}" :style="imgDivStyle">
        <div class="chat-holder">
         <div class="chat-stream">
           <div class="chat-messages" > 
            <div class="question-holder question-holder-left">
                <div class="chat-message bot-message" id="initial-message"><Header/></div>
            </div>
          <template v-for="message in messages">
               <div v-bind:class="{'question-holder':true, 'question-holder-left':message.sender=='bot', 'question-holder-right':message.sender=='user'}">
                <template v-if="message.sender=='bot'&&message.message.questionText=='thinking...'">
                  <div class="chat-message bot-message"><div class="thinking-animation" >.</div><div class="thinking-animation" style="animation-delay:0.1s">.</div><div class="thinking-animation" style="animation-delay:0.2s">.</div></div>
                </template>
                <template v-else>
                 <div v-bind:class="{'chat-message':true, 'bot-message':message.sender=='bot', 'user-message':message.sender=='user'}">{{ message.message.questionText }}</div>
                </template>
              </div> 
            </template>
            </div>
            <span id="input-holder"><input v-model="questionText" class="input-animation"  id="input-prompt"><button class="input-animation"  @click="addMessage( { questionText },'user')">submit</button></span>
          </div>
          <div id="more-info-holder">
      <FontAwesomeIcon :icon="faChevronDown" class="chevron-element"/>
      <FontAwesomeIcon :icon="faChevronDown" class="chevron-element"style="animation-delay:0.3s"/>
      <FontAwesomeIcon :icon="faChevronDown" class="chevron-element"style="animation-delay:0.6s"/>
    </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

@keyframes thinking {
  0%   {bottom: 0}
  50%  {bottom: 0.2rem}
  100% {bottom: 0}
}

.thinking-animation{
  position: relative;
  display: inline-block;
  animation-name: thinking;
  animation-duration: 0.5s;
  animation-iteration-count: infinite;
}

@keyframes fly-in-message-left{
  0%   {bottom: -15rem; left: -1rem}
  100% {bottom:0; left:0}
}

@keyframes fly-in-message-right{
  0%   {bottom: -15rem; right: -1rem; opacity:0.3}
  100% {bottom:0; right:0; opacity: 1;}
}


.question-holder{
    padding: 0.5rem 4rem;
    display: flex;
}

.question-holder-left{
  justify-content: flex-start;
}
.question-holder-right{
  justify-content: flex-end;
}

.chat-holder{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  background-color: rgba(0,0,0,0.2);
  flex-direction: column;
  font-family: monospace;
  font-size: 1.2rem;
}
.chat-messages{
    width: 100%;
    height: 80%;
    padding: 10px;
    overflow-y: auto;
}
.chat-message{
    padding: 0.8rem 2rem;
    line-height: 20px;
    color: #24292e;
    opacity: 0.8;
    vertical-align: middle;
    background-color: #ffffff;
    background-repeat: no-repeat;
    background-position: right 8px center;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    outline: none;
    box-shadow: rgba(50, 50, 93, 0.25) 0px 13px 27px -5px, rgba(0, 0, 0, 0.3) 0px 8px 16px -8px;
    min-width: 10rem;
    max-width: 30rem;
    animation-duration: 1s;
    position:relative;
    
}

.user-message{
  background-color: gray;
  animation-name: fly-in-message-left;
  border-color: gray;
  color:white;
}
.bot-message{
  background-color: white;
  animation-name: fly-in-message-right;
}
.chat-stream{
  width: 80%;
  height: 80%;
  background-color:rgba(1,1,1,0.3);
  border-radius: 10px;
  box-shadow: rgb(38, 57, 77) 0px 20px 30px -10px;
  position:relative;
}

#input-prompt{
    padding: 0.5rem 2rem;
    margin: 0 0.5rem;
    font-size: 14px;
    line-height: 20px;
    color: #24292e;
    vertical-align: middle;
    background-color: #ffffff;
    background-repeat: no-repeat;
    background-position: right 8px center;
    border-radius: 6px;
    outline: none;
    width: 60%;
    max-width: 45rem;
    min-width: 18rem;
    
    :focus{
        border-color: #0366d6;
        outline: none;
        box-shadow: rgba(3, 102, 214, 0.3) 0px 0px 0px 3px;
    }
}

.input-animation{
 animation-name: prompt-animation;
 animation-duration:9s;
 border-width:0;
}

@keyframes prompt-animation{
  0% { background-color: rgba(255,255,255,0);color: rgba(0,0,0,0)}
  90% { background-color: rgba(255,255,255,0);color: rgba(0,0,0,0)}
  100% { background-color: rgba(255,255,255,1); color: rgba(0,0,0,1)}

}


#input-holder{
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 20%;

}

#more-info-holder{
  padding: 1.5rem 0;
  display: flex;
  flex-direction: column;
  font-size:0.7rem;
  color: white;
  height: 3rem;
}

.chevron-element{
  animation-name: chevron-animation;
  animation-duration: 1.5s;
  animation-iteration-count: infinite;
}

@keyframes chevron-animation{
  0% {font-size: 0.7rem}
  50% {font-size: 0.9rem}
  100% {font-size: 0.7rem}
}

.blocked{
  pointer-events: none;
  opacity: 0.5;
}

.section-holder{
  width:100%;
}
.picture-holder{
  background-size:cover;
  background-position: center;
  width:100%;
  height:100vh;
  min-height: 500px;
}


#initial-message{
  background-color: rgba(255,255,255,1);
  border-width:0;
  color:black;
  box-shadow: rgba(225, 228, 232, 0.2) 0px 1px 0px 0px inset;
  position: relative;
  bottom: 0;
  margin: 0 0;
  width: 100%;
  font-size: 1rem;
  height: 3.5rem;
  animation-name: initial-message-animation;
  animation-duration: 8s;
}

@keyframes initial-message-animation{
  0% {
    background-color: rgba(0,0,0,0);
    color:white;
    box-shadow: 0 0 0;
    bottom: -30vh;
    margin: 0 20vw;
  }
  90% {
    background-color: rgba(0,0,0,0);
    color:white;
    box-shadow: 0 0 0;
    bottom: -30vh;
    margin: 0 20vw;
  }
  100% {
    background-color: rgba(255,255,255,1);
    color:black;
    box-shadow: rgba(225, 228, 232, 0.2) 0px 1px 0px 0px inset;
    bottom: 0;
    margin: 0 0;
  }
}

</style>
