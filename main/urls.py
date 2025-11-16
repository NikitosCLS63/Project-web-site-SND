# C:\WebsiteDjSND\main\urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import home, catalog, promotions, register, login, admin_panel, admin_users
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('apps.products.urls')),
    
    # Админ-панель с защитой
    path('admin-panel/', admin_panel, name='admin_panel'),
    path('admin-panel/users/', admin_users, name='admin_users'),

    path('', home, name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path('compony/', TemplateView.as_view(template_name='compony.html'), name='compony'),
    
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('catalog/', TemplateView.as_view(template_name='catalog.html'), name='catalog'),
    path('promotions/', TemplateView.as_view(template_name='promotions.html'), name='promotions'),
    path('cart/', TemplateView.as_view(template_name='cart.html'), name='cart'),
    path('decoration/', TemplateView.as_view(template_name='decoration.html'), name='decoration'),
    path('decoration-success/', TemplateView.as_view(template_name='decoration-success.html'), name='decoration_success'),
    path('password_reset/', TemplateView.as_view(template_name='auth/password_reset.html')),
    path('reset-password-confirm/', TemplateView.as_view(template_name='auth/reset_password_confirm.html')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)