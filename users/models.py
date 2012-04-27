from django.db import models
from django.contrib.auth.models import User
from players.models import Player, Team
from events.models import Event
from django.db.models.signals import post_save
from django_c2dm.models import AndroidDevice
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import base64

# UserProfile Model
# Links to a User.
# Contains lists of favorite player references, favorite team references,
#       and favorite event references.
# Contains a reference to a user's Android device.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    favorite_players = models.ManyToManyField(Player, blank=True, null=True)
    favorite_teams = models.ManyToManyField(Team, blank=True, null=True)
    favorite_events = models.ManyToManyField(Event, blank=True, null=True)
    device = models.OneToOneField(AndroidDevice, blank=True, null=True)
    
    def __unicode__(self):
        return self.user.username

    # favorites_to_dict - Returns a JSON format dictionary of the favorite lists,
    #                       using the database's private key as the identifier.
    def favorites_to_dict(self):
        return {
            'favorite_players':[player.pk for player in self.favorite_players.all()],
            'favorite_teams':[team.pk for team in self.favorite_teams.all()],
            'favorite_events':[event.pk for event in self.favorite_events.all()]
        }
        
# create_user_profile - Creates a UserProfile in the database.
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)


post_save.connect(create_user_profile, sender=User)


# is_auth - Authenticates a user before allowing the user to access any server functionality.
def is_auth(request):

    user = None
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            #only basic auth right now
            if auth[0].lower() == "basic":
                uname, passwd = base64.b64decode(auth[1]).split(':')
                user = authenticate(username=uname, password=passwd)
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        request.user = user
    return user

# auth_required_repsonse - Forms a required HttpResponse if user authentication fails.
def auth_required_response():
    response = HttpResponse()
    response.status_code = 401
    realm = ''
    response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
    return response
