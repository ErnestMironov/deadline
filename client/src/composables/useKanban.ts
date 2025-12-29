import { computed } from 'vue'
import { useTasksStore } from '@/stores/tasks'
import { TaskStatus } from '@/types/task'
import { TASK_STATUSES, TASK_STATUS_LABELS } from '@/utils/constants'

export function useKanban() {
  const tasksStore = useTasksStore()

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

  async function loadTasks() {
    await tasksStore.fetchTasks()
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

  return {
    tasksByStatus,
    loading: computed(() => tasksStore.loading),
    error: computed(() => tasksStore.error),
    loadTasks,
    handleTaskMove,
    TASK_STATUSES,
    TASK_STATUS_LABELS,
  }
}
