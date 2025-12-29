import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { UserCreate } from '@/types/auth'

export function useAuth() {
  const router = useRouter()
  const authStore = useAuthStore()

  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const user = computed(() => authStore.user)

  async function login(username: string, password: string) {
    try {
      await authStore.login(username, password)
      router.push('/')
    } catch (error) {
      throw error
    }
  }

  async function register(userData: UserCreate) {
    try {
      await authStore.register(userData)
      router.push('/')
    } catch (error) {
      throw error
    }
  }

  function logout() {
    authStore.logout()
    router.push('/login')
  }

  return {
    isAuthenticated,
    user,
    login,
    register,
    logout,
  }
}
