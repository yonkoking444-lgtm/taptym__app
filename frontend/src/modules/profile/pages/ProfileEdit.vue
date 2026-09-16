<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useAuthStore } from '../../../stores/auth'
import { allowPhoneKey, formatPhone, validatePasswordMatch } from '../../../services/auth'
import { UPLOAD_API_URL } from '../../../services/listings'

const router = useRouter()
const toast = useToast()
const authStore = useAuthStore()
const name = ref('')
const email = ref('')
const phone = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const imageUrl = ref('')
const errorMessage = ref('')
const deleteModalOpen = ref(false)
const uploadingImage = ref(false)
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const togglePassword = () => { showPassword.value = !showPassword.value }
const handlePhoneInput = (event: Event) => {
    phone.value = formatPhone((event.target as HTMLInputElement).value)
}
const handleImageUpload = async (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return
  if (file.size > 2 * 1024 * 1024) { errorMessage.value = 'Image size must be less than 2MB.'; return }
    uploadingImage.value = true
  const reader = new FileReader()
    reader.onload = (result) => { imageUrl.value = String(result.target?.result || ''); errorMessage.value = '' }
  reader.readAsDataURL(file)
    try {
        const uploadData = new FormData()
        uploadData.append('file', file)
        const response = await fetch(UPLOAD_API_URL, { method: 'POST', body: uploadData })
        if (!response.ok) throw new Error('Не удалось загрузить фото.')
        imageUrl.value = (await response.json()).url
    } catch (error) {
        errorMessage.value = error instanceof Error ? error.message : 'Ошибка загрузки фото.'
    } finally {
        uploadingImage.value = false
    }
}
const saveProfile = async () => {
  const passwordError = validatePasswordMatch(password.value, confirmPassword.value)
  if (passwordError) { errorMessage.value = passwordError; return }
    const payload = { name: name.value, phone: phone.value, password: password.value, imageUrl: imageUrl.value }
    try {
        const response = await fetch(`${apiUrl}/api/profiles/${encodeURIComponent(email.value)}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        })
        if (!response.ok) throw new Error('Не удалось сохранить профиль на сервере.')
        if (!authStore.updateProfile(payload)) { errorMessage.value = 'Пользователь не найден.'; return }
        errorMessage.value = ''
        toast.success('Профиль сохранён', { timeout: 3000 })
    } catch (error) {
        errorMessage.value = error instanceof Error ? error.message : 'Ошибка сохранения профиля.'
    }
}
const openModal = () => { deleteModalOpen.value = true }
const closeModal = () => { deleteModalOpen.value = false }
const deleteAccount = () => {
  if (!authStore.deleteAccount()) { errorMessage.value = 'Не удалось удалить аккаунт.'; return }
  deleteModalOpen.value = false
  router.push('/about')
}

onMounted(async () => {
  authStore.hydrate()
  const user = authStore.currentUser
  if (!user) { errorMessage.value = 'Пользователь не авторизован.'; router.push('/about'); return }
  name.value = user.name || ''
  email.value = user.email
  phone.value = user.phone
  password.value = user.password
  confirmPassword.value = user.password
  imageUrl.value = user.imageUrl || ''
    try {
        const response = await fetch(`${apiUrl}/api/profiles/${encodeURIComponent(user.email)}`)
        if (response.ok) {
            const profile = await response.json()
            name.value = profile.name || name.value
            phone.value = profile.phone || phone.value
            password.value = profile.password || password.value
            confirmPassword.value = password.value
            imageUrl.value = profile.imageUrl || imageUrl.value
            authStore.updateProfile({ name: name.value, phone: phone.value, password: password.value, imageUrl: imageUrl.value })
        }
    } catch {
        errorMessage.value = 'Не удалось загрузить профиль с сервера.'
    }
})
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
                <img :src="imageUrl || '/src/assets/images/profile-avatar.png'" class="w-24 h-24 rounded-full object-cover" alt="Profile" />
                <input type="file" class="hidden" @change="handleImageUpload" accept="image/*" />
                <div class="absolute -bottom-0 right-0">
                    <img src="@/assets/icons/button_edit copy.svg" alt="Edit" />
                </div>
            </label>
        </div>


        <form @submit.prevent="saveProfile" class="space-y-4">
            <p v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</p>
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
                <input :value="phone" @keydown="allowPhoneKey" @input="handlePhoneInput" type="tel" inputmode="numeric" class="w-full p-2 border rounded-md border-stone-400" required aria-label="Phone" />
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
                    <input v-model="confirmPassword" :type="showPassword ? 'text' : 'password'" class="w-full p-2 border rounded-md border-stone-400" required aria-label="Confirm password" />
                </div>
            </div>

            <div class="relative mt-20">
                <button type="submit" :disabled="uploadingImage" class="fixed bottom-5 px-35 bg-blue-500 text-white p-3 rounded-md disabled:bg-gray-300" aria-label="Save changes">
                    Сохранить
                </button>
            </div>
        </form>
    </div>
</template>
