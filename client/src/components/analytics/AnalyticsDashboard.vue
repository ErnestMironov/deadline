<template>
  <div class="p-6 space-y-6">
    <div v-if="loading" class="text-center py-8">Загрузка аналитики...</div>
    <div v-else-if="error" class="text-center py-8 text-destructive">{{ error }}</div>
    <div v-else class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card class="p-4">
          <div class="text-sm text-muted-foreground">Всего задач</div>
          <div class="text-2xl font-bold">{{ analytics?.total_tasks || 0 }}</div>
        </Card>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card class="p-4">
          <h3 class="font-semibold mb-4">Задачи по статусам</h3>
          <div class="space-y-2">
            <div
              v-for="(count, status) in analytics?.by_status"
              :key="status"
              class="flex items-center justify-between"
            >
              <span class="capitalize">{{ status }}</span>
              <div class="flex items-center gap-2">
                <span class="font-medium">{{ count }}</span>
                <span class="text-sm text-muted-foreground">
                  ({{ analytics?.status_percentage[status]?.toFixed(1) || 0 }}%)
                </span>
              </div>
            </div>
          </div>
        </Card>
        <Card class="p-4">
          <h3 class="font-semibold mb-4">Задачи по приоритетам</h3>
          <div class="space-y-2">
            <div
              v-for="(count, priority) in analytics?.by_priority"
              :key="priority"
              class="flex items-center justify-between"
            >
              <span class="capitalize">{{ priority }}</span>
              <div class="flex items-center gap-2">
                <span class="font-medium">{{ count }}</span>
                <span class="text-sm text-muted-foreground">
                  ({{ analytics?.priority_percentage[priority]?.toFixed(1) || 0 }}%)
                </span>
              </div>
            </div>
          </div>
        </Card>
      </div>
      <Card class="p-4">
        <h3 class="font-semibold mb-4">Задачи по исполнителям</h3>
        <div class="space-y-2">
          <div
            v-for="(count, assignee) in analytics?.by_assignee"
            :key="assignee"
            class="flex items-center justify-between"
          >
            <span>{{ assignee || 'Не назначен' }}</span>
            <span class="font-medium">{{ count }}</span>
          </div>
        </div>
      </Card>
      <Card class="p-4">
        <h3 class="font-semibold mb-4">График</h3>
        <img v-if="chartUrl" :src="chartUrl" alt="График задач" class="w-full" />
        <div v-else class="text-center text-muted-foreground py-8">Загрузка графика...</div>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { analyticsApi } from '@/api/analytics'
import type { TasksAnalyticsResponse } from '@/types/analytics'
import Card from '@/components/ui/Card.vue'

const analytics = ref<TasksAnalyticsResponse | null>(null)
const chartUrl = ref<string | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

async function loadAnalytics() {
  loading.value = true
  error.value = null
  try {
    analytics.value = await analyticsApi.getAnalytics()
    const chartBlob = await analyticsApi.getChart()
    chartUrl.value = URL.createObjectURL(chartBlob)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Не удалось загрузить аналитику'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAnalytics()
})
</script>
