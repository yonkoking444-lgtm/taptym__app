<script setup >
import CardCar from '../components/CardCar.vue'
import Footer from '../components/Footer.vue';
import Header from '../components/Header.vue';
</script>

<template>
<div class="container max-w-sm flex flex-col h-screen gap-4 justify-center italic"> 
    <header>
        <Header/>
    </header>

    <main class="flex flex-col overflow-y-auto flex-grow min-h-0 my-20 mt-27 gap-4">
        <CardCar/>  
    </main>

    <footer>
        <Footer/>
    </footer>
</div>

</template>

