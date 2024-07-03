from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import vendorForm
from . models import User, UserProfile
from django.contrib import messages, auth
from accounts.utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role ==1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role ==2:
        return True
    else:
        raise PermissionDenied



def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are alredy logged in!')
        return redirect('myAccount')

    elif request.method == "POST":
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
    if request.user.is_authenticated:
        messages.warning(request, 'You are alredy logged in!')
        return redirect('myAccount')
    
    elif request.method == 'POST':
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


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are alredy logged in!')
        return redirect('myAccount')
    
    elif request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email = email, password = password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request , 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')      
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')

@login_required(login_url = 'login')
def myAccount(request):
    user = request.user
    redirecturl = detectUser(user)
    return redirect(redirecturl)

@login_required(login_url = 'login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url = 'login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')