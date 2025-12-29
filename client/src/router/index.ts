import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
			path: "/login",
			name: "login",
			component: () => import("@/views/LoginPage.vue"),
			meta: { requiresAuth: false },
		},
		{
			path: "/register",
			name: "register",
			component: () => import("@/views/RegisterPage.vue"),
			meta: { requiresAuth: false },
		},
		{
			path: "/",
			name: "home",
			component: () => import("@/components/kanban/KanbanBoard.vue"),
			meta: { requiresAuth: true },
		},
		{
			path: "/analytics",
			name: "analytics",
			component: () => import("@/views/AnalyticsPage.vue"),
			meta: { requiresAuth: true },
		},
	],
});

router.beforeEach((to, _from, next) => {
	const authStore = useAuthStore();
	const requiresAuth = to.meta.requiresAuth !== false;

	if (requiresAuth && !authStore.isAuthenticated) {
		next({ name: "login" });
	} else if (
		!requiresAuth &&
		authStore.isAuthenticated &&
		(to.name === "login" || to.name === "register")
	) {
		next({ name: "home" });
	} else {
		next();
	}
});

export default router;
