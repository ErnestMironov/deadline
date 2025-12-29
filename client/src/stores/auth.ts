import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { UserResponse, UserCreate } from '@/types/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const user = ref<UserResponse | null>(() => {
    const stored = localStorage.getItem('user')
    return stored ? JSON.parse(stored) : null
  })

  const isAuthenticated = computed(() => !!token.value)

  function setAuth(newToken: string, newUser: UserResponse) {
    token.value = newToken
    user.value = newUser
    localStorage.setItem('access_token', newToken)
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  function clearAuth() {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  async function login(username: string, password: string) {
    const { access_token } = await authApi.login(username, password)
    const userData: UserResponse = { id: 0, username, email: '' }
    setAuth(access_token, userData)
    return { access_token, user: userData }
  }

  async function register(userData: UserCreate) {
    const newUser = await authApi.register(userData)
    const { access_token } = await authApi.login(userData.username, userData.password)
    setAuth(access_token, newUser)
    return { access_token, user: newUser }
  }

  function logout() {
    clearAuth()
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    setAuth,
    clearAuth,
  }
})
