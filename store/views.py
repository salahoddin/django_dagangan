from django.shortcuts import render, get_object_or_404
from . models import Category, Product

# Create your views here.
def store(request):
    return render(request, 'store/store.html')

def categories(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    return {'categories': categories, 'products': products}

def products(request):
    products = Product.objects.all()

    return render(request, '', {'products': products})

def product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    return render(request, 'store/product.html', {'product': product})