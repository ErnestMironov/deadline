<template>
  <div
    class="bg-card border rounded-lg p-2 sm:p-3 cursor-move hover:shadow-md transition-shadow"
    @click="$emit('click')"
  >
    <div class="flex items-start justify-between mb-1 sm:mb-2 gap-2">
      <h3 class="font-semibold text-xs sm:text-sm flex-1 min-w-0 break-words">{{ task.title }}</h3>
      <Badge :variant="priorityVariant" class="text-xs flex-shrink-0">{{ task.priority }}</Badge>
    </div>
    <p v-if="task.description" class="text-xs text-muted-foreground line-clamp-2 mb-1 sm:mb-2">
      {{ task.description }}
    </p>
    <div v-if="task.assignee" class="text-xs text-muted-foreground truncate">
      Assignee: {{ task.assignee }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { TaskResponse } from '@/types/task'
import Badge from '@/components/ui/Badge.vue'

interface Props {
  task: TaskResponse
}

const props = defineProps<Props>()
defineEmits<{
  click: []
}>()

const priorityVariant = computed(() => {
  const priority = props.task.priority
  if (priority === 'high') return 'destructive'
  if (priority === 'medium') return 'default'
  return 'secondary'
})
</script>
