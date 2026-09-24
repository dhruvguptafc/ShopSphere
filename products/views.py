from django.shortcuts import render
# Create your views here.
from django.views.generic import DetailView, ListView
from .serializers import OrderItemSerializer, ProductSerializer, RegisterSerializer
from .models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permisions import IsAdminForPost
from cart.models import OrderItem
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "product_list.html"
class ProductDetailView(DetailView):
    model = Product
    context_object_name = "productinfo"
    template_name = "product_detail.html"

@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=201)
    return Response(serializer.errors,status=400)

@api_view(["GET"])
def order_items(request):
    items = OrderItem.objects.all()
    serializer = OrderItemSerializer(items, many=True)
    return Response(serializer.data)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminForPost]

    def get_queryset(self):
        products=Product.objects.all()

        min_price = self.request.query_params.get("min_price")
        if min_price:
             products = products.filter(price__gte=min_price)

        max_price = self.request.query_params.get("max_price")
        if max_price:
            products = products.filter(price__lte=max_price)

        search = self.request.query_params.get("search")
        if search:
            products = products.filter(product_name__icontains=search)

        allowed_ordering = ["price", "product_name", "stock_quantity"]

        ordering = self.request.query_params.get("ordering")

        if ordering:
            field = ordering.lstrip("-")

            if field in allowed_ordering:
                products = products.order_by(ordering)
        

        return products


