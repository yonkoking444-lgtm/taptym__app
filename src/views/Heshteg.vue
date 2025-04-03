<template>
    <div class="p-3 ">
        <div class="mt-5 flex justify-between text-center">
            <RouterLink to="/profile">
                <img src="@/assets/icons/button_back copy.svg" alt="Back" />
            </RouterLink>    
            <h1 class="text-2xl mr-5 font-light italic">Хештеги</h1>
            <div></div>    
        </div>

        <div class="flex flex-wrap gap-3 p-2 mt-4">
            <span 
            v-for="tag in hashtags" :key="index" 
            class="bg-gray-100 text-black px-3 py-1 rounded-lg text-sm "
            >
            {{ tag }}
            </span>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";

    const hashtags = ref([
    '#ToyotaCamry', '#ToyotaCamry25', '#Toyota', '#Продаммашину', '#Срочно', '#черная',
    '#Продамдом', '#торгвозможен', '#Медеускийрайон', '#Дом', '#4комнаты',
    '#куплюстул', '#стул', '#компьютерный стул'
    ]);
</script>

