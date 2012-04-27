from django.db import models
from players.models import Player, Team
from django.db.models.signals import post_save
# Create your models here.


# Event
# This model is the root of the event class used
# to represent a variety of events. It contains simply
# basic information for the event and has a reverse link to
# a set of rounds
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

# Round
# The round class represents the rounds in a tournament
# from round of 64 or group stages. It contains a name and 
# a reverse link to a set of matches
class Round(models.Model):
    event = models.ForeignKey(Event, verbose_name="event the round is in")
    name = models.CharField(max_length=255) #the name of this round (i.e. RO4)
    
    def __unicode__(self):
        return self.event.name + ": " + self.name

    def export_to_dict(self):
        return {
            'pk' : self.pk,
            'name' : self.name,
            'player_matches' : [pmatch.export_to_dict() for pmatch in self.playermatch_related.all()],
            'team_matches' : [tmatch.export_to_dict() for tmatch in self.teammatch_related.all()],
        }

# Match
# The match class represents a match between two players or two teams.
# It is made up of any number of games, the round it is a part of, and the round
# that the loser proceeds to, and the winner proceeds to. This is an abstract class 
# made up of player and team matches
class Match(models.Model):
    match_round = models.ForeignKey(Round, verbose_name="round the game is in", related_name="%(class)s_related")
    winner_next_round = models.ForeignKey(Round, verbose_name="next round for winner of this game", related_name="+", blank=True, null=True)
    loser_next_round = models.ForeignKey(Round, verbose_name="next round for loser of this game", blank=True, null=True, related_name="+")
    class Meta:
        abstract = True #makes this an abstract class


# PlayerMatch
# The player match represents a match between two players, made up of games
class PlayerMatch(Match):
    first_player = models.ForeignKey(Player, verbose_name="player 1",related_name="%(class)s_firstplayer")
    second_player = models.ForeignKey(Player, verbose_name="player 2", related_name="%(class)s_secondplayer")

    def __unicode__(self):
        return self.match_round.event.name + " - " + self.match_round.name + ": " + self.first_player.handle + " vs. " + self.second_player.handle
    
    def export_to_dict(self):
        return {
            'pk': self.pk,
            'first_player' : self.first_player.pk,
            'second_player' : self.second_player.pk,
            'games' : [game.export_to_dict() for game in self.game_set.all()]
        }

# TeamMatch
# The team match represents a match between two teams, made up of games between players
class TeamMatch(Match):
    first_team = models.ForeignKey(Team, verbose_name="team 1", related_name="%(class)s_firstteam")
    second_team = models.ForeignKey(Team, verbose_name="team 2", related_name="%(class)s_secondteam")

    def __unicode__(self):
        return self.match_round.event.name + " - " + self.match_round.name + ": " + self.first_team.name + " vs. " + self.second_team.name

    def export_to_dict(self):
        return {}

# Map
# A map is the map that a game is played on, which has simply a name and an image representation
# of the map.
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

# Game Model
# Holds a reference to the parent match (player match or team match).
# Holds a reference to the Map on which the Game was played.
# Contains a short description of the match.
# Holds a reference to the winner's private key (the players/teams will be held in the parent Match).
# Contains an Integer value of which game this is in the series.      
# Contains a Boolean one-way flag to determine whether or not this Game has sent an alert to
#       relevant Android device.
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

    # export_to_dict - Returns a JSON format dictionary of relevant information from the Game Model
    def export_to_dict(self):
        map_dict = {}
        if (self.game_map is not None):
            map_dict = self.game_map.export_to_dict()
        winner_pk = -1
        if self.winner is not None:
            winner_pk = self.winner.pk
        description = ""
        if self.description is not None:
            description = self.description
        return {
            'pk': self.pk,
            'description': description,
            'winner' : winner_pk,
            'map' : map_dict
        }
    
    # get_relevant_players - Finds all UserProfiles that have favorited either player, either player's team,
    #                               or the parent Event and returns a list of those UserProfiles.
    def get_relevant_players(self):
        playerOne = self.player_game_match.first_player
        playerTwo = self.player_game_match.second_player
        teamOne = playerOne.team
        teamTwo = playerTwo.team
        event = self.player_game_match.match_round.event
        users = []
        users.extend(playerOne.userprofile_set.all())
        users.extend(playerTwo.userprofile_set.all())
        if teamOne is not None:
            users.extend(teamOne.userprofile_set.all())
        if teamTwo is not None:
            users.extend(teamTwo.userprofile_set.all())
        users.extend(event.userprofile_set.all())
        users = set(users)
        return users
    
    # alert_string - Returns a string of relevant Game information to be sent as a Push notification.
    def alert_string(self):
        playerOne = self.player_game_match.first_player
        playerTwo = self.player_game_match.second_player
        round = self.player_game_match.match_round
        winner = self.winner
        loser = winner
        if winner.pk == playerOne.pk:
            loser = playerTwo
        else:
            loser = playerOne
        prototype_string = winner.handle + " defeats " + loser.handle + " in game " + str(self.game_number)
        map = ""
        if self.game_map is not None:
            map = self.game_map.name
            prototype_string = prototype_string + " on " + map
        description = ""
        if self.description is not None:
            description = self.description
        return prototype_string
        
# send_alert - Sends an alert on Game save to all proper users' Android devices.
def send_alert(sender, instance, created, **kwargs):
    if instance.alert_sent is False and instance.winner is not None:
        instance.alert_sent = True
        instance.save()
        users = instance.get_relevant_players()
        firstPlayer = instance.player_game_match.first_player
        secondPlayer = instance.player_game_match.second_player
        alert_string = instance.alert_string()
        for user in users:
            if user.device is not None:
                user.device.send_message(message = alert_string)

post_save.connect(send_alert, sender = Game)
