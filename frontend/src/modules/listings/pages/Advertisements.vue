<script setup>
import CardCar from '../../../components/CardCar.vue';
import Footer from '../../../components/Footer.vue';
import Header from '../../../components/Header.vue';

</script>

<template>
    <div class="container max-w-sm flex flex-col h-screen gap-4 italic">
        <header>
        <Header/>
    </header>

        <main>
            <CardCar action="Куплю"/>
        </main>

    <footer>
        <Footer/>
    </footer>
    </div>
</template>
