<template>
	<input
		:class="
			cn(
				'flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
				$attrs.class
			)
		"
		:value="modelValue"
		@input="
			$emit('update:modelValue', ($event.target as HTMLInputElement).value)
		"
		v-bind="$attrs"
	/>
</template>

<script setup lang="ts">
import { cn } from "@/utils/cn";

interface Props {
	modelValue?: string;
}

defineProps<Props>();
defineEmits<{
	"update:modelValue": [value: string];
}>();
</script>

<style>
.windows98-theme input {
	border-radius: 0 !important;
	border: 2px inset #c0c0c0;
	background: #ffffff;
	color: #000000;
	font-family: "MS Sans Serif", "Segoe UI", sans-serif;
	box-shadow: none;
}

.windows98-theme input:focus {
	outline: 1px dotted #000000;
	outline-offset: -3px;
	border: 2px inset #c0c0c0;
}

.windows98-theme input:disabled {
	background: #c0c0c0;
	color: #808080;
	border: 2px inset #c0c0c0;
	opacity: 1;
}

.windows98-theme input::placeholder {
	color: #808080;
}
</style>
