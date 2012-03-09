# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from models import Player
from django.core import serializers
from django.utils import simplejson
import base64

def get_all_players(request):
    response = {}
    all_players = serializers.serialize("json",Player.objects.all())
    response['response'] = all_players
    return HttpResponse(simplejson.dumps(response),mimetype='application/json')

    
