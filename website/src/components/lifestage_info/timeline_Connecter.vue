<template>
    <div class="connector-holder">
        <div class="connector">
            <div v-if="text!=''" class="connector-text"><b>{{ text }}</b></div>
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
        position: sticky;
        top: 50vh;
        height: 20rem;
    }




    .connector-element {
        margin: 0 auto;
    }


    .connector-text {
        padding: 0.1rem 0;
        font-size: 2rem;
        white-space: nowrap;
        height: 20%;
        width: 20rem;
        background-color: #f8f8f8;
        z-index: -2;
        opacity:1;
    }

</style>