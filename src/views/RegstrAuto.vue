<script setup>
import { ref, computed, onMounted } from "vue";
import { useToast } from "vue-toastification";
import { useRouter } from "vue-router";

const toast = useToast();
const router = useRouter();

const users = ref([]);
const email = ref("");
const phone = ref("");
const password = ref("");
const confirmPassword = ref("");
const isLogin = ref(true);
const id = ref(1);

const handleAuth = () => {
    if (!phone.value || !password.value) {
        toast.error("Заполните все поля!", { timeout: 3000 });
        return;
    }

    const user = users.value.find(user => user.phone === phone.value);

    if (isLogin.value) {
        if (!user) {
            toast.error("Неверный номер!", { timeout: 3000 });
            return;
        }
        if (user.password !== password.value) {
            toast.error("Неверный пароль!", { timeout: 3000 });
            return;
        }
        
        localStorage.setItem("currentUser", JSON.stringify(user));
        toast.success("Успешный вход!", { timeout: 3000 });
        router.push("/profile");
        return;
    }

    if (user) {
        toast.error("Такой пользователь уже существует!", { timeout: 3000 });
        return;
    }

    if (!passwordsMatch.value) {
        toast.error(errorMessages.value, { timeout: 3000 });
        return;
    }

    const newUser = { id: id.value, email: email.value, phone: phone.value, password: password.value };
    users.value.push(newUser);
    saveUsers();
    id.value++;

    toast.success("Регистрация успешна!", { timeout: 3000 });
    isLogin.value = true;

    email.value = "";
    phone.value = "";
    password.value = "";
    confirmPassword.value = "";
};

const loadUsers = () => {
    const storedUsers = localStorage.getItem("users");
    if (storedUsers) {
        users.value = JSON.parse(storedUsers);
        if (users.value.length > 0) {
            id.value = users.value[users.value.length - 1].id + 1;
        }
    }
};

const saveUsers = () => {
    localStorage.setItem("users", JSON.stringify(users.value));
};

const passwordsMatch = computed(() => password.value === confirmPassword.value && password.value.length >= 6);
const errorMessages = computed(() => {
    if (password.value !== confirmPassword.value) return "Пароли не совпадают";
    if (password.value.length > 0 && password.value.length < 6) return "Пароль должен быть не менее 6 символов";
    return "";
});

const toggleAuthMode = () => {
    isLogin.value = !isLogin.value;
};

onMounted(loadUsers);
</script>

<template>
    <div class="container">
        <h2>{{ isLogin ? "Вход" : "Регистрация" }}</h2>
        <form class="forms" @submit.prevent="handleAuth">
            <div v-if="!isLogin">
                <label>Электронная почта</label>
                <input v-model="email" type="email" placeholder="example@gmail.com" required />
            </div>

            <div>
                <label>Телефон</label>
                <input v-model="phone" type="tel" placeholder="+7 (___) ___ __ __" required />
            </div>

            <div>
                <label>Пароль</label>
                <input v-model="password" type="password" required />
            </div>

            <div v-if="!isLogin">
                <label>Повторите пароль</label>
                <input v-model="confirmPassword" type="password" required />
                <p v-if="errorMessages" style="color: red">{{ errorMessages }}</p>
            </div>

            <button class="btn-auth" type="submit">
                {{ isLogin ? "Войти" : "Зарегистрироваться" }}
            </button>

            <p>
                {{ isLogin ? "Нет аккаунта?" : "Уже есть аккаунт?" }}
                <a @click="toggleAuthMode">{{ isLogin ? "Зарегистрироваться" : "Войти" }}</a>
            </p>
        </form>
    </div>
</template>


    <style scoped>
    .container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        border-radius: 16px;
        max-width: 390px;
        padding: 20px;
        position: relative;
    }
    button:disabled {
        opacity: 0.5;
        pointer-events: none;
    }
    .forms {
        display: flex;
        flex-direction: column;
        gap: 25px;
        width: 100%;
    }
    h2 {
        font-size: 1.5rem;
        font-weight: 100;
        font-style: italic;
        margin-bottom: 30px;
    }
    
    label {
        display: block;
        color: #374151;
        margin-bottom: 4px;
    }
    
    input {
        width: 92%;
        padding: 12px;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        outline: none;
    }
    
    input:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.5);
    }
    button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        padding: 12px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.3s;
    }
    
    button:hover {
        background-color: #1e40af;
    }
    
    p {
        text-align: center;
        color: #6b7280;
        margin-top: 16px;
    }
    
    a {
        color: #2563eb;
        text-decoration: none;
        cursor: pointer;
    }
    
    a:hover {
        text-decoration: underline;
    }
    </style>
    