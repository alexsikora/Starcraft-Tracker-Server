# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from models import *
from django.core import serializers
from django.utils import simplejson
from users.models import is_auth, auth_required_response


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

# get_match - Returns a match that's id matches the query in JSON format, for alert usage
def get_match(request):
    user = is_auth(request)
    if user is None:
        return auth_required_response()

    response = {}
    ident = request.GET['id']
    try:
        match = PlayerMatch.objects.get(pk=ident)
        response['status_code'] = 200
        response['response'] = match.export_to_dict()
    except PlayerMatch.DoesNotExist:
        response['status_code'] = 404
        response['response'] = "Player Match does not exist"
    
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

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
    
