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
						class="text-lg sm:text-xl font-bold bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent whitespace-nowrap"
					>
						DEADLINE
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
						<span class="hidden sm:inline">Analytics</span>
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
						<span class="hidden sm:inline">Kanban</span>
					</Button>
					<Button
						variant="outline"
						size="sm"
						@click="toggleTheme"
						class="h-7 px-2 text-xs hover:bg-primary/10 hover:border-primary/50 hover:text-primary transition-colors"
						:title="
							isWindowsTheme
								? 'Switch to default theme'
								: 'Switch to Windows theme'
						"
					>
						<svg
							v-if="isWindowsTheme"
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
								d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
							/>
						</svg>
						<svg
							v-else
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
								d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
							/>
						</svg>
						<span class="hidden sm:inline">{{
							isWindowsTheme ? "Windows" : "Default"
						}}</span>
					</Button>
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
						<span class="hidden sm:inline">Logout</span>
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
