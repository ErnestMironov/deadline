<template>
	<Teleport to="body">
		<div
			v-if="modelValue"
			class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6"
			@click.self="$emit('update:modelValue', false)"
		>
			<div class="fixed inset-0 bg-black/50" />
			<div
				:class="
					cn(
						'relative z-50 w-full max-w-lg rounded-lg border bg-background p-4 sm:p-6 shadow-lg max-h-[90vh] overflow-y-auto'
					)
				"
				v-bind="$attrs"
			>
				<slot />
			</div>
		</div>
	</Teleport>
</template>

<script setup lang="ts">
import { cn } from "@/utils/cn";

interface Props {
	modelValue: boolean;
}

defineProps<Props>();
defineEmits<{
	"update:modelValue": [value: boolean];
}>();
</script>
