<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useAuthStore } from '../../../stores/auth'
import { allowPhoneKey, formatPhone, validatePasswordMatch } from '../../../services/auth'

const toast = useToast()
const router = useRouter()
const authStore = useAuthStore()
const email = ref('')
const phone = ref('')
const password = ref('')
const confirmPassword = ref('')
const isLogin = ref(true)
const passwordError = computed(() => validatePasswordMatch(password.value, confirmPassword.value))

const handleAuth = () => {
  if (!phone.value || !password.value) {
    toast.error('Заполните все поля!', { timeout: 3000 })
    return
  }
  if (isLogin.value) {
    if (!authStore.login(phone.value, password.value)) {
      toast.error('Неверный номер или пароль!', { timeout: 3000 })
      return
    }
    toast.success('Успешный вход!', { timeout: 3000 })
    router.push('/profile')
    return
  }
  if (passwordError.value || password.value.length < 6) {
    toast.error(passwordError.value || 'Пароль должен быть не менее 6 символов.', { timeout: 3000 })
    return
  }
  if (!authStore.register({ email: email.value, phone: phone.value, password: password.value })) {
    toast.error('Такой пользователь уже существует!', { timeout: 3000 })
    return
  }
  toast.success('Регистрация успешна!', { timeout: 3000 })
  isLogin.value = true
  email.value = ''
  phone.value = ''
  password.value = ''
  confirmPassword.value = ''
}

const toggleAuthMode = () => {
  isLogin.value = !isLogin.value
  password.value = ''
  confirmPassword.value = ''
}

const handlePhoneInput = (event: Event) => {
    phone.value = formatPhone((event.target as HTMLInputElement).value)
}

onMounted(() => authStore.hydrate())
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
                <input :value="phone" @keydown="allowPhoneKey" @input="handlePhoneInput" type="tel" inputmode="numeric" placeholder="+7 (___) ___ __ __" required />
            </div>

            <div>
                <label>Пароль</label>
                <input v-model="password" type="password" required />
            </div>

            <div v-if="!isLogin">
                <label>Повторите пароль</label>
                <input v-model="confirmPassword" type="password" required />
                <p v-if="passwordError" style="color: red">{{ passwordError }}</p>
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
    