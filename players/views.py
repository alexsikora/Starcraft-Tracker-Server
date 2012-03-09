# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from models import Player
from django.core import serializers
import base64

def get_all_players(request):
    #response = []
    all_players = serializers.serialize("json",Player.objects.all())
    print "lolwut"+all_players
    return HttpResponse("notworking")

    
