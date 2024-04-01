<script setup lang="ts">

defineProps(['title','content','image']);

</script>

<template>
  <div class="section-holder">
    <div class="picture-holder">
      <div class="card-format">
        <h1>{{title}}</h1>
        <p>{{content}}</p>
      </div>
    </div>

  </div>
</template>

<style scoped>
.card-format{
  left:0;
  width:40%;
  height:65%;
  opacity:0.5;
}
.section-holder{
  display:flex;
  flex-direction:row;
  width:100vw;
}
.picture-holder{
  padding: 6rem 4rem;
  display:flex;
  flex-direction:row;
  background-size:cover;
  background-image: url('"../assets/imgs/" + "VU.jpg"');
  width:100vw;
  height:75vh;
  min-height: 500px;
}


</style>
