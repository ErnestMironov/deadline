<template>
	<Teleport to="body">
		<div
			v-if="modelValue"
			class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6"
		>
			<div
				class="fixed inset-0 bg-black/50 backdrop-blur-sm windows-dialog-backdrop"
				@click="$emit('update:modelValue', false)"
			/>
			<div
				:class="
					cn(
						'relative z-50 w-full max-w-lg rounded-xl border border-border/50 bg-card backdrop-blur-sm p-0 shadow-2xl max-h-[90vh] overflow-hidden windows-dialog'
					)
				"
				v-bind="$attrs"
				@click.stop
			>
				<div class="p-4 sm:p-6 max-h-[90vh] overflow-y-auto pb-6">
					<slot />
				</div>
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

<style>
.windows98-theme .windows-dialog-backdrop {
	background: #000000;
	backdrop-filter: none;
	opacity: 1;
}

.windows98-theme .windows-dialog {
	border-radius: 0 !important;
	border: 2px solid #000000;
	background: #c0c0c0;
	box-shadow: none;
	padding: 3px;
	overflow: hidden !important;
	max-height: 90vh !important;
	display: flex !important;
	flex-direction: column !important;
}

.windows98-theme .windows-dialog > div {
	background: #c0c0c0;
	border: 1px inset #c0c0c0;
	margin-top: 0 !important;
	padding-bottom: 2rem !important;
	flex: 1 !important;
	min-height: 0 !important;
	max-height: none !important;
	box-sizing: border-box;
	overflow-y: auto !important;
	overflow-x: hidden !important;
}
</style>
