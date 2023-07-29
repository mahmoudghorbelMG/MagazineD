from decimal import Decimal
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from .models import Cart
from Produit.models import Product, ProductSeries
from .models import Orders
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from notifications.signals import notify


def is_authenticated(user):
    return user.is_authenticated


def market(request):
    series = ProductSeries.objects.all()
    products = Product.objects.all()
    return render(
        request, "market/market.html", {"series": series, "products": products}
    )


def shop(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    total_price = (
        sum([item.quantity * item.product.price for item in cart_items])
        if cart_items
        else 0
    )
    products = Product.objects.all()
    series = ProductSeries.objects.all()

    # filtrer par prix minimum
    min_price = request.GET.get("min_price")
    if min_price:
        products = products.filter(pricegte=min_price)

    # filtrer par prix maximum
    max_price = request.GET.get("max_price")
    if max_price:
        products = products.filter(pricelte=max_price)

    return render(
        request,
        "market/shop.html",
        {"products": products, "total_price": total_price, "series": series},
    )


@user_passes_test(is_authenticated, login_url="sign")
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum([item.quantity * item.product.price for item in cart_items])
    return render(
        request,
        "market/cart.html",
        {"cart_items": cart_items, "total_price": total_price},
    )


@user_passes_test(is_authenticated, login_url="sign")
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    if not product.is_in_stock():
        notify.send(
            request.user,
            recipient=product.owner,
            verb=f"Your {product.Product_name}  is out of stock",
        )

    if quantity > product.quantity_in_stock:
        messages.error(
            request, f"Sorry, only {product.quantity_in_stock} left in stock."
        )
    else:
        cart_item, created = Cart.objects.get_or_create(
            user=request.user, product=product
        )
        if created:
            messages.success(request, f"{product.Product_name} added to your cart.")
        else:
            cart_item.quantity += quantity
            cart_item.save()
            messages.success(
                request, f"{quantity} {product.Product_name} added to your cart."
            )

    return redirect("shop")


def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(
        request, f"{cart_item.product.Product_name} removed from your cart."
    )
    return redirect("cart")


def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    new_quantity = int(request.POST.get("quantity", 1))
    if new_quantity > cart_item.product.quantity_in_stock:
        messages.error(
            request, f"Sorry, only {cart_item.product.quantity_in_stock} left in stock."
        )
    else:
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, f"{cart_item.product.Product_name} quantity updated.")
    return redirect("cart")


def check(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum([item.quantity * item.product.price for item in cart_items])
    if not cart_items:
        # Redirect the user to the cart page and show a message
        messages.warning(request, "Your cart is empty.")
        return redirect("cart")
    return render(
        request,
        "market/checkout.html",
        {"cart_items": cart_items, "total_price": total_price},
    )


def place_order(request):
    if request.method == "POST":
        # get form data
        user = request.user
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        country = request.POST.get("country")
        city = request.POST.get("city")
        zip_code = request.POST.get("zip_code")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        products = request.POST.getlist("products[]")
        quantities = request.POST.getlist("quantities[]")
        total = request.POST.get("total")

        # create a new order object
        order = Orders.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            country=country,
            city=city,
            zip_code=zip_code,
            phone=phone,
            email=email,
            products=json.dumps(list(zip(products, quantities))),
            total=total,
            quantity=sum(map(int, quantities)),
        )

        # decrement product quantities
        for product_name, quantity in zip(products, quantities):
            product = Product.objects.get(Product_name=product_name)
            product.quantity_in_stock -= int(quantity)
            product.save()

        Cart.objects.filter(user=request.user).delete()
        # show success message and redirect to success page
        messages.success(request, "Order placed successfully.")
        return render(request, "market/place_order.html")
    else:
        # show error message and redirect back to order form
        messages.error(
            request, "There was a problem with your order. Please try again."
        )
        return redirect("check")


def details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    products = Product.objects.all()
    return render(
        request,
        "market/details.html",
        context={"product": product, "products": products},
    )


def searchMarket(request):
    query = request.GET.get("q")
    products = Product.search(query) if query else Product.objects.all()
    context = {"products": products, "query": query}
    return render(request, "market/search_market.html", context)


def series_detail(request, series_id):
    series = get_object_or_404(ProductSeries, id=series_id)
    products = Product.objects.filter(series=series)
    ser = ProductSeries.objects.all()
    brands = set([product.brand for product in products])
    return render(
        request,
        "market/series_detail.html",
        {"series": series, "products": products, "ser": ser, "brands": brands},
    )
