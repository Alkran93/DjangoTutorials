from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from .models import Product 


# Create your views here.
##def homePageView(request): 
##    return HttpResponse('Hello World!')
class HomePageView(TemplateView):
    template_name = 'pages/home.html'
    
class AboutPageView(TemplateView):
 template_name = 'pages/about.html'

 def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
        "title": "About us - Online Store",
        "subtitle": "About us",
        "description": "This is an about page ...",
        "author": "Developed by: SOFIA ZAPATA ZULUAGA",
 })
    return context

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact - Online Store",
            "subtitle": "Contact Us",
            "email": "information@OnlineStore.com",
            "address": "Calle 30b #69b-5, Medellin, Colombia",
            "phone": "+57 (310) 821-0492",
        })
        return context

#class Product:
#    products = [
#       {"id":"1", "name":"TV", "description":"Best TV"},
#       {"id":"2", "name":"iPhone", "description":"Best iPhone"},
#       {"id":"3", "name":"Chromecast", "description":"Best Chromecast"},
#       {"id":"4", "name":"Glasses", "description":"Best Glasses"}
# ]

class ProductIndexView(View):
    template_name = 'products/index.html'
 
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] =  Product.objects.all()
        
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("El id del producto debe ser 1 o mayor")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            # Si el id del producto no es válido, redirige a la página principal
            return HttpResponseRedirect(reverse('home'))

        viewData = {}
        product = get_object_or_404(Product, pk=product_id)
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] =  product.name + " - Product information"
        viewData["product"] = product

        return render(request, self.template_name, viewData)
   
#class Product:
#    products = [
#        {"id": "1", "name": "TV", "description": "Best TV", "price": 499.999},
#       {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 999.999},
#       {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 39.999},
#       {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 89.999}
#    ]

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than zero')
        return price

 
class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create product",
            "form": form
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('product-created') 
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)

        
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'  # Esto te permitirá recorrer 'products' en tu plantilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context


