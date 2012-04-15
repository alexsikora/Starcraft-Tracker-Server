# Create your views here.
from models import Team, Player
from django.core import serializers
from django.http import HttpResponse
from django.http import Http404
from django.utils import simplejson
from users.models import is_auth, auth_required_response


# get_all_teams - Returns a JSON format HttpResponse of all teams in the database.
def get_all_teams(request):
    user = is_auth(request)
    if user is None:
        return auth_required_response()
    teams = Team.objects.all()
    jsonreturn = serializers.serialize("python", teams)
    teamarray = {}
    teamarray['response'] = jsonreturn
    teamarray['status_code'] = 200
    return HttpResponse(simplejson.dumps(teamarray), mimetype='application/json')

# get_matching_teams - Accepts a query string from the URL,
# then returns a JSON formatted HttpResponse of all teams matching the query.	
def get_matching_teams(request):
    user = is_auth(request)
    if user is None:
        return auth_required_response()
    query = request.GET['query']
    teams = Team.objects.filter(name__istartswith=query) | Team.objects.filter(tag__iexact=query)
    jsonreturn = serializers.serialize("python", teams)
    teamarray = {}
    teamarray['response'] = jsonreturn
    teamarray['status_code'] = 200
    return HttpResponse(simplejson.dumps(teamarray), mimetype='application/json')

# get_all_players - Returns a JSON format HttpsResponse of all players in the database.
def get_all_players(request):
    user = is_auth(request)
    if user is None:
        return auth_required_response()
    response = {}
    all_players = serializers.serialize("python", Player.objects.all())
    response['response'] = all_players
    response['status_code'] = 200
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

# player_with_id - Returns a JSON response of a single player based on the unique private key in the database matching the desired player.
def player_with_id(request):
    user = is_auth(request)
    if user is None:
        return auth_required_response()
    response = {}
    ident = request.GET['id']
    player = serializers.serialize("python",Player.objects.filter(pk=ident))
    response['response'] = player
    response['status_code'] = 200
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')
