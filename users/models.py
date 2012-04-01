from django.db import models
from django.contrib.auth.models import User
from players.models import Player, Team
from events.models import Event
from django.db.models.signals import post_save
from django_c2dm.models import AndroidDevice
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    favorite_players = models.ManyToManyField(Player)
    favorite_teams = models.ManyToManyField(Team)
    favorite_events = models.ManyToManyField(Event)
    device = models.OneToOneField(AndroidDevice, blank=True, null=True)
    
    def __unicode__(self):
        return self.user.username

    def favorites_to_dict(self):
        return {
            'favorite_players':[player.pk for player in self.favorite_players.all()],
            'favorite_teams':[team.pk for team in self.favorite_teams.all()],
            'favorite_events':[event.pk for event in self.favorite_events.all()]
        }
        
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)


post_save.connect(create_user_profile, sender=User)
