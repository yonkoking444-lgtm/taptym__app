<script setup>
import { useRouter } from 'vue-router';
import { useChatStore } from "/stores/messaginfo.ts";

const chatStore = useChatStore();
const router = useRouter();
</script>

<template>
    <div @click="router.push('/messageschat')" class="flex items-start gap-2 ">
        <div class="flex flex-col items-center gap-1">
            <img 
            :src="chatStore.imageUrl" 
            alt="User Avatar" 
            class="w-18 h-14 rounded-lg object-cover"
            />
            <p class="text-sm text-stone-500">{{ chatStore.name }}</p>
        </div>
        <div class="ml-2">
            <p class="text-black font-base italic text-base">
                <span>{{ chatStore.title }}</span>
            </p>
        <p class="text-balck truncate text-sm">{{ chatStore.lastMessage }}</p>
        </div>
        <div class="flex flex-col items-center gap-1">
            <span class="text-gray-400 text-sm">{{ chatStore.time }}</span>
            <img src="/src/assets/icons/circle.svg" alt="">
        </div>
    </div>
</template>
