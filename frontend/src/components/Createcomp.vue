<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";
import { useAuthStore } from "../stores/auth";
import { BUYER_REQUESTS_API_URL, CAR_API_URL, SELLER_CARS_API_URL, UPLOAD_API_URL } from "../services/listings";

const toast = useToast();
const router = useRouter();
const authStore = useAuthStore();
authStore.hydrate();
const formData = ref({
    action: "",
    category: "",
    title: "",
    location: "",
    price: "",
    description: "",
});

const userValid = computed(() => {
    return formData.value.action &&
            formData.value.title &&
            selectedCategory.value &&
            selectedCity.value &&
            priceInput.value &&
            formData.value.description &&
            (formData.value.action === "Куплю" || previewUrls.value.length > 0)
});

const submitForm = async () => {
    if (!userValid.value) {
        console.log("Заполните все поля!");
        return;
    }

    const price = Number(priceInput.value.replace(/\D/g, ""));
    const payload = {
        ...formData.value,
        category: selectedCategory.value,
        location: selectedCity.value,
        price,
        tags: hashtags.value.filter((tag) => tag.selected).map((tag) => tag.text),
        name: authStore.currentUser?.name || "Гость",
        avatar: authStore.currentUser?.imageUrl || "/src/assets/images/profile-avatar.png",
        owner_email: authStore.currentUser?.email || null,
    };

    try {
        const uploadedImages = await Promise.all(selectedFiles.value.map(async (file) => {
            const formData = new FormData();
            formData.append("file", file);
            const uploadResponse = await fetch(UPLOAD_API_URL, {
                method: "POST",
                body: formData,
            });
            if (!uploadResponse.ok) throw new Error("Ошибка загрузки фото");
            const uploadResult = await uploadResponse.json();
            return uploadResult.url;
        }));

        payload.image = uploadedImages[0] || null;
        payload.detailimg = uploadedImages[1] || null;
        const createUrl = formData.value.action === "Куплю" ? BUYER_REQUESTS_API_URL : SELLER_CARS_API_URL;
        const response = await fetch(createUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) throw new Error("Ошибка при сохранении");

        toast.success("Форма успешно отправлена!", { timeout: 3000 });
        await router.push({ name: "Main" });
    } catch (error) {
        toast.error("Ошибка: " + error.message, { timeout: 3000 });
    }
};


const previewUrls = ref([]);
const selectedFiles = ref([]);

const removeTag = (index) => {
    hashtags.value.splice(index, 1);
};

const toggleHashtag = (index) => {
    hashtags.value[index].selected = !hashtags.value[index].selected;
};



const points = ref(20);

const addPoints = () => {
    points.value += 10; 
};


const CardisModalOpen = ref(false)
const CategoryopenModal = ref(false);
const CityisModalOpen = ref(false);
const CarTitleModalOpen = ref(false);
const HeshtegModalOpen = ref(false)
const DelateModalOpen =ref(false)


const openModal = () => {
    DelateModalOpen.value = true
    HeshtegModalOpen.value = true;
    CardisModalOpen.value = true;
    CityisModalOpen.value = true;
    CategoryopenModal.value = true;
};

const closeModal = () => {
    DelateModalOpen.value = false
    HeshtegModalOpen.value = false;
    CardisModalOpen.value = false;
    CategoryopenModal.value = false;
    CityisModalOpen.value = false;
};

const selectedCategory = ref("Прочее");
const categories = ["Прочее", "Авто", "Запчасти", "Услуги"];
const carTitleSuggestions = [
    "Toyota Camry 25",
    "Honda CR-V 2020",
    "Lexus RX 350",
    "Mercedes-Benz E200 2021",
];
const carTitleSearch = ref("");
const filteredCarTitles = () => carTitleSuggestions.filter((title) =>
    title.toLowerCase().includes(carTitleSearch.value.toLowerCase())
);
const selectCarTitle = (title) => {
    formData.value.title = title;
    CarTitleModalOpen.value = false;
    carTitleSearch.value = "";
};

const selectCategory = (category) => {
    selectedCategory.value = category;
    CategoryopenModal.value = false;
};


const selectedCard = ref(null);

const cities = ref([]);
const selectedCity = ref("");


onMounted(async () => {
try {
    const response = await fetch(
        "https://products.halyklife.kz/gateway/product/products/dictionaries/?name=cityVillage"
    );
    const data = await response.json();
    cities.value = data; 
} catch (error) {
    console.error("Ошибка загрузки данных:", error);
}
});

const selectCity = (city) => {
    selectedCity.value = city.nameRu; 
    CityisModalOpen.value = false;
};

const searchQuery = ref();

const filteredCities = () => {
    return cities.value.filter((city) =>
    city.nameRu.toLowerCase().includes((searchQuery.value || "").toLowerCase())
    );
};



const hashtags = ref([
    { text: '#Купить', selected: true },
    { text: '#MercedesBenz', selected: false },

]);

watch(() => formData.value.action, (action) => {
    if (!action || !hashtags.value.length) return;
    hashtags.value[0].text = action === "Продам" ? "#Продам" : "#Купить";
    hashtags.value[0].selected = true;
});

const newTag = ref("");

const addTag = () => {
    let tagText = newTag.value.trim();
    
    if (!tagText) {
        console.log("Tag is empty.");
        return;
    }

    if (!tagText.startsWith("#")) {
        tagText = `#${tagText}`;
    }

    if (!hashtags.value.some(tag => tag.text.toLowerCase() === tagText.toLowerCase())) {
        hashtags.value.push({ text: tagText, selected: true });
        newTag.value = "";
    }
};

const showInput = ref(true);


    const saveTags = () => {
    HeshtegModalOpen.value = false;
    console.log('Selected Tags:', hashtags.value);
    };

    
const isModalOpen = ref(false);
const currentIndex = ref(0);


    const previewImage = (event) => {
    const file = event.target.files[0];
    if (file) {
        selectedFiles.value.push(file);
        const reader = new FileReader();
        reader.onload = (e) => {
        previewUrls.value.push(e.target.result);
        };
        reader.readAsDataURL(file);
    }
    };

    const openModalimg = (index) => {
    currentIndex.value = index;
    isModalOpen.value = true;
    };

    const closeModalimg = () => {
    isModalOpen.value = false;
    };

    const deleteImage = () => {
    previewUrls.value.splice(currentIndex.value, 1);
    if (previewUrls.value.length === 0) {
        closeModalimg();
    } else {
        currentIndex.value = Math.max(0, currentIndex.value - 1);
    }
    };




    const priceInput = ref("");
    const formatPrice = (event) => {
    let rawValue = event.target.value.replace(/\D/g, ""); 

    if (rawValue === "") {
        priceInput.value = "";
        return;
    }
    rawValue = rawValue.replace(/\B(?=(\d{3})+(?!\d))/g, " "); 
    if (event.inputType === "deleteContentBackward") {
        priceInput.value = rawValue; 
    } else {
        priceInput.value = rawValue + " ₸"; 
    }
    };
</script>




<template>
    <div>
        <div class="rounded-lg w-full max-w-[360px] p-4">
            <form @submit.prevent="submitForm" class="space-y-5 overflow-y-scroll max-h-[90vh]">
                <div>
                    <label class="block text-sm font-medium">Что хотите сделать*</label>
                    <el-select v-model="formData.action" size="large" style="width: 100%; height: 35px;">
                        <el-option value="Продам" label="Продам"></el-option>
                        <el-option value="Куплю" label="Куплю"></el-option>
                    </el-select>
                </div>

                <div>
                    <label class="block text-gray-700 font-medium">Категория*</label>
                    <button type="button"
                        class="w-full px-4 py-3 border border-zinc-300 rounded-xl text-left mt-1 text-black font-normal bg-white hover:border-blue-500 transition-colors"
                        @click="CategoryopenModal = true"
                    >
                        {{ selectedCategory || "Выберите категорию" }}
                    </button>

                    <div 
                        v-if="CategoryopenModal" 
                        class=" fixed inset-0 flex items-end justify-center bg-opacity-30 bg-white z-50" style="background: rgba(0, 0, 0, 0.3)"
                        @click="CategoryopenModal = false"
                    >
                        <div 
                        class="w-full max-w-md bg-white rounded-t-3xl p-5 text-black shadow-2xl" 
                        @click.stop
                        >
                        <div class="flex items-center justify-between mb-4">
                            <p class="font-semibold text-xl">Категория</p>
                            <button type="button" class="text-blue-600 text-sm" @click="CategoryopenModal = false">Готово</button>
                        </div>
                        <p class="text-sm text-zinc-500 mb-3">Выберите тип объявления</p>
                        <ul class="space-y-2">
                            <li
                            v-for="category in categories"
                            :key="category"
                            @click="selectCategory(category)"
                            class="p-4 border border-zinc-200 rounded-xl cursor-pointer flex justify-between items-center hover:border-blue-500 hover:bg-blue-50 transition-colors"
                            >
                            <span class="font-medium">{{ category }}</span>
                            <span v-if="category === selectedCategory" class="text-blue-600 font-bold">✓</span>
                            <span v-else class="w-5 h-5 rounded-full border border-zinc-300"></span>
                            </li>
                        </ul>
                        </div>
                    </div>
                </div>

                <div>
                    <label class="block text-sm font-medium">Заголовок*</label>
                    <button v-if="selectedCategory === 'Авто'" type="button"
                        @click="CarTitleModalOpen = true"
                        class="w-full p-3 border border-gray-300 rounded-xl text-left text-black font-normal bg-white hover:border-blue-500 transition-colors">
                        {{ formData.title || "Выберите машину" }}
                    </button>
                    <input v-else placeholder="Введите заголовок" v-model="formData.title" type="text"
                        class="w-full p-2 border border-gray-200 rounded-sm text-sm text-black font-normal">

                    <div v-if="CarTitleModalOpen" class="fixed inset-0 flex items-end justify-center z-50" style="background: rgba(0, 0, 0, 0.3)" @click="CarTitleModalOpen = false">
                        <div class="w-full max-w-md max-h-[92vh] bg-white rounded-t-3xl p-5 text-black shadow-2xl" @click.stop>
                            <div class="flex items-center justify-between mb-4">
                                <button type="button" class="text-blue-600 text-base font-medium" @click="CarTitleModalOpen = false">Назад</button>
                                <p class="text-xl font-bold text-black">Выберите машину</p>
                                <div class="w-8"></div>
                            </div>
                            <input v-model="carTitleSearch" type="text" placeholder="Поиск марки или модели"
                                class="w-full p-3 mb-3 border border-zinc-400 rounded-xl text-black placeholder:text-zinc-400">
                            <ul class="max-h-[55vh] overflow-y-auto">
                                <li v-for="title in filteredCarTitles()" :key="title" @click="selectCarTitle(title)"
                                    class="p-4 border-b border-zinc-300 cursor-pointer text-black text-lg font-normal hover:bg-zinc-50">
                                    {{ title }}
                                </li>
                            </ul>
                            <button v-if="carTitleSearch.trim()" type="button" class="w-full mt-4 p-3 text-blue-600 border border-blue-500 rounded-xl" @click="selectCarTitle(carTitleSearch.trim())">
                                Использовать введённое
                            </button>
                        </div>
                    </div>
                </div>
            
            
                <div>
                    <label class="block text-sm font-medium">Хештеги*</label>
                    <div class="flex flex-wrap gap-2 mt-2 p-2 border border-gray-200 rounded-md">
                    <button type="button" @click="HeshtegModalOpen = true" v-for="(hashtag, index) in hashtags" :key="index" 
                        class="px-3 py-1 rounded-full text-sm flex items-center gap-1"
                        :class="hashtag.selected ? 'bg-purple-200' : 'bg-gray-200'">
                        {{ hashtag.text }}
                        <span @click.stop="removeTag(index)" class="text-red-500 font-bold cursor-pointer">✖</span>
                    </button>
                    </div>
                    
                    <div
                        v-if="HeshtegModalOpen" class="fixed inset-0 flex items-center justify-center bg-opacity-30 bg-white z-50 " style="background: rgba(0, 0, 0, 0.3)">
                        <div  class="bg-white p-4 rounded-md w-96 h-90 ">
                            <h3 class="text-lg font-semibold mb-2">Добавить хештеги</h3>
                            <div class="flex flex-wrap gap-2 mb-2">
                            <button type="button" @click="toggleHashtag(index)" v-for="(hashtag, index) in hashtags" :key="index" class="px-3 py-1 rounded-full text-sm flex items-center gap-1 bg-gray-200 focus:outline-none focus:ring-0">
                                {{ hashtag.text }}
                                <span @click.stop="removeTag(index)" class="text-red-500 font-bold cursor-pointer">✖</span>
                            </button>
                            </div>
                            
                            
                            <div v-if="showInput" class="flex items-center border-b-2 border-blue-500 mt-50">
                                <span class="text-lg text-zinc-700">#</span>
                                <input
                                    v-model="newTag"
                                    @keyup.enter.prevent="addTag"
                                    placeholder="Введите хэштег"
                                    class="outline-none p-1 w-full text-sick-500"
                                />
                            </div>


                            <div class="relative">
                            <button type="button" @click="saveTags" class="text-blue-500 absolute bottom-70 right-0">Сохранить</button>
                            <button type="button" @click="addTag" class="text-blue-500 absolute -top-10 right-1"><img src="/src/assets/icons/button_add.svg" alt="Добавить хэштег"></button>
                        </div>
                    </div>
                </div>
                </div>

                <div>
                    <label class="block text-gray-700 font-medium">Город</label>
                    <button type="button"
                    class="w-full px-4 py-2 border border-zinc-400 rounded-lg text-left mt-1 text-zinc-400"
                    @click="CityisModalOpen = true"
                    >
                    {{ selectedCity || "Выберите город" }}
                    </button>



                <div
                    v-if="CityisModalOpen"
                    class="fixed inset-0 flex items-end justify-center z-50"
                    style="background: rgba(0, 0, 0, 0.3)"
                    >
                    <div class="w-full max-w-md max-h-[92vh] bg-white rounded-t-3xl p-5 text-black shadow-2xl">
                        <div class="flex items-center justify-between mb-4">
                        <button type="button" class="text-blue-600 text-base font-medium" @click="CityisModalOpen = false">
                            Назад
                        </button>
                        <p class="text-xl font-bold text-black">Выберите ваш город</p>
                        <div class="w-8"></div>
                        </div>

                        <div class="mb-4">
                            <div class="relative flex justify-center text-center text-black">
                                <input
                                    type="text"
                                    v-model="searchQuery"
                                    placeholder="Поиск"
                                    class="w-full p-3 border border-zinc-400 rounded-xl pl-10 text-black font-medium placeholder:text-zinc-400"
                                    />
                                    <img
                                        src="/src/assets/icons/ic_search.svg"
                                        class="absolute left-3 top-3 w-5 h-5"
                                />
                            </div>
                        </div>

                            <ul class="max-h-[62vh] overflow-y-auto">
                                <li
                                    v-for="city in filteredCities()"
                                    :key="city.ids"
                                    @click="selectCity(city)"
                                    class="p-4 border-b border-zinc-300 cursor-pointer flex justify-between items-center text-black text-lg font-normal hover:bg-zinc-50"
                                >
                                    {{ city.nameRu }}
                                    <span v-if="city.nameRu === selectedCity" class="text-blue-500">
                                    <img src="/src/assets/icons/ic_navigation.svg" class="w-5 h-5" />
                                    </span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div>
                    <label class="block text-sm font-medium">Цена</label>
                    <input 
                    v-model="priceInput" 
                    type="text" 
                    inputmode="numeric"
                    @input="formatPrice"
                    class="w-full p-2 border border-gray-200 rounded-sm text-sm text-zinc-900">
                </div>

                <div>
                    <label class="block text-sm font-medium">Описание*</label>
                    <textarea placeholder="Добавьте текст" v-model="formData.description" class="w-full p-2 border border-gray-200 rounded-sm text-sm text-zinc-900" rows="4"></textarea>
                </div>

                <div class="relative">
                    <label class="block text-lg font-medium mb-2">Добавьте фото{{ formData.action === 'Продам' ? '*' : '' }}</label>
                    <div class="flex gap-4 items-center">
                        <div class="relative w-22 h-22 flex items-center justify-center bg-sky-100 border-2 border-blue-400 rounded-2xl cursor-pointer">
                            <input type="file" class="absolute inset-0 opacity-0 cursor-pointer" @change="previewImage">
                            <img src="/src/assets/icons/ic_plus.svg" alt="Добавить" class="w-7 h-7">
                        </div>

                        <div class="flex gap-2 mt-2 overflow-x-auto max-w-full">
                            <div v-for="(url, index) in previewUrls" :key="index" class="relative w-25 h-25 flex-shrink-0 cursor-pointer" @click="openModalimg(index)">
                                <img :src="url" class="w-full h-full object-cover rounded-lg">
                            </div>
                        </div>
                    </div>

                    <div v-if="isModalOpen" class="fixed inset-0 bg-black flex flex-col items-center justify-center z-50">
                        <div class="absolute top-4 left-4 text-white text-lg cursor-pointer flex" @click="closeModalimg">
                            <img width="6" height="6" src="/src/assets/icons/ic_back.svg" alt=""> Назад
                        </div>                        
                        <div>
                            <div class="absolute top-4 right-4 text-red-500 text-lg cursor-pointer" @click="DelateModalOpen=true">Удалить</div>

                            <div v-if="DelateModalOpen"  class="z-55 fixed inset-0 flex items-center justify-center bg-white bg-opacity-50" style="background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px);">
                                <div class="bg-white/70 p-5 rounded-lg shadow-lg w-70 h-35 text-center">
                                    <p class="text-lg font-light italic">Хотите удалить фото?</p>
                                    <p class="text-sm text-gray-500">Вы точно хотите удалить фото?</p>

                                    <div class="flex justify-between mt-6 border-t-1 ">
                                    <button type="button" class="text-blue-500 font-medium w-1/2" @click="DelateModalOpen=false">Отмена</button>
                                        <div class="border-1"/>
                                    <button type="button" class="text-red-500 font-medium w-1/2" @click="deleteImage">Удалить</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <el-carousel :interval="5000" arrow="always">
                            <img :src="previewUrls[currentIndex]" class="w-full h-auto max-h-screen object-contain">
                            <el-carousel-item v-for="(url, index) in previewUrls" :key="index">
                                <img :src="url" class="w-full h-auto max-h-screen object-contain">
                            </el-carousel-item>
                        </el-carousel>
                    </div>
                </div>


                <div class="flex justify-between items-center">
                    <div>
                    <p class="text-base font-normal">Мои баллы</p>
                    <p class="text-orange-500 text-xl font-extralight">{{ points }} баллов</p>
                    </div>
                    <button type="button" @click="CardisModalOpen = true" class="flex items-center text-[#2580D5] hover:text-[#1E6BB8] gap-2">
                    <img src="/src/assets/shape.svg" alt="">
                    <span class="ml-1 text-lg">Добавить</span>
                    </button>
                </div>

                <div v-if ="CardisModalOpen" class="fixed inset-0 flex items-end justify-center bg-white z-50 -bottom-5" style="background: rgba(0, 0, 0, 0.3);"
                        @click="CardisModalOpen = false"
                >
                        <div 
                        class="w-96 bg-white rounded-t-xl p-4 text-black" 
                        @click.stop >
                        <h2 class="text-lg font-normal text-center italic mb-6">Добавить баллы</h2>
                    <div>
                        <button type="button"
                        @click="selectedCard = 'kaspi'" 
                        :class="selectedCard === 'kaspi' ? 'border-[#2580D5] bg-[#E6F0FB]' : 'border-gray-200'"
                        class="w-full p-3 border rounded-md mb-2 flex items-center justify-start"
                        >
                        <img src="/src/assets/icons/ic_kaspi.svg" alt="Kaspi" class="w-6 h-6 mr-2"> Kaspi
                        </button>
                        
                        <button type="button"
                        @click="selectedCard = 'other'" 
                        :class="selectedCard === 'other' ? 'border-[#2580D5] bg-[#E6F0FB]' : 'border-gray-200'"
                        class="w-full p-3 border rounded-md flex items-center justify-start"
                        >
                        <img src="/src/assets/icons/ic_card.svg" alt="Card" class="w-6 h-6 mr-2"> Другая карта
                        </button>
                    </div>
                </div>
                </div>

                <button type="submit" :disabled="!userValid" class="w-full bg-blue-500 text-white py-3 rounded-xl hover:bg-blue-700 disabled:bg-gray-300">
                    Создать
                </button>
            </form>
        </div>
    </div>
</template>


<style scoped>
    :deep(.custom-modal) {
    background: rgba(0, 0, 0, 0.8) !important;
    }
    :deep(.el-dialog) {
    background: transparent;
    box-shadow: none;
    }
    .el-carousel__item img {
    border-radius: 10px;
    }
    img {
    width:auto ;
    height: auto;
    object-fit: cover;
    }

</style>
