<script setup>
import { ref, computed, onMounted } from 'vue';
import { RouterLink, useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useToast } from "vue-toastification";
import { useAuthStore } from '../../../stores/auth';
import { CAR_API_URL } from '../../../services/listings';


const route = useRoute();
const router = useRouter();
const toast = useToast();
const authStore = useAuthStore();
authStore.hydrate();

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

const deleteCar = async () => {
    try {
        const response = await fetch(`${CAR_API_URL}/${item.value.id}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error('Не удалось удалить карточку');
        }

        toast.success('Карточка удалена', { timeout: 3000 });
        await router.push({ name: 'Main' });
    } catch (error) {
        toast.error(error instanceof Error ? error.message : 'Ошибка удаления', { timeout: 3000 });
    }
};

const removeExistingPhoto = () => {
    item.value.image = null;
    item.value.detailimg = null;
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
        formData.value.description
    );
});


async function submitForm() {
    if (!isFormValid.value) { 
        toast.error("Пожалуйста, заполните все поля!", { timeout: 3000 });
        return;
    }

    try {
        let image = item.value.image;
        let detailimg = item.value.detailimg;

        if (formData.value.photos.length > 0) {
            const uploadedImages = await Promise.all(formData.value.photos.map(async (file) => {
                const uploadData = new FormData();
                uploadData.append("file", file);
                const uploadResponse = await fetch(`${CAR_API_URL.replace('/api/cars', '/api/uploads')}`, {
                    method: "POST",
                    body: uploadData,
                });
                if (!uploadResponse.ok) throw new Error("Ошибка загрузки фото");
                return (await uploadResponse.json()).url;
            }));
            image = uploadedImages[0] || image;
            detailimg = uploadedImages[1] || uploadedImages[0] || detailimg;
        }

        const response = await fetch(`${CAR_API_URL}/${item.value.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                ...formData.value,
                price: Number(formData.value.price) || null,
                tags: tags.value.filter((tag) => tag.selected).map((tag) => tag.text),
                image,
                detailimg,
                name: authStore.currentUser ? (authStore.currentUser.name || 'Гость') : (item.value.name || 'Гость'),
                avatar: authStore.currentUser ? (authStore.currentUser.imageUrl || '/src/assets/images/profile-avatar.png') : (item.value.avatar || '/src/assets/images/profile-avatar.png'),
            }),
        });

        if (!response.ok) {
            throw new Error("Ошибка при сохранении данных!");
        }
        toast.success("Заявка успешно сохранена!", { timeout: 3000 });
        item.value = await response.json();
        isModalOpen.value = false;

    } catch (error) {
        toast.error(error.message, { timeout: 3000 });
    }
}



onMounted(async () => {
    try {
        const { data } = await axios.get(`${CAR_API_URL}/${route.params.id}`);
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
        tags.value = (data.tags || []).map((tag) => ({ text: tag, selected: true }));


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
            <img :src="item.detailimg || item.image" alt="Car" class="w-full aspect-[4/3] object-contain mt-3"/>
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
                class="px-3 py-1 rounded-full text-black text-sm transition-all my-1 bg-purple-200 focus:outline-none focus:ring-0"
                >
                {{ tag.text }}
                </button>
            </div>

            <div v-if="item" class="flex justify-between items-center mt-3 italic">
                <div class="flex items-center gap-2">
                    <img :src="item.avatar || '/src/assets/images/profile-avatar.png'" alt="Аватар автора" class="w-10 h-10 rounded-full object-cover"/>
                    <h3 class="text-sm font-medium">{{ item.name || 'Гость' }}</h3>
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
                    <el-option value="Запчасти" label="Запчасти"></el-option>
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
                <label class="block text-lg font-medium mb-2">Фото{{ formData.action === 'Продам' ? '*' : '' }}</label>
                <div v-if="item.image || item.detailimg" class="relative w-24 h-24 mb-3">
                    <img :src="item.detailimg || item.image" alt="Текущее фото" class="w-full h-full object-cover rounded-lg">
                    <button type="button" @click="removeExistingPhoto" class="absolute -right-2 -top-2 w-7 h-7 rounded-full bg-red-500 text-white">×</button>
                </div>
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
            <button type="button" @click="deleteCar" class="w-full text-red-500 py-2 rounded-xl hover:border-stone-300 border transition duration-200 hover:text-black hover:bg-stone-100">
                Удалить
            </button>
        </form>
    </div>
</div>

</template>


