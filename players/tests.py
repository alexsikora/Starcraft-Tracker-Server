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

