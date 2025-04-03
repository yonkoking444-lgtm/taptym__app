<script setup>
import { computed, onMounted, ref } from "vue";
import { useToast } from "vue-toastification";

const toast = useToast();
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
            formData.value.category &&
            formData.value.title &&
            formData.value.location &&
            formData.value.price &&
            formData.value.description &&
            formData.value.photo.length > 0
});

const submitForm = async () => {
    if (!userValid.value) {
        console.log("Заполните все поля!");
        return;
    }

    const { photo, map, hashtag, ...payload } = formData.value;

    try {
        const response = await fetch("https://e27f20bf16c931eb.mokky.dev/Createitem", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) throw new Error("Ошибка при сохранении");

        toast.success("Форма успешно отправлена!", { timeout: 3000 });
    } catch (error) {
        toast.error("Ошибка: " + error.message, { timeout: 3000 });
    }
};


const tags = ref([
    { text: "#Продам", selected: true },
    { text: "#Куплю", selected: false },
]);

const previewUrls = ref([]);

const toggleTag = (index) => {
    tags.value[index].selected = !tags.value[index].selected;
};

const removeTag = (index) => {
    tags.value.splice(index, 1);
    hashtags.value.splice(index, 1);
};



const points = ref(20);

const addPoints = () => {
    points.value += 10; 
};


const CardisModalOpen = ref(false)
const CategoryopenModal = ref(false);
const CityisModalOpen = ref(false);
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
const categories = ["Прочее", "Авто", "Жильё", "Услуги"];

const selectCategory = (category) => {
    selectedCategory.value = category;
    openModal.value = false;
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
    openModal.value = false;
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
        hashtags.value.push({ text: tagText, selected: false });
        console.log("Added tag:", hashtags.value);
        newTag.value = "";
    } else {
        console.log("Tag already exists.");
    }
};

const showInput = ref(true);


    const saveTags = () => {
    HeshtegModalOpen.value = false;
    console.log('Selected Tags:', hashtags.value);
    };

    const tagText = ref('');



    
const isModalOpen = ref(false);
const currentIndex = ref(0);


    const previewImage = (event) => {
    const file = event.target.files[0];
    if (file) {
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
                    <button
                        class="w-full px-4 py-2 border rounded-lg text-left mt-1 text-zinc-400"
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
                        class=" w-96 bg-white rounded-t-xl p-4 text-black" 
                        @click.stop
                        >
                        <p class="text-center font-base text-lg mb-2 italic">Выберите категорию</p>
                        <ul>
                            <li
                            v-for="category in categories"
                            :key="category"
                            @click="selectCategory(category)"
                            class="p-4 border-y border-zinc-300 cursor-pointer flex justify-between items-center"
                            >
                            {{ category }}
                            <span v-if="category === selectedCategory" class="text-blue-500">
                                <img src="/src/assets/icons/ic_check.svg">
                            </span>
                            </li>
                        </ul>
                        </div>
                    </div>
                </div>

                <div>
                    <label class="block text-sm font-medium">Заголовок*</label>
                    <input placeholder="Toyota Camry 25" v-model="formData.title" type="text" 
                        class="w-full p-2 border border-gray-200 rounded-sm text-sm text-zinc-600">
                </div>
            
            
                <div>
                    <label class="block text-sm font-medium">Хештеги*</label>
                    <div class="flex flex-wrap gap-2 mt-2 p-2 border border-gray-200 rounded-md">
                    <button @click="HeshtegModalOpen = true" v-for="(hashtag, index) in hashtags" :key="index" 
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
                            <button v-for="(hashtag, index) in hashtags" :key="index" class="px-3 py-1 rounded-full text-sm flex items-center gap-1"
                                :class="hashtag.selected ? 'bg-purple-200' : 'bg-gray-200'">
                                {{ hashtag.text }}
                                <span @click.stop="removeTag(index)" class="text-red-500 font-bold cursor-pointer">✖</span>
                            </button>
                            </div>
                            
                            
                            <input v-if="showInput" v-model="newTag" @keyup.enter="addTag" class=" before:content-['#'] before:text-blue-500 before:absolute before:left-2 border-blue-500 outline-none p-1 w-full border-b-2 border-b-blue-500 mt-50 text-sick-500" />


                            <div class="relative">
                            <button @click="saveTags" class="text-blue-500 absolute bottom-70 right-0">Сохранить</button>
                            <button @click="saveTags" class="text-blue-500 absolute -top-10 right-1"><img src="/src/assets/icons/button_add.svg" alt=""></button>
                        </div>
                    </div>
                </div>
                </div>

                <div>
                    <label class="block text-gray-700 font-medium">Город</label>
                    <button
                    class="w-full px-4 py-2 border border-zinc-400 rounded-lg text-left mt-1 text-zinc-400"
                    @click="CityisModalOpen = true"
                    >
                    {{ selectedCity || "Выберите город" }}
                    </button>



                <div
                    v-if="CityisModalOpen"
                    class="fixed inset-0 flex items-end justify-center bg-white z-50"
                    style="background: rgba(0, 0, 0, 0.3)"
                    >
                    <div class="w-96 bg-white rounded-t-xl p-4 text-black">
                        <div class="flex items-center justify-between">
                        <button class="text-blue-500 text-sm" @click="CityisModalOpen = false">
                            Назад
                        </button>
                        <p class="text-lg italic text-gray-800">Выберите ваш город</p>
                        <div class="w-8"></div>
                        </div>

                        <div class="p-4">
                            <div class="relative flex justify-center text-center text-gray-800">
                                <input
                                    type="text"
                                    v-model="searchQuery"
                                    placeholder="Поиск"
                                    class="w-full p-3 border border-zinc-400 rounded-lg  pl-10"
                                    />
                                    <img
                                        src="/src/assets/icons/ic_search.svg"
                                        class="absolute left-3 top-3 w-5 h-5"
                                />
                            </div>
                        </div>

                            <ul class="h-110 overflow-y-auto">
                                <li
                                    v-for="city in filteredCities()"
                                    :key="city.ids"
                                    @click="selectCity(city)"
                                    class="p-4 border-b border-zinc-400 cursor-pointer flex justify-between items-center "
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
                    <label class="block text-lg font-medium mb-2">Добавьте фото*</label>
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
                                    <button class="text-blue-500 font-medium w-1/2" @click="DelateModalOpen=false">Отмена</button>
                                        <div class="border-1"/>
                                    <button class="text-red-500 font-medium w-1/2" @click="deleteImage">Удалить</button>
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
                    <button @click="CardisModalOpen = true" class="flex items-center text-[#2580D5] hover:text-[#1E6BB8] gap-2">
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
                        <button 
                        @click="selectedCard = 'kaspi'" 
                        :class="selectedCard === 'kaspi' ? 'border-[#2580D5] bg-[#E6F0FB]' : 'border-gray-200'"
                        class="w-full p-3 border rounded-md mb-2 flex items-center justify-start"
                        >
                        <img src="/src/assets/icons/ic_kaspi.svg" alt="Kaspi" class="w-6 h-6 mr-2"> Kaspi
                        </button>
                        
                        <button 
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
