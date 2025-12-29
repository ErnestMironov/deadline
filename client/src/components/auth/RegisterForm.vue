<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div>
      <label for="username" class="block text-sm font-medium mb-1">Username</label>
      <Input
        id="username"
        v-model="username"
        type="text"
        required
        placeholder="Enter your username"
      />
    </div>
    <div>
      <label for="email" class="block text-sm font-medium mb-1">Email</label>
      <Input
        id="email"
        v-model="email"
        type="email"
        required
        placeholder="Enter your email"
      />
    </div>
    <div>
      <label for="password" class="block text-sm font-medium mb-1">Password</label>
      <Input
        id="password"
        v-model="password"
        type="password"
        required
        placeholder="Enter your password"
      />
    </div>
    <div v-if="error" class="text-sm text-destructive">{{ error }}</div>
    <Button type="submit" :disabled="loading" class="w-full">
      {{ loading ? 'Registering...' : 'Register' }}
    </Button>
    <div class="text-center text-sm">
      Already have an account?
      <router-link to="/login" class="text-primary hover:underline">Login</router-link>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '@/composables/useAuth'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'

const { register } = useAuth()
const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

async function handleSubmit() {
  error.value = null
  loading.value = true
  try {
    const userData = { username: username.value, email: email.value, password: password.value }
    await register(userData)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to register'
  } finally {
    loading.value = false
  }
}
</script>
