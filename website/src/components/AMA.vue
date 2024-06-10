
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
      <div class="video-background">
      <iframe id="ytplayer" class="picture-holder" type="text/html" width="720" height="405" src="https://www.youtube.com/embed/mqf8SdcFo9s?autoplay=1&controls=0&disablekb=1&fs=0&loop=1&modestbranding=1&mute=1&iv_load_policy=3&playlist=mqf8SdcFo9s" frameborder="0">
        </iframe></div>
        <div class="video-background">
        <div class="chat-holder">
         <div class="chat-stream">
           <div class="chat-messages" > 
            <div class="question-holder question-holder-left">
              <div id="initial-message-holder">
              <img id="profile-picture-icon-initial" src="https://raw.githubusercontent.com/RoelHuijskens/Website2.0/master/website/src/assets/imgs/me.jpg">
              <div class="header"></div> <div class="chat-message bot-message" id="initial-message">
                <img id="profile-picture-portrait" src="https://raw.githubusercontent.com/RoelHuijskens/Website2.0/master/website/src/assets/imgs/me.jpg">
                <Header/>
              </div>
                </div>
            </div>
          <template v-for="message in messages">
               <div v-bind:class="{'question-holder':true, 'question-holder-left':message.sender=='bot', 'question-holder-right':message.sender=='user'}">
                <template v-if="message.sender=='bot'">
                    <img id="profile-picture-icon" src="https://raw.githubusercontent.com/RoelHuijskens/Website2.0/master/website/src/assets/imgs/me.jpg">
                  </template> 
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
    opacity: 1;
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

#profile-picture-icon-initial{
  width: 4rem;
  max-width: 25rem;
  height: 4rem;
  max-height: 25rem;
  border-radius: 50%;
  margin: 0.5rem 0.5rem;
  animation-name: profile-picture-animation-appear;
  animation-duration: 10s;
}

#profile-picture-icon{
  width: 4rem;
  max-width: 25rem;
  height: 4rem;
  max-height: 25rem;
  border-radius: 50%;
  margin: 0.5rem 0.5rem;
}

#profile-picture-portrait{
  opacity: 0;
  width: 0;
  max-width: 25rem;
  height: 0;
  max-height: 25rem;
  border-radius: 50%;
  margin: 0 auto;
  animation-name: profile-picture-animation-disappear;
  animation-duration: 9s;
}


@keyframes profile-picture-animation-appear{
  0% {
    opacity: 0;
  }
  90% {opacity: 0;
  }
  100% {
  }
  
}

@keyframes profile-picture-animation-disappear{
  0% {opacity: 1;
    width: 15vw;
    height: 15vw;
  }
  
  80% {opacity: 1;
    width: 15vw;
    height: 15vw;
  }

  90% {opacity: 0;
    width: 15vw;
    height: 15vw;
  }
  100% {
    opacity: 0;
    width: 0;
    height: 0;
  }
  
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
  position: relative;
  bottom: 0;
  color:black;
  box-shadow: rgba(225, 228, 232, 0.2) 0px 1px 0px 0px inset;
  margin: 0 auto;
  width: 100%;
  font-size: 1rem;
  height: 3.5rem;
  animation-name: initial-message-color-animation, initial-message-animation;
  animation-duration: 10s;
  display: flex;
  flex-direction: column;
}

#initial-message-holder{
  display: flex;
  flex-direction: row;
  width: 40rem;
  animation-name: initial-message-holder-shrink;
  animation-duration: 10s;
}

@keyframes initial-message-color-animation{
  0% {
    background-color: rgba(0,0,0,0);
    color:white;
    box-shadow: 0 0 0;
  }
  90% {
    background-color: rgba(0,0,0,0);
    color:white;
    box-shadow: 0 0 0;
  }
  100% {
    background-color: rgba(255,255,255,1);
    color:black;
    box-shadow: rgba(225, 228, 232, 0.2) 0px 1px 0px 0px inset;
  }

}


@keyframes initial-message-animation{
  0% {
    flex-direction: column;
    bottom: -25vh;
  }
  80% {
    flex-direction: column;
    bottom: -25vh;
  }
  100% {
    flex-direction: row;
    bottom: 0;
  }
}

@keyframes initial-message-holder-shrink{
  0% {
    width: 100%;
  }
  83% {
    width: 100%;
  }
  100% {
    width: 40rem;
  }
}


.video-background {
  position: absolute;
  overflow: hidden;
  width: 99.35vw;
  height: 100vh;

  iframe {
    animation: background-fade-in 7s;
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100vw;
    height: 100vh;
    transform: translate(-50%, -50%);

    @media (min-aspect-ratio: 16/9) {
      height: 56.25vw
    }

    @media (max-aspect-ratio: 16/9) {
      width: 177.78vh
    }
  }
}


@keyframes background-fade-in {
  0% {
    background-color: rgb(0, 0, 0);
    opacity: 0;
  }
  100% {
    opacity: 1;
    background-color: rgba(0,0,0,);
  }
  
}

</style>
