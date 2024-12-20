"""
URL configuration for ECOMMERCE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from ecommerce_app.views import register_customer
from ecommerce_app.views import add_to_cart

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("ecommerce_app.urls")),
    path("add-to-cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("register/", register_customer, name="register_customer"),
    path("accounts/login/", views.LoginView.as_view(), name="login"),
    path("accounts/logout/", views.LogoutView.as_view(), name="logout"),
]


if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
