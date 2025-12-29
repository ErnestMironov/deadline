<template>
	<header class="p-3 sm:p-6 sm:pb-2">
		<div class="bg-white rounded-xl border border-border/50 p-2.5 sm:p-3">
			<div class="flex items-center justify-between gap-3 sm:gap-4">
				<div class="flex items-center gap-2.5 sm:gap-3 flex-shrink-0">
					<div
						class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-gradient-to-br from-primary to-primary/80 flex items-center justify-center shadow-md"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-primary-foreground"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
							/>
						</svg>
					</div>
					<h1
						:class="[
							'text-lg sm:text-xl font-bold whitespace-nowrap',
							isWindowsTheme
								? 'text-white py-[2px] px-[6px] bg-[#008080]'
								: 'bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent',
						]"
					>
						ТИКЕТНИЦА
					</h1>
				</div>
				<div class="flex items-center gap-1 sm:gap-1.5 flex-shrink-0">
					<Button
						v-if="showAnalyticsButton"
						variant="outline"
						size="sm"
						@click="router.push('/analytics')"
						class="h-7 px-2 text-xs hover:bg-primary/10 hover:border-primary/50 hover:text-primary transition-colors"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-3.5 h-3.5 mr-1"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
							/>
						</svg>
						<span class="hidden sm:inline">Аналитика</span>
					</Button>
					<Button
						v-if="showKanbanButton"
						variant="outline"
						size="sm"
						@click="router.push('/')"
						class="h-7 px-2 text-xs hover:bg-primary/10 hover:border-primary/50 hover:text-primary transition-colors"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-3.5 h-3.5 mr-1"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
							/>
						</svg>
						<span class="hidden sm:inline">Канбан</span>
					</Button>
					<div
						class="flex items-center gap-2 px-2 py-1 rounded-lg border border-border/50 bg-background/50"
						:title="
							isWindowsTheme
								? 'Переключить на стандартную тему'
								: 'Переключить на тему Windows'
						"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-4 h-4"
							:class="isWindowsTheme ? 'opacity-40' : 'opacity-100'"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						>
							<rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
							<circle cx="12" cy="12" r="5" />
						</svg>
						<button
							@click="toggleTheme"
							class="relative inline-flex h-5 w-9 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
							:class="isWindowsTheme ? 'bg-primary' : 'bg-muted'"
						>
							<span
								class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform shadow-sm"
								:class="isWindowsTheme ? 'translate-x-4' : 'translate-x-0.5'"
							/>
						</button>
						<img
							src="/windows.png"
							alt="Windows"
							class="w-4 h-4"
							:class="isWindowsTheme ? 'opacity-100' : 'opacity-40'"
						/>
					</div>
					<Button
						variant="ghost"
						size="sm"
						@click="logout"
						class="h-7 px-2 text-xs hover:bg-destructive/10 hover:text-destructive transition-colors"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-3.5 h-3.5 sm:mr-1"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
							/>
						</svg>
						<span class="hidden sm:inline">Выйти</span>
					</Button>
				</div>
			</div>
		</div>
	</header>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuth } from "@/composables/useAuth";
import { useTheme } from "@/lib/hooks/useTheme";
import Button from "@/components/ui/Button.vue";

const route = useRoute();
const router = useRouter();
const { logout } = useAuth();
const { isWindowsTheme, toggleTheme } = useTheme();

const title = computed(() => {
	if (route.name === "home") return "Kanban Board";
	if (route.name === "analytics") return "Analytics";
	return "Task Tracker";
});

const showAnalyticsButton = computed(() => route.name !== "analytics");
const showKanbanButton = computed(() => route.name === "analytics");
</script>
