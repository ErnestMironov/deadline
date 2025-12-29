export interface TasksAnalyticsResponse {
  total_tasks: number
  by_status: Record<string, number>
  by_priority: Record<string, number>
  by_assignee: Record<string, number>
  status_percentage: Record<string, number>
  priority_percentage: Record<string, number>
}
