from django.shortcuts import render
from django.views import View
from product.models import Product


# Create your views here.

class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(avalibale=True)
        return render(request, 'home/home.html', {'products':products})
