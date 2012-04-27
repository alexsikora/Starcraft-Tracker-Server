from django.db import models

#Teams Model
#Defines the Teams table 
#name - holds the name of the team
#tag - holds the tag abreviation of the name
class Team(models.Model):
    name = models.CharField("team name", max_length=255)
    tag = models.CharField("team tag", max_length=30)

    def __unicode__(self):
        return self.name + " (" + self.tag + ")"

#Players Model
#Contains Players table with FK team to Team
#name - name of player
#handle - in-game name of player
#team - FK to Team
#picture - default null pic of player
#race - Terran/Zerg/Protoss
#ELO - Player ranking
#Nationality - home country
class Player(models.Model):
    name = models.CharField("player's real name", max_length=255)
    handle = models.CharField("player's online handle", max_length=255)
    team = models.ForeignKey(Team, blank=True, null=True, verbose_name="player's team")
    picture = models.FileField(upload_to="player_pics/", blank=True, null=True)
    race = models.CharField("player's race", max_length=100)
    elo = models.IntegerField("player elo")
    nationality = models.CharField("player's nationality", max_length=100, blank=True)


    def __unicode__(self):
        return self.name + " aka " + self.handle


