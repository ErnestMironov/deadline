<template>
	<div
		class="bg-card border border-border/60 rounded-lg p-3 sm:p-4 cursor-pointer hover:shadow-lg hover:border-primary/30 transition-all duration-200 hover:-translate-y-0.5 bg-gradient-to-br from-card to-card/95 backdrop-blur-sm group relative"
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
				{{ priorityLabel }}
			</Badge>
		</div>
		<p
			v-if="task.description"
			class="text-xs sm:text-sm text-muted-foreground line-clamp-2 mb-2 leading-relaxed max-w-[200px]"
		>
			{{ task.description }}
		</p>
		<div class="flex items-center justify-between">
			<div
				v-if="task.assignee"
				class="flex items-center gap-1.5 text-xs text-foreground"
			>
				<div class="w-1.5 h-1.5 rounded-full bg-primary/60"></div>
				<span class="truncate">{{ task.assignee }}</span>
			</div>
			<div v-else></div>
			<button
				@click.stop="$emit('edit')"
				class="opacity-0 group-hover:opacity-100 transition-opacity p-1.5 hover:bg-primary/10 rounded-md ml-auto cursor-pointer"
				title="Редактировать задачу"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="w-4 h-4 text-primary"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					stroke-width="2"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
					/>
				</svg>
			</button>
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
	edit: [];
}>();

const priorityVariant = computed(() => {
	const priority = props.task.priority;
	if (priority === "high") return "destructive";
	if (priority === "medium") return "default";
	return "secondary";
});

const priorityLabel = computed(() => {
	const priority = props.task.priority;
	const labels: Record<string, string> = {
		low: "Низкий",
		medium: "Средний",
		high: "Высокий",
	};
	return labels[priority] || priority;
});
</script>
