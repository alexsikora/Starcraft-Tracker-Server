# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from models import *
from django.core import serializers
from django.utils import simplejson
import base64

def get_matches_from_round(request):
    fkey = request.GET['id']
    response = {}
    matches = serializers.serialize("python",Match.objects.filter(match_round__id=fkey))
    response['response'] = matches
    return HttpResponse(simplejson.dumps(response),mimetype='application/json')
	
def get_rounds_from_event(request):
    fkey = request.GET['id']
    response = {}
    rounds = serializers.serialize("python",Round.objects.filter(event_round__id=fkey))
    response['response'] = rounds
    return HttpResponse(simplejson.dumps(response),mimetype='application/json')

def get_events(request):
    response = {}
    events = Event.objects.all();
    response['response'] = [event.shallow_dict() for event in events]
    response['status_code'] = 200
    return HttpResponse(simplejson.dumps(response),mimetype='application/json')

def get_event(request):
    response = {}
    fkey = request.GET['id']
    event = Event.objects.get(pk=fkey)
    response = {}
    response['status_code'] = 200
    response['response'] = event.export_to_dict()
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')
