from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed
from apps.users.models import Customers
from django.contrib.auth.models import User


class CustomJWTAuthentication(JWTAuthentication):
    """
    Кастомная аутентификация JWT для работы с customer_id
    Вместо встроенной модели User использует Customers
    """
    
    def authenticate(self, request):
        """
        Override authenticate to allow unauthenticated requests to proceed
        Only raise AuthenticationFailed if a token is present but invalid
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        # Если нет Authorization header, вернуть None (позволить пройти дальше)
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        try:
            # Если header есть, валидировать токен
            return super().authenticate(request)
        except AuthenticationFailed:
            # Если токен невалидный, пропустить его
            return None
        except Exception:
            # Другие ошибки тоже пропускаем
            return None
    
    def get_user(self, validated_token):
        """
        Получает пользователя по customer_id из токена
        """
        try:
            # Извлекаем customer_id из токена
            customer_id = validated_token.get('customer_id')
            
            if not customer_id:
                raise AuthenticationFailed('Invalid token: no customer_id')
            
            # Ищем Customers объект по customer_id
            try:
                customer = Customers.objects.get(customer_id=customer_id)
                # Возвращаем Django User объект (для совместимости с DRF)
                # Но сохраняем reference на Customers в атрибут
                user = User.objects.filter(email=customer.email).first()
                if user:
                    user.customer = customer
                    return user
                else:
                    # Если Django User не существует, создаём временный объект для совместимости
                    user = User(username=customer.email, email=customer.email)
                    user.customer = customer
                    return user
            except Customers.DoesNotExist:
                raise AuthenticationFailed('Customer not found')
        except Exception as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')
