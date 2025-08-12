from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=256)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='supplier_logos/', blank=True, null=True)
    website = models.URLField(blank=True)
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/', default="default.jpg")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    suppliers = models.ManyToManyField(Supplier)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    expiry_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    quantity_change = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity_change})"
