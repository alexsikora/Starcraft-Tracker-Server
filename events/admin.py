from events.models import Event
from events.models import Round
from events.models import Match
from events.models import PlayerMatch
from events.models import TeamMatch
from events.models import Map
from events.models import Game
from django.contrib import admin
admin.site.register(Event)
admin.site.register(Round)
admin.site.register(PlayerMatch)
admin.site.register(TeamMatch)
admin.site.register(Map)
admin.site.register(Game)
