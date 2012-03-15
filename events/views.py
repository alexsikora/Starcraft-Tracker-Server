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
