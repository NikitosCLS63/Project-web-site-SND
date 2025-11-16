# apps/users/decorators.py
from functools import wraps
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from apps.users.models import Users, Customers
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_user_from_request(request):
    """Извлекает пользователя и его роль из JWT токена"""
    # Сначала проверяем в request.jwt_token (установлено middleware)
    if hasattr(request, 'jwt_token') and request.jwt_token:
        try:
            customer_id = request.jwt_token.get('customer_id')
            if customer_id:
                customer = Customers.objects.get(customer_id=customer_id)
                user = Users.objects.get(customer=customer)
                return user, customer
        except (Customers.DoesNotExist, Users.DoesNotExist):
            pass
    
    # Если нет в middleware, ищем в Authorization header
    auth_header = request.headers.get('Authorization', '')
    token = None
    
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]
    
    # Если всё ещё нет токена, проверяем cookies
    if not token:
        token = request.COOKIES.get('access_token')
    
    if not token:
        return None, None
    
    try:
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(token)
        customer_id = validated_token.get('customer_id')
        if customer_id:
            customer = Customers.objects.get(customer_id=customer_id)
            user = Users.objects.get(customer=customer)
            return user, customer
    except Exception as e:
        # Debug: выводим причину ошибки валидации токена
        try:
            print(f"[decorators] token validation error: {e}")
        except Exception:
            pass
        pass
    return None, None


def require_role(*allowed_roles):
    """
    Декоратор для проверки ролей на функциональных views
    Использование:
        @require_role('admin')
        @require_role('admin', 'employee')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user, customer = get_user_from_request(request)
            
            # Нет авторизации - перенаправить на логин
            if not user:
                if request.headers.get('Accept', '').startswith('application/json'):
                    return JsonResponse(
                        {"error": "Требуется авторизация"},
                        status=401
                    )
                return redirect('login')
            
            user_role = user.role.role_name if user.role else 'client'
            
            # Проверяем роль
            if user_role not in allowed_roles:
                # Показываем ошибку 403
                error_html = f"""
                <!DOCTYPE html>
                <html lang="ru">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>403 - Доступ запрещён</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        }}
                        .container {{
                            text-align: center;
                            background: white;
                            padding: 40px;
                            border-radius: 10px;
                            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                        }}
                        .error-code {{
                            font-size: 72px;
                            font-weight: bold;
                            color: #dc2626;
                            margin: 0;
                        }}
                        .error-title {{
                            font-size: 24px;
                            color: #333;
                            margin: 10px 0;
                        }}
                        .error-message {{
                            font-size: 16px;
                            color: #666;
                            margin: 20px 0;
                        }}
                        .user-role {{
                            background: #f3f4f6;
                            padding: 10px;
                            border-radius: 5px;
                            margin: 15px 0;
                            font-family: monospace;
                        }}
                        .back-link {{
                            display: inline-block;
                            margin-top: 20px;
                            padding: 10px 20px;
                            background: #667eea;
                            color: white;
                            text-decoration: none;
                            border-radius: 5px;
                        }}
                        .back-link:hover {{
                            background: #764ba2;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <p class="error-code">403</p>
                        <h1 class="error-title">Доступ запрещён</h1>
                        <p class="error-message">У вас нет прав доступа к этой странице</p>
                        <div class="user-role">
                            Ваша роль: <strong>{user_role}</strong>
                        </div>
                        <a href="/" class="back-link">← Вернуться на главную</a>
                    </div>
                </body>
                </html>
                """
                return HttpResponse(error_html, status=403)
            
            # Передаём user и customer в контекст request
            request.current_user = user
            request.current_customer = customer
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def require_auth(view_func):
    """Декоратор для проверки авторизации (без проверки ролей)"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user, customer = get_user_from_request(request)
        
        if not user:
            if request.headers.get('Accept', '').startswith('application/json'):
                return JsonResponse(
                    {"error": "Требуется авторизация"},
                    status=401
                )
            return redirect('login')
        
        request.current_user = user
        request.current_customer = customer
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
