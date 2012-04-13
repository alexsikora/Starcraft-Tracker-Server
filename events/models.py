from django.db import models
from players.models import Player, Team
from django.db.models.signals import post_save
# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return self.name

    def export_to_dict(self):
        return {
            'pk': self.pk, 
            'name': self.name,
            'start_date': self.start_date.strftime("%Y-%m-%d"), 
            'end_date': self.end_date.strftime("%Y-%m-%d"),
            'rounds': [round.export_to_dict() for round in self.round_set.all()]
        }

    def shallow_dict(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'model' : 'events.event',
            'start_date': self.start_date.strftime("%Y-%m-%d"),
            'end_date': self.end_date.strftime("%Y-%m-%d")
        }

class Round(models.Model):
    event = models.ForeignKey(Event, verbose_name="event the round is in")
    name = models.CharField(max_length=255) #the name of htis round (i.e. RO4)
    
    def __unicode__(self):
        return self.event.name + ": " + self.name

    def export_to_dict(self):
        return {
            'pk' : self.pk,
            'name' : self.name,
            'player_matches' : [pmatch.export_to_dict() for pmatch in self.playermatch_related.all()],
            'team_matches' : [tmatch.export_to_dict() for tmatch in self.teammatch_related.all()],
        }


class Match(models.Model):
    match_round = models.ForeignKey(Round, verbose_name="round the game is in", related_name="%(class)s_related")
    winner_next_round = models.ForeignKey(Round, verbose_name="next round for winner of this game", related_name="+", blank=True, null=True)
    loser_next_round = models.ForeignKey(Round, verbose_name="next round for loser of this game", blank=True, null=True, related_name="+")
    class Meta:
        abstract = True #makes this an abstract class


class PlayerMatch(Match):
    first_player = models.ForeignKey(Player, verbose_name="player 1",related_name="%(class)s_firstplayer")
    second_player = models.ForeignKey(Player, verbose_name="player 2", related_name="%(class)s_secondplayer")

    def __unicode__(self):
        return self.match_round.event.name + " - " + self.match_round.name + ": " + self.first_player.name + " vs. " + self.second_player.name
    
    def export_to_dict(self):
        return {
            'pk': self.pk,
            'first_player' : self.first_player.pk,
            'second_player' : self.second_player.pk,
            'games' : [game.export_to_dict() for game in self.game_set.all()]
        }

class TeamMatch(Match):
    first_team = models.ForeignKey(Team, verbose_name="team 1", related_name="%(class)s_firstteam")
    second_team = models.ForeignKey(Team, verbose_name="team 2", related_name="%(class)s_secondteam")

    def __unicode__(self):
        return self.match_round.event.name + " - " + self.match_round.name + ": " + self.first_team.name + " vs. " + self.second_team.name

    def export_to_dict(self):
        return {}

class Map(models.Model):
    name = models.CharField("map name", max_length=255)
    image = models.FileField(upload_to="map_images/")

    def __unicode__(self):
        return self.name

    def export_to_dict(self):
        return {
            'pk': self.pk,
            'name' : self.name,
            'image' : self.image.url
        }
    
class Game(models.Model):
    player_game_match = models.ForeignKey(PlayerMatch, verbose_name="player match this game is a part of")
    team_game_match = models.ForeignKey(TeamMatch, verbose_name="team match this game is a part of", blank=True, null=True)
    game_map = models.ForeignKey(Map, verbose_name="map this game is played on", blank = True, null = True)
    description = models.CharField("short description of game", max_length=1000, blank=True, null=True)
    winner = models.ForeignKey(Player, verbose_name="winner of this game", blank=True, null=True, related_name="+")
    game_number = models.IntegerField()
    alert_sent = models.BooleanField()

    def __unicode__(self):
        game_round = self.player_game_match.match_round
        return game_round.event.name + " - " + game_round.name + " - " + self.player_game_match.first_player.handle + " vs. " + self.player_game_match.second_player.handle + " Game " + str(self.game_number)

    def export_to_dict(self):
        map_dict = {}
        if (self.game_map is not None):
            map_dict = self.game_map.export_to_dict()

        return {
            'pk': self.pk,
            'description': self.description,
            'winner' : self.winner.pk,
            'map' : map_dict
        }
    
    def get_relevant_players(self):
        playerOne = self.player_game_match.first_player
        playerTwo = self.player_game_match.second_player
        teamOne = playerOne.team
        teamTwo = playerTwo.team
        event = self.player_game_match.match_round.event
        users = []
        users.extend(playerOne.userprofile_set.all())
        users.extend(playerTwo.userprofile_set.all())
        users.extend(teamOne.userprofile_set.all())
        users.extend(teamTwo.userprofile_set.all())
        users.extend(event.userprofile_set.all())
        users = set(users)
        return users
    
    def alert_string(self):
        playerOne = self.player_game_match.first_player
        playerTwo = self.player_game_match.second_player
        round = self.player_game_match.match_round
        winner = self.winner
        loser = winner
        if winner.pk is playerOne.pk:
            loser = playerTwo
        else:
            loser = playerOne
        map = ""
        if self.game_map is not None:
            map = self.game_map.name
        return winner.handle + " defeats " + loser.handle + " in game " + str(self.game_number) + " on " + map
        

def send_alert(sender, instance, created, **kwargs):
    if instance.alert_sent is False and instance.winner is not None:
        instance.alert_sent = True
        instance.save()
        users = instance.get_relevant_players()
        firstPlayer = instance.player_game_match.first_player
        secondPlayer = instance.player_game_match.second_player
        alert_string = instance.alert_string()
        print alert_string
        for user in users:
            if user.device is not None:
                user.device.send_message(message = alert_string)

post_save.connect(send_alert, sender = Game)
