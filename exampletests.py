from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson

from piston.utils import rc

import base64
from StringIO import StringIO

from models import *
from django.db import models
from django.contrib.auth.models import User

class RssTests(TestCase):
    username = 'usertest'
    password = 'test'
    email = 'test@test.com'

    firstRssName = 'Rss1'
    secondRssName = 'Rss2'

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(self.username, self.email, self.password)

        auth = self.getUserAuth(self.username, self.password)

        self.extra = {
            'HTTP_AUTHORIZATION': auth,
        }

        self.createRssFeeds()

    def getUserAuth(self, username, password):
        auth = '%s:%s' % (username, password)
        auth = 'Basic %s' % base64.encodestring(auth)
        auth = auth.strip()

        return auth

    def createRssFeeds(self):
        rss1 = RssFeed(
            name = self.firstRssName,
            url = 'rss://awesome.com',
        )
        rss1.save()

        rss2 = RssFeed(
            name = self.secondRssName,
            url = 'rss://awesome2.com',
        )
        rss2.save()

    def testGetRssFeeds(self):
        response = self.client.get('/api/rss/', {}, **self.extra)
        self.assertEqual(response.status_code, 200)

        result = simplejson.load(StringIO(response.content))

        self.failUnless(result)
        self.assertTrue(len(result) > 0)

    def testGetRssFeedById(self):
        response = self.client.get('/api/rss/1/', {}, **self.extra)
        self.assertEqual(response.status_code, 200)

        result = simplejson.load(StringIO(response.content))

        self.failUnless(result)
        self.assertEqual(result['name'], self.firstRssName)
    
    def testGetNonexistentRssFeed(self):
        response = self.client.get('/api/rss/3/', {}, **self.extra)
        self.assertEqual(response.status_code, 404)

    def testGetRssFeedAfterId(self):
        response = self.client.get('/api/rss/after/1/', {}, **self.extra)
        self.assertEqual(response.status_code, 200)

        result = simplejson.load(StringIO(response.content))

        self.failUnless(result)
        self.assertEqual(result[0]['name'], self.secondRssName)

    def testUnauthorizedRssRequest(self):
        response = self.client.get('/api/rss/')
        self.assertEqual(response.status_code, 401) 
