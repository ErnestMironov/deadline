export enum TaskStatus {
  NEW = 'new',
  IN_PROGRESS = 'in_progress',
  DONE = 'done',
  CANCELLED = 'cancelled'
}

export enum TaskPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high'
}

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

export enum SortBy {
  ID = 'id',
  TITLE = 'title',
  CREATED_AT = 'created_at',
  UPDATED_AT = 'updated_at',
  PRIORITY = 'priority',
  STATUS = 'status',
  ASSIGNEE = 'assignee'
}

export enum SortOrder {
  ASC = 'asc',
  DESC = 'desc'
}

export interface TaskFilters {
  status?: TaskStatus
  assignee?: string
  priority?: TaskPriority
  sort_by?: SortBy
  sort_order?: SortOrder
  skip?: number
  limit?: number
}
