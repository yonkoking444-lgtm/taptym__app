import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import type { User, UserUpdate } from '../types/models'

const USERS_STORAGE_KEY = 'users'
const CURRENT_USER_STORAGE_KEY = 'currentUser'
const readStorage = <T>(key: string, fallback: T): T => {
  if (typeof window === 'undefined') return fallback
  try {
    const raw = window.localStorage.getItem(key)
    return raw ? (JSON.parse(raw) as T) : fallback
  } catch { return fallback }
}

export const useAuthStore = defineStore('auth', () => {
  const users = ref<User[]>(readStorage<User[]>(USERS_STORAGE_KEY, []))
  const currentUser = ref<User | null>(readStorage<User | null>(CURRENT_USER_STORAGE_KEY, null))
  const isAuthenticated = computed(() => Boolean(currentUser.value))
  const persistUsers = () => window.localStorage.setItem(USERS_STORAGE_KEY, JSON.stringify(users.value))
  const persistCurrentUser = () => currentUser.value ? window.localStorage.setItem(CURRENT_USER_STORAGE_KEY, JSON.stringify(currentUser.value)) : window.localStorage.removeItem(CURRENT_USER_STORAGE_KEY)
  const hydrate = () => { users.value = readStorage<User[]>(USERS_STORAGE_KEY, []); currentUser.value = readStorage<User | null>(CURRENT_USER_STORAGE_KEY, null) }
  const login = (phone: string, password: string) => { const user = users.value.find((item) => item.phone === phone && item.password === password); if (!user) return null; currentUser.value = user; persistCurrentUser(); return user }
  const register = (payload: Omit<User, 'id'>) => { if (users.value.some((user) => user.phone === payload.phone || user.email === payload.email)) return false; const id = users.value.reduce((maxId, user) => Math.max(maxId, user.id), 0) + 1; const newUser: User = { id, ...payload }; users.value.push(newUser); currentUser.value = newUser; persistUsers(); persistCurrentUser(); return true }
  const updateProfile = (payload: UserUpdate) => { if (!currentUser.value) return false; const index = users.value.findIndex((user) => user.email === currentUser.value?.email); if (index === -1) return false; const updatedUser = { ...users.value[index], ...payload }; users.value[index] = updatedUser; currentUser.value = updatedUser; persistUsers(); persistCurrentUser(); return true }
  const logout = () => { currentUser.value = null; persistCurrentUser() }
  const deleteAccount = () => { if (!currentUser.value) return false; users.value = users.value.filter((user) => user.email !== currentUser.value?.email); persistUsers(); currentUser.value = null; persistCurrentUser(); return true }
  return { users, currentUser, isAuthenticated, hydrate, login, register, updateProfile, logout, deleteAccount }
})
