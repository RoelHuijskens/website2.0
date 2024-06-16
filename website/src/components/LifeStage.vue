
<script>
export default {
  props:['title','content','image', 'index'],
  data(){
    return {
      id: this.translate_name_to_id(this.title),
      full_view: false,
      section_width: "100%",
      section_height: "",
      section_position: "relative",
      section_justify_content: "center",
      section_z_index: ""
    }
  },
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
  },
  methods: {
    translate_name_to_id(name) {
      return name.toLowerCase().replace(/\s/g, "-");
    },
    set_full_view() {
      this.scroll_to_card(this.id)
      console.log("Setting full view")
      this.full_view = !this.full_view;
  },scroll_to_card(id) {
        console.log("Scrolling to card with label:", id)
        // Assuming each life stage element has an id corresponding to its label
        const elementId = `#${id}`;
        const element = document.querySelector(elementId);

        if (element) {
        // Scroll to the element
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
}
}

</script>

<template>
  <div class="section-holder" @click="set_full_view" :class="{ section_holder_full_view: full_view }" :id="this.id">
    <!-- <div v-bind:class="" :style="imgDivStyle"> -->
      <div v-bind:class="{'picture-holder': true}" :style="imgDivStyle">
        <div v-bind:class="{'card-holder':true, 'card-holder-left':allign_content_left, 'card-holder-right':!allign_content_left}">
      <div class="card-format">
        <h1>{{title}}</h1>
        <p >{{content}}</p>
      </div>
    </div>
  </div>
  </div>
</template>

<style scoped>
.card-format{
  width:30%;
  height:80%;
  background-color: white;
  box-shadow: rgb(38, 57, 77) 0px 20px 30px -10px;
  border-radius: 10px;
  padding: 0 2rem;
  position: relative;
}
.card-holder-left{
  justify-content: flex-start;
}
.card-holder-right{
  justify-content: flex-end;
}

.card-holder{
  padding: 6rem 4rem;
  display: flex;
}

.card-format:hover{
  box-shadow: rgba(50, 50, 93, 0.25) 0px 13px 27px -5px;
}

.section-holder{
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 3rem 0;
  position: relative;
}

.section_holder_full_view{
  width: 100vw;
  height: 100vh;
  justify-content: center;
  padding: 3rem 0;
  position: fixed;
  left:0;
  top:0;
  z-index: 100;

}

.picture-holder{
  background-size:cover;
  background-position: center;
  width:80vw;
  height:75vh;
  min-height: 500px;
  margin: auto;
  border-radius: 9px;
  box-shadow: rgba(50, 50, 93, 0.25) 0px 13px 27px -5px, rgba(0, 0, 0, 0.3) 0px 8px 16px -8px;
  max-width:100rem;
  min-width: 40rem;
  max-height: 30 rem;
}


</style>
