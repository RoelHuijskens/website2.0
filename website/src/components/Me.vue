<template>
    <div id="my-info-holder">
        <div id="my-info">
        <h1>About Me</h1>
        <p>
            Good day to you and welcome to my site! I keep this place around for experimentation and sharing some info about myself.
            My name is Roel Huijskens, I am {{ this.getAge() }} years old and currently live in The Hague. I am passionate about technology, software development, AI, and data engineering, which are integral to my daily work. You can learn more about these interests below.
            Currently, I work at at Stedin as a Platform Engineeer. Before I started at Stedin I worked as a DevOps Engineer at APG. Before getting a 'real' job I completed my masters degree in applied statistics at Utrecht University and my bachelors degree in psychology at the VU University.
            In my free time I also like to do stuff away from my PC such as working out, cycling, watching movies.
            If you have any questions, feel free to ask them in the chat above or get linked on linkedin.
        </p>
        </div>
    </div>
</template>

<script>
export default {
    methods :  {
        getAge() {
            var today = new Date();
            var birthDate = new Date("1996-11-21");
            var age = today.getFullYear() - birthDate.getFullYear();
            var m = today.getMonth() - birthDate.getMonth();
            if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
                age--;
            }
            return age;
}
        },
    }
</script>

<style scoped>

    #my-info-holder {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        width: 100vw;
        height: 50vh;
        margin: 15rem 0;
        font-size: 1.2rem;
    }

    #my-info {
        padding: 4rem;
        margin:4rem;
        width:40vw;
        text-align: left;
        min-height: 25rem;
        min-width: 35rem;
    }

</style>
