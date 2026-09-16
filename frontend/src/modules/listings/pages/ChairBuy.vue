<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted } from "vue";
import axios from "axios";

const items = ref([]);
const router = useRouter();

onMounted(async () => {
    try {
        const { data } = await axios.get("https://e27f20bf16c931eb.mokky.dev/ChairsDetail");
        items.value = data.map((item) => ({
            ...item,
            tags: item.tags ? item.tags.map(tag => ({ name: tag, selected: false })) : []
        }));
    } catch (err) {
        console.error("Ошибка загрузки данных:", err);
    }
});

const toggleTag = async (tag) => {
    tag.selected = !tag.selected;

    await fetch("https://e27f20bf16c931eb.mokky.dev/ChairsDetail", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tags: items.value.map(item => item.tags) }),
    });
};

const goToDetail = (id) => {
    router.push(`/chair/${id}`);
};


const ad = ref(null);

onMounted(async () => {
    try {
        const response = await fetch('https://e27f20bf16c931eb.mokky.dev/Advertisements');
        const data = await response.json();
        ad.value = data[0]; 
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
    }
});



</script>

<template>
    <div class="container mx-auto max-w-md w-full h-full flex flex-col items-center  ">
        <div class="w-[360px] relative mb-10 mt-5">
            <RouterLink to="/buyitems">
                <img src="/src/assets/icons/button_back.svg" class="absolute left-0 hover:scale-110 transition duration-200"/>
            </RouterLink>
            <RouterLink to="/EditAdvertis"> 
                <img
                src="/src/assets/icons/button_edit.svg"
                class="absolute right-0 hover:scale-110 transition duration-200"
                @click="isModalOpen = true"
            /> 
            </RouterLink>
        
        </div>

        <div class="max-w-md mx-auto bg-white  p-4 border-b-gray-300 border-b" v-if="ad">
        <h2 class="text-xl font-base italic my-2">{{ ad.text }}</h2>
        <div class="flex justify-between ">
            <p class="text-lg font-medium text-gray-700">{{ ad.price }}</p>
            <p class="text-gray-500">{{ ad.location }}</p>
        </div>
            <p class="mt-2 text-gray-700">{{ ad.description }}</p>
            <div class="mt-3 flex flex-wrap gap-2">
                <span v-for="tag in ad.hashtags" :key="tag"
                    class="px-3 py-1 rounded-full text-sm cursor-pointer transition bg-gray-200"
                > #{{ tag }}
                </span>                
            </div>
            <div class="mt-4 flex items-center justify-between ">
            <div class="flex ">
                <img :src="ad.image" alt="Author" class="w-6 h-6 rounded-full" v-if="ad.image" />
                <span class="ml-3 font-medium text-gray-700">{{ ad.author }}</span>
            </div>
            <p class="text-gray-500 text-sm mt-2">{{ ad.date }}</p>
            </div>
        </div>


<div class="relative w-[360px]">
    <h2 class="text-xl absolute left-0 my-3">Найдено:<span class="text-blue-500">2</span></h2>
    <div class="mt-15">
        <div v-for="item in items" :key="item.id" @click="goToDetail(item.id)" 
            class="w-full max-w-sm rounded-lg border border-gray-200 italic cursor-pointer mt-7 bg-white ">
            <img :src="item.image" alt="chair1" class="w-full rounded-lg" />
            <div class="p-4">
                <h2 class="text-lg font-normal my-3">{{ item.title }}</h2>
                <div class="flex flex-wrap gap-2">
                    <button
                        v-for="tag in item.tags || []"
                        :key="tag.name"
                        class="px-3 py-1 rounded-full text-black text-sm transition-all"
                        :class="tag.selected ? 'bg-purple-200' : 'bg-gray-200'"
                    >
                        {{ tag.name }}
                    </button>
                </div>

                <div v-if="item" class="flex justify-between items-center mt-5 italic">
                    <div class="flex items-center gap-2">
                        <img :src="item.avatar" alt="item Avatar" class="w-8 h-8 rounded-full"/>
                        <h3 class="text-sm font-medium">{{ item.name }}</h3>
                    </div>
                    <p class="text-sm text-gray-500">{{ item.date }}</p>
                </div>
            </div>
        </div>
    </div>
</div>
    </div>
</template>

