from django.shortcuts import render, redirect

from .models import Product


def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {"products": products})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    print(product.category)
    related_products = Product.objects.filter(category__id=product.category.id)[:4]
    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "related_products": related_products,
        },
    )


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import CustomerRegistrationForm
from .models import Customer


def register_customer(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the User
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
                email=form.cleaned_data["email"],
            )
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()

            # Create the Customer
            customer = form.save(commit=False)
            customer.user = user
            customer.save()

            # Log the user in and redirect
            login(request, user)
            return redirect("home")  # Replace 'home' with your target URL name
    else:
        form = CustomerRegistrationForm()
    return render(request, "register_customer.html", {"form": form})


from django.shortcuts import get_object_or_404, redirect
from .models import Product, Customer, CartItem
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required


@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart_item, cart_created = CartItem.objects.get_or_create(
        product=product,
        customer=request.user.customer,
        defaults={"quantity": int(request.GET["quantity"])},
    )

    if not cart_created:
        cart_item.quantity += int(request.GET["quantity"])
        cart_item.save()

    return redirect("product-detail", product_id)


def cart_list(request):
    carts=[]
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

    return render(request, "cart.html", {"carts": carts})

def remove_from_cart(request, cart_item_id):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()

    return redirect('cart_list')
