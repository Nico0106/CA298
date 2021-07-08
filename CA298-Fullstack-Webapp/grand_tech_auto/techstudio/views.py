from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import CaUser, Product, ShoppingBasketItems, ShoppingBasket
from .forms import *
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.decorators import login_required
from .permissions import admin_required
from .forms import SignUpForm
from django.core import serializers



'''
class CaUserSignUpView(CreateView):
    model = CaUser
    form_class = CASignForm
    template_name = 'causersignup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/') 
'''


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'causersignup.html', {'form': form})


def adminsignup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = AdminSignUpForm()
    return render(request, 'admin_signup.html', {'form': form})

'''
class AdminSignUpView(CreateView):
    model = CaUser
    form_class = AdminSignUpForm
    template_name = 'admin_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')
'''


def index(request):
    return render(request, 'index.html')


def category(request):
    return render(request, 'categories.html')


def blog(request):
    return render(request, 'blog.html')


def gaming(request):
    return render(request, 'gaming.html')


def headphones(request):
    return render(request, 'headphones.html')


def monitors(request):
    return render(request, 'monitors.html')


def stand(request):
    return render(request, 'stand.html')


def checkout(request):
    return render(request, 'checkout.html')


def cart(request):
    return render(request, 'cart.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def terms(request):
    return render(request, 'terms.html')


def privacy(request):
    return render(request, 'privacy.html')


def register(request):
    return render(request, 'registration.html')


def all_products(request):
    all_p = Product.objects.all()
    # check has a user passed in a format flag
    flag = request.GET.get('format', '')
    if flag == 'json':
        serialised_products = serializers.serialize("json", all_p)
        return HttpResponse(serialised_products, content_type="application/json")
    else:
        return render(request, 'all_products.html', {'products': all_p})


def singleproduct(request, prodid):
    prod = get_object_or_404(Product, pk=prodid)   # Product.object.get(pk=prodid)
    return render(request, 'single_product.html', {'product': prod})


@login_required
# @admin_required
def myform(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save()
            return render(request, 'single_product.html', {'product': new_product})
    else:
        form = ProductForm()
        return render(request, 'form.html', {'form': form})


from django.contrib.auth.views import LoginView


class Login(LoginView):
    template_name = 'login.html'


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def add_to_basket(request, prodid):
    user = request.user
    shopping_basket_list = ShoppingBasket.objects.filter(user_id=user).first()
    if not shopping_basket_list:
        shopping_basket = ShoppingBasket(user_id=user).save()
    product = Product.objects.get(pk=prodid)
    sbi = ShoppingBasketItems.objects.filter(basket_id=shopping_basket_list.id, product_id=product.id).first()
    if sbi is None:
        sbi = ShoppingBasketItems(basket_id=shopping_basket, product_id=product.id).save()
    else:
        sbi.quantity = sbi.quantity+1
        sbi.save()
    return render(request, 'single_product.html', {'product': product, 'added': True})
