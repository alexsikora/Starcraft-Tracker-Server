# Create your views here.
from models import Team, Player
from django.core import serializers
from django.http import HttpResponse
from django.http import Http404
from django.utils import simplejson
from django.contrib.auth import authenticate, login
import base64

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

def get_all_teams(request):
    user = is_auth(request)
    if user is None:
        return auth_required_response()
    teams = Team.objects.all()
    jsonreturn = serializers.serialize("json", teams)
    teamarray = {}
    teamarray['response'] = jsonreturn
    teamarray['status_code'] = 200
    return HttpResponse(simplejson.dumps(teamarray), mimetype='application/json')
	
def get_matching_teams(request):
    user = is_auth(request)
    if user is None:
        return auth_required_response()
    query = request.GET['query']
    teams = Team.objects.filter(name__istartswith=query) | Team.objects.filter(tag__iexact=query)
    jsonreturn = serializers.serialize("json", teams)
    teamarray = {}
    teamarray['response'] = jsonreturn
    teamarray['status_code'] = 200
    return HttpResponse(simplejson.dumps(teamarray), mimetype='application/json')

def get_all_players(request):
    user = is_auth(request)
    if user is None:
        return auth_required_response()
    response = {}
    all_players = serializers.serialize("json", Player.objects.all())
    response['response'] = all_players
    response['status_code'] = 200
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def player_with_id(request):
    user = is_auth(request)
    if user is None:
        return auth_required_response()
    response = {}
    ident = request.GET['id']
    player = serializers.serialize("json",Player.objects.filter(pk=ident))
    response['response'] = player
    response['status_code'] = 200
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')
