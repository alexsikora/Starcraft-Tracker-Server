# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from models import UserProfile
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect

def create_user(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        newUser = User.objects.create_user(username, username, password)
        return HttpResponse("Account successfully created");
    except IntegrityError:
        return HttpResponse("Account creation failed");

@csrf_protect
def authenticate_user(request):
    name = request.POST['username']
    passw = request.POST['password']
    user = authenticate(username=name, password=passw)
    if user is not None:
        if user.is_active:
            return HttpResponse("Successful authentication")
        else:
            return HttpResponse("Your account has been disabled")
    else:
        return HttpResponse("Your username or password was invalid")

@csrf_protect
def remove_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            user.delete()
            return HttpResponse("Successful account removal")
        else:
            return HttpResponse("Your account has been disabled")
    else:
        return HttpResponse("Your username or password was invalid")  
