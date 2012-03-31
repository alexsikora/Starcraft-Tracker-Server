from django.db import models
from django.contrib.auth.models import User
from players.models import Player, Team
from events.models import Event
from django.db.models.signals import post_save
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    favorite_players = models.ManyToManyField(Player)
    favorite_teams = models.ManyToManyField(Team)
    favorite_events = models.ManyToManyField(Event)
    
    def __unicode__(self):
        return self.user.username
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)

post_save.connect(create_user_profile, sender=User)
