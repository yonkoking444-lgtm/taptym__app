<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useAuthStore } from '../../../stores/auth'
import CardCar from '../../../components/CardCar.vue'
import Footer from '../../../components/Footer.vue'

const authStore = useAuthStore()
const email = ref('')

onMounted(() => {
  authStore.hydrate()
  email.value = authStore.currentUser?.email || ''
})
</script>

<template>
  <div class="container flex h-screen max-w-sm flex-col gap-4 italic">
    <h1 class="mx-2 mt-5 text-2xl font-light">Мои вещи</h1>
    <main class="flex min-h-0 flex-grow flex-col gap-4 overflow-y-auto px-2 pb-20">
      <CardCar v-if="email" :owner-email="email" />
      <p v-else class="py-20 text-center text-zinc-500">Войдите в аккаунт</p>
    </main>
    <Footer />
  </div>
</template>