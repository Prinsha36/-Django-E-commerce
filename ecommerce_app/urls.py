from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("product-detail/<int:pk>/", views.product_detail, name="product-detail"),
    path("cart-list/", views.cart_list, name="cart_list"),
]
