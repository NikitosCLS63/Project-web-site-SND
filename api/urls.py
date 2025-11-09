# api/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = routers.DefaultRouter()

# Products
router.register(r'categories', CategoryViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'products', ProductViewSet)


# Users
router.register(r'customers', CustomerViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)
router.register(r'addresses', AddressViewSet)

# Cart
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'wishlists', WishlistViewSet)

# Orders
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'shipments', ShipmentViewSet)
router.register(r'product-returns', ProductReturnViewSet)

# Reviews
router.register(r'reviews', ReviewViewSet)

# Promotions
router.register(r'promotions', PromotionViewSet)

# Analytics
router.register(r'audit-logs', AuditLogViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'report-items', ReportItemViewSet)
router.register(r'analytics-snapshots', AnalyticsSnapshotViewSet)
router.register(r'analytics-metrics', AnalyticsMetricViewSet)
router.register(r'backup-logs', BackupLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # === АВТОРИЗАЦИЯ ===
    path('login/', views.LoginView.as_view(), name='api_login'),
    path('register/', views.RegisterView.as_view(), name='api_register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', views.PasswordResetView.as_view()),
    path('password_reset_confirm/', views.PasswordResetConfirmView.as_view()),
]
