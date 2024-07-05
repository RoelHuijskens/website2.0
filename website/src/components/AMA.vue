
<script setup>
import Header from './Header.vue'
import Logo from './Logo.vue'
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
</script>
<script>
export default {
  data() {
   return{
      messages: [],
      startup_animation_duration: "12s"
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
    async addMessage(message, role){
      if (message.questionText == ''){
        console.log("Please ask a question... don't be shy!")
        return
      }
      this.messages.push({content: message, role: role})
      this.questionText = ''
      await new Promise(r => setTimeout(r, 1000));
      this.messages.push({content: {'questionText':'thinking...'}, role: 'bot'})

      let response

      try{
        response = await axios.post(
        import.meta.env.VITE_BACKEND_URL + '/chat', 
        this.messages.slice(0, -1))
      } catch (error){
        console.log(error)
        response = {
          data: {
            message:{
              questionText:"I'm sorry, I'm not able to answer that question at the moment. Please try again later."
            }
          }
        }
      }
      this.messages.pop()
      response.data.role = 'bot'
      this.messages.push(response.data)
    }
  },


}

</script>

<template>
  <div class=section-holder>
    <!-- <div v-bind:class="" :style="imgDivStyle"> -->
      <div class=video-background>
      <iframe id=ytplayer class="picture-holder" type="text/html"  src="https://www.youtube.com/embed/3Jn3UbF12fA?autoplay=1&controls=0&disablekb=1&fs=0&loop=1&modestbranding=1&mute=1&iv_load_policy=3&playlist=3Jn3UbF12fA" frameborder="0">
        </iframe>
      </div>
        <div id=video-fade-in>
        <div class=chat-holder>
         <div class=chat-stream>
           <div class=chat-messages > 
            <div class=question-holder question-holder-left>
              <div id=initial-message-holder>
              <div class=header></div> <div id=initial-message>
                <img id=profile-picture-icon-initial src="https://raw.githubusercontent.com/RoelHuijskens/Website2.0/master/website/src/assets/imgs/me.jpg">
                <div class=chat-message bot-message id=initial-message-text>
                <Header/>
                </div>
              </div>
                </div>
            </div>
          <template v-for="message in messages">
               <div v-bind:class="{'question-holder':true, 'question-holder-left':message.role=='bot', 'question-holder-right':message.role=='user'}">
                <template v-if="message.role=='bot'">
                    <img id="profile-picture-icon" src="https://raw.githubusercontent.com/RoelHuijskens/Website2.0/master/website/src/assets/imgs/me.jpg">
                  </template> 
                <template v-if="message.role=='bot'&&message.content.questionText=='thinking...'">
                  <div class="chat-message bot-message-anmimated"><div class="thinking-animation" >.</div><div class="thinking-animation" style="animation-delay:0.1s">.</div><div class="thinking-animation" style="animation-delay:0.2s">.</div></div>
                </template>
                <template v-else>
                <div v-bind:class="{'chat-message':true, 'bot-message':message.role=='bot', 'user-message':message.role=='user'}">{{ message.content.questionText }}</div>
                </template>
              </div> 
            </template>
            </div>
            <span id="input-holder">
              <form @submit.prevent="addMessage( { questionText },'user')">
                <input v-model="questionText" class="input-animation"  id="input-prompt">
              </form>
              <button class="input-animation" id="submit-prompt"  @click="addMessage( { questionText },'user')">submit</button>
            </span>  
              
              </div>
          <div id="more-info-holder">
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
    margin: 1rem 0;
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
  flex-direction: column;
  font-family: monospace;
  font-size: 1.2rem;
  padding: 6vh 0;

}



.chat-messages{
    width: 100%;
    height: 80%;
    padding: 10px;
    overflow-y: auto;
}

.chat-message{
    padding: 1.5rem 2rem;
    line-height: 20px;
    color: #24292e;
    opacity: 1;
    vertical-align: middle;
    background-color: #ffffff;
    background-repeat: no-repeat;
    background-position: right 8px center;
    border-radius: 10px;
    outline: none;
    box-shadow: 0px 5px 8px black;
    min-width: 10rem;
    max-width: 30rem;
    animation-duration: 1s;
    position:relative;
    text-align: left;

}


.user-message{
  background-color: rgb(118, 153, 228);
  animation-name: fly-in-message-left;
  color:white;
}
.bot-message{
  background-color: white;
}

.bot-message-anmimated{
  background-color: white;
  animation-name: fly-in-message-right;
}

.chat-stream{
  width: 80%;
  min-width: 50rem;
  height: 80%;
  background-color:rgba(1,1,1,0.5);
  border-radius: 10px;
  box-shadow: rgb(38, 57, 77) 0px 20px 30px -10px;
  position:relative;
  animation: chat-stream-shadow-animation 11s;
  padding: 2rem 1rem;
}

@keyframes chat-stream-shadow-animation{
  0% {box-shadow: rgb(38, 57, 77) 0 0 0 0;}
  95% {box-shadow: rgb(38, 57, 77) 0 0 0 0;}
  100% {box-shadow: rgb(38, 57, 77) 0px 20px 30px -10px;}  
}


#profile-picture-icon-initial{
  width: 4rem;
  max-width: 25rem;
  height: 4rem;
  max-height: 25rem;
  border-radius: 50%;
  margin: 0.5rem 0.5rem;
  animation-name: profile-picture-animation;
  animation-duration: v-bind("startup_animation_duration");
  box-shadow: 0px 5px 8px black;
  position: relative;
}

#profile-picture-icon{
  width: 4rem;
  max-width: 25rem;
  height: 4rem;
  max-height: 25rem;
  border-radius: 50%;
  margin: 0.5rem 0.5rem;
  animation-name: fly-in-message-right;
  animation-duration: 1s;
  position: relative;
  box-shadow: 0px 5px 8px black;
}



@keyframes profile-picture-animation{
  0% {opacity: 0;
    width: 15vw;
    height: 15vw;
    border-radius: 12% 12% 12% 12%;
  }

  25% {opacity: 1;
    box-shadow: 0px 0px 80px -18px rgba(255,255,255,1);
    width: 15vw;
    height: 15vw;
    border-radius: 12% 12% 12% 12%;
  }
  
  80% {opacity: 1;
    box-shadow: 0px 0px 80px -18px rgba(255,255,255,1);
    width: 15vw;
    height: 15vw;
    border-radius: 4% 4% 4% 4%;
  }
  100% {
    opacity: 1;
    width: 4rem;
    height: 4rem;
  }
  
}


#input-prompt{
    padding: 0.5rem 2rem;
    margin: 0 0.5rem;
    font-size: 1.5rem;
    line-height: 20px;
    color: #24292e;
    vertical-align: middle;
    background-color: #ffffff;
    background-repeat: no-repeat;
    background-position: right 8px center;
    border-radius: 0 6px 6px 6px;
    border: 2px solid black;
    box-shadow: 0px 5px 8px black;
    outline: none;
    width: 34rem;
    max-width: 45rem;
    min-width: 18rem;
    
    :focus{
        border-color: #0366d6;
        outline: none;
        box-shadow: rgba(3, 102, 214, 0.3) 0px 0px 0px 3px;
    }
}

#submit-prompt{
  box-shadow: 0px 5px 8px black;
}


.input-animation{
 animation-name: prompt-animation;
 animation-duration:v-bind("startup_animation_duration");
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



.blocked{
  pointer-events: none;
  opacity: 0.5;
}

.section-holder{
  width:100%;
  background-color: BLACK;
}


#initial-message{
  position: relative;
  bottom: 0;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  animation-name:  initial-message-animation;
  animation-duration: v-bind("startup_animation_duration");
  transition: bottom ease 0.3s;
}


#initial-message:hover {
  bottom: 0.5rem;
}


#initial-message-text{
  animation-name:  initial-message-color-animation;
  animation-duration: v-bind("startup_animation_duration");
  font-size: 1rem;
  width: 100%;
  height: 100%;
  padding: 0.2rem 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

#initial-message-holder{
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 36rem;
  animation-duration: v-bind("startup_animation_duration");
  animation-name: initial-message-holder-shrink;
}

@keyframes initial-message-color-animation{
  0% {
    background-color: rgba(0,0,0,0);
    color:white;
    box-shadow: 0 0 0;
  }
  95% {
    background-color: rgba(0,0,0,0);
    color:white;
    box-shadow: 0 0 0;
  }
  100% {
    background-color: rgba(255,255,255,1);
    color:black;
    box-shadow: 0px 5px 8px black;
  }

}


@keyframes initial-message-animation{
  0% {
    bottom: -20vh;
  }
  80% {
    bottom: -20vh;
  }
  100% {
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
    width: 36rem;
  }
}

#video-fade-in{
  animation-name: background-fade-in;
  animation-duration: v-bind("startup_animation_duration");
  position: relative;
  height: 100vh;
  background-color: rgba(0,0,0,0);
}


.video-background {
  position: absolute;
  overflow: hidden;
  width: 99.35vw;
  height: 100vh;
  box-shadow: 0px 5px 10px black;

  iframe {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100vw;
    height: 100vh;
    transform: translate(-50%, -50%);
    border-radius: 0 0 12px 12px;

    

    @media (-webkit-min-aspect-ratio: 16/9), (min-aspect-ratio: 16/9){
        height: 56.25vw
    }

    @media (-webkit-min-aspect-ratio: 16/9), (max-aspect-ratio: 16/9) {
      width: 177.78vh
    }
  }
}


@keyframes background-fade-in {
  0% {
    background-color: rgb(0, 0, 0,1);
  }
  75% {
    background-color: rgb(0, 0, 0,1);
  }
  100% {
    background-color: rgba(0,0,0,0);
  }
  
}

</style>
