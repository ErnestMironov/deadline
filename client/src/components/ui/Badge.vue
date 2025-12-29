<template>
	<div
		:class="
			cn(
				'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 badge-wrapper',
				variantClasses[variant],
				$attrs.class
			)
		"
		v-bind="$attrs"
	>
		<slot />
	</div>
</template>

<script setup lang="ts">
import { cn } from "@/utils/cn";

interface Props {
	variant?: "default" | "secondary" | "destructive" | "outline";
}

withDefaults(defineProps<Props>(), {
	variant: "default",
});

const variantClasses = {
	default:
		"border-transparent bg-primary text-primary-foreground hover:bg-primary/80",
	secondary:
		"border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
	destructive:
		"border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80",
	outline: "text-foreground",
};
</script>

<style>
.windows98-theme .badge-wrapper {
	border-radius: 0 !important;
	border: 1px solid #808080;
	font-family: "MS Sans Serif", "Segoe UI", sans-serif;
}

.windows98-theme .badge-wrapper.bg-primary {
	background: #0000ff;
	color: #ffffff;
	border: 1px solid #000000;
}

.windows98-theme .badge-wrapper.bg-secondary {
	background: #c0c0c0;
	color: #000000;
	border: 1px solid #808080;
}

.windows98-theme .badge-wrapper.bg-destructive {
	background: #ff0000;
	color: #ffffff;
	border: 1px solid #000000;
}

.windows98-theme .badge-wrapper:not(.bg-primary):not(.bg-secondary):not(.bg-destructive) {
	background: transparent;
	color: #000000;
	border: 1px solid #808080;
}
</style>
