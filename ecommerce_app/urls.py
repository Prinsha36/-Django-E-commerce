from django.urls import path
from . import views
from .views import EsewaPaymentView, EsewaPaymentSuccessView, EsewaPaymentFailedView

urlpatterns = [
    path("", views.home, name="home"),
    path("product-detail/<int:pk>/", views.product_detail, name="product-detail"),
    path("cart-list/", views.cart_list, name="cart_list"),
    path(
        "remove-cart/<int:cart_item_id>",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("payment/", views.PaymentDetailView.as_view(), name="payment"),
    path("esewa-payment/", EsewaPaymentView.as_view(), name="esewa-payment"),
    path("payment-success/", EsewaPaymentSuccessView.as_view(), name="payment_success"),
    path("payment-failed/", EsewaPaymentFailedView.as_view(), name="payment_failed"),
]
