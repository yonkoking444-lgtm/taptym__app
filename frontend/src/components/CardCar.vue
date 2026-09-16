<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { BUYER_REQUESTS_API_URL, fetchCarListings, profileCarsUrl, saveCarListingTags, SELLER_CARS_API_URL, type CarListing } from '../services/listings'

const items = ref<CarListing[]>([])
const router = useRouter()
const props = defineProps<{ action?: string; ownerEmail?: string }>()
const visibleItems = computed(() => props.action ? items.value.filter((item) => item.action === props.action) : items.value)

onMounted(async () => {
  try {
    const endpoint = props.ownerEmail ? profileCarsUrl(props.ownerEmail) : props.action === 'Продам' ? SELLER_CARS_API_URL : props.action === 'Куплю' ? BUYER_REQUESTS_API_URL : undefined
    items.value = endpoint ? (await fetch(endpoint).then((response) => response.json())).map((item: CarListing) => ({ ...item, tags: (item.tags || []).map((name) => ({ name, selected: false })) })) : await fetchCarListings()
  }
  catch (error) { console.error('Ошибка загрузки данных:', error) }
})

const toggleTag = async (tag: { selected: boolean }) => {
  tag.selected = !tag.selected
  await saveCarListingTags(items.value)
}

const goToDetail = (id: CarListing['id']) => router.push(`/cardetail/${id}`)
</script>

<template>
  <div v-for="item in visibleItems" :key="item.id" class="group mx-2 flex max-w-sm gap-3 rounded-2xl border border-zinc-200 bg-white p-3 italic shadow-sm transition duration-300 hover:-translate-y-0.5 hover:shadow-lg" @click="goToDetail(item.id)">
    <div class="relative h-32 w-32 shrink-0 overflow-hidden rounded-xl">
      <img :src="item.image || '/src/assets/images/profile-avatar.png'" alt="Car" class="h-full w-full object-cover transition duration-500 group-hover:scale-105" />
      <span class="absolute bottom-2 left-2 rounded-full bg-white/90 px-2 py-1 text-[10px] font-medium text-zinc-800 shadow-sm backdrop-blur">
        {{ item.action || 'Объявление' }}
      </span>
    </div>
    <div class="min-w-0 flex-1 py-1">
      <div class="flex items-start justify-between gap-3">
        <h2 class="truncate text-base font-medium text-zinc-900">{{ item.title }}</h2>
        <span v-if="item.category" class="shrink-0 text-xs text-zinc-400">{{ item.category }}</span>
      </div>
      <div class="mt-2 flex items-center justify-between gap-3 text-sm">
        <span v-if="item.price" class="truncate font-semibold text-zinc-900">{{ item.price.toLocaleString('ru-RU') }} ₸</span>
        <span class="truncate text-zinc-500">{{ item.location || 'Город не указан' }}</span>
      </div>
      <div class="mt-3 flex max-h-12 flex-wrap gap-1 overflow-hidden">
        <button v-for="tag in item.tags" :key="tag.name" class="rounded-full bg-purple-200 px-2 py-1 text-xs text-black focus:outline-none focus:ring-0" @click.stop="toggleTag(tag)">
          {{ tag.name }}
        </button>
      </div>
      <div class="mt-2 flex items-center justify-between gap-2 text-xs">
        <p class="text-zinc-500">Тегов: <span class="font-medium text-blue-600">{{ item.tags.length }}</span></p>
        <p class="truncate text-zinc-400">{{ item.date || 'Нет даты' }}</p>
      </div>
    </div>
  </div>
</template>
