<template>
	<Dialog
		:model-value="modelValue"
		@update:model-value="handleClose"
	>
		<div v-if="loading" class="text-center py-8">Загрузка задачи...</div>
		<div v-else-if="error" class="text-center py-8 text-destructive">
			{{ error }}
		</div>
		<div v-else-if="task" class="space-y-5 sm:space-y-6">
			<div class="flex items-center justify-between pb-3 border-b border-border/50">
				<div class="flex items-center gap-3">
					<div
						class="w-10 h-10 rounded-xl bg-primary flex items-center justify-center shadow-md"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-5 h-5 text-primary-foreground"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
							/>
						</svg>
					</div>
					<h2 class="text-xl sm:text-2xl font-bold text-foreground">
						{{ task.title }}
					</h2>
				</div>
				<Button
					variant="outline"
					size="sm"
					@click="handleEdit"
					class="flex items-center gap-2"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="w-4 h-4"
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
					Редактировать
				</Button>
			</div>

			<div class="space-y-4">
				<div v-if="task.description" class="space-y-2">
					<label class="flex items-center gap-2 text-sm font-semibold text-foreground">
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
								d="M4 6h16M4 12h16M4 18h7"
							/>
						</svg>
						Описание
					</label>
					<p class="text-sm text-foreground whitespace-pre-wrap bg-muted/50 p-3 rounded-md">
						{{ task.description }}
					</p>
				</div>

				<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
					<div class="space-y-2">
						<label class="flex items-center gap-2 text-sm font-semibold text-foreground">
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
									d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
								/>
							</svg>
							Приоритет
						</label>
						<Badge :variant="priorityVariant" class="text-xs font-medium">
							{{ priorityLabel }}
						</Badge>
					</div>

					<div class="space-y-2">
						<label class="flex items-center gap-2 text-sm font-semibold text-foreground">
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
									d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
								/>
							</svg>
							Статус
						</label>
						<Badge variant="secondary" class="text-xs font-medium">
							{{ statusLabel }}
						</Badge>
					</div>

					<div v-if="task.assignee" class="space-y-2">
						<label class="flex items-center gap-2 text-sm font-semibold text-foreground">
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
									d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
								/>
							</svg>
							Исполнитель
						</label>
						<p class="text-sm text-foreground">{{ task.assignee }}</p>
					</div>

					<div class="space-y-2">
						<label class="flex items-center gap-2 text-sm font-semibold text-foreground">
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
									d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
								/>
							</svg>
							Создана
						</label>
						<p class="text-sm text-muted-foreground">
							{{ formatDate(task.created_at) }}
						</p>
					</div>

					<div class="space-y-2">
						<label class="flex items-center gap-2 text-sm font-semibold text-foreground">
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
									d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
								/>
							</svg>
							Обновлена
						</label>
						<p class="text-sm text-muted-foreground">
							{{ formatDate(task.updated_at) }}
						</p>
					</div>
				</div>
			</div>
		</div>
	</Dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { tasksApi } from "@/api/tasks";
import type { TaskResponse } from "@/types/task";
import { TaskPriority, TaskStatus } from "@/types/task";
import Dialog from "@/components/ui/Dialog.vue";
import Button from "@/components/ui/Button.vue";
import Badge from "@/components/ui/Badge.vue";

interface Props {
	modelValue: boolean;
	taskId: number | null;
}

const props = defineProps<Props>();

const emit = defineEmits<{
	"update:modelValue": [value: boolean];
	edit: [taskId: number];
}>();

const router = useRouter();

const task = ref<TaskResponse | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

const priorityVariant = computed(() => {
	if (!task.value) return "secondary";
	const priority = task.value.priority;
	if (priority === TaskPriority.HIGH) return "destructive";
	if (priority === TaskPriority.MEDIUM) return "default";
	return "secondary";
});

const priorityLabel = computed(() => {
	if (!task.value) return "";
	const priority = task.value.priority;
	const labels: Record<TaskPriority, string> = {
		[TaskPriority.LOW]: "Низкий",
		[TaskPriority.MEDIUM]: "Средний",
		[TaskPriority.HIGH]: "Высокий",
	};
	return labels[priority] || priority;
});

const statusLabel = computed(() => {
	if (!task.value) return "";
	const status = task.value.status;
	const labels: Record<TaskStatus, string> = {
		[TaskStatus.NEW]: "Новая",
		[TaskStatus.IN_PROGRESS]: "В работе",
		[TaskStatus.DONE]: "Выполнена",
		[TaskStatus.CANCELLED]: "Отменена",
	};
	return labels[status] || status;
});

function formatDate(dateString: string): string {
	const date = new Date(dateString);
	return date.toLocaleDateString("ru-RU", {
		year: "numeric",
		month: "long",
		day: "numeric",
		hour: "2-digit",
		minute: "2-digit",
	});
}

async function loadTask() {
	if (!props.taskId) {
		task.value = null;
		return;
	}

	loading.value = true;
	error.value = null;
	try {
		task.value = await tasksApi.getTask(props.taskId);
	} catch (err) {
		error.value =
			err instanceof Error ? err.message : "Не удалось загрузить задачу";
		task.value = null;
	} finally {
		loading.value = false;
	}
}

function handleEdit() {
	if (task.value) {
		emit("edit", task.value.id);
		emit("update:modelValue", false);
	}
}

function handleClose(value: boolean) {
	emit("update:modelValue", value);
	if (!value && router.currentRoute.value.name === "task") {
		router.push({ name: "home" });
	}
}

watch(
	() => [props.modelValue, props.taskId],
	([isOpen, taskId]) => {
		if (isOpen && taskId) {
			loadTask();
		} else {
			task.value = null;
			error.value = null;
		}
	},
	{ immediate: true }
);

</script>
