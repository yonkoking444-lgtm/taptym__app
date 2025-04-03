    <script setup>
    import { ref } from 'vue';

    const points = ref(20);
    const history = ref([
    { amount: 1, date: '14 июля 20:23' },
    { amount: 2, date: '14 июля 12:41' },
    { amount: 1, date: '17 июля 18:03' },
    { amount: 3, date: '19 июля 21:16' }
    ]);

    const CardisModalOpen = ref(false);
    const otherCardModalOpen = ref(false);
    const selectedCard = ref(null);

    const cardNumber = ref('');
    const expiryDate = ref('');
    const cvc = ref('');

    const addCard = () => {
    console.log('Добавлена карта:', {
        cardNumber: cardNumber.value,
        expiryDate: expiryDate.value,
        cvc: cvc.value,
    });
    };
    </script>

    <template>
    <div class="p-3">
        <div class="flex items-center justify-between">
        <router-link to="/profile">
            <img src="@/assets/icons/button_back.svg" alt="Back" />
        </router-link>
        <h1 class="text-center text-lg italic font-light">Мои баллы</h1>
        <div class="w-4"></div>
        </div>

        <p class="text-orange-500 text-lg italic mt-4">{{ points }} баллов</p>
        <p class="text-gray-700 text-base">
        Баллы нужны для того, чтобы создавать заявки.<br />
        <span class="italic font-medium">1 балл = 1 заявка</span>
        </p>

        <h2 class="text-gray-400 mt-6 text-sm">История</h2>
        <div v-if="history.length === 0" class="text-gray-400 text-center mt-2">
        История пока пустая
        </div>
        <div v-else class="mt-3 space-y-2">
        <div v-for="(item, index) in history" :key="index" class="flex justify-between items-center">
            <div class="flex items-center">
            <img src="/src/assets/icons/ic_bonuses.svg">
            <span>{{ item.amount }} балл</span>
            </div>
            <span class="text-gray-500 text-sm">{{ item.date }}</span>
        </div>
        </div>

        <button 
        @click="CardisModalOpen = true"
        class="fixed bottom-5 left-1/2 transform -translate-x-1/2 w-[360px] bg-blue-500 text-white py-3 rounded-xl hover:bg-blue-700 shadow-md">
        Добавить
        </button>

        <div v-if="CardisModalOpen" 
        class="fixed inset-0 flex items-end justify-center bg-opacity-50 z-50" style="background: rgba(0, 0, 0, 0.3)"
        @click="CardisModalOpen = false">
        <div class="w-96 bg-white rounded-t-xl p-4 text-black" @click.stop>
            <div class="text-center text-lg font-normal italic mb-6">Способ оплаты</div>

            <button @click="selectedCard = 'kaspi'" 
                    :class="selectedCard === 'kaspi' ? 'border-[#2580D5] bg-[#E6F0FB]' : 'border-gray-200'"
                    class="w-full p-3 border rounded-md mb-2 flex items-center">
            <img src="/src/assets/icons/ic_kaspi.svg" alt="Kaspi" class="w-6 h-6 mr-2"> Kaspi
            </button>

            <button @click="CardisModalOpen = false; otherCardModalOpen = true"
                    class="w-full p-3 border rounded-md flex items-center">
            <img src="/src/assets/icons/ic_card.svg" alt="Card" class="w-6 h-6 mr-2"> Другая карта
            </button>
        </div>
        </div>


    <div v-if="otherCardModalOpen" 
    class="fixed inset-0 flex items-end justify-center bg-opacity-50 z-50" 
    style="background: rgba(0, 0, 0, 0.3)">
    <div class="w-96 bg-white rounded-t-xl p-4 text-black" @click.stop>
        <div class="flex items-center mb-6">
        <button @click="otherCardModalOpen = false; CardisModalOpen = true">
            <img class="absolute top-5 left-5" src="@/assets/icons/button_back.svg" alt="Назад" />
        </button>
        
        <div class="text-center flex-grow text-lg font-normal italic h-196">Другая картa</div>
        
        </div>

<div class="z-55 absolute top-15 p-2">
    <div class="">
        <label class="block text-gray-600">Номер карты</label>
        <div class="relative">
            <input v-model="cardNumber" type="password" placeholder="•••• •••• •••• ••••"
                class="w-full p-3 border rounded-md mt-2"/>
            <button class="absolute right-3 top-1/2 transform -translate-y-1/2">
            <img src="/src/assets/icons/ic_card.svg" alt="Scan" class="w-6 h-6"/>
            </button>
        </div>
        </div>

        <div class="flex gap-4 mt-1">
        <div class="w-1/2">
            <label class="block text-gray-600">Дата</label>
            <input v-model="expiryDate" placeholder="MM/ГГ"
                class="w-full p-3 border rounded-md mt-2"/>
        </div>
        <div class="w-1/2">
            <label class="block text-gray-600">CCV/CVC</label>
            <input v-model="cvc" placeholder="•••"
                class="w-full p-3 border rounded-md mt-2"/>
        </div>
        </div>

        <button @click="addCard"
        class="fixed bottom-5 left-1/2 transform -translate-x-1/2 w-[360px] bg-blue-500 text-white py-3 rounded-xl hover:bg-blue-700">
        Добавить
        </button>
</div>


    </div>
    </div>

    </div>
    </template>

    <style scoped>
    p {
    line-height: 1.5;
    }
    input {
    outline: none;
    border: 1px solid #ccc;
    }
    </style>
