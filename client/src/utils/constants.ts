import { TaskStatus as TaskStatusEnum } from '@/types/task'
import type { TaskStatus } from '@/types/task'

export const TASK_STATUSES: TaskStatus[] = [
  TaskStatusEnum.NEW,
  TaskStatusEnum.IN_PROGRESS,
  TaskStatusEnum.DONE,
  TaskStatusEnum.CANCELLED
]

export const TASK_STATUS_LABELS: Record<TaskStatus, string> = {
  [TaskStatusEnum.NEW]: 'Новая',
  [TaskStatusEnum.IN_PROGRESS]: 'В работе',
  [TaskStatusEnum.DONE]: 'Выполнена',
  [TaskStatusEnum.CANCELLED]: 'Отменена'
}
