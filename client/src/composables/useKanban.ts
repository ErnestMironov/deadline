import { computed, ref } from 'vue'
import { useTasksStore } from '@/stores/tasks'
import { TaskStatus } from '@/types/task'
import type { TaskFilters } from '@/types/task'
import { TASK_STATUSES, TASK_STATUS_LABELS } from '@/utils/constants'

export function useKanban() {
  const tasksStore = useTasksStore()
  const filters = ref<TaskFilters>({})

  const tasksByStatus = computed(() => {
    const grouped: Record<TaskStatus, ReturnType<typeof tasksStore.getTasksByStatus>> = {
      [TaskStatus.NEW]: [],
      [TaskStatus.IN_PROGRESS]: [],
      [TaskStatus.DONE]: [],
      [TaskStatus.CANCELLED]: [],
    }

    TASK_STATUSES.forEach((status) => {
      grouped[status] = tasksStore.getTasksByStatus(status)
    })

    return grouped
  })

  async function loadTasks(customFilters?: TaskFilters) {
    const filtersToUse = customFilters || filters.value
    await tasksStore.fetchTasks(filtersToUse)
  }

  async function handleTaskMove(taskId: number, newStatus: TaskStatus) {
    try {
      await tasksStore.updateTaskStatusOptimistic(taskId, newStatus)
    } catch (error) {
      console.error('Failed to move task:', error)
      await loadTasks()
      throw error
    }
  }

  async function handleDeleteTask(taskId: number) {
    try {
      await tasksStore.deleteTask(taskId)
    } catch (error) {
      console.error('Failed to delete task:', error)
      throw error
    }
  }

  function updateFilters(newFilters: TaskFilters) {
    filters.value = newFilters
    loadTasks()
  }

  return {
    tasksByStatus,
    loading: computed(() => tasksStore.loading),
    error: computed(() => tasksStore.error),
    filters,
    loadTasks,
    handleTaskMove,
    handleDeleteTask,
    updateFilters,
    TASK_STATUSES,
    TASK_STATUS_LABELS,
  }
}
