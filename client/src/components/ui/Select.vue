<template>
	<div class="relative" :style="wrapperStyle" :class="wrapperClass">
		<select
			:value="modelValue"
			@change="
				$emit('update:modelValue', ($event.target as HTMLSelectElement).value)
			"
			:class="
				cn(
					'flex h-10 rounded-md border border-input bg-white px-3 py-2 pr-8 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 appearance-none cursor-pointer',
					selectWidthClass,
					$attrs.class
				)
			"
			:style="selectStyle"
			v-bind="$attrs"
		>
			<slot />
		</select>
		<div
			class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none select-arrow"
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="h-4 w-4 text-muted-foreground"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
				stroke-width="2"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M19 9l-7 7-7-7"
				/>
			</svg>
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed, useAttrs } from "vue";
import { cn } from "@/utils/cn";

interface Props {
	modelValue?: string;
}

defineProps<Props>();
defineEmits<{
	"update:modelValue": [value: string];
}>();

const attrs = useAttrs();
const style = computed(() => {
	const styleAttr = attrs.style;
	if (typeof styleAttr === "string") {
		const styles: Record<string, string> = {};
		styleAttr.split(";").forEach((rule) => {
			const [key, value] = rule.split(":").map((s) => s.trim());
			if (key && value) {
				styles[key.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase())] =
					value;
			}
		});
		return styles;
	}
	return styleAttr as Record<string, string> | undefined;
});

const hasAutoWidth = computed(() => {
	return (
		style.value?.width === "auto" || (attrs.class as string)?.includes("w-auto")
	);
});

const wrapperStyle = computed(() => {
	if (hasAutoWidth.value && style.value) {
		const result: Record<string, string> = {};
		if (style.value.width && style.value.width !== "auto") {
			result.width = style.value.width;
		}
		if (style.value.minWidth || style.value["min-width"]) {
			result.minWidth = style.value.minWidth || style.value["min-width"] || "";
		}
		if (style.value.maxWidth || style.value["max-width"]) {
			result.maxWidth = style.value.maxWidth || style.value["max-width"] || "";
		}
		return result;
	}
	return {};
});

const wrapperClass = computed(() => {
	return hasAutoWidth.value ? "inline-block" : "w-full";
});

const selectWidthClass = computed(() => {
	return "w-full";
});

const selectStyle = computed(() => {
	if (hasAutoWidth.value) {
		return {
			overflow: "hidden",
			textOverflow: "ellipsis",
			whiteSpace: "nowrap",
			maxWidth: "100%",
		};
	}
	return {};
});
</script>

<style scoped></style>

<style>
.windows98-theme select {
	border-radius: 0 !important;
	border: 2px inset #c0c0c0;
	background: #ffffff;
	color: #000000;
	font-family: "MS Sans Serif", "Segoe UI", sans-serif;
	box-shadow: none;
	appearance: none;
	background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='8' height='4'%3E%3Cpath d='M0 0 L4 4 L8 0' stroke='%23000000' stroke-width='1' fill='none'/%3E%3C/svg%3E");
	background-repeat: no-repeat;
	background-position: right 4px center;
}

.windows98-theme select:focus {
	outline: 1px dotted #000000;
	outline-offset: -3px;
	border: 2px inset #c0c0c0;
}

.windows98-theme select:disabled {
	background: #c0c0c0;
	color: #808080;
	border: 2px inset #c0c0c0;
	opacity: 1;
}

.windows98-theme .select-arrow {
	display: none;
}
</style>
