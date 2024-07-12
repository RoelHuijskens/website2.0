
<script setup>
import Header from './Header.vue'
import Logo from './Logo.vue'
import VideoBackground from './VideoBackground.vue'
import Messages from './Messages.vue'
import axios from 'axios';
// import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
</script>

<script>
export default {
  data() {
   return{
      messages: [],
      startup_animation_duration: "12s",
      chat_id: null,
      user_question: ''
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
  mounted() {
    this.messages = []
  },
  methods: {
    async addMessage(input, role){
      
      if (input.user_question == ''){
        console.log("Please ask a question... don't be shy!")
        return
      }
      
      this.messages.push({content: input.user_question, role: role})
      this.user_question = ''
      
      await new Promise(r => setTimeout(r, 1000));
      
      this.messages.push({content: 'thinking...', role: 'bot'})

      let response
      let conversation_endpoint

      if (this.chat_id){
        conversation_endpoint = '?conversation_id=' + this.chat_id
      } else {
        conversation_endpoint = ''
      }

      try{
        response = await axios.post(
        import.meta.env.VITE_BACKEND_URL + '/chat' + conversation_endpoint, 
        this.messages.slice(-2)[0])
      } catch (error){
        let response_text

        if(error.response) {
          if (error.response.status == 404){
            response_text = "It seems like something went wrong while processing your question, please refresh your page and try again."
          } else if (error.response.status == 503) {
            console.log(error.response)
            response_text = error.response.data.detail
          } else {
            response_text = "I'm sorry, I'm not able to answer that question at the moment. Please try again later."
          }

        }
        response = {
          data: {
              content: response_text
          }
        }
      }
      response.data.role = 'bot'
      this.chat_id = response.data.chat_id

      this.messages.pop()
      this.messages.push(response.data)
    }
  },


}

</script>

<template>
  <div class=section-holder>
    <!-- <div v-bind:class="" :style="imgDivStyle"> -->
        <VideoBackground/>
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
            <Messages :messages="messages"/>
            </div>
            <span id="input-holder">
              <form @submit.prevent="addMessage( { user_question },'user')">
                <input v-model="user_question" class="input-animation"  id="input-prompt">
              </form>
              <button class="input-animation" id="submit-prompt"  @click="addMessage( { user_question },'user')">submit</button>
            </span>  
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>


.chat-holder{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
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
    padding: 1.5rem 2rem;
    line-height: 20px;
    color: #24292e;
    opacity: 1;
    vertical-align: middle;
    background-color: #f8f8f8;
    background-repeat: no-repeat;
    background-position: right 8px center;
    border-radius: 20px;
    outline: none;
    box-shadow: 0px 5px 8px black;
    min-width: 10rem;
    max-width: 30rem;
    animation-duration: 1s;
    position:relative;
    text-align: left;
    margin: 0 0 0 1rem;
}


.bot-message{
  background-color: white;
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
    padding: 1rem 3rem;
    margin: 0 0.5rem;
    font-size: 1.2rem;
    line-height: 20px;
    color: #24292e;
    vertical-align: middle;
    background-color: #f8f8f8;
    background-repeat: no-repeat;
    background-position: right 8px center;
    border-radius: 10px;
    box-shadow: 0px 5px 8px black;
    outline: none;
    width: 34rem;
    height: 1rem;
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



.section-holder{
  width:100%;
  background-color: BLACK;
}


#initial-message{
  position: relative;
  bottom: 0;
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
  width: 90rem;
  height: 100%;
  padding: 0.2rem 2rem;
  display: flex;
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
