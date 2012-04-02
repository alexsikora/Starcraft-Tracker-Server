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

