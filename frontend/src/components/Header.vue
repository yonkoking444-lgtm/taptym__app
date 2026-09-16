<template>
    <div class="fixed top-0 left-0 right-0 w-full bg-white z-20">
        <div class="max-w-[360px] mx-auto">
            <h1 class="text-2xl my-5 mx-2 font-light">Продаю</h1>
            <div class="flex justify-around space-x-6 border-b border-gray-300 italic">
                <div v-for="tab in tabs" :key="tab.name" class="relative group pb-2 cursor-pointer">
                    <RouterLink 
                        :to="tab.path" 
                        class="transition-all"
                        :class="isActive(tab.path) ? 'font-semibold text-blue-600' : 'text-zinc-400 hover:text-blue-500'"
                    >
                        {{ tab.name }}
                    </RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const isActive = (path) => route.path.toLowerCase() === path.toLowerCase();

const tabs = ref([
    { name: 'Прочее', path: '/Other' },
    { name: 'Авто', path: '/Main' },
    { name: 'Запчасти', path: '/SpareParts' },
    { name: 'Услуги', path: '/Services' }
]);
</script>
