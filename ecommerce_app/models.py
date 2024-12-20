from django.db import models
import datetime


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# customers
class Customer(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures", blank=True, null=True
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# all of ours products
class Product(models.Model):
    name = models.CharField(max_length=100)
    discount = models.IntegerField(default=0)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="uploads/product/")
    # add salte stufff
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=7)

    def discounted_price(self):
        # 40 - 40 * 10 / 100
        dis_price = self.price - self.price * self.discount / 100
        return dis_price

    def __str__(self):
        return self.name


# customers order
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default="", blank=True)
    phone = models.CharField(max_length=20, default="", blank=True)
    date_ordered = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Order of {self.quantity} {self.product.name} by {self.customer.first_name} {self.customer.last_name}"


# Cart Item model
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * (
            self.product.discounted_price()
            if self.product.discount
            else self.product.price
        )

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for {self.customer.user.first_name} {self.customer.user.last_name}"