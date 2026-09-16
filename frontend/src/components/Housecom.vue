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
<div class="container flex flex-col justify-center h-screen max-w-sm gap-4 italic">  
    <Header/>
    <Othercom/>
    <Footer/>
    </div>
</template>
