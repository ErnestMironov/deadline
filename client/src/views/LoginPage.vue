<template>
	<div class="min-h-screen flex items-center justify-center bg-white">
		<Card class="w-full max-w-md p-6">
			<h1 class="text-2xl font-bold mb-6 text-center">Login</h1>
			<LoginForm />
		</Card>
	</div>
</template>

<script setup lang="ts">
import Card from "@/components/ui/Card.vue";
import LoginForm from "@/components/auth/LoginForm.vue";
</script>
