from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from .tasks import send_order_confirmation_email
# Create your views here.
from products.models import Product
from .cart import Cart
from django.contrib.auth.decorators import login_required
from .models import Order,OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin
import razorpay
from django.conf import settings
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from .models import Order
from .serializers import OrderSerializer
def add_to_cart(request,pk):
    product = get_object_or_404(Product,pk=pk)
    cart = Cart(request)
    cart.add(product)
    return redirect('product_list')


def cart(request):
    cart = Cart(request)

    context  = {
        'cart':cart
    }

    return render(request,'cart.html',context)

def remove(request,pk):
    product = get_object_or_404(Product,pk=pk)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart')


def update_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart(request)
    quantity = int(request.POST['quantity'])
    cart.cart[str(pk)]['quantity'] = quantity
    cart.save()
    return redirect('cart')


@login_required
def checkout(request):
    cart = Cart(request)
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )
    total = cart.get_total_price()
    amount = int(total * 100)

    payment_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })
    return render(request, "checkout.html", {
        "cart": cart,
        "payment_order": payment_order,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID
    })
    



class OrderHistoryView(LoginRequiredMixin,ListView):
    model = Order
    def get_queryset(self):
        
        return Order.objects.filter(user=self.request.user)
    context_object_name = "orderhistory"
    template_name = "order_history.html"


@csrf_exempt
@login_required
def payment_success(request):

    data = json.loads(request.body)

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })

    except razorpay.errors.SignatureVerificationError:
        return JsonResponse(
            {"error": "Payment verification failed"},
            status=400
        )

    cart = Cart(request)

    with transaction.atomic():

        order = Order.objects.create(
            user=request.user,
            total_price=cart.get_total_price(),
            status="completed"
        )
        transaction.on_commit(
            lambda: send_order_confirmation_email.delay(order.id)
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                price=item["price"],
                quantity=item["quantity"]
            )

        for item in cart:
            product = item["product"]
            product.stock_quantity -= item["quantity"]
            product.save()

    cart.clear()

    return JsonResponse({
        "message": "Payment successful",
        "order_id": order.id
    })

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return (Order.objects.filter(user=self.request.user).prefetch_related("orderitem_set__product"))

    