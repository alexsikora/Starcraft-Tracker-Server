"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *
from django.db import models
from django.contrib.auth.models import User
import base64
from StringIO import StringIO
from django.test.client import Client
from django.utils import simplejson
from players.models import Player, Team
from users.models import UserProfile

class EventTest(TestCase):
    username = 'testuser'
    password = 'testpass'
    email = 'test@test.com'

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(self.username,self.username,self.password)
        auth = self.getUserAuth(self.username, self.password)

        self.extra = {
            'HTTP_AUTHORIZATION' : auth,
        }

        event = Event.objects.create(name="MLG",start_date="2012-03-13",end_date="2012-03-13")
        round = Round.objects.create(name="Round of 64",event=event)
        team1 = Team.objects.create(name="Team 1", tag="T1")
        team2 = Team.objects.create(name="Team 2", tag="T2")
        player1 = Player.objects.create(name="Player One", handle="p1ayerOne", team=Team.objects.get(pk=1), race="Protoss", elo=1200, nationality="Brazil")
        player2 = Player.objects.create(name="Player Two", handle="playel2tw0", team=Team.objects.get(pk=2), race="Zerg", elo=1230, nationality="Chile")
        player3 = Player.objects.create(name="Player Three", handle="play3rthr3e", race="Terran", elo=1256, nationality="Argentina")
        match1 = PlayerMatch.objects.create(first_player=player1, second_player=player2, match_round=round)
        match2 = PlayerMatch.objects.create(first_player=player1, second_player=player3, match_round=round)
        map = Map.objects.create(name="Cloud Kingdom LE", image="Image_not_found.jpg")
        game1 = Game.objects.create(player_game_match=match1, winner=player1, game_number=1, alert_sent=False)
        game2 = Game.objects.create(player_game_match=match2, winner=player3, game_number=1, alert_sent=False, game_map=map)
        
        user1 = User.objects.create_user("username1", "user1@user.com", "password")
        user2 = User.objects.create_user("username2", "user2@user.com", "password")
        profile1 = user1.userprofile
        profile1.favorite_events.add(event)
        profile1.favorite_teams.add(team2)
        profile2 = user2.userprofile
        profile2.favorite_players.add(player3)

    def getUserAuth(self, username, password):
        auth = '%s:%s' % (username, password)
        auth = 'Basic %s' % base64.encodestring(auth)
        auth = auth.strip()

        return auth

    def test_get_events(self):
        response = self.client.post('/events/allevents/', {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        result = simplejson.load(StringIO(response.content))
        self.assertTrue(len(result) > 0)
        self.assertEqual(result['status_code'], 200)
        self.assertEqual(result['response'][0]['name'], 'MLG')

    def test_get_event(self):
        response = self.client.post('/events/get_event/?id=1', {}, **self.extra)
        self.assertEqual(response.status_code, 200)

        result = simplejson.load(StringIO(response.content))
        self.assertTrue(len(result) > 0)

        self.assertEqual(result['status_code'], 200)
        self.assertEqual(result['response']['name'], 'MLG')

    def test_get_nonexistent_event(self):
        response = self.client.post('/events/get_event/?id=2', {}, **self.extra)
        self.assertEqual(response.status_code, 200)

        result = simplejson.load(StringIO(response.content))
        self.assertTrue(len(result) > 0)

        self.assertEqual(result['status_code'], 404)
        self.assertEqual(result['response'], "Event does not exist")
        
    def test_export_to_dict(self):
        event = Event.objects.get(pk=1)
        result = event.export_to_dict()
        
        self.assertEqual(result['name'], "MLG")
        self.assertEqual(result['start_date'], "2012-03-13")
        self.assertEqual(result['end_date'], "2012-03-13")
        
        rounds = result['rounds']
        for round in rounds: # Should only be 1 round
            self.assertEqual(round['name'], "Round of 64")
            player_matches = round['player_matches']
            for pmatch in player_matches:
                self.assertEqual(pmatch['first_player'], 1)
                if pmatch['pk'] == 1:
                    self.assertEqual(pmatch['second_player'], 2)
                    games = pmatch['games']
                    for game in games: # Should only be 1
                        self.assertEqual(game['winner'], 1)
                else:
                    self.assertEqual(pmatch['second_player'], 3)
                    games = pmatch['games']
                    for game in games: # Should only be 1
                        self.assertEqual(game['winner'], 3)
        
    def test_get_relevant_users(self):
        game1 = Game.objects.get(pk=1)
        game2 = Game.objects.get(pk=2)
        
        user1 = UserProfile.objects.get(pk=2)
        user2 = UserProfile.objects.get(pk=3)
        
        userlist1 = game1.get_relevant_players()
        userlist2 = game2.get_relevant_players()
        
        self.assertTrue(user1 in userlist1)
        self.assertTrue(user2 not in userlist1)
        self.assertTrue(user1 in userlist2)
        self.assertTrue(user2 in userlist2)
        
    def test_alert_string(self):
        game1 = Game.objects.get(pk=1)
        game2 = Game.objects.get(pk=2)
        
        string1 = game1.alert_string()
        string2 = game2.alert_string()
        
        self.assertEqual(string1, "p1ayerOne defeats playel2tw0 in game 1")
        self.assertEqual(string2, "play3rthr3e defeats p1ayerOne in game 1 on Cloud Kingdom LE")
        