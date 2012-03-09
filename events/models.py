from django.db import models
from players.models import Player, Team
# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

class Round(models.Model):
    event = models.ForeignKey(Event, verbose_name="event the round is in")
    name = models.CharField(max_length=255) #the name of htis round (i.e. RO4)



class Match(models.Model):
    match_round = models.ForeignKey(Round, verbose_name="round the game is in")
    winner_next_round = models.ForeignKey(Round, verbose_name="next round for winner of this game")
    loser_next_round = models.ForeignKey(Round, verbose_name="next round for loser of this game", blank=True, null=True)
    class Meta:
        abstract = True #makes this an abstract class

class PlayerMatch(Match):
    first_player = models.ForeignKey(Player, verbose_name="player 1")
    second_player = models.ForeignKey(Player, verbose_name="player 2")

class TeamMatch(Match):
    first_team = models.ForeignKey(Team, verbose_name="team 1")
    second_team = models.ForeignKey(Team, verbose_name="team 2")

class Map(models.Model):
    name = models.CharField("map name", max_length=255)
    image = models.FileField(upload_to="/map_images/")
    
class Game(models.Model):
    # game_match = models.ForeignKey(Match, verbose_name="match this game is a part of")
    game_map = models.ForeignKey(Map, verbose_name="map this game is played on", blank=True, null=True)
    description = models.CharField("short description of game", max_length=1000, blank=True, null=True)
    

