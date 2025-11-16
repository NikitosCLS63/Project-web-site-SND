# api/auth_middleware.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed


class JWTAuthMiddleware:
    """
    Middleware для проверки JWT токена из localStorage
    Добавляет user информацию в request если токен валиден
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Пытаемся извлечь токен из Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token = None

        if auth_header.startswith('Bearer '):
            token = auth_header[7:]

        # Если токен найден, пытаемся его валидировать
        if token:
            try:
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(token)
                
                # Сохраняем в request для использования в decorators
                request.jwt_token = validated_token
                request.jwt_customer_id = validated_token.get('customer_id')
            except (InvalidToken, AuthenticationFailed):
                request.jwt_token = None
                request.jwt_customer_id = None
        else:
            request.jwt_token = None
            request.jwt_customer_id = None

        response = self.get_response(request)
        return response
