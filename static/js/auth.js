// === СОХРАНЯЕМ ТОКЕН В COOKIES ДЛЯ ПЕРЕДАЧИ ПРИ НАВИГАЦИИ ===
// Когда токен изменяется в localStorage, сохраняем его в cookies

function updateTokenCookie() {
  const token = localStorage.getItem('access_token');
  
  if (token) {
    // Сохраняем токен в cookie с длительностью жизни (24 часа)
    document.cookie = `access_token=${token}; path=/; max-age=86400; SameSite=Lax`;
    console.log('✅ Токен сохранён в cookie');
  } else {
    // Удаляем cookie если токена нет
    document.cookie = 'access_token=; path=/; max-age=0';
    console.log('🗑️ Токен удалён из cookie');
  }
}

// Проверяем токен при загрузке страницы
updateTokenCookie();

// Следим за изменениями в localStorage
window.addEventListener('storage', (e) => {
  if (e.key === 'access_token') {
    updateTokenCookie();
  }
});

// === ДОБАВЛЯЕМ ТОКЕН КО ВСЕМ FETCH ЗАПРОСАМ ===
const originalFetch = window.fetch;

window.fetch = function(...args) {
  const token = localStorage.getItem('access_token');
  
  if (token) {
    if (!args[1]) args[1] = {};
    if (!args[1].headers) args[1].headers = {};
    args[1].headers['Authorization'] = 'Bearer ' + token;
  }
  
  return originalFetch.apply(this, args);
};

