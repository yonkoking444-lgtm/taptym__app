<script setup>
    import Createcomp from '../components/Createcomp.vue';
</script>


<template>
    <div class="container max-w-sm flex flex-col h-screen ">
        <div class="flex justify-between items-center my-2 sticky top-0 z-10 p-4">
            <h1 class="text-2xl italic">Создайте заявку</h1> 
            <RouterLink to="/Main"><img class="w-6 h-6 hover:scale-110 transition duration-200 cursor-pointer" src="/src/assets/icons/ic_close.svg"></RouterLink>
        </div>
        <div>
            <Createcomp/>
        </div>
    </div>
</template>


