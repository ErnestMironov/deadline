import { computed, ref } from 'vue'
import { useTasksStore } from '@/stores/tasks'
import { TaskStatus as TaskStatusEnum } from '@/types/task'
import type { TaskStatus, TaskFilters } from '@/types/task'
import { TASK_STATUSES, TASK_STATUS_LABELS } from '@/utils/constants'

export function useKanban() {
  const tasksStore = useTasksStore()
  const filters = ref<TaskFilters>({})

  const tasksByStatus = computed(() => {
    const grouped: Record<TaskStatus, ReturnType<typeof tasksStore.getTasksByStatus>> = {
      [TaskStatusEnum.NEW]: [],
      [TaskStatusEnum.IN_PROGRESS]: [],
      [TaskStatusEnum.DONE]: [],
      [TaskStatusEnum.CANCELLED]: [],
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
      console.error('Не удалось переместить задачу:', error)
      await loadTasks()
      throw error
    }
  }

  async function handleDeleteTask(taskId: number) {
    try {
      await tasksStore.deleteTask(taskId)
    } catch (error) {
      console.error('Не удалось удалить задачу:', error)
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
