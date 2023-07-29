import json
from django.db import models
from django.contrib.auth.models import User
from Produit.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s cart: {self.product.Product_name}"


    

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    products = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name}  {self.last_name}"
    def get_products(self):
        products = json.loads(self.products)
        product_names = [p[0] for p in products]
        product_quantities = [p[1] for p in products]
        product_objects = Product.objects.filter(Product_name__in=product_names)
        return zip(product_objects, product_quantities)

