<template>
	<Dialog
		:model-value="modelValue"
		@update:model-value="$emit('update:modelValue', $event)"
	>
		<div class="space-y-5 sm:space-y-6">
			<div class="flex items-center gap-3 pb-3 border-b border-border/50">
				<div
					class="w-10 h-10 rounded-xl bg-primary flex items-center justify-center shadow-md"
				>
					<svg
						v-if="task"
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
							d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
						/>
					</svg>
					<svg
						v-else
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
							d="M12 4v16m8-8H4"
						/>
					</svg>
				</div>
				<h2 class="text-xl sm:text-2xl font-bold text-foreground">
					{{ task ? "Edit Task" : "Create Task" }}
				</h2>
			</div>
			<form @submit.prevent="handleSubmit" class="space-y-4 sm:space-y-5">
				<div class="space-y-2">
					<label
						for="title"
						class="flex items-center gap-2 text-sm font-semibold text-foreground"
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
								d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"
							/>
						</svg>
						Title
					</label>
					<Input
						id="title"
						v-model="formData.title"
						required
						placeholder="Enter task title..."
						class="transition-all focus:border-primary/50 focus:ring-primary/20"
					/>
				</div>
				<div class="space-y-2">
					<label
						for="description"
						class="flex items-center gap-2 text-sm font-semibold text-foreground"
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
								d="M4 6h16M4 12h16M4 18h7"
							/>
						</svg>
						Description
					</label>
					<textarea
						id="description"
						v-model="formData.description"
						placeholder="Add a detailed description..."
						class="flex min-h-[100px] w-full rounded-md border border-input bg-white px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-all focus:border-primary/50 focus:ring-primary/20 resize-none"
					/>
				</div>
				<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
					<div class="space-y-2">
						<label
							for="priority"
							class="flex items-center gap-2 text-sm font-semibold text-foreground"
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
									d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
								/>
							</svg>
							Priority
						</label>
						<Select
							id="priority"
							v-model="formData.priority"
							:class="[
								formData.priority === 'high'
									? 'border-red-300 focus:border-red-400 focus:ring-red-200'
									: '',
								formData.priority === 'medium'
									? 'border-yellow-300 focus:border-yellow-400 focus:ring-yellow-200'
									: '',
								formData.priority === 'low'
									? 'border-green-300 focus:border-green-400 focus:ring-green-200'
									: '',
							]"
						>
							<option value="low">Low</option>
							<option value="medium">Medium</option>
							<option value="high">High</option>
						</Select>
					</div>
					<div class="space-y-2">
						<label
							for="assignee"
							class="flex items-center gap-2 text-sm font-semibold text-foreground"
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
									d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
								/>
							</svg>
							Assignee
						</label>
						<Select id="assignee" v-model="formData.assignee">
							<option value="">Unassigned</option>
							<option
								v-for="user in users"
								:key="user.id"
								:value="user.username"
							>
								{{ user.username }}
							</option>
						</Select>
					</div>
				</div>
				<div v-if="task || initialStatus" class="space-y-2">
					<label
						for="status"
						class="flex items-center gap-2 text-sm font-semibold text-foreground"
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
								d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
							/>
						</svg>
						Status
					</label>
					<Select id="status" v-model="formData.status">
						<option value="new">New</option>
						<option value="in_progress">In Progress</option>
						<option value="done">Done</option>
						<option value="cancelled">Cancelled</option>
					</Select>
				</div>
				<div
					class="flex flex-col-reverse sm:flex-row justify-between gap-2 pt-4 border-t border-border/50"
				>
					<Button
						v-if="task"
						type="button"
						variant="destructive"
						@click="handleDelete"
						:disabled="loading || deleting"
						class="w-full sm:w-auto"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-4 h-4 mr-1.5"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
							/>
						</svg>
						{{ deleting ? "Deleting..." : "Delete" }}
					</Button>
					<div class="flex gap-2 ml-auto">
						<Button
							type="button"
							variant="outline"
							@click="$emit('close')"
							class="w-full sm:w-auto"
						>
							Cancel
						</Button>
						<Button
							type="submit"
							:disabled="loading || deleting"
							class="w-full sm:w-auto shadow-md hover:shadow-lg transition-shadow"
						>
							<svg
								v-if="!loading"
								xmlns="http://www.w3.org/2000/svg"
								class="w-4 h-4 mr-1.5"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
								stroke-width="2"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									d="M5 13l4 4L19 7"
								/>
							</svg>
							{{ loading ? "Saving..." : "Save" }}
						</Button>
					</div>
				</div>
			</form>
		</div>
	</Dialog>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { useTasksStore } from "@/stores/tasks";
import { authApi } from "@/api/auth";
import type {
	TaskResponse,
	TaskCreate,
	TaskUpdate,
	TaskStatus,
	TaskPriority,
} from "@/types/task";
import type { UserResponse } from "@/types/auth";
import Dialog from "@/components/ui/Dialog.vue";
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";
import Select from "@/components/ui/Select.vue";

interface Props {
	modelValue: boolean;
	task?: TaskResponse | null;
	initialStatus?: TaskStatus | null;
}

const props = withDefaults(defineProps<Props>(), {
	task: null,
	initialStatus: null,
});

const emit = defineEmits<{
	"update:modelValue": [value: boolean];
	save: [];
	close: [];
	delete: [taskId: number];
}>();

const tasksStore = useTasksStore();
const loading = ref(false);
const deleting = ref(false);
const users = ref<UserResponse[]>([]);

const formData = ref<{
	title: string;
	description: string;
	priority: TaskPriority;
	assignee: string;
	status?: TaskStatus;
}>({
	title: "",
	description: "",
	priority: "medium",
	assignee: "",
	status: "new",
});

async function loadUsers() {
	try {
		users.value = await authApi.getUsers();
	} catch (error) {
		console.error("Failed to load users:", error);
	}
}

watch(
	() => [props.task, props.initialStatus],
	([task, initialStatus]) => {
		if (task) {
			formData.value = {
				title: task.title,
				description: task.description || "",
				priority: task.priority,
				assignee: task.assignee || "",
				status: task.status,
			};
		} else {
			formData.value = {
				title: "",
				description: "",
				priority: "medium",
				assignee: "",
				status: (initialStatus as TaskStatus) || "new",
			};
		}
	},
	{ immediate: true }
);

watch(
	() => props.modelValue,
	(isOpen) => {
		if (isOpen) {
			loadUsers();
		}
	}
);

onMounted(() => {
	if (props.modelValue) {
		loadUsers();
	}
});

async function handleSubmit() {
	loading.value = true;
	try {
		if (props.task) {
			await tasksStore.updateTask(props.task.id, {
				title: formData.value.title,
				description: formData.value.description || null,
				priority: formData.value.priority,
				assignee: formData.value.assignee || null,
				status: formData.value.status,
			});
		} else {
			await tasksStore.createTask({
				title: formData.value.title,
				description: formData.value.description || null,
				priority: formData.value.priority,
				assignee: formData.value.assignee || null,
				status: formData.value.status || "new",
			});
		}
		emit("save");
		emit("update:modelValue", false);
	} catch (error) {
		console.error("Failed to save task:", error);
	} finally {
		loading.value = false;
	}
}

async function handleDelete() {
	if (!props.task) return;

	if (!confirm("Are you sure you want to delete this task?")) {
		return;
	}

	deleting.value = true;
	try {
		await tasksStore.deleteTask(props.task.id);
		emit("delete", props.task.id);
		emit("update:modelValue", false);
	} catch (error) {
		console.error("Failed to delete task:", error);
	} finally {
		deleting.value = false;
	}
}
</script>
