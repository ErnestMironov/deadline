export const TaskStatus = {
  NEW: 'new',
  IN_PROGRESS: 'in_progress',
  DONE: 'done',
  CANCELLED: 'cancelled'
} as const

export type TaskStatus = typeof TaskStatus[keyof typeof TaskStatus]

export const TaskPriority = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high'
} as const

export type TaskPriority = typeof TaskPriority[keyof typeof TaskPriority]

export interface TaskBase {
  title: string
  description?: string | null
  status: TaskStatus
  priority: TaskPriority
  assignee?: string | null
}

export interface TaskCreate extends TaskBase {}

export interface TaskUpdate {
  title?: string
  description?: string | null
  status?: TaskStatus
  priority?: TaskPriority
  assignee?: string | null
}

export interface TaskStatusUpdate {
  status: TaskStatus
}

export interface TaskResponse extends TaskBase {
  id: number
  created_at: string
  updated_at: string
}

export const SortBy = {
  ID: 'id',
  TITLE: 'title',
  CREATED_AT: 'created_at',
  UPDATED_AT: 'updated_at',
  PRIORITY: 'priority',
  STATUS: 'status',
  ASSIGNEE: 'assignee'
} as const

export type SortBy = typeof SortBy[keyof typeof SortBy]

export const SortOrder = {
  ASC: 'asc',
  DESC: 'desc'
} as const

export type SortOrder = typeof SortOrder[keyof typeof SortOrder]

export interface TaskFilters {
  status?: TaskStatus
  assignee?: string
  priority?: TaskPriority
  sort_by?: SortBy
  sort_order?: SortOrder
  skip?: number
  limit?: number
}
