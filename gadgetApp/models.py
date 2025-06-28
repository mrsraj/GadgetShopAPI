from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    role = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    # Avoid field name clashes by setting `related_name` attributes
    groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_users_permissions", blank=True)

    def __str__(self):
        return self.username
    
    
## project releted Model:-

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    stock_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()  # or use ImageField if storing files

    def __str__(self):
        return f"Image for {self.product.name}"
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    ram = models.CharField(max_length=50)         # 4GB, 8GB, 16GB, etc.
    processor = models.CharField(max_length=50)   # i3, i5, i7
    storage = models.CharField(max_length=50)     # 256GB, 512GB
    
class ProductPrice(models.Model):
    product = models.ForeignKey(Product, related_name='prices', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, related_name='prices', on_delete=models.CASCADE)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.IntegerField()
    bought_last_month = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # 3.6
    review_count = models.IntegerField(default=0)
    
class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, related_name='specs', on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    value = models.TextField()
    
class ProductPolicy(models.Model):  # Fixing name from ProductPlicy
    product = models.ForeignKey(Product, related_name='policies', on_delete=models.CASCADE)
    delivery_note = models.CharField(max_length=100)          # e.g., "7 Days Replacement"
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)  # e.g., 0 or 199.00

    def __str__(self):
        return f"{self.delivery_note} (₹{self.delivery_charge})"
    
##CART TABLE
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Credit Card', 'Credit Card'),
        ('UPI', 'UPI'),
        ('Netbanking', 'Netbanking'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    paid_at = models.DateTimeField(null=True, blank=True)
