<template>
	<div class="min-h-screen flex items-center justify-center bg-white">
		<Card class="w-full max-w-md p-6">
			<h1 class="text-2xl font-bold mb-6 text-center">Регистрация</h1>
			<RegisterForm />
		</Card>
	</div>
</template>

<script setup lang="ts">
import Card from "@/components/ui/Card.vue";
import RegisterForm from "@/components/auth/RegisterForm.vue";
</script>
