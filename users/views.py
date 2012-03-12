# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from models import UserProfile
from django.db import IntegrityError
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.csrf.middleware import csrf_exempt
import base64
from django.utils import simplejson

def is_auth(request):
    #if (request.user is not AnonymouseUser):
    #    return request.user

    user = None
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            #only basic auth right now
            if auth[0].lower() == "basic":
                uname, passwd = base64.b64decode(auth[1]).split(':')
                user = authenticate(username=uname, password=passwd)
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        request.user = user
    return user

def auth_required_response():
    response = HttpResponse()
    response.status_code = 401
    realm = ''
    response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
    return response

def create_user(request):
    username = request.POST['username']
    password = request.POST['password']
    response = {}
    try:
        newUser = User.objects.create_user(username, username, password)
        response['response'] = "Account successfully created"
        response['status_code'] = 200
    except IntegrityError:
        response['response'] = "Account creation failed"
        response['status_code'] = 0
    return HttpResponse(simplejson.dumps(response), mimetype="application/json")

def authenticate_user(request):
    user = is_auth(request)
    response = {}
    if user is not None:
        if user.is_active:
            response['status_code'] = 200
            response['response'] = "Successful authentication"
        else:
            response['status_code'] = 0 #TOOD: Figure out what this should be
            response['response'] = "Your account has been disabled"
        return HttpResponse(simplejson.dumps(response),mimetype="application/json")
    else:
        return auth_required_response()

def remove_user(request):
    user = is_auth(request)
    response = {}
    if user is not None:
        if user.is_active:
            user.delete()
            response['status_code'] = 200
            response["response"] = "Successful account removal"
        else:
            response['status_code'] = 0
            response["response"] = "Your account has been disabled"
    else:
        return auth_required_response()
    return HttpResponse(simplejson.dumps(response), mimetype="application/json")

create_user = csrf_exempt(create_user)
authenticate_user = csrf_exempt(authenticate_user)
remove_user = csrf_exempt(remove_user)
