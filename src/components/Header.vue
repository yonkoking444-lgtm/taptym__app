<template>
    <div class="fixed top-0 w-full bg-white z-20">
        <h1 class="text-2xl my-5 mx-2 font-light ">Продаю</h1>
        <div class="w-[360px] flex justify-around space-x-6 border-b border-gray-300 italic">
            <div v-for="tab in tabs" :key="tab.name" class="relative group pb-2 cursor-pointer">
                <RouterLink 
                    :to="tab.path" 
                    class="transition-all"
                    :class="{ 'text-blue-500 font-semibold': $route.path === tab.path, 'text-gray-400 hover:text-blue-500': $route.path !== tab.path }"
                >
                    {{ tab.name }}
                </RouterLink>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const tabs = ref([
    { name: 'Прочее', path: '/Other' },
    { name: 'Авто', path: '/Main' },
    { name: 'Жилье', path: '/Hous' },
    { name: 'Услуги', path: '/Services' }
]);
</script>
