<template>
	<div
		class="bg-card border border-border/60 rounded-lg p-3 sm:p-4 cursor-move hover:shadow-lg hover:border-primary/30 transition-all duration-200 hover:-translate-y-0.5 bg-gradient-to-br from-card to-card/95 backdrop-blur-sm group"
		@click="$emit('click')"
	>
		<div class="flex items-start justify-between mb-2 gap-2">
			<h3
				class="font-semibold text-sm sm:text-base flex-1 min-w-0 break-words text-foreground group-hover:text-primary transition-colors"
			>
				{{ task.title }}
			</h3>
			<Badge
				:variant="priorityVariant"
				class="text-xs flex-shrink-0 font-medium shadow-sm"
			>
				{{ task.priority }}
			</Badge>
		</div>
		<p
			v-if="task.description"
			class="text-xs sm:text-sm text-muted-foreground line-clamp-2 mb-2 leading-relaxed"
		>
			{{ task.description }}
		</p>
		<div
			v-if="task.assignee"
			class="flex items-center gap-1.5 text-xs text-foreground"
		>
			<div class="w-1.5 h-1.5 rounded-full bg-primary/60"></div>
			<span class="truncate">{{ task.assignee }}</span>
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { TaskResponse } from "@/types/task";
import Badge from "@/components/ui/Badge.vue";

interface Props {
	task: TaskResponse;
}

const props = defineProps<Props>();
defineEmits<{
	click: [];
}>();

const priorityVariant = computed(() => {
	const priority = props.task.priority;
	if (priority === "high") return "destructive";
	if (priority === "medium") return "default";
	return "secondary";
});
</script>
