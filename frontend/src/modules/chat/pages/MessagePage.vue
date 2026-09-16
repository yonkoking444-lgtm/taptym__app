<template>
    <div class="container max-w-sm flex flex-col h-screen gap-4">
        <div class="p-2 mt-3">
            <h1 class="italic text-2xl font-light">Сообщения</h1>
        <div class="mt-4 gap-5 flex flex-col">
            <Messagecom/>

        </div>
        </div>
            <Footer/>
    </div>
</template>
<script setup>
import { RouterLink, useRoute } from 'vue-router';
const route = useRoute();

    import Footer from '../../../components/Footer.vue';
    import Messagecom from '../../../components/Messagecom.vue';
</script>


