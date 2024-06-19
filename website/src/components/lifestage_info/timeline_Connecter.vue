<template>
    <div class="connector-holder">
        <div class="connector">
            <div v-if="position=='start'" class="connector-end connector-element"></div>
            <div class="connector-body connector-element"></div>
            <div v-if="text!=''" class="connector-text"><b>{{ text }}</b></div>
            <div class="connector-body connector-element"></div>
            <div v-if="position=='end'" class="connector-end connector-element"></div>

        </div>
    </div>
</template>

<script setup>

    const props = defineProps({
        text: {
            type: String,
            default: ""

        },
        position:String
    })


</script>

<script>


export default {
    name: 'YourComponentName',

    data() {
        return {
            // Your component data
        };
    },
    methods: {
        // Your component methods
    },
};
</script>

<style scoped>
    .connector-holder {
        width: 100%;
        display: flex;
        justify-content: center;
        position: relative;
        z-index: -20;
    }

    .connector {
        width: 10vw;
        display: flex;
        justify-content: center;
        flex-direction: column;
        height: 30vh;
    }


    .connector-element {
        margin: 0 auto;
    }

    .connector-body {
        width: 0.2rem;
        height: 30%;
        background-color: rgb(33,53,71,1);
    }

    .connector-end {
        border-radius: 50%;
        border-width: 0.2rem;
        border-color: rgb(33,53,71,1);
        border-style: solid;
        width: 20px;
        height: 20px;
    }

    .connector-text {
        padding: 0.1rem 0;
        font-size: 2rem;
        white-space: nowrap;
        height: 20%;
    }

</style>