# apps/users/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users, Customers, Roles
import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.contrib.auth.hashers import make_password
import hashlib
from apps.users.decorators import require_role, require_auth

def get_user_from_token(request):
    """Извлекает пользователя из JWT токена"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None, None
    
    token = auth_header[7:]
    try:
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(token)
        customer_id = validated_token.get('customer_id')
        if customer_id:
            customer = Customers.objects.get(customer_id=customer_id)
            user = Users.objects.get(customer=customer)
            return user, customer
    except Exception as e:
        print(f"Token validation error: {e}")
        pass
    return None, None

@csrf_exempt
def users_api(request):
    # GET - без проверки авторизации (можно смотреть список)
    if request.method == "GET":
        users = Users.objects.select_related('customer', 'role').all()
        data = []
        for u in users:
            c = u.customer
            data.append({
                "users_id": u.users_id,
                "email": c.email,
                "first_name": c.first_name or "-",
                "last_name": c.last_name or "-",
                "role_name": u.role.role_name if u.role else "client"
            })
        return JsonResponse(data, safe=False)

    # DELETE и POST требуют авторизацию с проверкой ролей
    user, customer = get_user_from_token(request)
    if not user:
        return JsonResponse({"error": "Требуется авторизация"}, status=401)

    try:
        current_user_role = user.role.role_name
    except:
        return JsonResponse({"error": "Нет прав доступа"}, status=403)

    # DELETE - только admin
    if request.method == "DELETE":
        if current_user_role != 'admin':
            return JsonResponse({"error": "Доступ запрещён. Требуется роль: admin"}, status=403)

        user_id = request.GET.get('id')
        try:
            user_to_delete = Users.objects.get(users_id=user_id)
            customer = user_to_delete.customer
            
            # Проверка - нельзя удалить главного админа
            if customer.email == "admin@snd.ru":
                return JsonResponse({"error": "Нельзя удалить главного админа"}, status=403)
            
            # Удаляем и Users, и Customers (CASCADE в БД должен все удалить)
            customer.delete()  # Это удалит и самого customer, и связанные Users
            return JsonResponse({"ok": True})
        except Users.DoesNotExist:
            return JsonResponse({"error": "Не найдено"}, status=404)
        except Customers.DoesNotExist:
            return JsonResponse({"error": "Пользователь не найден"}, status=404)

    # POST - только admin или employee
    elif request.method == "POST":
        if current_user_role not in ['admin', 'employee']:
            return JsonResponse({"error": "Доступ запрещён. Требуется роль: admin, employee"}, status=403)

        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip().lower()
            password = data.get('password', '').strip()
            first_name = data.get('first_name', '').strip()
            last_name = data.get('last_name', '').strip()
            role_name = data.get('role', 'employee').strip()

            # Валидация
            if not email or '@' not in email:
                return JsonResponse({"error": "Некорректный email"}, status=400)
            if not password or len(password) < 6:
                return JsonResponse({"error": "Пароль должен быть минимум 6 символов"}, status=400)
            if role_name not in ['admin', 'employee']:
                return JsonResponse({"error": "Роль может быть только 'admin' или 'employee'"}, status=400)

            # Проверка существования
            if Customers.objects.filter(email__iexact=email).exists():
                return JsonResponse({"error": "Email уже используется"}, status=400)

            # Создание пользователя
            customer = Customers.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password_hash=hashlib.sha256(password.encode()).hexdigest()
            )

            role = Roles.objects.get(role_name=role_name)
            user = Users.objects.create(customer=customer, role=role)

            return JsonResponse({
                "ok": True,
                "users_id": user.users_id,
                "email": customer.email,
                "role": role_name
            }, status=201)
        except Roles.DoesNotExist:
            return JsonResponse({"error": "Роль не найдена"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Метод не разрешён"}, status=405)