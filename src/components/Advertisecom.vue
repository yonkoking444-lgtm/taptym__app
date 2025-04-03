        <script setup>
        import { computed, onMounted, reactive, ref } from "vue";
        import { useToast } from "vue-toastification";

        const toast = useToast();

        const formData = ref({
        title: "",
        location: "",
        price: "",
        description: "",
        });


        const userValid = computed(() => {
        return formData.value.title &&
                formData.value.location &&
                formData.value.price &&
                formData.value.description;
        });

        const hashtags = ref([]);
        const newTag = ref("");
        const showInput = ref(true);

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
            newTag.value = "";
        } else {
            console.log("Tag already exists.");
        }
        };

        const removeTag = (index) => {
        hashtags.value.splice(index, 1);
        };

        const saveTags = () => {
        HeshtegModalOpen.value = false;
        console.log("Selected Tags:", hashtags.value);
        };

        const openAddTagModal = () => {
        showInput.value = true;
        };

        const previewUrls = ref([]);
        const isModalOpen = ref(false);
        const currentIndex = ref(0);



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
            formData.value.price = "";
            return;
        }
        rawValue = rawValue.replace(/\B(?=(\d{3})+(?!\d))/g, " ");
        if (event.inputType === "deleteContentBackward") {
            priceInput.value = rawValue;
        } else {
            priceInput.value = rawValue + " ₸";
        }
        formData.value.price = priceInput.value;
        };

        const HeshtegModalOpen = ref(false);
        const CityisModalOpen = ref(false);
        const selectedCity = ref("");

        const cities = ref([]);
        const searchQuery = ref("");

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

        const filteredCities = () => {
        return cities.value.filter((city) =>
            city.nameRu.toLowerCase().includes((searchQuery.value || "").toLowerCase())
        );
        };

        const selectCity = (city) => {
        selectedCity.value = city.nameRu;
        formData.value.location = city.nameRu;
        CityisModalOpen.value = false;
        };


        onMounted(async () => {
        try {
            const response = await fetch("https://e27f20bf16c931eb.mokky.dev/Advertisements");
            const data = await response.json();
            if (Array.isArray(data) && data.length > 0) {
            const advertisement = data[0];
            formData.value.title = advertisement.text;
            formData.value.price = advertisement.price;
            formData.value.location = advertisement.location;
            formData.value.description = advertisement.description;

            hashtags.value = advertisement.hashtags.map(tag => ({
                text: `#${tag.replace(/^#/, "")}`,
                selected: false
            }));
            }
        } catch (error) {
            console.error("Ошибка загрузки объявления:", error);
        }
        });
        

        
        const submitForm = async () => {
    if (!userValid.value) {
        toast.error("Заполните все поля!", { timeout: 3000 });
        return;
    }

    const updatedData = {
        text: formData.value.title,
        location: formData.value.location,
        price: formData.value.price,
        description: formData.value.description,
    };

    try {
        const response = await fetch(
        "https://e27f20bf16c931eb.mokky.dev/Advertisements/1", 
        {
            method: "PUT", 
            headers: {
        "Content-Type": "application/json",
            },
            body: JSON.stringify(updatedData),
        }
        );

        if (!response.ok) {
        throw new Error("Ошибка при обновлении объявления");
        }

        const data = await response.json();
        toast.success("Объявление успешно обновлено!", { timeout: 3000 });
        console.log("Updated advertisement:", data);
    } catch (error) {
        console.error("Ошибка обновления объявления:", error);
        toast.error("Ошибка обновления объявления", { timeout: 3000 });
    }
    };


        </script>

        <template>
        <div>
            <div class="rounded-lg w-full max-w-[360px] p-4">

            <form @submit.prevent="submitForm" class="space-y-5 overflow-y-scroll max-h-[90vh]">
                <div>
                <label class="block text-sm font-medium">Заголовок*</label>
                <input
                    placeholder="Toyota Camry 25"
                    v-model="formData.title"
                    type="text"
                    class="w-full p-2 border border-gray-200 rounded-sm text-sm text-zinc-600"
                />
                </div>

                <div>
                <label class="block text-sm font-medium">Хештеги*</label>
                <div class="flex flex-wrap gap-2 mt-2 p-2 border border-gray-200 rounded-md">
                    <button
                    type="button"
                    @click="HeshtegModalOpen = true"
                    v-for="(hashtag, index) in hashtags"
                    :key="index"
                    class="px-3 py-1 rounded-full text-sm flex items-center gap-1"
                    :class="hashtag.selected ? 'bg-purple-200' : 'bg-gray-200'"
                    >
                    {{ hashtag.text }}
                    <span @click.stop="removeTag(index)" class="text-red-500 font-bold cursor-pointer">✖</span>
                    </button>
                </div>

                <div
                    v-if="HeshtegModalOpen"
                    class="fixed inset-0 flex items-center justify-center bg-opacity-30 bg-white z-50"
                    style="background: rgba(0, 0, 0, 0.3)"
                >
                    <div class="bg-white p-4 rounded-md w-96 h-90">
                    <h3 class="text-lg font-semibold mb-2">Добавить хештеги</h3>
                    <div class="flex flex-wrap gap-2 mb-2">
                        <button
                        type="button"
                        v-for="(hashtag, index) in hashtags"
                        :key="index"
                        class="px-3 py-1 rounded-full text-sm flex items-center gap-1"
                        :class="hashtag.selected ? 'bg-purple-200' : 'bg-gray-200'"
                        >
                        {{ hashtag.text }}
                        <span @click.stop="removeTag(index)" class="text-red-500 font-bold cursor-pointer">✖</span>
                        </button>
                    </div>

                    <input
                        v-if="showInput"
                        v-model="newTag"
                        @keyup.enter="addTag"
                        class="before:content-['#'] before:text-blue-500 before:absolute before:left-2 border-blue-500 outline-none p-1 w-full border-b-2 border-b-blue-500 text-sick-500"
                    />

                    <div class="relative">
                        <button type="button" @click="saveTags" class="text-blue-500 absolute bottom-5 right-0">
                        Сохранить
                        </button>
                        <button type="button" @click="openAddTagModal" class="text-blue-500 absolute top-5 right-1">
                        <img src="/src/assets/icons/button_add.svg" alt="Add Tag" />
                        </button>
                    </div>
                    </div>
                </div>
                </div>

                <div>
                <label
                
                class="block text-gray-700 font-medium">Город</label>
                <input
                    v-model="formData.location"
                    type="button"
                    class="w-full px-4 py-2 border border-zinc-400 rounded-lg text-left mt-1 text-zinc-400"
                    @click="CityisModalOpen = true"
                >
                    {{ selectedCity || "Выберите город" }}
                </input>

                <div
                    v-if="CityisModalOpen"
                    class="fixed inset-0 flex items-end justify-center bg-white z-50"
                    style="background: rgba(0, 0, 0, 0.3)"
                >
                    <div class="w-96 bg-white rounded-t-xl p-4 text-black">
                    <div class="flex items-center justify-between">
                        <button type="button" class="text-blue-500 text-sm" @click="CityisModalOpen = false">
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
                            class="w-full p-3 border border-zinc-400 rounded-lg pl-10"
                        />
                        <img src="/src/assets/icons/ic_search.svg" class="absolute left-3 top-3 w-5 h-5" />
                        </div>
                    </div>

                    <ul class="h-110 overflow-y-auto">
                        <li
                        v-for="city in filteredCities()"
                        :key="city.ids"
                        @click="selectCity(city)"
                        class="p-4 border-b border-zinc-400 cursor-pointer flex justify-between items-center"
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
                    v-model="formData.price"
                    type="text"
                    inputmode="numeric"
                    @input="formatPrice"
                    class="w-full p-2 border border-gray-200 rounded-sm text-sm text-zinc-900"
                />
                </div>

                <div>
                <label class="block text-sm font-medium">Описание*</label>
                <textarea
                    placeholder="Добавьте текст"
                    v-model="formData.description"
                    class="w-full p-2 border border-gray-200 rounded-sm text-sm text-zinc-900"
                    rows="4"
                ></textarea>
                </div>

                <button
                type="submit"
                :disabled="!userValid"
                class="w-full bg-blue-500 text-white py-3 rounded-xl hover:bg-blue-700 disabled:bg-gray-300"
                >
                Изменить
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
        width: auto;
        height: auto;
        object-fit: cover;
        }
        </style>
