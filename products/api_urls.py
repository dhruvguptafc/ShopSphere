from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProductViewSet
from . import views

router = DefaultRouter()

router.register("products", ProductViewSet)

urlpatterns = [
    *router.urls,

    path("register/", views.register, name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("order-items/", views.order_items, name="order_items"),
]