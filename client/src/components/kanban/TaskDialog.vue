<template>
	<Dialog
		:model-value="modelValue"
		@update:model-value="$emit('update:modelValue', $event)"
	>
		<div class="space-y-4">
			<h2 class="text-lg sm:text-xl font-semibold">
				{{ task ? "Edit Task" : "Create Task" }}
			</h2>
			<form @submit.prevent="handleSubmit" class="space-y-3 sm:space-y-4">
				<div>
					<label for="title" class="block text-sm font-medium mb-1"
						>Title</label
					>
					<Input id="title" v-model="formData.title" required />
				</div>
				<div>
					<label for="description" class="block text-sm font-medium mb-1"
						>Description</label
					>
					<textarea
						id="description"
						v-model="formData.description"
						class="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>
				<div>
					<label for="priority" class="block text-sm font-medium mb-1"
						>Priority</label
					>
					<select
						id="priority"
						v-model="formData.priority"
						class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
					>
						<option value="low">Low</option>
						<option value="medium">Medium</option>
						<option value="high">High</option>
					</select>
				</div>
				<div>
					<label for="assignee" class="block text-sm font-medium mb-1"
						>Assignee</label
					>
					<Input id="assignee" v-model="formData.assignee" />
				</div>
				<div v-if="task">
					<label for="status" class="block text-sm font-medium mb-1"
						>Status</label
					>
					<select
						id="status"
						v-model="formData.status"
						class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
					>
						<option value="new">New</option>
						<option value="in_progress">In Progress</option>
						<option value="done">Done</option>
						<option value="cancelled">Cancelled</option>
					</select>
				</div>
				<div class="flex flex-col-reverse sm:flex-row justify-end gap-2 pt-2">
					<Button
						type="button"
						variant="outline"
						@click="$emit('close')"
						class="w-full sm:w-auto"
						>Cancel</Button
					>
					<Button type="submit" :disabled="loading" class="w-full sm:w-auto">{{
						loading ? "Saving..." : "Save"
					}}</Button>
				</div>
			</form>
		</div>
	</Dialog>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useTasksStore } from "@/stores/tasks";
import type {
	TaskResponse,
	TaskCreate,
	TaskUpdate,
	TaskStatus,
	TaskPriority,
} from "@/types/task";
import Dialog from "@/components/ui/Dialog.vue";
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";

interface Props {
	modelValue: boolean;
	task?: TaskResponse | null;
}

const props = withDefaults(defineProps<Props>(), {
	task: null,
});

const emit = defineEmits<{
	"update:modelValue": [value: boolean];
	save: [];
	close: [];
}>();

const tasksStore = useTasksStore();
const loading = ref(false);

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

watch(
	() => props.task,
	(task) => {
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
				status: "new",
			};
		}
	},
	{ immediate: true }
);

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
</script>
