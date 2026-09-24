from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import OrderItemSerializer

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source="orderitem_set", many=True, read_only=True)
    class Meta:
        model = Order
        fields = ["id", "created_at", "total_price", "status","items"]
