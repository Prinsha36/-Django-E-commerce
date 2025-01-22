from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View, TemplateView, CreateView


from django.shortcuts import get_object_or_404, redirect
from .models import Product, Customer, CartItem
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import CustomerRegistrationForm
from .models import Customer
import hashlib

from .models import Product
import requests
from django.urls import reverse_lazy


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
    carts = []
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
        return redirect("login")

    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()

    return redirect("cart_list")


class PaymentDetailView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "payment.html")

    def post(self, request, *args, **kwargs):
        payment_method = request.POST.get("payment_method")
        print(payment_method)
        if payment_method == "esewa":
            return redirect("esewa-payment")
        # payment gateway integration
        return redirect("payment_success")


class EsewaPaymentView(TemplateView):
    template_name = "esewa_payment/esewa_payment_form.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        total_price = CartItem.objects.total_price_for_customer(customer)
        print("total_price: ", total_price, type(total_price))
        context.update(
            {
                "total_amount": total_price,
                "amount": total_price,
                "tax_amount": 0,
                "service_charge": 0,
                "delivery_charge": 0,
                "merchant_code": "YOUR_MERCHANT_CODE",
                "product_id": "PRODUCT_12345",
                "success_url": "http://localhost:8000/",
                "failure_url": "http://localhost:8000/payment-failed/",
            }
        )

        return context


class EsewaPaymentSuccessView(View):
    def get(self, request, *args, **kwargs):
        ref_id = request.GET.get("refId")
        amount = request.GET.get("amt")
        product_id = request.GET.get("pid")
        merchant_code = "YOUR_MERCHANT_CODE"

        if self.validate_esewa_payment(ref_id, amount, merchant_code, product_id):
            return HttpResponse("Payment Successful!")
        else:
            return HttpResponse("Payment Failed!")

    def validate_esewa_payment(self, ref_id, amount, merchant_code, product_id):
        url = "https://esewa.com.np/epay/transrec"
        params = {
            "amt": amount,
            "rid": ref_id,
            "pid": product_id,
            "scd": merchant_code,
        }
        response = requests.get(url, data=params)
        return "Success" in response.text


class EsewaPaymentFailedView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Payment Failed!")


class CustomerRegistrationView(CreateView):
    template_name = "CustomerRegistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecommerce_app:home")

    def form_valid(self, form):
        username = form.cleaned_data.get(username)
        password = form.cleaned_data.get(password)
        email = form.cleaned_data.get(email)


# class EsewaRequestView(View):
#     def get(self, request, *args, **kwargs):
#         # Retrieve the order data and other necessary information
#         o_id = request.GET.get("o_id")
#         order = Ordered.objects.get(id=o_id)  # Replace with your actual model and logic
#         access_key = "your_access_key"  # Replace with your eSewa access key
#         secret_key = "your_secret_key"  # Replace with your eSewa secret key

# # Prepare the data dictionary
#         data = {
#             "amount": "100",
#             "tax_amount": "10",
#             "total_amount": "110",
#             "transaction_uuid": "ab14a8f2b02c3",
#             "product_code": "EPAYTEST",

#             "access_key": access_key,
#             "signature": None,
#         }
