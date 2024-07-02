from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import vendorForm
from . models import User, UserProfile
from django.contrib import messages

# Create your views here.

def registerUser(request):
    if request.method == "POST":
        form =UserForm(request.POST)
        if form.is_valid():
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.role =User.CUSTOMER
            # user.set_password(password)
            # user.save()
            # return redirect('registeruser')

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            user =User.objects.create_user(first_name = first_name, last_name=last_name, username= username, email=email, password = password)
            user.role =User.CUSTOMER
            user.save()
            messages.success(request, "Your account has been register successfully")
            return redirect('registeruser')

        else:
            print(form.errors)
    else:
        form = UserForm()
    context = { 
        'form' : form,
    }
    return render(request, 'accounts/registeruser.html', context)


def registerVendor(request):
    if request.method == 'POST':
        #store the data and create the user
        form = UserForm(request.POST)
        v_form = vendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            user =User.objects.create_user(first_name = first_name, last_name=last_name, username= username, email=email, password = password)
            user.role =User.VENDOR
            user.save()
            vendor =v_form.save(commit=False)
            vendor.user= user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your account has been register sucessfully ! Please wait for the approval.")
            return redirect('registervendor')

        else:
            print('invalid data')
            print(form.errors)

    else:
        form = UserForm()
        v_form = vendorForm()

    context ={
        'form'  : form,
        'v_form'  : v_form
    }
    return render(request, 'accounts/registerVendor.html', context)