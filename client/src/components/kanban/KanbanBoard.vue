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
			@task-click="handleTaskView"
			@task-edit="handleTaskEdit"
			@task-move="handleTaskMove"
			@create-task="handleCreateTask"
		/>
		</div>
		<TaskViewDialog
			v-model="showViewDialog"
			:task-id="viewTaskId"
			@edit="handleTaskEditFromView"
		/>
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
import { ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useKanban } from "@/composables/useKanban";
import { TaskStatus } from "@/types/task";
import type { TaskResponse } from "@/types/task";
import KanbanColumn from "./KanbanColumn.vue";
import TaskDialog from "./TaskDialog.vue";
import TaskViewDialog from "./TaskViewDialog.vue";
import FilterBar from "./FilterBar.vue";

const route = useRoute();
const router = useRouter();

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
const showViewDialog = ref(false);
const selectedTask = ref<TaskResponse | null>(null);
const viewTaskId = ref<number | null>(null);
const initialStatus = ref<TaskStatus | null>(null);

onMounted(() => {
	loadTasks();
	// Проверяем, есть ли ID задачи в URL
	if (route.name === "task" && route.params.id) {
		const taskId = parseInt(route.params.id as string);
		if (!isNaN(taskId)) {
			viewTaskId.value = taskId;
			showViewDialog.value = true;
		}
	}
});

watch(
	() => route.params.id,
	(newId) => {
		if (route.name === "task" && newId) {
			const taskId = parseInt(newId as string);
			if (!isNaN(taskId)) {
				viewTaskId.value = taskId;
				showViewDialog.value = true;
			}
		} else if (route.name === "home") {
			showViewDialog.value = false;
			viewTaskId.value = null;
		}
	}
);

function handleTaskView(task: TaskResponse) {
	viewTaskId.value = task.id;
	showViewDialog.value = true;
	// Обновляем URL
	router.push({ name: "task", params: { id: task.id.toString() } });
}

function handleTaskEdit(task: TaskResponse) {
	selectedTask.value = task;
	initialStatus.value = null;
	showCreateDialog.value = true;
}

function handleTaskEditFromView(taskId: number) {
	showViewDialog.value = false;
	// Возвращаемся на главную, чтобы закрыть модалку просмотра
	if (route.name === "task") {
		router.push({ name: "home" });
	}
	// Найдем задачу в списке задач
	const allTasks = Object.values(tasksByStatus.value).flat();
	const task = allTasks.find((t) => t.id === taskId);
	if (task) {
		handleTaskEdit(task);
	}
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
