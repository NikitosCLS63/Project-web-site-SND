# api/views.py
from rest_framework import viewsets

# Products
from apps.products.models import (
    Categories, Brands, Suppliers, Products
)
from apps.products.serializers import (
    CategorySerializer, BrandSerializer, SupplierSerializer, ProductSerializer,
    
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brands.objects.all()
    serializer_class = BrandSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Suppliers.objects.all()
    serializer_class = SupplierSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer



# Users
from apps.users.models import Customers, Roles, Users, Addresses
from apps.users.serializers import CustomerSerializer, RoleSerializer, UserSerializer, AddressSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Addresses.objects.all()
    serializer_class = AddressSerializer


# Cart
from apps.cart.models import Carts, CartItems, Wishlists
from apps.cart.serializers import CartSerializer, CartItemSerializer, WishlistSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Carts.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItems.objects.all()
    serializer_class = CartItemSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlists.objects.all()
    serializer_class = WishlistSerializer


# Orders
from apps.orders.models import Orders, OrderItems, Payments, Shipments, ProductReturns
from apps.orders.serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer, ShipmentSerializer, ProductReturnSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipments.objects.all()
    serializer_class = ShipmentSerializer

class ProductReturnViewSet(viewsets.ModelViewSet):
    queryset = ProductReturns.objects.all()
    serializer_class = ProductReturnSerializer


# Reviews
from apps.reviews.models import Reviews
from apps.reviews.serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer


# Promotions
from apps.promotions.models import Promotions
from apps.promotions.serializers import PromotionSerializer

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotions.objects.all()
    serializer_class = PromotionSerializer


# Analytics
from apps.analytics.models import AuditLog, Reports, ReportItems, AnalyticsSnapshots, AnalyticsMetrics, BackupLogs
from apps.analytics.serializers import (
    AuditLogSerializer, ReportSerializer, ReportItemSerializer,
    AnalyticsSnapshotSerializer, AnalyticsMetricSerializer, BackupLogSerializer
)

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportSerializer

class ReportItemViewSet(viewsets.ModelViewSet):
    queryset = ReportItems.objects.all()
    serializer_class = ReportItemSerializer

class AnalyticsSnapshotViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsSnapshots.objects.all()
    serializer_class = AnalyticsSnapshotSerializer

class AnalyticsMetricViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsMetrics.objects.all()
    serializer_class = AnalyticsMetricSerializer

class BackupLogViewSet(viewsets.ModelViewSet):
    queryset = BackupLogs.objects.all()
    serializer_class = BackupLogSerializer



from django.contrib.auth.hashers import check_password
# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from .tokens import CustomRefreshToken
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response({
                "message": "Регистрация успешна",
                "customer_id": customer.customer_id,
                "email": customer.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'detail': 'Введите email и пароль'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customers.objects.get(email__iexact=email)
            user = Users.objects.get(customer=customer)
        except (Customers.DoesNotExist, Users.DoesNotExist):
            return Response({'detail': 'Неверный email или пароль'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка пароля
        if not check_password(password, customer.password_hash):
            return Response({'detail': 'Неверный email или пароль'}, status=status.HTTP_400_BAD_REQUEST)

        role = user.role.role_name

        # ПРОВЕРКА ДЛИНЫ ТОЛЬКО ДЛЯ ПОЛЬЗОВАТЕЛЕЙ
        if role not in ['admin', 'employee']:
            if len(password) < 6:
                return Response({'detail': 'Пароль должен быть не менее 6 символов'}, status=status.HTTP_400_BAD_REQUEST)

        # Генерация токена
        refresh = CustomRefreshToken.for_user(customer)
        refresh['role'] = role

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "customer_id": customer.customer_id,
            "role": role,
            "email": customer.email
        })
    



# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from apps.users.models import Customers  # ← ТВОЯ МОДЕЛЬ!
import re

class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email', '').strip()

        # Проверка формата email
        if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return Response({'error': 'Введите корректный email'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customers.objects.get(email__iexact=email)
        except Customers.DoesNotExist:
            # Безопасность: не говорим, есть ли email
            return Response({'success': 'Если email зарегистрирован, ссылка отправлена'}, status=status.HTTP_200_OK)

        # Генерируем токен
        token = get_random_string(40)
        expires_at = timezone.now() + timedelta(minutes=15)

        customer.password_reset_token = token
        customer.password_reset_expires = expires_at
        customer.save()

        # Ссылка
        reset_url = f"{settings.FRONTEND_URL}/reset-password-confirm/?token={token}&email={email}"
        print("ОТПРАВЛЯЮ ПИСЬМО НА:", email)
        print("ССЫЛКА:", reset_url)
        # Отправляем письмо
        try:
            send_mail(
                subject='Восстановление пароля — SND',
                message=f'''
Здравствуйте!

Вы запросили восстановление пароля.

Перейдите по ссылке, чтобы установить новый пароль:
{reset_url}

Ссылка действительна 15 минут.

Если вы не запрашивали сброс — проигнорируйте это письмо.

С уважением,
Команда SND
                '''.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
               
            )
        except Exception as e:
            print("ОШИБКА SMTP:", e)  # ← Для дебага
            return Response({'error': 'Ошибка отправки email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': 'Ссылка отправлена'}, status=status.HTTP_200_OK)
      


# api/views.py (добавь)
import hashlib

class PasswordResetConfirmView(APIView):
    def post(self, request):
        token = request.data.get('token')
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([token, email, password]):
            return Response({'error': 'Заполните все поля'}, status=400)

        try:
            customer = Customers.objects.get(
                email__iexact=email,
                password_reset_token=token
            )
        except Customers.DoesNotExist:
            return Response({'error': 'Неверный токен'}, status=400)

        if customer.password_reset_expires < timezone.now():
            return Response({'error': 'Ссылка истекла'}, status=400)

        # Хешируем пароль (SHA256)
        customer.password_hash = hashlib.sha256(password.encode()).hexdigest()
        customer.password_reset_token = None
        customer.password_reset_expires = None
        customer.save()

        return Response({'success': 'Пароль изменён'}) 
    

