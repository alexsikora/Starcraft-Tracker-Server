# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from models import *
from django.core import serializers
from django.utils import simplejson
from django.contrib.auth import authenticate, login
import base64

# is_auth - Authenticates a user before allowing the user to access any server functionality.
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

# auth_required_repsonse - Forms a required HttpResponse if user authentication fails.
def auth_required_response():
    response = HttpResponse()
    response.status_code = 401
    realm = ''
    response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
    return response

# get_matches_from_round - Allows a user to search for a specific Round,
# then returns a JSON format response of all Matches belonging to that Round.
def get_matches_from_round(request):
    user = is_auth(request)
    if user is None:
        return auth_required_response()

    fkey = request.GET['id']
    response = {}
    matches = serializers.serialize("python",Match.objects.filter(match_round__id=fkey))
    response['response'] = matches
    return HttpResponse(simplejson.dumps(response),mimetype='application/json')

# get_rounds_from_event - Allows a user to search for a specific Event,
# then returns a JSON format response of all Rounds belonging to that Event.	
def get_rounds_from_event(request):
    user = is_auth(request)
    if user is None:
        return auth_required_response()

    fkey = request.GET['id']
    response = {}
    rounds = serializers.serialize("python",Round.objects.filter(event_round__id=fkey))
    response['response'] = rounds
    return HttpResponse(simplejson.dumps(response),mimetype='application/json')

# get_events - Returns a JSON format response of all Events in the database.
def get_events(request):
    user = is_auth(request)
    if user is None:
        return auth_required_response()

    response = {}
    events = Event.objects.all();
    response['response'] = [event.shallow_dict() for event in events]
    response['status_code'] = 200
    return HttpResponse(simplejson.dumps(response),mimetype='application/json')

#get_event - Allows a user to search for a specific Event by it's unique private key,
# then returns a JSON format response of the matching Event.
def get_event(request):
    user = is_auth(request)
    if user is None:
        return auth_required_response()

    response = {}
    fkey = request.GET['id']
    response = {}
    try:
        event = Event.objects.get(pk=fkey)
        response['status_code'] = 200
        response['response'] = event.export_to_dict()
    except Event.DoesNotExist:
        response['status_code'] = 404
        response['response'] = "Event does not exist"
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')
    
