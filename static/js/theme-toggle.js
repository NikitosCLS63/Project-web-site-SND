// static/js/theme-toggle.js
(function() {
    const THEME_KEY = 'theme-preference';
    const THEME_DARK = 'dark';
    const THEME_LIGHT = 'light';

    // 1. Загружаем сохранённую тему при загрузке страницы
    function loadTheme() {
        const savedTheme = localStorage.getItem(THEME_KEY);
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const theme = savedTheme || (prefersDark ? THEME_DARK : THEME_LIGHT);
        applyTheme(theme);
    }

    // 2. Применяем тему к документу
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(THEME_KEY, theme);
        
        // Обновляем кнопку переключения (если она есть)
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.innerHTML = theme === THEME_DARK 
                ? '<i class="fas fa-sun"></i>' 
                : '<i class="fas fa-moon"></i>';
        }
        
        // Отправляем событие для синхронизации
        window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
    }

    // 3. Переключение темы
    function toggleTheme() {
        const current = localStorage.getItem(THEME_KEY) || THEME_LIGHT;
        const newTheme = current === THEME_DARK ? THEME_LIGHT : THEME_DARK;
        applyTheme(newTheme);
    }

    // 4. Слушаем изменения в других вкладках
    window.addEventListener('storage', (e) => {
        if (e.key === THEME_KEY && e.newValue) {
            applyTheme(e.newValue);
        }
    });

    // 5. Следим за изменением системных настроек
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem(THEME_KEY)) {
            applyTheme(e.matches ? THEME_DARK : THEME_LIGHT);
        }
    });

    // 6. API для использования в других скриптах
    window.Theme = {
        toggle: toggleTheme,
        set: applyTheme,
        get: () => localStorage.getItem(THEME_KEY) || THEME_LIGHT,
        DARK: THEME_DARK,
        LIGHT: THEME_LIGHT
    };

    // 7. Обработчик клика на кнопку переключения (если есть)
    document.addEventListener('DOMContentLoaded', () => {
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', toggleTheme);
        }
    });

    // 8. Загружаем тему при готовности
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadTheme);
    } else {
        loadTheme();
    }
})();