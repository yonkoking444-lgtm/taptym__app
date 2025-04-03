<script setup>
import { ref, computed, onMounted } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import axios from 'axios';
import { useToast } from "vue-toastification";

const currentIndex = ref(0);

const route = useRoute();
const toast = useToast();

const item = ref({});
const tags = ref([]);


const resetForm = () => {
    formData.value = { ...defaultFormData };
};

const previewUrls = ref([]); 

const formData = ref({
    action: '',
    category: '',
    title: '',
    hashtags: '',
    city: '',
    price: null,
    description: '',
    photos: []
});

function previewImage(event) {
    const files = event.target.files;
    if (files.length) {
        Array.from(files).forEach((file) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                previewUrls.value.push(e.target.result);

                if (!Array.isArray(formData.value.photos)) {
                    formData.value.photos = [];
                }

                formData.value.photos.push(file);
            };
            reader.readAsDataURL(file);
        });
    }
}

const previewUrl = ref('');

const isFormValid = computed(() => {
    return (
        formData.value.action &&
        formData.value.category &&
        formData.value.title &&
        formData.value.description &&
        formData.value.photo.length > 0
    );
});


async function submitForm() {
    if (!isFormValid.value) { 
        toast.error("Пожалуйста, заполните все поля!", { timeout: 3000 });
        return;
    }

    const formDataToSend = new FormData();
    formDataToSend.append("action", formData.value.action);
    formDataToSend.append("category", formData.value.category);
    formDataToSend.append("title", formData.value.title);
    formDataToSend.append("hashtags", formData.value.hashtags);
    formDataToSend.append("city", formData.value.city);
    formDataToSend.append("price", formData.value.price);
    formDataToSend.append("description", formData.value.description);
    
    formData.value.photos.forEach((file) => {
        formDataToSend.append("photos", file);
    });

    try {
        let response;
        if (item.value.id) {
            response = await fetch(`https://e27f20bf16c931eb.mokky.dev/ChairsDetail/${item.value.id}`, {
                method: "PUT",
                body: formDataToSend
            });
        } else {
            response = await fetch("https://e27f20bf16c931eb.mokky.dev/ChairsDetail", {
                method: "POST",
                body: formDataToSend
            });
        }

        if (!response.ok) {
            throw new Error("Ошибка при сохранении данных!");
        }
        toast.success("Заявка успешно сохранена!", { timeout: 3000 });

        isModalOpen.value = false; 

    } catch (error) {
        toast.error(error.message, { timeout: 3000 });
    }
}



onMounted(async () => {
    try {
        const { data } = await axios.get(`https://e27f20bf16c931eb.mokky.dev/ChairsDetail/${route.params.id}`);
        console.log('Загруженные данные:', data);

        item.value = data;

        formData.value = {
        title: data.title || '',
        price: data.price || '',
        category: data.category || '',
        action: data.action || '',
        location: data.location || '', 
        description: data.description || '',
        tag: data.tags || '',
        photos: Array.isArray(data.photos) ? data.photos : [],
    };


    } catch (err) {
        console.error('Ошибка загрузки данных:', err);
        item.value = {};
    }
});

const formattedPrice = computed({
    get: () => {
    if (!formData.value.price) return "";
    return new Intl.NumberFormat("ru-RU").format(formData.value.price) + " ₸";
},

    set: (value) => {
        formData.value.price = value.replace(/\D/g, ""); 
    },
});

onMounted(async () => {
    try {
        const response = await fetch("https://e27f20bf16c931eb.mokky.dev/ChairsDetail"); 
        const data = await response.json();
        console.log("Данные из API:", data); 
        
        if (Array.isArray(data) && data.length > 0 && data[0].tags) {
            tags.value = data[0].tags.map((tag) => ({ text: tag, selected: false }));
        } else {
            console.error("Ошибка: Теги не найдены в API", data);
            tags.value = []; 
        }
    } catch (error) {
        console.error("Ошибка загрузки данных:", error);
    }
});

const removeTag = (index) => {
    tags.value.splice(index, 1);
};

    const toggleTag = (index) => {
    tags.value[index].selected = !tags.value[index].selected;
    };


    const openModalimg = (index) => {
    currentIndex.value = index;
    isModalOpen.value = true;
    };
    

    onMounted(async () => {
    try {
    const { data } = await axios.get(`https://e27f20bf16c931eb.mokky.dev/ChairsDetail/${route.params.id}`);
    console.log("Загруженные данные:", data);

    item.value = data;

    previewUrls.value = [];


        if (data.detailimgmodal) {
        if (typeof data.detailimgmodal === "string") {
            previewUrls.value.push(data.detailimgmodal);
        } else if (Array.isArray(data.detailimgmodal)) {
            previewUrls.value.push(...data.detailimgmodal);
        }
        }

        if (Array.isArray(data.photos)) {
        previewUrls.value.push(...data.photos);
        }

        console.log("Финальный список изображений:", previewUrls.value);
    } catch (err) {
        console.error("Ошибка загрузки данных:", err);
    }
    });


    const isModalOpen = ref(false);

    const openModal = () => {
    isModalOpen.value = true;
    };

    // const closeModal = () => {
    // isModalOpen.value = false;
    // };

    const closeModal = () => {
    console.log("Закрытие модального окна"); 
    isModalOpen.value = false;
};

</script>



<template>
    <div v-if="item && item.title" class="h-screen container max-w-sm">
        <div class="flex relative ">
        <RouterLink to="/ChairBuy">
            <img src="/src/assets/icons/ic_backchair.svg" class=" absolute top-5 left-2 hover:scale-110 transition duration-200"/>
        </RouterLink>
        <img src="/src/assets/icons/button_save.svg" class=" absolute top-5 right-2 hover:scale-110 transition duration-200"/>
        
        <div>
            <img
            :src="item.detailimg"
            alt="Изображение товара"
            class="object-cover cursor-pointer rounded-lg mt-10"
            @click="openModal"
            />

            <div v-if="isModalOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-80 z-50">
                <div class="relative w-full max-w-2xl">
                
                <button @click="closeModal" class="absolute top-0 left-5 z-60">
                    <img src="/src/assets/images/button_backwhite.svg" class="hover:scale-110 transition duration-200"/>
                </button>

                <button class="absolute top-0 right-5 z-60">
                    <img src="/src/assets/images/button_savewhite.svg" class="hover:scale-110 transition duration-200"/>
                </button>

                <el-carousel :interval="5000" arrow="always" height="85vh">
                    <el-carousel-item v-for="(img, index) in item.detailimgmodal" :key="index">
                    <img :src="img" alt="Дополнительное изображение" class="w-full h-full object-contain" />
                    </el-carousel-item>
                </el-carousel>

                <div class="mt-10 flex justify-center gap-4">
                    <button class="px-10 py-2 bg-blue-500 text-white italic rounded-lg border hover:border-blue-500 active:text-blue-500 active:bg-white transition">
                    Написать
                    </button>
                    <button class="px-10 py-2 border border-blue-500 text-blue-500 active:bg-blue-500 transition active:text-white italic rounded-lg">
                    Позвонить
                    </button>
                </div>
                </div>
            </div>
    </div>
</div>

        <div class="p-3 flex flex-col gap-2 align-center">
            <h2 class="text-xl font-light italic ">{{ item.title }}</h2>
            <div class="flex justify-between mb-2 italic">
                <p class="text-lg font-normal">{{ item.price }} ₸</p>
                <p class="text-base">{{ item.location }}</p>
            </div>

            <p class="text-base">{{ item.description }}</p>

            <div class="flex flex-wrap gap-1 mt-2">
                <button
                v-for="(tag, index) in tags"
                :key="index"
                @click="toggleTag(index)"
                class="px-3 py-1 rounded-full text-black text-sm transition-all my-1"
                :class="{ 'bg-purple-200': tag.selected, 'bg-gray-200': !tag.selected }"
                >
                {{ tag.text }}
                </button>
            </div>

            <div v-if="item" class="flex justify-between items-center mt-3 italic">
                <div class="flex items-center gap-2">
                    <img :src="item.avatar" alt="item Avatar" class="w-9 h-9 rounded-full"/>
                    <h3 class="text-sm font-medium">{{ item.name }}</h3>
                </div>
                <p class="text-sm text-gray-500">{{ item.date }}</p>
            </div>
        </div>

        <div class="relative h-[100px]"> 
            <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-4">
            <button class="px-12 py-3 bg-blue-500 text-white italic rounded-lg border hover:border-blue-500 active:text-blue-500  active:bg-white transition">
                Написать
            </button>
            <button class="px-12 py-3 border border-blue-500 text-blue-500 active:bg-blue-500 transition active:text-white italic rounded-lg">
                Позвонить
            </button>
            </div>
        </div>
    </div>

</template>

