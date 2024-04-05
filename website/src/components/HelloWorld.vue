<script>
export default {
  props:['title','content','image', 'index'],
  computed: {
    allign_content_left() {
      console.log(this.index%2 == 0 )
      return this.index%2 == 0 
    },
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
        <div v-bind:class="{'card-holder':true, 'card-holder-left':allign_content_left, 'card-holder-right':!allign_content_left}">
      <div class="card-format">
        <h1>{{title}}</h1>
        <p>{{content}}</p>
      </div>
    </div>
  </div>
  </div>
</template>

<style scoped>
.card-format{
  width:40%;
  height:65%;
  opacity:0.5;
}
.card-holder-left{
  justify-content: left;
}
.card-holder-right{
  justify-content: right;
}

.card-holder{
  padding: 6rem 4rem;
  display: flex;
  justify-content: flex-end;
}

.section-holder{
  width:100vw;
}
.picture-holder{
  background-size:cover;
  width:100vw;
  height:75vh;
  min-height: 500px;
  justify-content: right;
}


</style>
