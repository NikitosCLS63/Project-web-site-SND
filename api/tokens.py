# api/tokens.py
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError

class CustomRefreshToken(RefreshToken):
    """
    Custom RefreshToken for Customers model with customer_id
    """
    @classmethod
    def for_user(cls, user):
        """
        Overrides for_user to use customer_id
        """
        if not user.pk:
            raise ValueError('User must have a PK to generate token.')

        token = cls()
        token[api_settings.USER_ID_CLAIM] = getattr(user, user._meta.pk.name)  # customer_id
        token[api_settings.USER_ID_FIELD] = getattr(user, user._meta.pk.name)
        token[api_settings.JTI_CLAIM] = token[api_settings.JTI_CLAIM]

        # Add role to token
        try:
            user_role = user.users_set.first().role.role_name if hasattr(user, 'users_set') else 'client'
            token['role'] = user_role
        except:
            token['role'] = 'client'

        # Blacklist old tokens
        from django.db import transaction
        with transaction.atomic():
            for token_list in OutstandingToken.objects.filter(user_id=user.pk):
                if token_list.jti != token[api_settings.JTI_CLAIM]:
                    BlacklistedToken.objects.get_or_create(token=token_list)

        return token

    def __str__(self):
        return f"CustomRefreshToken for {self[api_settings.USER_ID_CLAIM]}"