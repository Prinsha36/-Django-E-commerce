from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("product-detail/<int:pk>/", views.product_detail, name="product-detail"),
    path("cart-list/", views.cart_list, name="cart_list"),
    path("remove-cart/<int:cart_item_id>",views.remove_from_cart,name="remove_from_cart")
]
