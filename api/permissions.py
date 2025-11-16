# api/permissions.py
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.users.models import Users, Customers


class HasRole(BasePermission):
    """
    Проверяет, есть ли у пользователя одна из требуемых ролей
    Используется: permission_classes = [HasRole]
    Затем переопределить get_required_roles() в ViewSet
    """
    required_roles = []

    def has_permission(self, request, view):
        # Если требуемые роли не указаны, разрешаем всем
        if not self.required_roles:
            return True

        # Пытаемся получить пользователя из токена
        try:
            auth = JWTAuthentication()
            validated_token = auth.get_validated_token(
                auth.get_raw_token(auth.get_header(request))
            )
            customer_id = validated_token.get('customer_id')
            if customer_id:
                customer = Customers.objects.get(customer_id=customer_id)
                user = Users.objects.get(customer=customer)
                user_role = user.role.role_name if user.role else 'client'
                return user_role in self.required_roles
        except Exception as e:
            print(f"Permission check error: {e}")
            pass

        return False


class IsAdmin(BasePermission):
    """Только администраторы"""
    def has_permission(self, request, view):
        try:
            auth = JWTAuthentication()
            validated_token = auth.get_validated_token(
                auth.get_raw_token(auth.get_header(request))
            )
            customer_id = validated_token.get('customer_id')
            if customer_id:
                customer = Customers.objects.get(customer_id=customer_id)
                user = Users.objects.get(customer=customer)
                return user.role.role_name == 'admin'
        except Exception as e:
            print(f"Admin permission check error: {e}")
            pass

        return False


class IsAdminOrEmployee(BasePermission):
    """Администраторы или сотрудники"""
    def has_permission(self, request, view):
        try:
            auth = JWTAuthentication()
            validated_token = auth.get_validated_token(
                auth.get_raw_token(auth.get_header(request))
            )
            customer_id = validated_token.get('customer_id')
            if customer_id:
                customer = Customers.objects.get(customer_id=customer_id)
                user = Users.objects.get(customer=customer)
                user_role = user.role.role_name
                return user_role in ['admin', 'employee']
        except Exception as e:
            print(f"Admin or Employee permission check error: {e}")
            pass

        return False


class IsClient(BasePermission):
    """Только клиенты (не админ и не employee)"""
    def has_permission(self, request, view):
        try:
            auth = JWTAuthentication()
            validated_token = auth.get_validated_token(
                auth.get_raw_token(auth.get_header(request))
            )
            customer_id = validated_token.get('customer_id')
            if customer_id:
                customer = Customers.objects.get(customer_id=customer_id)
                user = Users.objects.get(customer=customer)
                user_role = user.role.role_name
                return user_role == 'client'
        except Exception as e:
            print(f"Client permission check error: {e}")
            pass

        return False
