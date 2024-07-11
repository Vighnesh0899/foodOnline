from django.shortcuts import render, get_object_or_404, redirect
from vendor.forms import vendorForm
from accounts.forms import UserProfileForm

from vendor.models import Vendor
from accounts.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from Menu.models import Category, FoodItem
from Menu.forms import CategoryForm
from django.template.defaultfilters import slugify

def get_vendor(request):
    vendor = Vendor.objects.get(user = request.user)
    return vendor

# Create your views here.
@login_required(login_url = 'login')
@user_passes_test(check_role_vendor)
def v_profile(request):
    profile = get_object_or_404(UserProfile, user = request.user)
    vendor = get_object_or_404(Vendor, user = request.user)

    if request.method =='POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = vendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Profile Updated.")
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(profile_form.errors)
    else:

        profile_form = UserProfileForm(instance=profile)
        vendor_form = vendorForm(instance=vendor)

    context ={
        'profile_form' : profile_form,
        'vendor_form' : vendor_form,
        'profile' : profile,
        'vendor' :  vendor,
    }
    return render(request, 'vendor/vprofile.html', context)

def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor = vendor).order_by('created_at')
    context = {
        'categories' : categories,
    }

    return render(request, 'vendor/menu_builder.html', context)

def fooditems_by_category(request,pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor= vendor, category=category)
    context ={
        'fooditems' : fooditems,
        'category' : category,
    }
    return render(request, 'vendor/fooditems_by_category.html', context)


def add_category(request):
    if request.method =="POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "category added successfully!")
            return redirect('menu_builder')
        else:
            pass
    else:
        form = CategoryForm()
    context = {
        'form' : form,
    }
    return render(request, 'vendor/add_category.html', context)


def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method =="POST":
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "category updated successfully!")
            return redirect('menu_builder')
        else:
            pass
    else:
        form = CategoryForm(instance=category)
    context = {
        'form' : form,
        'category' : category,
    }
    return render(request, 'vendor/edit_category.html', context)

def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request,' Category has been detele successfully!')
    return redirect('menu_builder')