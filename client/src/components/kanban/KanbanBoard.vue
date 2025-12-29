<template>
	<div>
		<FilterBar :filters="filters" @update:filters="updateFilters" />
		<div v-if="loading" class="text-center py-8">Loading tasks...</div>
		<div v-else-if="error" class="text-center py-8 text-destructive">
			{{ error }}
		</div>
		<div
			v-else
			class="flex gap-3 sm:gap-6 overflow-x-auto pb-4 px-3 sm:px-6 scrollbar-hide"
		>
			<KanbanColumn
				v-for="status in TASK_STATUSES"
				:key="status"
				:title="TASK_STATUS_LABELS[status]"
				:tasks="tasksByStatus[status]"
				:status="status"
				@task-click="handleTaskClick"
				@task-move="handleTaskMove"
				@create-task="handleCreateTask"
			/>
		</div>
		<TaskDialog
			v-model="showCreateDialog"
			:task="selectedTask"
			:initial-status="initialStatus"
			@save="handleTaskSave"
			@delete="handleTaskDelete"
			@close="showCreateDialog = false"
		/>
	</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useKanban } from "@/composables/useKanban";
import { TaskStatus } from "@/types/task";
import type { TaskResponse } from "@/types/task";
import KanbanColumn from "./KanbanColumn.vue";
import TaskDialog from "./TaskDialog.vue";
import FilterBar from "./FilterBar.vue";

const {
	tasksByStatus,
	loading,
	error,
	loadTasks,
	handleTaskMove,
	filters,
	updateFilters,
	TASK_STATUSES,
	TASK_STATUS_LABELS,
} = useKanban();

const showCreateDialog = ref(false);
const selectedTask = ref<TaskResponse | null>(null);
const initialStatus = ref<TaskStatus | null>(null);

onMounted(() => {
	loadTasks();
});

function handleTaskClick(task: TaskResponse) {
	selectedTask.value = task;
	initialStatus.value = null;
	showCreateDialog.value = true;
}

function handleCreateTask(status: TaskStatus) {
	selectedTask.value = null;
	initialStatus.value = status;
	showCreateDialog.value = true;
}

async function handleTaskSave() {
	await loadTasks();
	showCreateDialog.value = false;
	selectedTask.value = null;
	initialStatus.value = null;
}

async function handleTaskDelete() {
	await loadTasks();
	showCreateDialog.value = false;
	selectedTask.value = null;
	initialStatus.value = null;
}
</script>
