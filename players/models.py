from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField("team name", max_length=255)
    tag = models.CharField("team tag", max_length=30)
    # nevermind, just the top one is necessary players = models.OneToManyField(Player, verbose_name="team's players")

    def __unicode__(self):
        return self.name + " (" + self.tag + ")"
    
class Player(models.Model):
    name = models.CharField("player's real name", max_length=255)
    handle = models.CharField("player's online handle", max_length=255)
    team = models.ForeignKey(Team, blank=True, null=True, verbose_name="player's team", on_delete=models.SET_NULL)
    picture = models.FileField(upload_to="/player_pics/", blank=True, null=True)
    race = models.CharField("player's race", max_length=100)
    elo = models.IntegerField("player elo")
    nationality = models.CharField("player's nationality", max_length=100, blank=True)


    def __unicode__(self):
        return self.name + " aka " + self.handle


