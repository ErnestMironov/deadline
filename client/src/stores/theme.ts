import { defineStore } from "pinia";
import { ref, watch } from "vue";

export type Theme = "default" | "windows";

const THEME_STORAGE_KEY = "theme";
const WINDOWS_THEME_CLASS = "windows98-theme";

export const useThemeStore = defineStore("theme", () => {
	const storedTheme = localStorage.getItem(THEME_STORAGE_KEY);
	const initialTheme: Theme = storedTheme === "windows" || storedTheme === "default" ? storedTheme : "default";
	
	const theme = ref<Theme>(initialTheme);

	function applyTheme(themeValue: Theme) {
		const root = document.documentElement;
		if (themeValue === "windows") {
			root.classList.add(WINDOWS_THEME_CLASS);
		} else {
			root.classList.remove(WINDOWS_THEME_CLASS);
		}
	}

	function setTheme(newTheme: Theme) {
		theme.value = newTheme;
		localStorage.setItem(THEME_STORAGE_KEY, newTheme);
		applyTheme(newTheme);
	}

	applyTheme(initialTheme);

	watch(
		theme,
		(newTheme) => {
			applyTheme(newTheme);
		}
	);

	return {
		theme,
		setTheme,
	};
});
