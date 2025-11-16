# api/tokens.py
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError

class CustomRefreshToken(RefreshToken):
    """
    Custom RefreshToken для модели Customers с customer_id
    """
    @classmethod
    def for_user(cls, user):
        """
        Генерирует токен для Customers объекта с customer_id
        """
        if not user.pk:
            raise ValueError('User must have a PK to generate token.')

        token = cls()
        # Используем customer_id как USER_ID_CLAIM
        token[api_settings.USER_ID_CLAIM] = user.customer_id
        
        # Добавляем email и роль
        token['email'] = user.email
        
        # Получаем роль из связанного Users объекта
        try:
            user_role = user.users_set.first().role.role_name if hasattr(user, 'users_set') else 'client'
            token['role'] = user_role
        except:
            token['role'] = 'client'

        return token

    def __str__(self):
        return f"CustomRefreshToken for customer_id={self[api_settings.USER_ID_CLAIM]}"