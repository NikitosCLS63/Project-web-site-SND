# C:\WebsiteDjSND\main\urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import home, catalog, promotions, register, login
from django.views.generic import TemplateView
urlpatterns = [
    path('', include('apps.products.urls')),
    
    # Админ-панель
    path('admin-panel/', TemplateView.as_view(template_name='admin/admin_panel.html'), name='admin_panel'),
    
    path('', home, name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('catalog/', TemplateView.as_view(template_name='catalog.html'), name='catalog'),
    path('promotions/', TemplateView.as_view(template_name='promotions.html'), name='promotions'),
    path('password_reset/', TemplateView.as_view(template_name='auth/password_reset.html')),
    path('reset-password-confirm/', TemplateView.as_view(template_name='auth/reset_password_confirm.html')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)