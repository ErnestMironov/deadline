<template>
  <div class="p-3 sm:p-6">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-0 mb-4 sm:mb-6">
      <h1 class="text-xl sm:text-2xl font-bold">Kanban Board</h1>
      <div class="flex flex-wrap gap-2">
        <Button @click="showCreateDialog = true" class="text-xs sm:text-sm">Create Task</Button>
        <Button variant="outline" @click="$router.push('/analytics')" class="text-xs sm:text-sm">Analytics</Button>
        <Button variant="ghost" @click="logout" class="text-xs sm:text-sm">Logout</Button>
      </div>
    </div>
    <div v-if="loading" class="text-center py-8">Loading tasks...</div>
    <div v-else-if="error" class="text-center py-8 text-destructive">{{ error }}</div>
    <div v-else class="flex gap-2 sm:gap-4 overflow-x-auto pb-4 -mx-3 sm:mx-0 px-3 sm:px-0">
      <KanbanColumn
        v-for="status in TASK_STATUSES"
        :key="status"
        :title="TASK_STATUS_LABELS[status]"
        :tasks="tasksByStatus[status]"
        :status="status"
        @task-click="handleTaskClick"
        @task-move="handleTaskMove"
      />
    </div>
    <TaskDialog
      v-model="showCreateDialog"
      :task="selectedTask"
      @save="handleTaskSave"
      @close="showCreateDialog = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useKanban } from '@/composables/useKanban'
import { useAuth } from '@/composables/useAuth'
import type { TaskResponse } from '@/types/task'
import KanbanColumn from './KanbanColumn.vue'
import TaskDialog from './TaskDialog.vue'
import Button from '@/components/ui/Button.vue'

const { tasksByStatus, loading, error, loadTasks, handleTaskMove, TASK_STATUSES, TASK_STATUS_LABELS } = useKanban()
const { logout } = useAuth()

const showCreateDialog = ref(false)
const selectedTask = ref<TaskResponse | null>(null)

onMounted(() => {
  loadTasks()
})

function handleTaskClick(task: TaskResponse) {
  selectedTask.value = task
  showCreateDialog.value = true
}

async function handleTaskSave() {
  await loadTasks()
  showCreateDialog.value = false
  selectedTask.value = null
}
</script>
