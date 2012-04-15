# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.models import User
from players.models import Player, Team
from events.models import Event
from django.contrib.auth import authenticate, login
from models import UserProfile, is_auth, auth_required_response
from django.db import IntegrityError
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.csrf.middleware import csrf_exempt
from django.utils import simplejson
from django_c2dm.models import AndroidDevice


# create_user - Creates a new User and adds User to database.
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

# authenticate_user - Authenticates a User and allows them access to the server.
def authenticate_user(request):
    user = is_auth(request)
    response = {}
    if user is not None:
        if user.is_active:
            response['status_code'] = 200
            response['response'] = "Successful authentication"
        else:
            response['status_code'] = 401
            response['response'] = "Your account has been disabled"
        return HttpResponse(simplejson.dumps(response),mimetype="application/json")
    else:
        return auth_required_response()

# remove_user - Removes an active User. If User is inactive, simply notifies User of inactivity.
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

# add_favorite_player - Adds a Player to a UserProfile's subscription list. This notifies the server
# that the User desires updates on this Player's activity and will allow the system to notify the User.   
def add_favorite_player(request):
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
    profile.favorite_players.add(player)
    profile.save()
    response['status_code'] = 200
    response["response"] = "Add favorite player successful!"
    return HttpResponse(simplejson.dumps(response), mimetype="application/json")

# add_favorite_team - Adds a Team to a UserProfile's subscription list. This notifies the server
# that the User desires updates on this Team's activity and will allow the system to notify the User.      
def add_favorite_team(request):
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
    profile.favorite_teams.add(team)
    profile.save()
    response['status_code'] = 200
    response["response"] = "Add favorite team successful!"
    return HttpResponse(simplejson.dumps(response), mimetype="application/json")

# add_favorite_event - Adds an Event to a UserProfile's subscription list. This notifies the server
# that the User desires updates on this Event's activity and will allow the system to notify the User.      
def add_favorite_event(request):
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
    profile.favorite_events.add(event)
    profile.save()
    response['status_code'] = 200
    response["response"] = "Add favorite event successful!"
    return HttpResponse(simplejson.dumps(response), mimetype="application/json")

# remove_favorite_player - Removes a Player from a User's subscription list. This will stop
# the server from sending any future updates to a User about this Player, barring the User's resubscription.    
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

# remove_favorite_team - Removes a Team from a User's subscription list. This will stop
# the server from sending any future updates to a User about this Team, barring the User's resubscription.     
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

# remove_favorite_event - Removes an Event from a User's subscription list. This will stop
# the server from sending any future updates to a User about this Event, barring the User's resubscription. 
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

# get_favorites - Returns a JSON formatted HttpResponse with all of a User's favorites (Player, Team, Event).
def get_favorites(request):
    user = is_auth(request)
    response = {}
    if user is None:
        return auth_required_response()
    profile = user.get_profile()
    response['status_code'] = 200
    response['response'] = [profile.favorites_to_dict()]
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

# set_device - Stores information about a User's Android Device in the database to be used when sending Push notifications.
def set_device(request):
    user = is_auth(request)
    if user is None:
        return auth_required_response()
    response = {}
    type = request.GET['type']
    registration_id = request.GET['rid']
    device = user.get_profile().device
    if device is None:
        user.get_profile().device = AndroidDevice.objects.create(registration_id=registration_id, collapse_key="")
        user.get_profile().save()
    else:
        device.registration_id = registration_id
        device.save()
    response['status_code'] = 200
    response['response'] = "Device set successful"
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')
        
create_user = csrf_exempt(create_user)
authenticate_user = csrf_exempt(authenticate_user)
remove_user = csrf_exempt(remove_user)
