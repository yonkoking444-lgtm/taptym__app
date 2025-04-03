<script setup>
    import Advertisecom from '../components/Advertisecom.vue';
</script>


<template>
    <div class="container max-w-sm flex flex-col h-screen ">
        <div class="flex justify-between items-center sticky top-0 z-10 p-4">
            <h1 class="text-2xl italic">Изменить заявку</h1> 
            <RouterLink to="/ChairBuy"><img class="w-6 h-6 hover:scale-110 transition duration-200 cursor-pointer" src="/src/assets/icons/ic_close.svg"></RouterLink>
        </div>
        <div>
            <Advertisecom/>
        </div>
    </div>
</template>


