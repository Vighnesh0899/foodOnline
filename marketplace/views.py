from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from vendor.models import Vendor
from django.shortcuts import get_object_or_404
from Menu.models import Category, FoodItem
from django.db.models import Prefetch
from .models import Cart
from marketplace.context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required

# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved = True, user__is_active =True)
    vendor_count = vendors.count()
    context = {
        'vendors' : vendors,
        'vendor_count' : vendor_count, 
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor =get_object_or_404(Vendor, vendor_slug = vendor_slug)
    categories = Category.objects.filter(vendor = vendor).prefetch_related(
        Prefetch(
            'fooditems', queryset= FoodItem.objects.filter(is_available = True)
        )
    )

    if request.user.is_authenticated:
        cart_item =Cart.objects.filter(user=request.user)
    else:
        cart_item=None

    context={
        'vendor' : vendor,
        'categories' : categories,
        'cart_item' :cart_item
    }

    return render(request, 'marketplace/vendor_details.html',context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        # if request.is_ajax():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #check if the food item exist
            try:
                fooditem = FoodItem.objects.get(id =food_id)
                # check if the user has already added that food to the cart
                try:
                    chkcart = Cart.objects.get(user = request.user, fooditem=fooditem)
                    #Increase the cart quntity
                    chkcart.quantity+=1
                    chkcart.save()
                    return JsonResponse({'status' : 'success', 'message': 'Increased the cart quantity', 'cart_counter' : get_cart_counter(request), 'qty' : chkcart.quantity, 'cart_amount' : get_cart_amounts(request)})
                except:
                    chkcart = Cart.objects.create(user = request.user, fooditem = fooditem, quantity = 1)
                    return JsonResponse({'status' : 'success', 'message': 'added food to the cart', 'cart_counter' : get_cart_counter(request), 'qty' : chkcart.quantity, 'cart_amount' : get_cart_amounts(request)})
            except:
                return JsonResponse({'status' : 'Failed', 'message': 'food does not exist. '})
        else:
            return JsonResponse({'status' : 'Failed', 'message': 'Invalid. '})
       
    else:

        return JsonResponse({'status' : 'login reqired', 'message': 'Please login to continue. '})
    


def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        # if request.is_ajax():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #check if the food item exist
            try:
                fooditem = FoodItem.objects.get(id =food_id)
                # check if the user has already added that food to the cart
                try:
                    chkcart = Cart.objects.get(user = request.user, fooditem=fooditem)
                    if chkcart.quantity > 1:
                        #Decrease the cart quntity
                        chkcart.quantity-=1
                        chkcart.save()
                    else:
                        chkcart.delete()
                        chkcart.quantity=0    
                    return JsonResponse({'status' : 'success', 'message': 'Decreased the cart quantity', 'cart_counter' : get_cart_counter(request),'qty' : chkcart.quantity, 'cart_amount' : get_cart_amounts(request)})
                except:
                    
                    return JsonResponse({'status' : 'Failed', 'message': 'You do not have a item in your cart!'})
            except:
                return JsonResponse({'status' : 'Failed', 'message': 'food does not exist. '})
        else:
            return JsonResponse({'status' : 'Failed', 'message': 'Invalid. '})
       
    else:

        return JsonResponse({'status' : 'login reqired', 'message': 'Please login to continue. '})
    
    
@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user = request.user).order_by('created_at')
    context ={
        'cart_items' : cart_items,
    }
    return render(request, 'marketplace/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status' : 'success', 'message': 'cart item has been deleted ', 'cart_counter' : get_cart_counter(request), 'cart_amount' : get_cart_amounts(request)})
            except:
                return JsonResponse({'status' : 'Failed', 'message': 'food does not exist. '})
        else:
            return JsonResponse({'status' : 'Failed', 'message': 'Invalid request. '})