<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted } from "vue";
import axios from "axios";

const items = ref([]);
const router = useRouter();

onMounted(async () => {
    try {
        const { data } = await axios.get("https://e27f20bf16c931eb.mokky.dev/CarDetail");
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

    await fetch("https//e27f20bf16c931eb.mokky.dev/CarDetail", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tags: items.value.map(item => item.tags) }),
    });
};

const goToDetail = (id) => {
    router.push(`/cardetail/${id}`);
};
</script>

<template>
    <div v-for="item in items" :key="item.id" @click="goToDetail(item.id)" class="max-w-sm rounded-lg border border-gray-200 italic cursor-pointer ">
        <img :src="item.image" alt="Car" class="w-full rounded-lg" />
        <div class="p-4">
            <h2 class="text-lg font-normal my-3">{{ item.title }}</h2>
                <div class="flex flex-wrap gap-2">
                    <button
                        v-for="tag in items[0]?.tags || []"
                        :key="tag.name"
                        class="px-3 py-1 rounded-full text-black text-sm transition-all"
                        :class="tag.selected ? 'bg-purple-200' : 'bg-gray-200'"
                    >
                        {{ tag.name }}
                    </button>
                </div>

            <div class="flex justify-between items-center mt-3 italic">
                <p class="text-base">Найдено: <span class="text-blue-600">{{ item.tags.length }}</span></p>
                <p class="text-gray-400 text-sm">{{ item.date || 'Нет даты' }}</p>
            </div>
        </div>
    </div>
</template>
