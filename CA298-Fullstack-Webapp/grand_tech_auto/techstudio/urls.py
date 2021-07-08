from django.urls import path
from django.conf.urls import include
from . import views
from .forms import UserLoginForm
from rest_framework import routers, serializers, viewsets
from .models import CaUser, Product
from rest_framework.authtoken.views import obtain_auth_token


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CaUser
        fields = ['url', 'username', 'email', 'is_staff']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = []


class UserViewSet(viewsets.ModelViewSet):
    queryset = CaUser.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('products/<int:prodid>', views.singleproduct, name='single_product'),
    path('', views.index, name="index"),
    path('registration/', views.register, name="register"),
    path('blog/', views.blog, name="blog"),
    path('gaming/', views.gaming, name="gaming"),
    path('headphones/', views.headphones, name="headphones"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('monitor/', views.monitors, name="monitor"),
    path('stand/', views.stand, name="stand"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('category/', views.category, name="category"),
    path('terms/', views.terms, name="terms"),
    path('privacy/', views.privacy, name="privacy"),
    path('allproducts/', views.all_products, name="allproducts"),
    path('singleproduct/<int:prodid>', views.singleproduct),
    path('myform/', views.myform),
    path('usersignup/', views.signup, name="register"),
    path('adminsignup/', views.adminsignup, name="register"),
    path('login/', views.Login.as_view(template_name='login.html', authentication_form=UserLoginForm), name='login'),
    path('logout/', views.logout_view, name="logout"),
    path('addbasket/<int:prodid>', views.add_to_basket, name='add_to_basket'),
    path('api/', include(router.urls)),
    path('token/', obtain_auth_token, name="api_token_auth")
]
