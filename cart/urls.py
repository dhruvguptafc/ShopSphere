
from django.urls import  path
from .views import OrderHistoryView
from . import views



urlpatterns = [
   
    
    path('add/<int:pk>/',views.add_to_cart,name="add_to_cart"),
    path('',views.cart,name="cart"),
    path('remove/<int:pk>/',views.remove,name="remove"),
    path('update/<int:pk>/',views.update_cart,name="update_cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('OrderHistoryView/',OrderHistoryView.as_view(),name="order_history"),
    path('payment-success/', views.payment_success, name='payment_success'),
]

