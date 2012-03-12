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


class UserTest(TestCase):

    username = 'testuser'
    password = 'testpass'
    email = 'test@test.com'
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(self.username,self.username,self.password)
        auth = self.getUserAuth(self.username, self.password)
        self.extra = {
            'HTTP_AUTHORIZATION': auth,
        }
        
        nonauth = self.getUserAuth('nonexistant', 'nonexistant')
        self.nonextra = {
            'HTTP_AUTHORIZATION': nonauth,
        }

        inactiveauth = self.getUserAuth('inactive', 'inactive')
        self.inacextra = {
            'HTTP_AUTHORIZATION': inactiveauth,
        }

    def getUserAuth(self, username, password):
        auth = '%s:%s' % (username, password)
        auth = 'Basic %s' % base64.encodestring(auth)
        auth = auth.strip()

        return auth
        
    def test_create_user(self):
        response = self.client.post('/users/register/', {'username': 'test2', 'password': 'test2'})
        self.assertEqual(response.status_code, 200)
        result = simplejson.load(StringIO(response.content))
        self.assertEqual(result['response'], 'Account successfully created')
        
        finalUser = User.objects.get(username = 'test2')
        self.assertTrue(finalUser is not None)

    def test_create_user_already_existing(self):
        response = self.client.post('/users/register/', {'username': self.username, 'password': self.password});

        self.assertEqual(response.status_code, 200)
        result = simplejson.load(StringIO(response.content))
        self.assertEqual(result['response'], 'Account creation failed')

    def test_authenticate_user(self):
        response = self.client.post('/users/authenticate/', {}, **self.extra)
        self.assertEqual(response.status_code, 200)
        result = simplejson.load(StringIO(response.content))
        self.assertEqual(result['response'], 'Successful authentication')

    def test_authenticate_inactive(self):
        inactive_user = User.objects.create_user('inactive_user','inactive_user','inactive_password')
        inactive_user.is_active = False
        inactive_user.save()
        response = self.client.post('/users/authenticate/', {}, **{'HTTP_AUTHORIZATION': self.getUserAuth('inactive_user','inactive_password'),})
        self.assertEqual(response.status_code, 200)
        result = simplejson.load(StringIO(response.content))
        self.assertEqual(result['response'], 'Your account has been disabled')

    def test_authenticate_nonexistant(self):
        response = self.client.post('/users/authenticate/', {}, **self.nonextra)
        self.assertEqual(response.status_code, 401)

    def test_remove_user (self):
        response = self.client.post('/users/remove/',{}, **self.extra)
        self.assertEqual(response.status_code, 200)
        result = simplejson.load(StringIO(response.content))
        self.assertEqual(result['response'], "Successful account removal")

    def test_remove_nonexistant(self):
        response = self.client.post('/users/remove/',{}, **self.nonextra)
        self.assertEqual(response.status_code, 401)
        
    def testRemoveDisabled(self):
        self.user = User.objects.create_user('dummy','dummy','test')
        self.user.is_active = False
        self.user.save()
        response = self.client.post('/users/remove/',{},**{'HTTP_AUTHORIZATION': self.getUserAuth('dummy','test'),})
        self.assertEqual(response.status_code, 200)
        result = simplejson.load(StringIO(response.content))
        self.assertEqual(result['response'], "Your account has been disabled")
        
        
        
