"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson

from piston.utils import rc

import base64
from StringIO import StringIO

from models import *
from django.db import models
from django.contrib.auth.models import User


class TeamTest(TestCase):
    
    username = 'testuser'
    password = 'testpass'
    email = 'test@test.com'
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(self.username, self.email, self.password)
        auth = self.getUserAuth(self.username, self.password)
        self.extra = {
            'HTTP_AUTHORIZATION': auth,
        }
        
        newTeam = Team.objects.create(name="Test1", tag="T")
        newTeam2 = Team.objects.create(name="AnotherTeam", tag="Test")
        newTeam3 = Team.objects.create(name="TestableTeam", tag="TT")

    def getUserAuth(self, username, password):
        auth = '%s:%s' % (username, password)
        auth = 'Basic %s' % base64.encodestring(auth)
        auth = auth.strip()

        return auth
        
    def test_find_all_teams(self):
        response = self.client.get('/players/allteams/', {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        
        result = response.content
        
        self.failUnless(result)
        self.assertTrue("Test1" in result)
        self.assertTrue("AnotherTeam" in result)
        self.assertTrue("TestableTeam" in result)

    def test_find_all_teams_unauthenticated(self):
        response = self.client.get('/players/allteams/', {})
        self.assertEqual(response.status_code, 401)
        
    def test_find_matching_teams_1(self):
        response = self.client.get('/players/teamquery/?query=t', {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        
        result = response.content
        
        self.failUnless(result)
        self.assertTrue("Test1" in result)
        self.assertTrue("AnotherTeam" not in result)
        self.assertTrue("TestableTeam" in result)

    def test_find_matching_teams_1_unauthenticated(self):
        response = self.client.get('/players/teamquery/?query=t', {})
        self.assertEqual(response.status_code, 401)
        
    def test_find_matching_teams_2(self):
        response = self.client.get('/players/teamquery/?query=another', {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        
        result = response.content
        
        self.failUnless(result)
        self.assertTrue("Test1" not in result)
        self.assertTrue("AnotherTeam" in result)
        self.assertTrue("TestableTeam" not in result)
        
    def test_find_matching_teams_3(self):
        response = self.client.get('/players/teamquery/?query=TEST', {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        
        result = response.content
        
        self.failUnless(result)
        self.assertTrue("Test1" in result)
        self.assertTrue("AnotherTeam" in result)
        self.assertTrue("TestableTeam" in result)
        
    def test_find_matching_teams_4(self):
        response = self.client.get('/players/teamquery/?query=tT', {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        
        result = response.content
        
        self.failUnless(result)
        self.assertTrue("Test1" not in result)
        self.assertTrue("AnotherTeam" not in result)
        self.assertTrue("TestableTeam" in result)
        
    def test_find_matching_teams_5(self):
        response = self.client.get('/players/teamquery/?query=nope', {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        
        result = response.content
        
        self.failUnless(result)
        self.assertTrue("Test1" not in result)
        self.assertTrue("AnotherTeam" not in result)
        self.assertTrue("TestableTeam" not in result)


class PlayerTest(TestCase):
    username = 'testuser'
    password = 'testpass'
    email = 'test@test.com'
    player1pk = '0'
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(self.username, self.email, self.password)
        auth = self.getUserAuth(self.username, self.password)
        self.extra = {
            'HTTP_AUTHORIZATION': auth,
        }

        newTeam = Team.objects.create(name="Test1", tag="T")
        newTeam2 = Team.objects.create(name="AnotherTeam", tag="Test")
        newTeam3 = Team.objects.create(name="TestableTeam", tag="TT")

        player1 = Player.objects.create(name = "p1", handle = "ph1", team = newTeam, race = "Terran", elo = "1500", nationality = "US")
        self.player1pk = player1.pk
        player2 = Player.objects.create(name = "p2", handle = "ph2", team = newTeam2, race = "Protoss", elo = "1600", nationality = "RU")
        player3 = Player.objects.create(name = "p3", handle = "ph3", team = newTeam3, race = "Zerg", elo = "1700", nationality = "KR")

    def getUserAuth(self, username, password):
        auth = '%s:%s' % (username, password)
        auth = 'Basic %s' % base64.encodestring(auth)
        auth = auth.strip()

        return auth

    def test_find_all_players(self):
        response = self.client.get('/players/getall/',{}, **self.extra)
        self.assertEqual(response.status_code, 200)
        result = response.content

        self.failUnless(result)
        self.assertTrue("p1" in result)
        self.assertTrue("p2" in result)
        self.assertTrue("p3" in result)

    def test_player_with_id(self):
        response = self.client.get('/players/withid/?id='+ str(self.player1pk),{}, **self.extra)
        result = response.content

        self.failUnless(result)
        self.assertTrue("p1" in result)

    def test_find_all_players_unauthenticated(self):
        response = self.client.get('/players/getall/', {})
        self.assertEqual(response.status_code, 401)

    def test_player_with_id_unauthenticated(self):
        response = self.client.get('/players/withid/?id='+ str(self.player1pk), {})
        self.assertEqual(response.status_code, 401)

