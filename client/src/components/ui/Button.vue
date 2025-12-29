<template>
	<button
		:class="
			cn(
				buttonVariants({ variant: props.variant, size: props.size }),
				$attrs.class
			)
		"
		v-bind="$attrs"
	>
		<slot />
	</button>
</template>

<script setup lang="ts">
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/utils/cn";

const buttonVariants = cva(
	"inline-flex items-center justify-center text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 cursor-pointer",
	{
		variants: {
			variant: {
				default:
					"bg-primary text-primary-foreground hover:bg-primary/90 rounded-md",
				destructive:
					"bg-destructive text-destructive-foreground hover:bg-destructive/90 rounded-md",
				outline:
					"border border-input bg-white hover:bg-accent hover:text-accent-foreground rounded-md",
				secondary:
					"bg-secondary text-secondary-foreground hover:bg-secondary/80 rounded-md",
				ghost: "hover:bg-accent hover:text-accent-foreground rounded-md",
				link: "text-primary underline-offset-4 hover:underline",
			},
			size: {
				default: "h-10 px-4 py-2",
				sm: "h-9 rounded-md px-3",
				lg: "h-11 rounded-md px-8",
				icon: "h-10 w-10",
			},
		},
		defaultVariants: {
			variant: "default",
			size: "default",
		},
	}
);

interface Props extends /* @vue-ignore */ VariantProps<typeof buttonVariants> {}

const props = withDefaults(defineProps<Props>(), {
	variant: "default",
	size: "default",
});
</script>

<style>
.windows98-theme button {
	border-radius: 0 !important;
	border: 2px outset #c0c0c0 !important;
	background: #c0c0c0 !important;
	background-color: #c0c0c0 !important;
	color: #000000 !important;
	font-family: "MS Sans Serif", "Segoe UI", sans-serif;
	box-shadow: none;
}

.windows98-theme button[class*="bg-"] {
	background: #c0c0c0 !important;
	background-color: #c0c0c0 !important;
}

.windows98-theme button:not(:disabled):hover {
	background: #d4d0c8 !important;
	background-color: #d4d0c8 !important;
}

.windows98-theme button:not(:disabled):active {
	border: 2px inset #c0c0c0 !important;
	background: #c0c0c0 !important;
	background-color: #c0c0c0 !important;
}

.windows98-theme button:disabled {
	border: 2px outset #c0c0c0 !important;
	background: #c0c0c0 !important;
	background-color: #c0c0c0 !important;
	color: #808080 !important;
	opacity: 1;
}

.windows98-theme button.text-primary.underline-offset-4 {
	background: transparent !important;
	background-color: transparent !important;
	color: #0000ff !important;
	border: none !important;
	text-decoration: underline;
	padding: 0;
}
</style>
