<script setup>
import ChairCartcom from '../components/ChairCartcom.vue';
import Footer from '../components/Footer.vue';
import Header from '../components/Header.vue';

</script>

<template>
    <div class="container max-w-sm flex flex-col h-screen gap-4 italic">
        <header>
        <Header/>
    </header>

        <main>  
            <ChairCartcom/>
        </main>

    <footer>
        <Footer/>
    </footer>
    </div>
</template>
