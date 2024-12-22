from ecommerce_app.models import CartItem


def ecom_data(request):
    data = {}

    print(request.user)
    # CartItem.objects.filter
    if hasattr(request.user, "customer"):
        total_cart_items = 0

        carts = CartItem.objects.filter(customer=request.user.customer)
        for cart in carts:
            total_cart_items += cart.quantity

        data.update({"total_cart_items": total_cart_items})
        print(request.user.customer)

    print(data)

    return data
