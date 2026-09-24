from celery import shared_task
from django.core.mail import send_mail

from .models import Order


@shared_task
def send_order_confirmation_email(order_id):
    order = Order.objects.get(id=order_id)

    send_mail(
        subject=f"Order #{order.id} confirmed",
        message=f"Your order #{order.id} has been successfully placed.\n\n"
                f"Total: ₹{order.total_price}\n\n"
                f"Thank you for shopping with us!",
        from_email="test@example.com",
        recipient_list=[order.user.email],
    )

    return f"Confirmation email sent for order #{order.id}"