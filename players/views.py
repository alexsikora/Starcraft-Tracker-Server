# Create your views here.
from models import Team
from django.core import serializers
from django.http import HttpResponse
from django.http import Http404
from django.utils import simplejson

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