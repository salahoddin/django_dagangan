from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_summary, name='cart-summary'),
    path('add', views.cart_add, name='cart-add'),
    path('delete', views.cart_summary, name='cart-delete'),
    path('update', views.cart_summary, name='cart-update'),
]