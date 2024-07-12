<template>
    <div class=video-background>
      <iframe id=ytplayer class="picture-holder" type="text/html"  src="https://www.youtube.com/embed/-UKp1VIsX9E?autoplay=1&controls=0&disablekb=1&fs=0&loop=1&modestbranding=1&mute=1&iv_load_policy=3&playlist=-UKp1VIsX9E" frameborder="0">
        </iframe>
      </div>
</template>


<style>

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



</style>