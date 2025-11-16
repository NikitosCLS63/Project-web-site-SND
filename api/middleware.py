# api/middleware.py
from django.utils.deprecation import MiddlewareMixin
from urllib.parse import unquote


class TokenFromURLMiddleware(MiddlewareMixin):
    """
    Middleware для извлечения токена из URL параметра ?token=...
    и добавления его в заголовок Authorization для первого запроса
    """
    
    def process_request(self, request):
        # Получаем токен из URL параметра
        token = request.GET.get('token')
        
        if token:
            # Декодируем токен (на случай, если он был URL-encoded)
            token = unquote(token)
            
            # Добавляем его в заголовок Authorization
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
            
            print(f"✅ Токен из URL добавлен в заголовок Authorization")
        
        return None
