<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const items = ref([]);

onMounted(async () => {
    try {
    const { data } = await axios.get("https://e27f20bf16c931eb.mokky.dev/HousDetail");
    items.value = data.map(item => ({
        ...item,
        tags: item.tags.map(tag => ({ text: tag, selected: false }))
    }));
    } catch (err) {
    console.error("Ошибка загрузки данных:", err);
    }
});

const toggleTag = (tag) => {
    tag.selected = !tag.selected;
};
</script>



    
    <template>
        <div>
        <div class="max-w-sm rounded-lg max-h-390px italic border-1 border-gray-200 max-h-390px">
            <div 
            v-for="item in items" 
            :key="item.id" 
            class="max-w-sm rounded-lg border border-gray-200"
            >
            <img :src="item.image" alt="Car" class="w-full rounded-lg" />
            <div class="p-4">
                <h2 class="text-lg font-normal my-3">{{ item.title }}</h2>
                <div class="flex flex-wrap gap-1 mt-2">
                <button
                    v-for="tag in item.tags"
                    :key="tag"
                    @click="toggleTag(tag)"
                    class="px-3 py-1 rounded-full text-black text-sm transition-all my-1"
                    :class="{ 'bg-purple-200': tag.selected, 'bg-gray-200': !tag.selected }"
                >
                    {{ tag.text }}
                </button>
                </div>
                <div class="flex justify-between items-center mt-3 italic">
                <p class="text-base">Найдено: <span class="text-blue-600">4</span></p>
                <p class="text-gray-400 text-sm">{{ item.date }}</p>
                </div>
            </div>
            </div>
        </div>
        </div>
    </template>
    
    