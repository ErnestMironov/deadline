<template>
  <div class="flex flex-col h-full min-w-[240px] sm:min-w-[280px] flex-shrink-0 bg-muted/30 rounded-xl p-3 sm:p-4 border border-border/50 shadow-sm backdrop-blur-sm" :data-status="status">
    <div class="flex items-center justify-between mb-4 sm:mb-5 pb-3 border-b border-border/50">
      <div class="flex items-center gap-2">
        <div class="w-2 h-2 rounded-full" :class="statusColorDot"></div>
        <h2 class="font-semibold text-base sm:text-lg text-foreground">{{ title }}</h2>
      </div>
      <Badge variant="secondary" class="text-xs font-medium px-2 py-0.5">{{ tasks.length }}</Badge>
    </div>
    <draggable
      v-model="localTasks"
      :group="{ name: 'kanban', pull: true, put: true }"
      :animation="200"
      item-key="id"
      class="flex-1 space-y-3 min-h-[100px]"
      ghost-class="opacity-50"
      @end="handleDragEnd"
    >
      <template #item="{ element }">
        <div :data-task-id="element.id">
          <KanbanCard 
            :task="element" 
            @click="$emit('task-click', element)"
            @edit="$emit('task-edit', element)"
          />
        </div>
      </template>
    </draggable>
    <button
      @click="$emit('create-task', status)"
      class="mt-3 w-full py-2 px-3 text-xs font-medium text-muted-foreground hover:text-foreground border border-dashed border-border/50 rounded-lg hover:border-primary/50 hover:bg-primary/5 transition-colors flex items-center justify-center gap-1.5 cursor-pointer"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
      </svg>
      Добавить задачу
    </button>
  </div>
</template>

<script setup lang="ts">
import draggable from 'vuedraggable'
import { watch, ref, computed } from 'vue'
import type { TaskResponse } from '@/types/task'
import { TaskStatus } from '@/types/task'
import KanbanCard from './KanbanCard.vue'
import Badge from '@/components/ui/Badge.vue'

interface Props {
  title: string
  tasks: TaskResponse[]
  status: TaskStatus
}

const props = defineProps<Props>()

const localTasks = ref<TaskResponse[]>([])

watch(() => props.tasks, (newTasks) => {
  localTasks.value = [...newTasks]
}, { immediate: true, deep: true })

const statusColorDot = computed(() => {
  const colors: Record<TaskStatus, string> = {
    [TaskStatus.NEW]: 'bg-blue-500',
    [TaskStatus.IN_PROGRESS]: 'bg-yellow-500',
    [TaskStatus.DONE]: 'bg-green-500',
    [TaskStatus.CANCELLED]: 'bg-gray-500',
  }
  return colors[props.status] || 'bg-gray-500'
})

const emit = defineEmits<{
  'task-click': [task: TaskResponse]
  'task-edit': [task: TaskResponse]
  'task-move': [taskId: number, newStatus: TaskStatus]
  'create-task': [status: TaskStatus]
}>()

function handleDragEnd(event: any) {
  // event.item is the dragged element
  // event.to is the target container
  // event.from is the source container
  const draggedElement = event.item
  
  // Find taskId from the dragged element
  const taskIdElement = draggedElement.querySelector('[data-task-id]') || draggedElement
  const taskId = parseInt(taskIdElement.dataset?.taskId || taskIdElement.getAttribute('data-task-id') || '')
  
  if (!taskId || !event.to) return
  
  // Find the parent column element with data-status
  const targetColumn = event.to.closest('[data-status]') || event.to.parentElement?.closest('[data-status]')
  if (!targetColumn) return
  
  const newStatus = targetColumn.dataset.status as TaskStatus
  if (newStatus && newStatus !== props.status) {
    emit('task-move', taskId, newStatus)
  }
}
</script>
