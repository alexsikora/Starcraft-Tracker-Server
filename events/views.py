# Create your views here.
from events import Round
from events import Event
from django.core import serializers
from django.http import HttpResponse
from django.http import Http404
from django.utils import simplejson

#def get_rounds_from_event(request):
