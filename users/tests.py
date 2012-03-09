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

    username = 'lolwut'
    password = 'lolhai'
    email = 'lol@wut.com'
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(self.username,self.username,self.password)
        

    def testRemoveUser (self):
        response = self.client.post('/users/remove/',{'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Succesful account removal")

    def testRemoveNonexistant(self):
        response = self.client.post('/users/remove/',{'username': 'banana', 'password': 'lol'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Your username or password was invalid")
        
    def testRemoveDisabled(self):
        self.user = User.objects.create_user('dummy','dummy','test')
        User.user_permissions.remove(is_active)
        response = self.client.post('/users/remove/',{'username': 'dummy', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Your account has been disabled")
        
        
        
