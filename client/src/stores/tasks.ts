import { defineStore } from 'pinia'
import { ref } from 'vue'
import { tasksApi } from '@/api/tasks'
import type { TaskResponse, TaskCreate, TaskUpdate, TaskFilters, TaskStatus } from '@/types/task'

export const useTasksStore = defineStore('tasks', () => {
  const tasks = ref<TaskResponse[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchTasks(filters?: TaskFilters) {
    loading.value = true
    error.value = null
    try {
      tasks.value = await tasksApi.getTasks(filters)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch tasks'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchTask(taskId: number) {
    loading.value = true
    error.value = null
    try {
      const task = await tasksApi.getTask(taskId)
      const index = tasks.value.findIndex((t) => t.id === taskId)
      if (index !== -1) {
        tasks.value[index] = task
      } else {
        tasks.value.push(task)
      }
      return task
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch task'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createTask(task: TaskCreate) {
    loading.value = true
    error.value = null
    try {
      const newTask = await tasksApi.createTask(task)
      tasks.value.push(newTask)
      return newTask
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create task'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateTask(taskId: number, task: TaskUpdate) {
    loading.value = true
    error.value = null
    try {
      const updatedTask = await tasksApi.updateTask(taskId, task)
      const index = tasks.value.findIndex((t) => t.id === taskId)
      if (index !== -1) {
        tasks.value[index] = updatedTask
      }
      return updatedTask
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update task'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateTaskStatusOptimistic(taskId: number, newStatus: TaskStatus) {
    const task = tasks.value.find((t) => t.id === taskId)
    if (!task) return

    const oldStatus = task.status
    task.status = newStatus

    try {
      const updatedTask = await tasksApi.updateTaskStatus(taskId, { status: newStatus })
      const index = tasks.value.findIndex((t) => t.id === taskId)
      if (index !== -1) {
        tasks.value[index] = updatedTask
      }
    } catch (err) {
      task.status = oldStatus
      error.value = err instanceof Error ? err.message : 'Failed to update task status'
      throw err
    }
  }

  async function deleteTask(taskId: number) {
    loading.value = true
    error.value = null
    try {
      await tasksApi.deleteTask(taskId)
      tasks.value = tasks.value.filter((t) => t.id !== taskId)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete task'
      throw err
    } finally {
      loading.value = false
    }
  }

  function getTasksByStatus(status: TaskStatus): TaskResponse[] {
    return tasks.value.filter((task) => task.status === status)
  }

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    fetchTask,
    createTask,
    updateTask,
    updateTaskStatusOptimistic,
    deleteTask,
    getTasksByStatus,
  }
})
