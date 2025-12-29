<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div>
      <label for="username" class="block text-sm font-medium mb-1">Имя пользователя</label>
      <Input
        id="username"
        v-model="username"
        type="text"
        required
        placeholder="Введите имя пользователя"
      />
    </div>
    <div>
      <label for="password" class="block text-sm font-medium mb-1">Пароль</label>
      <Input
        id="password"
        v-model="password"
        type="password"
        required
        placeholder="Введите пароль"
      />
    </div>
    <div v-if="error" class="text-sm text-destructive">{{ error }}</div>
    <Button type="submit" :disabled="loading" class="w-full">
      {{ loading ? 'Вход...' : 'Войти' }}
    </Button>
    <div class="text-center text-sm">
      Нет аккаунта?
      <router-link to="/register" class="text-primary hover:underline">Зарегистрироваться</router-link>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '@/composables/useAuth'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'

const { login } = useAuth()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

async function handleSubmit() {
  error.value = null
  loading.value = true
  try {
    await login(username.value, password.value)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Не удалось войти'
  } finally {
    loading.value = false
  }
}
</script>
