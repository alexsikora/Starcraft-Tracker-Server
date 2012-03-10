# Create your views here.
from models import Team
from models import Player
from django.http import HttpResponse
from django.http import Http404
from django.core import serializers
from django.utils import simplejson
import base64

def get_all_players(request):
    response = {}
    all_players = serializers.serialize("json",Player.objects.all())
    response['response'] = all_players
    return HttpResponse(simplejson.dumps(response),mimetype='application/json')

def get_all_teams(request):
	teams = Team.objects.all()
	jsonreturn = serializers.serialize("json", teams)
	teamarray = {}
	teamarray['response'] = jsonreturn
	return HttpResponse(simplejson.dumps(teamarray), mimetype='application/json')
	
def get_matching_teams(request):
	query = request.GET['query']
	teams = Team.objects.filter(name__istartswith=query) | Team.objects.filter(tag__iexact=query)
	jsonreturn = serializers.serialize("json", teams)
	teamarray = {}
	teamarray['response'] = jsonreturn
	return HttpResponse(simplejson.dumps(teamarray), mimetype='application/json')
