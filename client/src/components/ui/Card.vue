<template>
	<div
		:class="
			cn(
				'rounded-lg border bg-card text-card-foreground shadow-sm card-wrapper',
				($attrs.class as string | undefined)
			)
		"
	>
		<slot />
	</div>
</template>

<script setup lang="ts">
import { cn } from "@/utils/cn";
</script>

<style>
.windows98-theme .card-wrapper {
	border-radius: 0 !important;
	border: 2px inset #c0c0c0;
	background: #c0c0c0;
	box-shadow: none;
}
</style>
