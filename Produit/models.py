from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Q


class ProductManager(models.Manager):
    def search(self, query):
        return self.filter(
            Q(Product_name__icontains=query)
            | Q(brand__icontains=query)
            | Q(description__icontains=query)
        )


class ProductSeries(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField("Series slug", null=False, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Series"


class Product(models.Model):
    Product_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_slug = models.SlugField("Product slug", null=False, blank=False)
    currency = models.CharField(max_length=3, default="USD")
    image = models.ImageField(upload_to="products")
    description = models.TextField()
    brand = models.CharField(max_length=255)
    series = models.ForeignKey(
        ProductSeries, default="", verbose_name="Series", on_delete=models.SET_DEFAULT
    )
    quantity_in_stock = models.IntegerField()
    is_in_stock = models.BooleanField(default=True)
    objects = ProductManager()

    def is_in_stock(self):
        return self.quantity_in_stock > 0

    def save(self, *args, **kwargs):
        if not self.product_slug:
            self.product_slug = str(uuid.uuid4())
        super().save(*args, **kwargs)

    @staticmethod
    def search(query, owner=None):
        products = Product.objects.filter(Product_name__icontains=query)
        if owner:
            products = products.filter(owner=owner)
        return products
