// static/js/auth-headers.js
// Автоматически добавляет JWT токен ко всем fetch запросам

const originalFetch = window.fetch;

window.fetch = function(...args) {
    const [resource, config] = args;
    
    // Не добавляем заголовок для некоторых запросов
    if (resource.includes('/api/login/') || 
        resource.includes('/api/register/') ||
        resource.includes('/api/token/')) {
        return originalFetch.apply(this, args);
    }
    
    const token = localStorage.getItem('access_token');
    
    if (token) {
        if (!config) {
            args[1] = {};
        }
        if (!config.headers) {
            config.headers = {};
        }
        config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    return originalFetch.apply(this, args);
};

// Функция для проверки, авторизован ли пользователь
function isAuthenticated() {
    return !!localStorage.getItem('access_token');
}

// Функция для получения роли пользователя
function getUserRole() {
    return localStorage.getItem('role');
}

// Функция для выхода
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('role');
    localStorage.removeItem('user_email');
    
    // Очищаем cookies
    document.cookie = 'access_token=; path=/; max-age=0';
    document.cookie = 'role=; path=/; max-age=0';
    
    window.location.href = '/login/';
}

// Проверяем авторизацию при загрузке страницы
// НО ТОЛЬКО ЕСЛИ МЫ НЕ НА СТРАНИЦЕ ЛОГИНА ИЛИ РЕГИСТРАЦИИ
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    
    // Не выполняем проверку на страницах логина/регистрации
    if (currentPath === '/login/' || currentPath === '/register/' || currentPath === '/password_reset/') {
        console.log('📄 Страница логина/регистрации - пропускаем автоматическое перенаправление');
        return;
    }
    
    const token = localStorage.getItem('access_token');
    const role = localStorage.getItem('role');
    
    if (token) {
        console.log('✅ Токен найден:', token.substring(0, 20) + '...');
        console.log('👤 Роль:', role);
        
        // Если мы на защищённой странице и нет нужной роли - перенаправляем
        if (currentPath === '/admin-panel/' && role !== 'admin' && role !== 'employee') {
            console.log('❌ Нет прав на админ-панель, перенаправляем на главную...');
            setTimeout(() => {
                window.location.href = '/';
            }, 500);
        }
        
        if (currentPath === '/admin-panel/users/' && role !== 'admin') {
            console.log('❌ Только админ может управлять пользователями, перенаправляем...');
            setTimeout(() => {
                window.location.href = '/';
            }, 500);
        }
    } else {
        console.log('❌ Токен не найден');
        
        // Если мы на защищённой странице без токена - перенаправляем на логин
        if (currentPath === '/admin-panel/' || currentPath === '/admin-panel/users/' || currentPath === '/employee-panel/') {
            console.log('🔄 Перенаправляем на логин...');
            window.location.href = '/login/';
        }
    }
});


