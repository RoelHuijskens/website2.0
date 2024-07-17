<script setup>

    import VueMarkdown from 'vue-markdown-render'
    const props = defineProps({
        messages: {
            type: Array,
            default: []
        },
    })

</script>

<template>
<template v-for="message in props.messages">
    <div v-bind:class="{'question-holder':true, 'question-holder-left':message.role=='bot', 'question-holder-right':message.role=='user'}">
     <template v-if="message.role=='bot'">
         <img id="profile-picture-icon" src="https://raw.githubusercontent.com/RoelHuijskens/Website2.0/master/website/src/assets/imgs/me.jpg">
       </template>
     <template v-if="message.role=='bot'&&message.content=='thinking...'">
       <div class="chat-message bot-message-anmimated"><div class="thinking-animation" >.</div><div class="thinking-animation" style="animation-delay:0.1s">.</div><div class="thinking-animation" style="animation-delay:0.2s">.</div></div>
     </template>
     <template v-else>
     <VueMarkdown v-bind:class="{'chat-message':true, 'bot-message':message.role=='bot', 'user-message':message.role=='user'}" :source="message.content"/>
     </template>
   </div>
 </template>
</template>



<style>

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


.user-message{
  background-color: rgb(118, 153, 228);
  animation-name: fly-in-message-left;
  color:white;
}


.bot-message-anmimated{
  background-color: white;
  animation-name: fly-in-message-right;
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



</style>
