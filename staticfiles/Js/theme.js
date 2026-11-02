/**
 * Eventix Cameroon - Theme Switcher (Light / Dark Mode)
 * Defaults to a clean, crisp, premium Light Theme with Dark Theme toggle.
 */

(function initTheme() {
    // Check saved preference or default to light
    const savedTheme = localStorage.getItem('eventix-theme') || 'light';
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
})();

function toggleTheme() {
    const isDark = document.documentElement.classList.contains('dark');
    const newTheme = isDark ? 'light' : 'dark';
    
    if (newTheme === 'dark') {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
    
    localStorage.setItem('eventix-theme', newTheme);
    updateThemeIcon();
}

function updateThemeIcon() {
    const isDark = document.documentElement.classList.contains('dark');
    const icons = document.querySelectorAll('.theme-toggle-icon');
    const labels = document.querySelectorAll('.theme-toggle-label');

    icons.forEach(icon => {
        if (isDark) {
            icon.className = 'fa-solid fa-sun text-amber-400 theme-toggle-icon';
        } else {
            icon.className = 'fa-solid fa-moon text-slate-600 theme-toggle-icon';
        }
    });

    labels.forEach(label => {
        label.innerText = isDark ? 'Light' : 'Dark';
    });
}

document.addEventListener('DOMContentLoaded', () => {
    updateThemeIcon();
});
