<script>
export default {
  data() {
   return{
      messages: [
        {
          message: {'questionText':'Hi, ask me anything!'},
          sender: 'bot'
        },
      ]
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
      this.messages.push({message: {'questionText':'thinking...'}, sender: 'bot'})
      this.questionText = ''
      await new Promise(r => setTimeout(r, 12000));
      this.messages.pop()
      this.messages.push({message: {'questionText':'I dont know mate'}, sender: 'bot'})
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
          <template v-for="message in messages">
               <div v-bind:class="{'question-holder':true, 'question-holder-left':message.sender=='bot', 'question-holder-right':message.sender=='user'}">
                <template v-if="message.sender=='bot'&&message.message.questionText=='thinking...'">
                  <div class="chat-message bot-message"><div class="thinking-animation" >.</div><div class="thinking-animation" style="animation-delay:0.2s">.</div><div class="thinking-animation" style="animation-delay:0.4s">.</div></div>
                </template>
                <template v-else>
                 <div v-bind:class="{'chat-message':true, 'bot-message':message.sender=='bot', 'user-message':message.sender=='user'}">{{ message.message.questionText }}</div>
                </template>
              </div> 
            </template>
            </div>
            <span id="input-holder"><input v-model="questionText" id="input-prompt"><button @click="addMessage( { questionText },'user')">submit</button></span>
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
  animation-duration: 2s;
  animation-iteration-count: infinite;
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
}
.chat-messages{
    width: 100%;
    height: 80%;
    padding: 10px;
}
.chat-message{
    padding: 5px 12px;
    font-size: 14px;
    line-height: 20px;
    color: #24292e;
    vertical-align: middle;
    background-color: #ffffff;
    background-repeat: no-repeat;
    background-position: right 8px center;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    outline: none;
    box-shadow: rgba(225, 228, 232, 0.2) 0px 1px 0px 0px inset;
    min-width: 10rem;
}

.user-message{
  background-color: bisque;
}
.bot-message{
  background-color: lightblue;
}
.chat-stream{
  width: 80%;
  height: 80%;
  background-color:rgba(1,1,1,0.2);
  border-radius: 10px;
  box-shadow: rgb(38, 57, 77) 0px 20px 30px -10px;
}

#input-prompt{
    padding: 5px 12px;
    font-size: 14px;
    line-height: 20px;
    color: #24292e;
    vertical-align: middle;
    background-color: #ffffff;
    background-repeat: no-repeat;
    background-position: right 8px center;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    outline: none;
    box-shadow: rgba(225, 228, 232, 0.2) 0px 1px 0px 0px inset;
    width: 60%;
    min-width: 18rem;
    :focus{
        border-color: #0366d6;
        outline: none;
        box-shadow: rgba(3, 102, 214, 0.3) 0px 0px 0px 3px;
    }

                


}
#input-holder{
    display: flex;
    justify-content: space-around;
    align-items: center;
    width: 100%;
    height: 20%;

}

.blocked{
  pointer-events: none;
  opacity: 0.5;
}

.section-holder{
  width:100vw;
}
.picture-holder{
  background-size:cover;
  background-position: center;
  width:100vw;
  height:75vh;
  min-height: 500px;
  justify-content: right;
}


</style>
