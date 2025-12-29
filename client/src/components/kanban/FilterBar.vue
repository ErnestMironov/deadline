<template>
	<div class="px-3 sm:px-6 mb-2">
		<div class="bg-card/50 backdrop-blur-sm rounded-lg p-2 sm:p-2.5">
			<div class="flex flex-wrap items-center gap-2 sm:gap-3 justify-end">
				<Select
					v-model="localFilters.assignee"
					class="h-9 text-xs truncate"
					style="width: auto; min-width: 120px; max-width: 200px"
					@update:model-value="handleFilterChange"
				>
					<option value="">Все исполнители</option>
					<option value="__unassigned__">Не назначен</option>
					<option
						v-for="user in users"
						:key="user.id"
						:value="user.username"
						:title="user.username"
					>
						{{ user.username }}
					</option>
				</Select>
				<Select
					v-model="localFilters.priority"
					class="h-9 text-xs max-w-[140px]"
					@update:model-value="handleFilterChange"
				>
					<option value="">Все приоритеты</option>
					<option value="low">Низкий</option>
					<option value="medium">Средний</option>
					<option value="high">Высокий</option>
				</Select>
				<Select
					v-model="localFilters.sort_by"
					class="h-9 text-xs max-w-[140px]"
					@update:model-value="handleFilterChange"
				>
					<option value="">Сортировать по...</option>
					<option value="created_at">Дате создания</option>
					<option value="updated_at">Дате обновления</option>
					<option value="title">Названию</option>
					<option value="priority">Приоритету</option>
				</Select>
				<button
					v-if="localFilters.sort_by"
					@click="toggleSortOrder"
					class="h-9 px-2 rounded-md border border-input bg-white hover:bg-accent text-xs flex items-center gap-1 cursor-pointer transition-colors"
					:title="
						localFilters.sort_order === 'asc' ? 'По возрастанию' : 'По убыванию'
					"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="w-3.5 h-3.5"
						:class="localFilters.sort_order === 'asc' ? '' : 'rotate-180'"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M5 15l7-7 7 7"
						/>
					</svg>
				</button>
				<button
					v-if="hasActiveFilters"
					@click="clearFilters"
					class="h-9 px-2 rounded-md border border-input bg-white hover:bg-accent text-xs flex items-center gap-1 cursor-pointer transition-colors"
					title="Очистить фильтры"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="w-3.5 h-3.5"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M6 18L18 6M6 6l12 12"
						/>
					</svg>
					<span class="hidden sm:inline">Очистить</span>
				</button>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import { authApi } from "@/api/auth";
import type {
	TaskFilters,
	TaskPriority,
	SortBy,
	SortOrder,
} from "@/types/task";
import type { UserResponse } from "@/types/auth";
import Select from "@/components/ui/Select.vue";

interface Props {
	filters: TaskFilters;
}

const props = defineProps<Props>();

const emit = defineEmits<{
	"update:filters": [filters: TaskFilters];
}>();

const localFilters = ref<{
	assignee: string;
	priority: string;
	sort_by: string;
	sort_order: string;
}>({
	assignee: props.filters.assignee || "",
	priority: props.filters.priority || "",
	sort_by: props.filters.sort_by || "",
	sort_order: props.filters.sort_order || "desc",
});

const users = ref<UserResponse[]>([]);

async function loadUsers() {
	try {
		users.value = await authApi.getUsers();
	} catch (error) {
		console.error("Не удалось загрузить пользователей:", error);
	}
}

onMounted(() => {
	loadUsers();
});

watch(
	() => props.filters,
	(newFilters) => {
		localFilters.value = {
			assignee:
				newFilters.assignee === ""
					? "__unassigned__"
					: newFilters.assignee || "",
			priority: newFilters.priority || "",
			sort_by: newFilters.sort_by || "",
			sort_order: newFilters.sort_order || "desc",
		};
	},
	{ deep: true }
);

const hasActiveFilters = computed(() => {
	return !!(
		(localFilters.value.assignee && localFilters.value.assignee !== "") ||
		localFilters.value.priority ||
		localFilters.value.sort_by
	);
});

function handleFilterChange() {
	const filters: TaskFilters = {};
	if (localFilters.value.assignee) {
		if (localFilters.value.assignee === "__unassigned__") {
			filters.assignee = "";
		} else {
			filters.assignee = localFilters.value.assignee;
		}
	} else if (localFilters.value.assignee === "") {
		filters.assignee = "";
	}
	if (localFilters.value.priority)
		filters.priority = localFilters.value.priority as TaskPriority;
	if (localFilters.value.sort_by) {
		filters.sort_by = localFilters.value.sort_by as SortBy;
		filters.sort_order = (localFilters.value.sort_order || "desc") as SortOrder;
	}
	emit("update:filters", filters);
}

function toggleSortOrder() {
	localFilters.value.sort_order =
		localFilters.value.sort_order === "asc" ? "desc" : "asc";
	handleFilterChange();
}

function clearFilters() {
	localFilters.value = {
		assignee: "",
		priority: "",
		sort_by: "",
		sort_order: "desc",
	};
	emit("update:filters", {});
}
</script>
