<template>
	<div class="bg-gradient-to-br from-background via-muted/20 to-background min-h-screen">
		<Header v-if="isAuthenticated" />
		<router-view />
	</div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Header from '@/components/layout/Header.vue'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>
