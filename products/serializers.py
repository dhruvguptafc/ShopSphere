from rest_framework import serializers
from .models import Product
from django.contrib.auth.models import User
from cart.models import OrderItem

class ProductSerializer(serializers.ModelSerializer):
    def validate_stock_quantity(self,value):
        if value > 1000:
            raise serializers.ValidationError(
                "Stock quantity can not be more than 1000"
            )
        return value
    def validate(self,data):
        if data["stock_quantity"] > 0 and data["price"] == 0:
            raise serializers.ValidationError(
                "a product with stock must have a price greater than 0"
            )
        return data
    class Meta:
        model = Product
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username","email","password",]
        extra_kwargs = {
         "password": {"write_only": True}
        }

    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "price", "quantity"]