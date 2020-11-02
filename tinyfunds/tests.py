#Testing File for Tinyfunds Main Web-Application

#Various Python imports
import unittest #from python Unit testing
import datetime #for determining login/ account create times
import json
import random
import warnings
from urllib.parse import parse_qs, urlparse

#Django Imports
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sites.models import Site
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.urls import reverse
from django.utils import timezone

#Model Imports
from django.apps import apps
from .models import Event  # From Tinyfunds models
User = apps.get_model('users','User') #Get User class from theu sers app

#Django Testing Imports
from django.test import Client
from django.test.utils import setup_test_environment


# #AllAuth install at tinyfunds proj: env/bin/...ajango-allauth/allauth/.../socialaccount/tests.py
# from allauth.account import app_settings as account_settings
# from allauth.account.models import EmailAddress
# from allauth.account.utils import user_email, user_username
# from allauth.tests import MockedResponse, TestCase, mocked_response
# from allauth.utils import get_user_model
# from allauth.socialaccount import app_settings, providers
# from allauth.socialaccount.helpers import complete_social_login
# from allauth.socialaccount.models import SocialAccount, SocialApp, SocialLogin
# from allauth.socialaccount.views import signup

# A Generic test-class to ensure that manage.py testing is working and finds a file
# Self:Note, tests must start with keyword test_name or they won't work
#classes should also contain the word Test as a convention to run
class FirstTest(TestCase): 
    def test_first_test(self):
        self.assertTrue("Hello" == "Hello")
        self.assertTrue("world" == "world")
        self.assertFalse(False) # yes, I actually just wrote this.

class EventsTest(TestCase):
    def test_create_event(self):
        self.assertFalse(Event.objects.exists()) # No objects currently exist

        testevent = Event(title="New Event",pub_date=timezone.now())
        testevent.save()
        self.assertTrue(Event.objects.exists()) # Event was created

    def test_event_publish_date(self):
        old_event = Event(title="Old Event",pub_date=timezone.now()-datetime.timedelta(days=30))
        old_event.save() # save to SQL

        self.assertTrue(Event.objects.filter(title="Old Event").exists()) #Event Exists
        self.assertTrue(Event.objects.filter(pub_date__lte=timezone.now()).exists()) # Event is before or on today
        self.assertFalse(Event.objects.filter(pub_date__gte=timezone.now()).exists()) # Event is not on or before today

    def test_event_relative_publish_dates(self):
        old_event = Event(title="Old Event",pub_date=timezone.now()-datetime.timedelta(days=30))
        old_event.save() # save to SQL

        new_event = Event(title="New Event",pub_date=timezone.now()+datetime.timedelta(days=30))
        new_event.save() # save to SQL

        self.assertTrue(Event.objects.filter(title="Old Event").exists()) #Old Event Exists
        self.assertTrue(Event.objects.filter(title="New Event").exists()) #New Event Exists
        
        # Manual Check
        self.assertTrue(old_event.pub_date < new_event.pub_date)

        #Database Check
        self.assertTrue(Event.objects.filter(title="Old Event")[0].pub_date < Event.objects.filter(title="New Event")[0].pub_date)

class VisitViewsTest(TestCase):
    def test_home_view(self):
        #setup_test_environment() #Prepares test envrionment with views
        client = Client()        # Dummy Client for testing exploring pages
        response = client.get(reverse('home'))
        statcode = response.status_code
        self.assertTrue(statcode == 200)  # Code 200 Means homepage loads okay!

    def test_explore_view(self):
        client = Client()        # Dummy Client for testing exploring pages
        response = client.get(reverse('explore'))
        statcode = response.status_code
        self.assertTrue(statcode == 200)  # Code 200 Means explore index loads okay!

    def test_account_view(self):
        client = Client()        # Dummy Client for testing exploring pages
        response = client.get(reverse('account'))
        statcode = response.status_code
        self.assertTrue(statcode == 200)  # Code 200 Means accounts page loads okay!

    def test_account_edit_view(self):
        client = Client()        # Dummy Client for testing exploring pages
        response = client.get(reverse('editAccount'))
        statcode = response.status_code
        self.assertTrue(statcode == 200)  # Code 200 Means account edit page loads okay!

    def test_create_event_view(self):
        client = Client()        # Dummy Client for testing exploring pages
        response = client.get(reverse('create_event'))
        statcode = response.status_code
        self.assertTrue(statcode == 200)  # Code 200 Means event creation page loads okay!

    def test_user_page_view(self):
        client = Client()        # Dummy Client for testing exploring pages
        # Create some dummy User #
        newuser = User(email="newuseremail@email.com", name="newuser's_name",bio="New User's Bio. I like Kittens.", is_staff=False, last_login=timezone.now())
        newuser.save()
        ############################
        response = client.get(reverse('user', kwargs={'pk' : 1})) # First User's id.
        statcode = response.status_code
        self.assertTrue(statcode == 200)  # Code 200 Means user pages load okay!

    def test_event_page_view(self):
        client = Client()        # Dummy Client for testing exploring pages
        # Create some dummy Users #
        newuser = User(email="newuseremail@email.com", name="newuser's_name",bio="New User's Bio. I like Kittens.", is_staff=False, last_login=timezone.now())
        newuser.save()
        # Create a dummy Event #
        testevent = Event(title="New Event",pub_date=timezone.now())
        testevent.save()
        ####################
        response = client.get(reverse('event', kwargs={'pk' : 1})) # First Event key.
        statcode = response.status_code
        self.assertTrue(statcode == 200)  # Code 200 Means event pages load okay!



########### OUTDATED TEST CASES ##############

# # Testing Google Login Class
# class SocialAccountTests(TestCase):
#     #setup for next test
#     @override_settings(
#         SOCIALACCOUNT_AUTO_SIGNUP=True,
#         ACCOUNT_SIGNUP_FORM_CLASS=None,
#         ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.NONE,  # noqa
#     )

#     # Checking to make sure account creation works
#     def test_email_address_created(self):
#         factory = RequestFactory() #to be able to send inputs as a Client
#         request = factory.get("/accounts/login/callback/")
#         request.user = AnonymousUser()
#         SessionMiddleware().process_request(request)
#         MessageMiddleware().process_request(request)

#         User = get_user_model()  # User Model (class) from allauth package
#         tinyfunds_user = User()  #using the method to get an object
#         setattr(tinyfunds_user, account_settings.USER_MODEL_USERNAME_FIELD, "test")
#         setattr(tinyfunds_user, account_settings.USER_MODEL_EMAIL_FIELD, "test@example.com")

#         tinyfundsacct = SocialAccount(provider="openid", uid="123") #UID random test number
#         sociallogin = SocialLogin(user=tinyfunds_user, account=tinyfundsacct)  # sociallogin based on account object
#         complete_social_login(request, sociallogin)

#         tinyfunds_user = User.objects.get(**{acxxcount_settings.USER_MODEL_USERNAME_FIELD: "test"})
#         self.assertTrue(
#             SocialAccount.objects.filter(user=tinyfunds_user, uid=tinyfundsacct.uid).exists() #check all social accounts for the new user account and verify account id
#         )
#         self.assertTrue(
#             EmailAddress.objects.filter(user=tinyfunds_user, email=user_email(tinyfunds_user)).exists() #check all email addresses for the test email
#         )

#     #rewrite predefined settings here for the next test.
#     @override_settings(
#         ACCOUNT_EMAIL_REQUIRED=True,
#         ACCOUNT_UNIQUE_EMAIL=True,
#         ACCOUNT_USERNAME_REQUIRED=True,
#         ACCOUNT_AUTHENTICATION_METHOD="email",
#         SOCIALACCOUNT_AUTO_SIGNUP=True,
#     )

#     #checking to make sure Old account to sign-up gets used, not an empty new provider
#     def test_email_address_clash_username_required(self):
#         """Test clash on both username and email"""
#         request, resp = self._email_address_clash("test", "test@example.com") #calls helpser function
#         self.assertEqual(resp["location"], reverse("socialaccount_signup"))

#         # POST different username/email to social signup form
#         request.method = "POST"
#         request.POST = {"username": "other", "email": "other@example.com"}
#         resp = signup(request) #from the views imported above
#         user = get_user_model().objects.get(
#             **{account_settings.USER_MODEL_EMAIL_FIELD: "other@example.com"}
#         )
#         self.assertEqual(user_username(user), "other")


#     #Helper function (NOT TEST), used in email account testing
#     #Code taken from the default testing kit
#     #Credit to pennersr  @ github.com/pennersr/django-allauth/blob/master/allauth
#     def _email_address_clash(self, username, email):
#         User = get_user_model()
#         # Some existig user
#         exi_user = User()
#         user_username(exi_user, "test")
#         user_email(exi_user, "test@example.com")
#         exi_user.save()

#         # A social user being signed up...
#         account = SocialAccount(provider="twitter", uid="123")
#         user = User()
#         user_username(user, username)
#         user_email(user, email)
#         sociallogin = SocialLogin(user=user, account=account)

#         # Signing up, should pop up the social signup form
#         factory = RequestFactory()
#         request = factory.get("/accounts/twitter/login/callback/")
#         request.user = AnonymousUser()
#         SessionMiddleware().process_request(request)
#         MessageMiddleware().process_request(request)
#         resp = complete_social_login(request, sociallogin)
#         return request, resp
