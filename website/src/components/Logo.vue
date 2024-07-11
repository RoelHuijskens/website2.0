<script setup>
    defineProps(['run_animation'])
</script>


<template>

    <div class= "logo-holder">
    <div :class="{'logo-line-holder': true, 'top-holder': this.run_animation}">
        <div :class="{'logo-text': this.run_animation, 'top-text':true}">Roe</div>

        <div :class="{line_holder: this.run_animation,  top: this.run_animation}">
            <div class="vertical_line">
            
        </div>
            <div :class="{ horizontal_line: this.run_animation }">                
            </div></div></div>

    <div :class="{'logo-line-holder': true, 'bottom-holder': this.run_animation}">
        <div :class="{line_holder: this.run_animation, bottom: this.run_animation}">
            <div :class="{ horizontal_line: this.run_animation }">
            </div>
            <div class="vertical_line">

            </div>
        </div><div :class="{'logo-text': this.run_animation, 'bottom-text':true}">uijskens</div></div>
    </div>
</template>


<style>
.logo-holder{
    width: 20rem;
    font-size: 3rem;
}


.line_holder{
    display: flex;
    width: 100%;
    background-color: #f8f8f8;
    margin: 0 0 0 0;
    z-index: 10;

}

.horizontal_line {
    height:0.3rem;
    background-color: #213547;
    margin: auto 0;
    z-index: 20;
    animation: line-width-animation 2s;
    width: 100%
}



.vertical_line{
    margin: auto 0;
    width: 0.25rem;
    height: 2.7rem;
    background-color: #213547;
}

.top {
    margin: auto 0 auto 0;
    animation-name:  logo-slide-animation-top;
    animation-duration: 5s;
    justify-content: flex-start;
}

.bottom {
    margin: auto 0 auto 0;
    animation-name:  logo-slide-animation-bottom;
    animation-duration: 5s;
    justify-content: flex-end;
}

.top-holder{
    animation-name: logo-holder-slide-animation-top;
    animation-duration: 5s;
}

.bottom-holder{
    animation-name: logo-holder-slide-animation-bottom;
    animation-duration: 5s;
}

.logo-line-holder {
    display: flex;
    justify-content: center;
    z-index: 10;
    position:relative;
}

.logo-text{
    margin: auto 0;
    opacity: 1;
    animation-name: text-reveal-animation;
    animation-duration: 5s;

}



.top-text {
    padding: 0 2px 0 0;
   
}

.bottom-text {
    padding: 0 0 0 2px;
}


@keyframes logo-slide-animation-bottom {
    0% {
        margin: 0 -3rem 0 0;
        background-color: rgb(248, 248, 248, 0);

    }

    20% {
        margin: 0 -3rem 0 0;
        background-color: rgb(248, 248, 248, 0);

    }

    35% {
        margin: 0 -12.5rem 0 0;
        background-color: rgb(248, 248, 248, 0);

    }


    50%{
        margin: 0 -12.5rem 0 0;
        background-color: rgb(248, 248, 248, 0);
    }

    60% {
        margin: 0 -12.5rem 0 0;
        background-color: rgb(248, 248, 248, 1);
    }


    100% {
        margin: 0;
        background-color: rgb(248, 248, 248, 1);
    }
}

@keyframes logo-slide-animation-top {
    
    0% {
        margin: 0 0 0 3rem;
    }

    20% {
        margin: 0 0 0 3rem;
    }



    35% {
        margin: 0 0 0 -6rem;
    }

    60% {
        margin: 0 0 0 -6rem;
        
    }


    100% {
        margin: 0;
        
    }
}

@keyframes logo-holder-slide-animation-top {
    0% {
        top: 2.25rem;
    }

    40% {
        top: 2.25rem;
    }

    60% {
        top: 0;
    }

    100% {
        top: 0;
    }
}


@keyframes logo-holder-slide-animation-bottom {
    0% {
        bottom: 2.25rem;
    }

    40% {
        bottom: 2.25rem;
    }

    60% {
        bottom: 0;
    }

    100% {
        bottom: 0;
    }
}




@keyframes text-reveal-animation {
    0% {
        opacity: 0;
    }


    60% {
        opacity: 0;
    }
    
    65% {
        opacity: 1;
    }


    100% {
        opacity: 1;
    }
}

@keyframes line-width-animation {
    0% {
        width:1.5rem;
    }

    50% {
        width:1.5rem;
    }

    90% {
        width: 100%;
    }

    100% {
        width: 100%;
    }


}



</style>