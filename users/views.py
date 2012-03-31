# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.models import User
from players.models import Player, Team
from events.models import Event
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
    
def add_favorite_player(request):
    user = is_auth(request)
    response = {}
    if user is None:
        return auth_required_response()
    pid = request.GET['id']
    player = Player.objects.get(pk=pid)
    if player is None:
        response['status_code'] = 404
        response["response"] = "Player id does not exist!"
    else:
        profile = user.get_profile()
        profile.favorite_players.add(player)
        profile.save()
        response['status_code'] = 200
        response["response"] = "Add favorite player successful!"
    return HttpResponse(simplejson.dumps(response), mimetype="application/json")
        
def add_favorite_team(request):
    user = is_auth(request)
    response = {}
    if user is None:
        return auth_required_response()
    tid = request.GET['id']
    team = Team.objects.get(pk=tid)
    if team is None:
        response['status_code'] = 404
        response["response"] = "Team id does not exist!"
    else:
        profile = user.get_profile()
        profile.favorite_teams.add(team)
        profile.save()
        response['status_code'] = 200
        response["response"] = "Add favorite team successful!"
    return HttpResponse(simplejson.dumps(response), mimetype="application/json")
    
def add_favorite_event(request):
    user = is_auth(request)
    response = {}
    if user is None:
        return auth_required_response()
    eid = request.GET['id']
    event = Event.objects.get(pk=eid)
    if event is None:
        response['status_code'] = 404
        response["response"] = "Event id does not exist!"
    else:
        profile = user.get_profile()
        profile.favorite_events.add(event)
        profile.save()
        response['status_code'] = 200
        response["response"] = "Add favorite event successful!"
    return HttpResponse(simplejson.dumps(response), mimetype="application/json")
        
def remove_favorite_player(request):
    user = is_auth(request)
    response = {}
    if user is None:
        return auth_required_response()
    pid = request.GET['id']
    try:
        player = Player.objects.get(pk=pid)
    except Player.DoesNotExist:
        response['status_code'] = 404
        response["response"] = "Player id does not exist!"
        return HttpResponse(simplejson.dumps(response), mimetype="application/json")
    profile = user.get_profile()
    try:
        fav_player = profile.favorite_players.get(pk=player.pk)
    except Player.DoesNotExist:
        response['status_code'] = 404
        response["response"] = "Player not in favorites!"
        return HttpResponse(simplejson.dumps(response), mimetype="application/json")
    profile.favorite_players.remove(player)
    profile.save()
    response['status_code'] = 200
    response["response"] = "Remove favorite player successful!"
    return HttpResponse(simplejson.dumps(response), mimetype="application/json")
        
def remove_favorite_team(request):
    user = is_auth(request)
    response = {}
    if user is None:
        return auth_required_response()
    tid = request.GET['id']
    try:
        team = Team.objects.get(pk=tid)
    except Team.DoesNotExist:
        response['status_code'] = 404
        response["response"] = "Team id does not exist!"
        return HttpResponse(simplejson.dumps(response), mimetype="application/json")
    profile = user.get_profile()
    try:
        fav_team = profile.favorite_teams.get(pk=team.pk)
    except Team.DoesNotExist:
        response['status_code'] = 404
        response["response"] = "Team not in favorites!"
        return HttpResponse(simplejson.dumps(response), mimetype="application/json")
    profile.favorite_teams.remove(team)
    profile.save()
    response['status_code'] = 200
    response["response"] = "Remove favorite team successful!"
    return HttpResponse(simplejson.dumps(response), mimetype="application/json")

def remove_favorite_event(request):
    user = is_auth(request)
    response = {}
    if user is None:
        return auth_required_response()
    eid = request.GET['id']
    try:
        event = Event.objects.get(pk=eid)
    except Event.DoesNotExist:
        response['status_code'] = 404
        response["response"] = "Event id does not exist!"
        return HttpResponse(simplejson.dumps(response), mimetype="application/json")
    profile = user.get_profile()
    try:
        fav_event = profile.favorite_events.get(pk=event.pk)
    except Event.DoesNotExist:
        response['status_code'] = 404
        response["response"] = "Event not in favorites!"
        return HttpResponse(simplejson.dumps(response), mimetype="application/json")
    profile.favorite_events.remove(event)
    profile.save()
    response['status_code'] = 200
    response["response"] = "Remove favorite event successful!"
    return HttpResponse(simplejson.dumps(response), mimetype="application/json")

def get_favorites(request):
    user = is_auth(request)
    response = {}
    if user is None:
        return auth_required_response()
    profile = user.get_profile()
    response['status_code'] = 200
    response['response'] = profile.favorites_to_dict()
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

        
create_user = csrf_exempt(create_user)
authenticate_user = csrf_exempt(authenticate_user)
remove_user = csrf_exempt(remove_user)
