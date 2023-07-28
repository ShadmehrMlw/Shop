from django.shortcuts import render, get_object_or_404
from django.views import View
from product.models import Product, Category
from accounts.forms import ProductDetailForm


# Create your views here.

class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(avalibale=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        context = {
            'products': products,
            'categories': categories
        }
        return render(request, 'home/home.html', context)

class DetailView(View):
    def get(self, reqest, slug):
        product = get_object_or_404(Product, slug=slug)
        form = ProductDetailForm()
        context = {
            'product': product,
            'form': form
        }
        return render(reqest, 'home/detail.html', context)
