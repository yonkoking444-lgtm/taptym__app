<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const name = ref('');
const email = ref('');
const phone = ref('');
const password = ref('');
const confirmPassword = ref('');
const showPassword = ref(false);
const imageUrl = ref('');
const errorMessage = ref('');
const deleteModalOpen = ref(false);

const togglePassword = () => {
    showPassword.value = !showPassword.value;
};

const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
        if (file.size > 2 * 1024 * 1024) {
            errorMessage.value = 'Image size must be less than 2MB.';
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            imageUrl.value = e.target.result;
            errorMessage.value = ''; 
        };
        reader.readAsDataURL(file);
    }
};

const saveProfile = () => {
    if (password.value !== confirmPassword.value) {
        errorMessage.value = 'Пароли не совпадают.';
        return;
    }

    const users = JSON.parse(localStorage.getItem("users")) || [];
    const userIndex = users.findIndex(user => user.email === email.value);

    if (userIndex !== -1) {
        users[userIndex] = {
            ...users[userIndex],
            name: name.value,
            phone: phone.value,
            password: password.value,
            imageUrl: imageUrl.value
        };

        localStorage.setItem("users", JSON.stringify(users));
        console.log("Профиль успешно обновлён!");
        errorMessage.value = ''; 
    } else {
        errorMessage.value = 'Пользователь не найден.';
    }
};

const openModal = () => {
    deleteModalOpen.value = true;
};

const closeModal = () => {
    deleteModalOpen.value = false;
};

const deleteAccount = () => {
    const users = JSON.parse(localStorage.getItem("users")) || [];
    const updatedUsers = users.filter(user => user.email !== email.value);
    localStorage.setItem("users", JSON.stringify(updatedUsers));
    localStorage.removeItem("currentUser");

    console.log("Аккаунт удалён!");
    deleteModalOpen.value = false;

    name.value = '';
    email.value = '';
    phone.value = '';
    password.value = '';
    imageUrl.value = '';

    router.push("/about");
};

onMounted(() => {
    const users = JSON.parse(localStorage.getItem("users")) || [];
    const currentUser = JSON.parse(localStorage.getItem("currentUser"));

    if (currentUser) {
        const user = users.find(u => u.email === currentUser.email);

        if (user) {
            name.value = user.name;
            email.value = user.email;
            phone.value = user.phone;
            password.value = user.password;
            imageUrl.value = user.imageUrl || '';
        } else {
            errorMessage.value = 'Пользователь не найден.';
            router.push("/about");
        }
    } else {
        errorMessage.value = 'Пользователь не авторизован.';
        router.push("/about");
    }
});


onMounted(() => {
  const currentUser = JSON.parse(localStorage.getItem("currentUser"));

  if (currentUser) {
    name.value = currentUser.name || 'Гость';
    phone.value = currentUser.phone || 'Не указан';
  }
});
</script>

<template>
    <div class="max-w-md mx-auto mt-5 bg-white rounded-xl">
        <div class="flex justify-between items-center mb-4">
            <RouterLink to="/profile" aria-label="Back to profile">
                <img src="@/assets/icons/button_back copy.svg" alt="Back" />
            </RouterLink>
            <h2 class="text-center text-xl font-base italic">Личные данные</h2>
            <button class="top-4 right-4 text-red-500 text-lg cursor-pointer" @click="openModal" aria-label="Delete account">
                <img src="@/assets/icons/Frame 8040.svg" alt="Delete"/>
            </button>
        </div>

        <div v-if="deleteModalOpen" class="z-55 fixed inset-0 flex items-center justify-center bg-opacity-30 backdrop-blur-md">
            <div class="bg-white p-5 rounded-lg shadow-lg w-70 h-35 text-center">
                <p class="text-lg font-light italic">Хотите удалить аккаунт?</p>
                <p class="text-sm text-gray-500">Все ваши данные будут удалены.</p>
                <div class="flex justify-between mt-6">
                    <button class="text-blue-500 font-medium w-1/2" @click="closeModal" aria-label="Cancel">Отмена</button>
                    <button class="text-red-500 font-medium w-1/2" @click="deleteAccount" aria-label="Confirm delete">Удалить</button>
                </div>
            </div>
        </div>

        <div class="flex justify-center relative mb-4">
            <label class="relative cursor-pointer" aria-label="Upload profile picture">
                <img src="/src/assets/icons/avatar.svg" class="w-24 h-24 rounded-full object-cover" alt="Profile" />
                <input type="file" class="hidden" @change="handleImageUpload" accept="image/*" />
                <div class="absolute -bottom-0 right-0">
                    <img src="@/assets/icons/button_edit copy.svg" alt="Edit" />
                </div>
            </label>
        </div>


        <form @submit.prevent="saveProfile" class="space-y-4">
            <div>
                <label class="block text-gray-700">Имя</label>
                <input v-model="name" type="text" class="w-full p-2 border rounded-md border-stone-400" required aria-label="Name" />
            </div>

            <div>
                <label class="block text-gray-700">Электронная почта</label>
                <input v-model="email" type="email" class="w-full p-2 border rounded-md border-stone-400" disabled aria-label="Email" />
            </div>

            <div>
                <label class="block text-gray-700">Телефон</label>
                <input v-model="phone" type="tel" class="w-full p-2 border rounded-md border-stone-400" required aria-label="Phone" />
            </div>

            <div>
                <label class="block text-gray-700">Пароль</label>
                <div class="relative">
                    <input v-model="password" :type="showPassword ? 'text' : 'password'" class="w-full p-2 border rounded-md border-stone-400" required aria-label="Password" />
                    <button type="button" @click="togglePassword" class="absolute right-3 top-2" aria-label="Toggle password visibility">
                        <img src="/src/assets/icons/ic_eye_closed.svg"  />
                    </button>
                </div>
            </div>

            <div>
                <label class="block text-gray-700">Повторите пароль</label>
                <div class="relative">
                    <input v-model="password" :type="showPassword ? 'text' : 'password'" class="w-full p-2 border rounded-md border-stone-400" required aria-label="Confirm password" />
                </div>
            </div>

            <div class="relative mt-20">
                <button type="submit" class="fixed bottom-5 px-35 bg-blue-500 text-white p-3 rounded-md" aria-label="Save changes">
                    Сохранить
                </button>
            </div>
        </form>
    </div>
</template>
