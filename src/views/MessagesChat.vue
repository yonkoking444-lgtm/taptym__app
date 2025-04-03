
<script setup>
import { useRouter } from 'vue-router';
import { useChatStore } from "/stores/messaginfo.ts";

const chatStore = useChatStore();
const router = useRouter();
</script>


<template>
  <div class="flex items-center gap-4 p-2 border-b border-stone-200 mt-3">
    <RouterLink to="/message">
      <img :src="chatStore.iconUrl" class="cursor-pointer w-6">
    </RouterLink>
    
    <img :src="chatStore.imageUrl" alt="User Avatar" class="w-14 h-14 rounded-lg object-cover">

    <div class="flex flex-col">
      <p class="text-black font-semibold text-base">
        {{ chatStore.title }}
      </p>
      <p class="text-gray-500 text-sm">
        {{ chatStore.name }}
      </p>
    </div>
  </div>

  <div class="p-4 space-y-3">
    <div class="flex justify-end">
      <div class="bg-blue-500 text-white p-3 rounded-lg max-w-[75%]">
        Здравствуйте, можешь договориться о цене?
      </div>
    </div>
    
    <div class="flex justify-end">
      <div class="bg-blue-500 text-white p-3 rounded-lg max-w-[75%]">
        И во сколько можем созвониться?
      </div>
    </div>

    <div class="flex justify-start">
      <div class="bg-gray-100 text-black p-3 rounded-lg max-w-[75%]">
        Здравствуйте! Да, цену можем обсудить. Давайте созвонимся завтра после 6 вечера.
      </div>
    </div>
  </div>

  <div class="fixed bottom-0  bg-white p-3 border-t border-gray-300 flex items-center gap-5">
    <input
      type="text"
      placeholder="Сообщение..."
      class="flex-1 p-3 px-12 pl-10 rounded-lg border border-gray-300 focus:outline-none"
    />
    <img class="absolute left-5 w-6 h-6" src="/src/assets/icons/camera.svg" alt="Camera Icon">
    
    <button class="ml-1 bg-blue-500 text-white p-3 rounded-lg">
      ➤
    </button>
  </div>


</template>



