import api from '@/utils/api'
import type {
  TaskResponse,
  TaskCreate,
  TaskUpdate,
  TaskStatusUpdate,
  TaskFilters,
} from '@/types/task'

export const tasksApi = {
  async getTasks(filters?: TaskFilters): Promise<TaskResponse[]> {
    const params = new URLSearchParams()
    
    if (filters?.status) params.append('status', filters.status)
    if (filters?.assignee) params.append('assignee', filters.assignee)
    if (filters?.priority) params.append('priority', filters.priority)
    if (filters?.sort_by) params.append('sort_by', filters.sort_by)
    if (filters?.sort_order) params.append('sort_order', filters.sort_order)
    if (filters?.skip !== undefined) params.append('skip', filters.skip.toString())
    if (filters?.limit !== undefined) params.append('limit', filters.limit.toString())

    const url = `/tasks${params.toString() ? '?' + params.toString() : ''}`
    const response = await api.get<TaskResponse[]>(url)
    return response.data
  },

  async getTask(taskId: number): Promise<TaskResponse> {
    const response = await api.get<TaskResponse>(`/tasks/${taskId}`)
    return response.data
  },

  async createTask(task: TaskCreate): Promise<TaskResponse> {
    const response = await api.post<TaskResponse>('/tasks', task)
    return response.data
  },

  async updateTask(taskId: number, task: TaskUpdate): Promise<TaskResponse> {
    const response = await api.put<TaskResponse>(`/tasks/${taskId}`, task)
    return response.data
  },

  async updateTaskStatus(taskId: number, statusUpdate: TaskStatusUpdate): Promise<TaskResponse> {
    const response = await api.patch<TaskResponse>(`/tasks/${taskId}/status`, statusUpdate)
    return response.data
  },

  async deleteTask(taskId: number): Promise<void> {
    await api.delete(`/tasks/${taskId}`)
  },
}
