import { TaskStatus } from '@/types/task'

export const TASK_STATUSES: TaskStatus[] = [
  TaskStatus.NEW,
  TaskStatus.IN_PROGRESS,
  TaskStatus.DONE,
  TaskStatus.CANCELLED
]

export const TASK_STATUS_LABELS: Record<TaskStatus, string> = {
  [TaskStatus.NEW]: 'Новая',
  [TaskStatus.IN_PROGRESS]: 'В работе',
  [TaskStatus.DONE]: 'Выполнена',
  [TaskStatus.CANCELLED]: 'Отменена'
}
