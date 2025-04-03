<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted } from "vue";
import axios from "axios";

const items = ref([]);
const router = useRouter();

onMounted(async () => {
    try {
        const { data } = await axios.get("https://e27f20bf16c931eb.mokky.dev/Advertisements");
        items.value = data.map((item) => ({
            ...item,
            hashtags: item.hashtags.map(tag => ({ name: tag, selected: false }))
        }));
    } catch (err) {
        console.error("Ошибка загрузки данных:", err);
    }
});

const toggleTag = async (item, tag) => {
    tag.selected = !tag.selected;

    try {
        await axios.put(`https://e27f20bf16c931eb.mokky.dev/Advertisements/${item.id}`, {
            hashtags: item.hashtags.map(t => t.name)
        });
    } catch (err) {
        console.error("Ошибка обновления тега:", err);
    }
};

</script>

<template>
    <div>
    <RouterLink to="/ChairBuy">
        <div class="mt-20 flex flex-col items-center gap-10">
            <div v-for="item in items" :key="item.id" class="bg-white p-3 rounded-lg border border-gray-300 ">
                <h3 class="text-lg font-base mb-2 italic">{{ item.text }}</h3>
                <div class="flex flex-wrap gap-2 mb-2">
                    <span v-for="tag in item.hashtags" :key="tag.name"
                        :class="tag.selected ? 'bg-purple-200 ' : 'bg-gray-200'"
                        class="px-3 py-1 rounded-full text-sm cursor-pointer transition"
                        >
                        #{{ tag.name }}
                    </span>
                </div>
                <div class="flex justify-between items-center mt-4">
                    <p class="text-gray-500 text-sm">Найдено:{{ item.found }}</p>
                    <p class="text-gray-500 text-sm">{{ item.date }}</p>
                </div>
            </div>
        </div>
        </RouterLink>
    </div>
</template>
