<template>

    <div class= "logo-holder">
    <div class=logo-line-holder>
        <div>Roe</div>

        <div class="line_holder">
            <div class="vertical_line">
            
        </div>
            <div class="horizontal_line top">                
            </div></div></div>

    <div class=logo-line-holder>
        <div class="line_holder">
            <div class="horizontal_line bottom">
            </div>
            <div class="vertical_line">

            </div>
        </div><div class="logo-text">uijskens</div></div>
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
    margin: 0 -5rem 0 0;
}

.horizontal_line {
    width:100%;
    height:4px;
    background-color: #213547;
}

.vertical_line{
    margin: auto 0;
    width: 0.25rem;
    height: 3rem;
    background-color: #213547;
}

.top {
    margin: auto 0 auto 0;
}

.bottom {
    margin: auto 0 auto 0;
}

.logo-line-holder {
    display: flex;
    justify-content: center;
    z-index: 10;
}

.logo-text{
    margin: auto 0;
}

</style>