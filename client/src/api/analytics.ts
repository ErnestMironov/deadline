import api from '@/utils/api'
import type { TasksAnalyticsResponse } from '@/types/analytics'

export const analyticsApi = {
  async getAnalytics(): Promise<TasksAnalyticsResponse> {
    const response = await api.get<TasksAnalyticsResponse>('/analytics/tasks')
    return response.data
  },

  async getChart(): Promise<Blob> {
    const response = await api.get('/analytics/tasks/chart', {
      responseType: 'blob',
    })
    return response.data
  },
}
