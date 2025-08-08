from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from .forms import CustomUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from shop.models import Cart
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Favourite


# Create your views here.
def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})

def favouritepage(request):
    if request.user.is_authenticated:
        favourite=Favourite.objects.filter(user=request.user)
        return render(request,"shop/favourite.html",{"favourite":favourite})
    else:
        return redirect("/")
    
@login_required
def remove_favourite(request, fid):
    fav_item = get_object_or_404(Favourite, id=fid, user=request.user)
    fav_item.delete()
    return redirect("favourites")


def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect("/")
    
@login_required
def remove_cart(request, cid):
    cart_item = get_object_or_404(Cart, id=cid, user=request.user)
    cart_item.delete()
    return redirect("cart")

@login_required
def favourite_list(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product_id = data['pid']

                product = Product.objects.get(id=product_id)

                fav_item, created = Favourite.objects.get_or_create(
                    user=request.user,
                    product=product
                )

                if not created:
                    return JsonResponse({'status': 'Already in favourites'}, status=200)
                else:
                    return JsonResponse({'status': 'Added to favourites'}, status=200)

            except Product.DoesNotExist:
                return JsonResponse({'status': 'Product not found'}, status=404)
            except Exception as e:
                return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)
        else:
            return JsonResponse({'status': 'Login to add to favourites'}, status=401)
    else:
        return JsonResponse({'status': 'Invalid request'}, status=400)


        
    

@csrf_exempt
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product_qty = data['product_qty']
                product_id = data['pid']

                product_status = Product.objects.get(id=product_id)
                if product_status:
                    cart_item, created = Cart.objects.get_or_create(
                        user=request.user,
                        product_id=product_id,
                        defaults={'product_qty': product_qty}
                    )

                    if not created:
                        if product_status.quantity >= cart_item.product_qty + int(product_qty):
                            cart_item.product_qty += product_qty
                            cart_item.save()
                            return JsonResponse({'status': 'Cart updated'}, status=200)
                        else:
                            return JsonResponse({'status': 'Not enough stock'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product added to cart'}, status=200)

            except Product.DoesNotExist:
                return JsonResponse({'status': 'Product not found'}, status=404)
            except Exception as e:
                return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)
        else:
            return JsonResponse({'status': 'Login to add to cart'}, status=401)
    else:
        return JsonResponse({'status': 'Invalid request'}, status=400)

   

def logout_page(request):
   if request.user.is_authenticated:
      logout(request)
      messages.success(request,"Logged out Successfully")
   return redirect("/")

def login_page(request):
    if request.user.is_authenticated:
       return redirect("/")
    else:
       if request.method=='POST':
          name=request.POST.get('username')
          pwd=request.POST.get('password')
          user=authenticate(request,username=name,password=pwd)
          if user is not None:
             login(request,user)
             messages.success(request,"Logged in Successfully")
             return redirect("/")
          else:
             messages.error(request,"Invalid User Name or Password")
             return redirect("/login")
       return render(request,"shop/login_page.html")


def register(request):
    form=CustomUserForm()
    if request.method=='POST':
       form=CustomUserForm(request.POST)
       if form.is_valid():
          form.save()
          messages.success(request,"Registration Success You can Login Now!!")
          return redirect('login')
    return render(request,"shop/register.html",{'form':form})

def collections(request):
    category = Category.objects.filter(status=0)
    return render(request,"shop/collections.html",{"category":category})

def collection_view(request,cname):
   if(Category.objects.filter(name=cname,status=0)):
     products=Product.objects.filter(category__name=cname)
     return render(request,"shop/products/index.html",{"products":products,"category_name":cname})
   else:
      messages.warning(request,"No such category found")
      return redirect('collections')

def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
       if(Product.objects.filter(name=pname,status=0)):
          products=Product.objects.filter(name=pname,status=0).first()
          return render(request,"shop/products/product_details.html",{"products":products})
       else:
          messages.error(request,"No Such Product Found")
          return redirect('collections')
    else:
       messages.error(request,"No Such Category Found")
       return redirect('collections')
       