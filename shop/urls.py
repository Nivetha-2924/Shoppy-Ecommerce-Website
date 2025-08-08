from django.urls import path
from . import views

urlpatterns=[
    path('',views.home, name="home"),
    path('register/',views.register, name="register"),
    path('login/',views.login_page, name="login"),
    path('logout/',views.logout_page, name="logout"),
    path('cart/',views.cart_page, name="cart"),
    path('favourites/',views.favouritepage, name="favourites"),
    path('favouritepage/',views.favouritepage, name="favouritepage"),
    path('remove_fav/<int:fid>',views.remove_favourite, name="remove_favourite"),
    path('remove_cart/<str:cid>',views.remove_cart, name="remove_cart"),
    path('collections/',views.collections, name="collections"),
    path('collections/<str:cname>/',views.collection_view, name="collections_view"),
    path('collections/<str:cname>/<str:pname>',views.product_details, name="product_details"),
    path('addtocart/',views.add_to_cart, name="add_to_cart"),
    
    
]