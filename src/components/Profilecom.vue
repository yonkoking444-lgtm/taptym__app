<script setup>
import { ref, onMounted } from 'vue';
import Profilehesh from './profilehesh.vue';

const deleteModalOpen = ref(false);
const name = ref('');
const phone = ref('');

const openModal = () => {
  deleteModalOpen.value = true;
};

const closeModal = () => {
  deleteModalOpen.value = false;
};

onMounted(() => {
  const currentUser = JSON.parse(localStorage.getItem("currentUser"));

  if (currentUser) {
    name.value = currentUser.name || 'Гость';
    phone.value = currentUser.phone || 'Не указан';
  }
});
</script>

<template>
  <div class="w-full flex-col flex gap-3 max-w-md mx-auto bg-white rounded-lg">
    <RouterLink to="/profiledit">
      <div class="flex items-center justify-between p-4 border-b border-stone-300">
        <div class="flex items-center gap-4">
          <img class="w-14 h-14 rounded-full" src="/src/assets/icons/profile.svg" alt="User Avatar">
          <div>
            <h2 class="text-lg font-base italic">{{ name }}</h2>
            <p class="text-gray-500 text-sm">{{ phone }}</p>
          </div>
        </div>
        <img src="/src/assets/icons/ic_chevron_right.svg">
      </div>
    </RouterLink>
    
    <div class="h-screen overflow-y-scroll mb-4">
      <RouterLink to="/heshteg">
        <Profilehesh heshteg="/src/assets/icons/ic_hashtag.svg" text="Mои хештеги" />
      </RouterLink>
      <Profilehesh heshteg="/src/assets/icons/ic_hashtag.svg" text="Мои вещи" />
      <Profilehesh heshteg="/src/assets/icons/ic_hashtag.svg" text="Мой гараж" />
      <Profilehesh heshteg="/src/assets/icons/ic_hashtag.svg" text="Мой дом" />
      <Profilehesh heshteg="/src/assets/icons/ic_hashtag.svg" text="Мои услуги" />
      <Profilehesh heshteg="/src/assets/icons/ic_save.svg" text="Избранное" />
      
      <RouterLink to="/pointpage">
        <Profilehesh heshteg="/src/assets/icons/ic_bonuses (1).svg" text="Мои баллы" />
      </RouterLink>

      <RouterLink to="/termsofuse">
        <Profilehesh heshteg="/src/assets/icons/ic_terms&cond.svg" text="Условия пользования" />
      </RouterLink>
      <RouterLink to="/privacypolicy">
        <Profilehesh heshteg="/src/assets/icons/ic_lock.svg" text="Политика конфиденциальности" />
      </RouterLink>

      <div class="flex items-center justify-between p-4 border-b border-stone-300 cursor-pointer hover:bg-gray-100" @click="openModal">
        <div class="flex items-center">
          <img src="/src/assets/icons/ic_logout.svg" alt="icon">
          <span class="ml-3 text-lg font-base text-red-600">Выйти</span>
        </div>
      </div>

      <div v-if="deleteModalOpen" class="z-55 fixed inset-0 flex items-center justify-center bg-opacity-30 backdrop-blur-md">
        <div class="bg-white p-5 rounded-lg shadow-lg w-72 h-30 text-center">
          <p class="text-lg font-light italic">Вы точно хотите выйти?</p>
          <div class="flex justify-between mt-6">
            <button class="text-blue-500 font-medium w-1/2" @click="closeModal" aria-label="Cancel">Отмена</button>
            <RouterLink to="/about" class="w-1/2">
              <button class="text-red-500 font-medium w-full" aria-label="Confirm exit">Выйти</button>
            </RouterLink> 
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
