<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const navigation = [
    { label: 'Продаю', path: '/Main', icon: '/src/assets/icons/home.svg', badge: '5' },
    { label: 'Куплю', path: '/buyitems', icon: '/src/assets/icons/shape.svg' },
    { label: 'Создать', path: '/create', icon: '/src/assets/icons/ic_plusgray.svg' },
    { label: 'Сообщения', path: '/message', icon: '/src/assets/icons/message-circle-lines.svg' },
    { label: 'Профиль', path: '/profile', icon: '/src/assets/icons/profile.png' },
]
const isActive = (path: string) => route.path.toLowerCase() === path.toLowerCase()
</script>

<template>
    <nav class="fixed bottom-0 left-1/2 z-30 flex w-full max-w-[360px] -translate-x-1/2 justify-between border-t border-zinc-200 bg-white/95 px-1 py-2 shadow-[0_-4px_16px_rgba(0,0,0,0.06)] backdrop-blur">
        <RouterLink
            v-for="item in navigation"
            :key="item.path"
            :to="item.path"
            class="group flex min-w-0 flex-1 flex-col items-center gap-1 rounded-xl px-1 py-1 text-[11px] transition-colors"
            :class="isActive(item.path) ? 'text-blue-600' : 'text-zinc-400 hover:text-blue-500'"
            :aria-label="item.label"
        >
            <span class="relative flex h-7 w-7 items-center justify-center">
                <img :src="item.icon" :alt="item.label" class="h-6 w-6 object-contain transition-transform group-hover:scale-110" />
                <span v-if="item.badge" class="absolute -right-2 -top-2 flex h-4 min-w-4 items-center justify-center rounded-full bg-blue-600 px-1 text-[10px] font-bold text-white">{{ item.badge }}</span>
            </span>
            <span class="truncate">{{ item.label }}</span>
        </RouterLink>
    </nav>
</template>



