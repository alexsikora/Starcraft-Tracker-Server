from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'starcraft_tracker.views.home', name='home'),
    # url(r'^starcraft_tracker/', include('starcraft_tracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/register/', 'users.views.create_user'),
    url(r'^users/authenticate/', 'users.views.authenticate_user'),
    url(r'^users/remove/', 'users.views.remove_user'),
    url(r'^users/addfavoriteplayer/', 'users.views.add_favorite_player'),
    url(r'^users/addfavoriteteam/', 'users.views.add_favorite_team'),
    url(r'^users/addfavoriteevent/', 'users.views.add_favorite_event'),
    url(r'^users/removefavoriteplayer/', 'users.views.remove_favorite_player'),
    url(r'^users/removefavoriteteam/', 'users.views.remove_favorite_team'),
    url(r'^users/removefavoriteevent/', 'users.views.remove_favorite_event'),
    url(r'^players/allteams/', 'players.views.get_all_teams'),
    url(r'^players/teamquery/', 'players.views.get_matching_teams'),
    url(r'^players/allplayers/', 'players.views.get_all_players'),
    url(r'^players/withid/', 'players.views.player_with_id'),
    url(r'^events/getmatches/', 'events.views.get_matches_from_round'),
    url(r'^events/allevents/', 'events.views.get_events'),
    url(r'^events/get_event/', 'events.views.get_event'),
)
