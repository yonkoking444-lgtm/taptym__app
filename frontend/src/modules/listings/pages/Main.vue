<script setup >
import CardCar from '../../../components/CardCar.vue'
import Footer from '../../../components/Footer.vue';
import Header from '../../../components/Header.vue';
</script>

<template>
<div class="container flex flex-col justify-center h-screen max-w-sm gap-4 italic"> 
    <header>
        <Header/>
    </header>

    <main class="flex flex-col flex-grow min-h-0 gap-4 my-20 overflow-y-auto mt-27">
        <CardCar action="Продам"/>
    </main>

    <footer>
        <Footer/>
    </footer>
</div>

</template>

