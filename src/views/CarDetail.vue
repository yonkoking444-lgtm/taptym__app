<script setup>
import { ref, computed, onMounted } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import axios from 'axios';
import { useToast } from "vue-toastification";


const route = useRoute();
const toast = useToast();

const item = ref({});
const tags = ref([]);

const isModalOpen = ref(false);

const defaultFormData = {
    action: '',
    category: '',
    title: '',
    hashtags: '',
    city: '',
    price: null,
    description: '',
    photos: []
};

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
            response = await fetch(`https://e27f20bf16c931eb.mokky.dev/CarDetail/${item.value.id}`, {
                method: "PUT",
                body: formDataToSend
            });
        } else {
            response = await fetch("https://e27f20bf16c931eb.mokky.dev/CarDetail", {
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
        const { data } = await axios.get(`https://e27f20bf16c931eb.mokky.dev/CarDetail/${route.params.id}`);
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
        const response = await fetch("https://e27f20bf16c931eb.mokky.dev/CarDetail"); 
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

</script>

<template>
    <div v-if="item && item.title" class="h-screen container max-w-sm">
        <div class="flex relative  ">
        <RouterLink to="/Main">
            <img src="/src/assets/icons/button_back.svg" class=" absolute top-4 left-2 hover:scale-110 transition duration-200"/>
        </RouterLink>
            <img :src="item.detailimg" alt="Car" class="w-360 h-auto mt-3"/>
            <img
                src="/src/assets/icons/button_edit.svg"
                class="absolute top-4 right-2 hover:scale-110 transition duration-200"
                @click="isModalOpen = true"
                />
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
                    <img :src="item.avatar" alt="item Avatar" class="w-10 h-10 rounded-full"/>
                    <h3 class="text-sm font-medium">{{ item.name }}</h3>
                </div>
                <p class="text-sm text-gray-500">{{ item.date }}</p>
            </div>
        </div>

        <div class="mt-5 gap-2">
            <h3 class="text-lg font-light italic ml-3">Найдено:4</h3>
            <img src="/src/assets/images/user.png" class=""/>
            <img src="/src/assets/images/user.png" class=""/>
            <img src="/src/assets/images/user.png" class=""/>
            <img src="/src/assets/images/user.png" class=""/>
        </div>
    </div>


    <div v-if="isModalOpen" class="fixed inset-0 bg-white bg-opacity-50 flex items-center justify-center transition-opacity duration-300  ">
    <div class="bg-white rounded-lg w-full max-w-[390px] p-4 ">
        <div class="flex justify-between items-center my-2 sticky top-0 bg-white z-10 p-2">
            <h1 class="text-2xl italic">Редактировать заявку</h1>
            <img src="/src/assets/icons/ic_close.svg" class="w-6 h-6 hover:scale-110 transition duration-200 cursor-pointer"
                @click="isModalOpen = false"
            />
        </div>

        <form @submit.prevent="submitForm" class="space-y-5 overflow-y-scroll max-h-[90vh] ">
            <div>
                <label class="block text-sm font-medium">Что хотите сделать*</label>
                    <el-select
                        v-model="formData.action" 
                        size="large" 
                        style="width: 100%; height: 35px;"
                        >
                        <el-option value="Продам" label="Продам"></el-option>
                        <el-option value="Куплю" label="Куплю"></el-option>
                        </el-select>

            </div>


            <div>
                <label class="block text-sm font-medium">Категория*</label>
                <el-select
                    v-model="formData.category" 
                    size="large" 
                    style="width: 100%; height: 35px;"
                    >
                    <el-option value="Авто" label="Авто"></el-option>
                    <el-option value="Недвижимость" label="Недвижимость"></el-option>
                    </el-select>
            </div>

            <div>
                <label class="block text-sm font-medium">Заголовок*</label>
                <input placeholder="Toyota Camry 25" v-model="formData.title" type="text" class="w-full p-2 border border-gray-200 rounded-sm text-sm text-zinc-600">
            </div>

            <div>
                <label class="block text-sm font-medium">Хештеги</label>
                <div class="flex flex-wrap gap-1 mt-2 w-full p-2 border border-gray-200 rounded-sm ">
                    <button
                        v-for="(tag, index) in tags"
                        :key="index"
                        @click="toggleTag(index)"
                        class="px-3 py-1 rounded-full  text-sm transition-all my-1 flex items-center gap-1 text-zinc-900"
                        :class="{ 'bg-purple-200': tag.selected, 'bg-gray-200': !tag.selected }"
                    >
                        {{ tag.text }}
                        <span 
                            @click.stop="removeTag(index)" 
                            class="text-red-500 font-bold cursor-pointer"
                        >
                            ✖
                        </span>
                    </button>
                </div>
            </div>

            <div>
                <label class="block text-sm font-medium">Город</label>
                <el-select
                        v-model="formData.location" 
                        size="large" 
                        style="width: 100%; height: 35px;"
                        >
                        <el-option value="Астана" label="Астана"></el-option>
                        <el-option value="Алматы" label="Алматы"></el-option>
                        </el-select>
            </div>

            <div>
                <label class="block text-sm font-medium">Цена</label>
                <input
                    v-model="formattedPrice"
                    type="text"
                    inputmode="numeric"
                    class="w-full p-2 border border-gray-200 rounded-sm text-sm text-zinc-900 "
                />
            </div>

            <div>
                <label class="block text-sm font-medium">Описание*</label>
                <textarea
                v-model="formData.description" 
                class="w-full p-2 border border-gray-200 rounded-sm text-sm text-zinc-900" 
                rows="4">
                </textarea>
            </div>

            <div class="relative">
                <label class="block text-lg font-medium mb-2">Добавьте фото*</label>
                <div class="flex gap-4 items-center">
                    <div class="relative w-22 h-22 flex items-center justify-center bg-sky-100 border-2 border-blue-400 rounded-2xl cursor-pointer">
                        <input type="file" class="absolute inset-0 opacity-0 cursor-pointer" @change="previewImage">
                        <img src="/src/assets/icons/ic_plus.svg" alt="Добавить" class="w-7 h-7">
                    </div>
                    <div class="flex gap-2 mt-2 overflow-x-auto max-w-full">
                        <div v-for="(url, index) in previewUrls" :key="index" class="relative w-22 h-20 flex-shrink-0">
                            <img :src="url" class="w-full h-full object-cover rounded-lg">
                        </div>
                    </div>
                </div>
            </div>

            <button type="submit" class="w-full bg-blue-500 text-white py-3 rounded-xl hover:bg-blue-700 disabled:bg-gray-300">
                Сохранить
            </button>
            <button type="button" @click="resetForm" class="w-full text-red-500 py-2 rounded-xl hover:border-stone-300 border transition duration-200 hover:text-black hover:bg-stone-100">
                Удалить
            </button>
        </form>
    </div>
</div>

</template>


