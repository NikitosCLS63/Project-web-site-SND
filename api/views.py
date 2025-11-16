# api/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import random
import string
from datetime import datetime
from django.utils import timezone

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
    permission_classes = [IsAuthenticatedOrReadOnly]

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brands.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Suppliers.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



# Users
from apps.users.models import Customers, Roles, Users, Addresses
from apps.users.serializers import CustomerSerializer, RoleSerializer, UserSerializer, AddressSerializer
from api.permissions import IsAdmin, IsAdminOrEmployee

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminOrEmployee]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin]
    
    
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.select_related('customer', 'role').all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        # Use a lightweight public serializer for listing/retrieving users
        if self.action in ['list', 'retrieve']:
            from apps.users.serializers import UserListSerializer
            return UserListSerializer
        return super().get_serializer_class()

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Addresses.objects.all()
    serializer_class = AddressSerializer

    def get_permissions(self):
        """Allow anonymous users to create an address (used by checkout),
        but require authentication for list/retrieve/update/delete."""
        if self.action in ['create']:
            return [AllowAny()]
        return [IsAuthenticated()]


# Cart
from apps.cart.models import Carts, CartItems, Wishlists
from apps.cart.serializers import CartSerializer, CartItemSerializer, WishlistSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Carts.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItems.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlists.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]


# Orders
from apps.orders.models import Orders, OrderItems, Payments, Shipments, ProductReturns
from apps.orders.serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer, ShipmentSerializer, ProductReturnSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        """Allow anonymous users to create orders via the API (checkout flow),
        but require authentication for listing/updating orders."""
        if self.action in ['create']:
            return [AllowAny()]
        return [IsAuthenticated()]

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminOrEmployee]

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrEmployee]

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipments.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAdminOrEmployee]

class ProductReturnViewSet(viewsets.ModelViewSet):
    queryset = ProductReturns.objects.all()
    serializer_class = ProductReturnSerializer
    permission_classes = [IsAuthenticated]


# Reviews
from apps.reviews.models import Reviews
from apps.reviews.serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Promotions
from apps.promotions.models import Promotions
from apps.promotions.serializers import PromotionSerializer

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotions.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Analytics
from apps.analytics.models import AuditLog, Reports, ReportItems, AnalyticsSnapshots, AnalyticsMetrics, BackupLogs
from apps.analytics.serializers import (
    AuditLogSerializer, ReportSerializer, ReportItemSerializer,
    AnalyticsSnapshotSerializer, AnalyticsMetricSerializer, BackupLogSerializer
)

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdminOrEmployee]

class ReportItemViewSet(viewsets.ModelViewSet):
    queryset = ReportItems.objects.all()
    serializer_class = ReportItemSerializer
    permission_classes = [IsAdminOrEmployee]

class AnalyticsSnapshotViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsSnapshots.objects.all()
    serializer_class = AnalyticsSnapshotSerializer
    permission_classes = [IsAdminOrEmployee]

class AnalyticsMetricViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsMetrics.objects.all()
    serializer_class = AnalyticsMetricSerializer
    permission_classes = [IsAdminOrEmployee]

class BackupLogViewSet(viewsets.ModelViewSet):
    queryset = BackupLogs.objects.all()
    serializer_class = BackupLogSerializer
    permission_classes = [IsAdmin]



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

        # Генерация токена с customer_id
        refresh = CustomRefreshToken.for_user(customer)

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
    

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ===== PAYMENT PROCESSING WITH YOOKASSA =====
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import random
import string
import uuid
import os

# YooKassa credentials для SANDBOX (для тестирования)
# Для production замените на реальные учетные данные
YOOKASSA_ACCOUNT_ID = '199347'  # Тестовый shop ID для sandbox
YOOKASSA_SECRET_KEY = 'test_MsLMuEqoKWDEu9o7LLVIQ_k2vRr0Yq1yqr-QBDfMXJk'  # Тестовый ключ для sandbox

# API endpoints
YOOKASSA_SANDBOX_URL = 'https://sandbox.yookassa.ru/api/v3'
YOOKASSA_PRODUCTION_URL = 'https://payment.yookassa.ru/api/v3'

# Используем sandbox по умолчанию, но в режиме MOCK для тестирования без интернета
YOOKASSA_API_URL = YOOKASSA_SANDBOX_URL
USE_MOCK_PAYMENTS = True  # Установите False для реальных платежей с интернетом

@api_view(['POST'])
@permission_classes([AllowAny])
def create_payment(request):
    """
    Create payment in YooKassa and return payment form
    """
    try:
        data = request.data
        
        # Calculate total with delivery
        items_total = float(data.get('total', 0))
        delivery_cost = 349 if data.get('delivery_type') == 'courier' else 0
        total_amount = items_total + delivery_cost
        
        # Validation: минимальная сумма платежа
        if total_amount < 0.01:
            return Response({
                'success': False,
                'error': 'Сумма платежа должна быть больше нуля'
            }, status=400)
        
        if USE_MOCK_PAYMENTS:
            # MOCK режим - симулируем платеж для тестирования
            payment_id = f"mock_{uuid.uuid4().hex[:12]}"
            confirmation_url = f"http://localhost:8000/decoration-success/?payment_id={payment_id}&mock=true"
            
            print(f"[MOCK] Created mock payment: {payment_id}")
            print(f"[MOCK] Confirmation URL: {confirmation_url}")
            
            return Response({
                'success': True,
                'payment_id': payment_id,
                'confirmation_url': confirmation_url,
                'message': 'Переходим на страницу оплаты (ТЕСТОВЫЙ РЕЖИМ)'
            }, status=201)
        else:
            # РЕАЛЬНЫЙ режим - отправляем запрос на YooKassa
            payment_data = {
                "amount": {
                    "value": f"{total_amount:.2f}",
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "http://localhost:8000/decoration-success/"
                },
                "capture": True,
                "description": f"Заказ от {data.get('first_name')} {data.get('last_name')}",
                "metadata": {
                    "phone": data.get('phone'),
                    "email": data.get('email'),
                    "delivery_type": data.get('delivery_type')
                }
            }
            
            # Create payment using requests directly
            import requests
            from requests.auth import HTTPBasicAuth
            
            print(f"Creating real payment with credentials: {YOOKASSA_ACCOUNT_ID}")
            print(f"Payload: {payment_data}")
            
            response = requests.post(
                f'{YOOKASSA_API_URL}/payments',
                json=payment_data,
                auth=HTTPBasicAuth(YOOKASSA_ACCOUNT_ID, YOOKASSA_SECRET_KEY),
                headers={
                    'Idempotency-Key': str(uuid.uuid4()),
                    'Content-Type': 'application/json'
                },
                timeout=10
            )
            
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
            
            if response.status_code in [200, 201]:
                result = response.json()
                return Response({
                    'success': True,
                    'payment_id': result['id'],
                    'confirmation_url': result['confirmation']['confirmation_url'],
                    'message': 'Переходим на страницу оплаты'
                }, status=201)
            else:
                return Response({
                    'success': False,
                    'error': f'YooKassa error: {response.text}'
                }, status=response.status_code)
        
    except Exception as e:
        import traceback
        print(f"YooKassa Error: {str(e)}")
        print(traceback.format_exc())
        return Response({
            'success': False,
            'error': f'Ошибка при создании платежа: {str(e)}'
        }, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def check_payment_status(request):
    """
    Check payment status by payment_id
    """
    try:
        payment_id = request.query_params.get('payment_id')
        is_mock = request.query_params.get('mock') == 'true'
        
        if not payment_id:
            return Response({
                'success': False,
                'error': 'Payment ID not provided'
            }, status=400)
        
        if USE_MOCK_PAYMENTS or is_mock:
            # MOCK режим - автоматически считаем платеж успешным
            print(f"[MOCK] Checking mock payment status: {payment_id}")
            return Response({
                'success': True,
                'payment_id': payment_id,
                'status': 'succeeded',
                'amount': 0,  # Не важно в mock режиме
                'paid': True  # Всегда успешно в mock режиме
            }, status=200)
        else:
            # РЕАЛЬНЫЙ режим - отправляем запрос на YooKassa
            import requests
            from requests.auth import HTTPBasicAuth
            
            response = requests.get(
                f'{YOOKASSA_API_URL}/payments/{payment_id}',
                auth=HTTPBasicAuth(YOOKASSA_ACCOUNT_ID, YOOKASSA_SECRET_KEY),
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                payment = response.json()
                return Response({
                    'success': True,
                    'payment_id': payment['id'],
                    'status': payment['status'],
                    'amount': float(payment['amount']['value']),
                    'paid': payment['status'] == 'succeeded'
                }, status=200)
            else:
                return Response({
                    'success': False,
                    'error': f'Payment not found: {response.text}'
                }, status=response.status_code)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Ошибка при проверке платежа: {str(e)}'
        }, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    """
    Create order from cart and save to database
    """
    try:
        from apps.orders.models import Orders, OrderItems
        from apps.users.models import Customers, Addresses
        from apps.products.models import Products
        from datetime import datetime
        
        order_data = request.data
        
        # Get or create customer (guest user)
        phone = order_data.get('phone', '')
        email = order_data.get('email', '')
        first_name = order_data.get('first_name', '')
        last_name = order_data.get('last_name', '')
        
        # Try to find existing customer or create guest customer
        customer = None
        if email:
            try:
                customer = Customers.objects.get(email=email)
            except Customers.DoesNotExist:
                pass
        
        # If no customer found, create a guest customer
        if not customer:
            import hashlib
            import uuid
            # Create a guest customer with unique email
            if email:
                guest_email = email
            else:
                # Create unique email using phone hash
                phone_hash = hashlib.md5(phone.encode()).hexdigest()[:8]
                guest_email = f"guest_{phone_hash}@store.local"
            
            try:
                customer = Customers.objects.create(
                    first_name=first_name or 'Guest',
                    last_name=last_name or 'Customer',
                    email=guest_email,
                    password_hash=hashlib.sha256(phone.encode()).hexdigest(),
                    phone=phone,
                    created_at=timezone.now()
                )
            except Exception as customer_error:
                # If email already exists, try with UUID
                try:
                    unique_id = str(uuid.uuid4())[:8]
                    guest_email = f"guest_{unique_id}@store.local"
                    customer = Customers.objects.create(
                        first_name=first_name or 'Guest',
                        last_name=last_name or 'Customer',
                        email=guest_email,
                        password_hash=hashlib.sha256(phone.encode()).hexdigest(),
                        phone=phone,
                        created_at=timezone.now()
                    )
                except Exception as second_error:
                    # If still fails, use first customer as default
                    customer = Customers.objects.first()
                    if not customer:
                        return Response({
                            'success': False,
                            'error': 'Не удалось создать заказ. Попробуйте позже.'
                        }, status=500)
        
        # Create or get shipping address
        address = None
        if order_data.get('delivery_type') == 'courier':
            try:
                address = Addresses.objects.create(
                    customer=customer,
                    country=order_data.get('country', ''),
                    region=order_data.get('region', ''),
                    city=order_data.get('city', ''),
                    street=order_data.get('street', ''),
                    house=order_data.get('house', ''),
                    apartment=order_data.get('apartment', ''),
                    type='delivery',
                    created_at=timezone.now()
                )
            except Exception as e:
                pass  # Address creation failed, but order can be created
        
        # Calculate total amount
        items = order_data.get('items', [])
        total_amount = 0
        
        # Create the order
        try:
            order = Orders.objects.create(
                customer=customer,
                order_date=timezone.now(),
                total_amount=0,  # Will be calculated from items
                status='pending',
                payment_method=order_data.get('payment_method', 'card'),
                payment_status='completed',
                shipping_address=address,
                tracking_number=None
            )
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Ошибка при создании заказа: {str(e)}'
            }, status=500)
        
        # Create order items
        try:
            for item in items:
                product_id = int(item.get('product_id'))
                quantity = int(item.get('quantity', 1))
                
                try:
                    product = Products.objects.get(product_id=product_id)
                    price = product.price
                    
                    OrderItems.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price_at_purchase=price
                    )
                    
                    total_amount += float(price) * quantity
                except Products.DoesNotExist:
                    continue  # Skip if product not found
        except Exception as e:
            pass  # Item creation error, but order is still valid
        
        # Update order total amount
        order.total_amount = total_amount
        # Add delivery cost
        if order_data.get('delivery_type') == 'courier':
            order.total_amount += 349
        order.save()
        
        # Generate order ID
        order_id = f'ORD_{order.order_id:08d}'
        transaction_id = order_data.get('transaction_id', 'TXN_' + str(order.order_id))
        
        return Response({
            'success': True,
            'order_id': order_id,
            'order_db_id': order.order_id,
            'transaction_id': transaction_id,
            'total': float(order.total_amount),
            'message': 'Заказ успешно создан'
        }, status=201)
        
    except Exception as e:
        import traceback
        print(f"Error creating order: {str(e)}")
        print(traceback.format_exc())
        return Response({
            'success': False,
            'error': f'Ошибка при создании заказа: {str(e)}'
        }, status=500)
    
