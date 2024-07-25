from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('product/<slug:slug>/', views.product, name='product'),
    path('category/<slug:slug>/', views.list_category, name='list-category'),
]