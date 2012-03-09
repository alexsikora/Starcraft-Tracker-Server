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
        
    def test_create_user(self):
        response = self.client.post('/users/register/', {'username': 'test2', 'password': 'test2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Account successfully created')
        
        finalUser = User.objects.get(username = 'test2')
        self.assertTrue(finalUser is not None)

    def test_create_user_already_existing(self):
        response = self.client.post('/users/register/', {'username': self.username, 'password': self.password});

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Account creation failed')

    def test_authenticate_user(self):
        response = self.client.post('/users/authenticate/', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Successful authentication')

    def test_authenticate_inactive(self):
        inactive_user = User.objects.create_user('inactive_user','inactive_user','inactivepassword')
        inactive_user.is_active = False
        inactive_user.save()
        response = self.client.post('/users/authenticate/', {'username': 'inactive_user', 'password': 'inactivepassword'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Your account has been disabled')

    def test_authenticate_nonexistant(self):
        response = self.client.post('/users/authenticate/', {'username': 'nonexistant', 'password': 'nonexistant'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'Your username or password was invalid')

    def test_remove_user (self):
        response = self.client.post('/users/remove/',{'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Successful account removal")

    def test_remove_nonexistant(self):
        response = self.client.post('/users/remove/',{'username': 'banana', 'password': 'lol'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Your username or password was invalid")
        
    def testRemoveDisabled(self):
        self.user = User.objects.create_user('dummy','dummy','test')
        User.user_permissions.remove(is_active)
        response = self.client.post('/users/remove/',{'username': 'dummy', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Your account has been disabled")
        
        
        
