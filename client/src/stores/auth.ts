import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { UserResponse, UserCreate } from '@/types/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
  const storedUser = localStorage.getItem('user')
  const user = ref<UserResponse | null>(storedUser ? JSON.parse(storedUser) : null)

  const isAuthenticated = computed(() => !!token.value)

  function setAuth(newToken: string, newRefreshToken: string, newUser: UserResponse) {
    token.value = newToken
    refreshToken.value = newRefreshToken
    user.value = newUser
    localStorage.setItem('access_token', newToken)
    localStorage.setItem('refresh_token', newRefreshToken)
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  function clearAuth() {
    token.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }

  async function login(username: string, password: string) {
    const { access_token, refresh_token } = await authApi.login(username, password)
    const userData: UserResponse = { id: 0, username, email: '' }
    setAuth(access_token, refresh_token, userData)
    return { access_token, refresh_token, user: userData }
  }

  async function register(userData: UserCreate) {
    const newUser = await authApi.register(userData)
    const { access_token, refresh_token } = await authApi.login(newUser.username, userData.password)
    setAuth(access_token, refresh_token, newUser)
    return { access_token, refresh_token, user: newUser }
  }

  async function refresh() {
    if (!refreshToken.value) {
      throw new Error('No refresh token available')
    }
    const { access_token, refresh_token } = await authApi.refresh(refreshToken.value)
    token.value = access_token
    refreshToken.value = refresh_token
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    return { access_token, refresh_token }
  }

  function logout() {
    clearAuth()
  }

  return {
    token,
    refreshToken,
    user,
    isAuthenticated,
    login,
    register,
    refresh,
    logout,
    setAuth,
    clearAuth,
  }
})
