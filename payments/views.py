from django.conf import settings  # new
from django.http.response import JsonResponse  # new
from django.views.decorators.csrf import csrf_exempt  # new
from django.views.generic.base import TemplateView
import stripe
from django.shortcuts import render, redirect

class test(TemplateView):
    template_name = "subscription/subscription.html"


# new
@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


from django.contrib.auth.models import Group

def under_development(request):
    return render(request, 'dashboard/Product/under_development.html')
@csrf_exempt
def create_checkout_session(request):
    if request.method == "GET":
        domain_url = "http://127.0.0.1:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "price": "price_1N6Vs3FKWJoO9geeL81754r2",
                        "quantity": 1,
                    }
                ],
            )

            # Add user to Subscriber group upon successful payment
            return redirect('under_development')
            #return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return redirect('under_development')
            #return JsonResponse({"error": str(e)})
    return redirect('under_development')

class SuccessView(TemplateView):
    template_name = "dashboard/subscription/success.html"


class CancelledView(TemplateView):
    template_name = "dashboard/subscription/cancelled.html"


@csrf_exempt
def create_checkout_session_market(request):
    if request.method == "GET":
        domain_url = "http://127.0.0.1:8000/"
        try:
            # Get the total price from the previous order
            total_price = request.POST.get("total_price")

            # Create a new Checkout Session for the order
            checkout_session = stripe.checkout.Session.create(
                success_url=request.build_absolute_uri(
                    "/success?session_id={CHECKOUT_SESSION_ID}"
                ),
                cancel_url=request.build_absolute_uri("/cancelled/"),
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": int(total_price * 100),  # convert to cents
                            "product_data": {
                                "name": "Order payment",
                            },
                        },
                        "quantity": 1,
                    },
                ],
            )

            # Redirect to the checkout page
            return redirect('under_development')
            #return redirect(checkout_session.url)

        except Exception as e :
            return redirect('under_development')
            #return JsonResponse({"error": str(e)})



