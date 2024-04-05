<script>
export default {
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
  }

}

</script>

<template>
  <div class="section-holder">
    <!-- <div v-bind:class="" :style="imgDivStyle"> -->
      <div v-bind:class="{'picture-holder': true}" :style="imgDivStyle">
        <div class="chat-holder">
         <div class="chat-stream">
            <input id="input-prompt">
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
  background-color: rgba(0,0,0,0.2);
}

.chat-stream{
  width: 80%;
  height: 80%;
  background-color: white;
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
    :focus{
        border-color: #0366d6;
        outline: none;
        box-shadow: rgba(3, 102, 214, 0.3) 0px 0px 0px 3px;
    }
                
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
