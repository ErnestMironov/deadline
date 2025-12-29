<template>
  <div class="flex flex-col h-full min-w-[240px] sm:min-w-[280px] flex-shrink-0" :data-status="status">
    <div class="flex items-center justify-between mb-3 sm:mb-4">
      <h2 class="font-semibold text-base sm:text-lg">{{ title }}</h2>
      <Badge variant="secondary" class="text-xs">{{ tasks.length }}</Badge>
    </div>
    <draggable
      v-model="localTasks"
      :group="{ name: 'kanban', pull: true, put: true }"
      :animation="200"
      item-key="id"
      class="flex-1 space-y-2 sm:space-y-2 min-h-[100px]"
      ghost-class="opacity-50"
      @end="handleDragEnd"
    >
      <template #item="{ element }">
        <div :data-task-id="element.id">
          <KanbanCard :task="element" @click="$emit('task-click', element)" />
        </div>
      </template>
    </draggable>
  </div>
</template>

<script setup lang="ts">
import draggable from 'vuedraggable'
import { watch, ref } from 'vue'
import type { TaskResponse, TaskStatus } from '@/types/task'
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


const emit = defineEmits<{
  'task-click': [task: TaskResponse]
  'task-move': [taskId: number, newStatus: TaskStatus]
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
