#Testing File for Tinyfunds Main Web-Application

#Various Python imports
import unittest #from python Unit testing
import datetime #for determining login/ account create times
import json
import random
import warnings
from urllib.parse import parse_qs, urlparse
from decimal import Decimal

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
from .models import Event, Pledge  # From Tinyfunds models
User = apps.get_model('users','User') #Get User class from the users app

#Views imports
from .users import views as user_views
from . import views
from .views import *

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

#Comprehensive Testing for Events Model
#Tests Event creation, sorting, and all functions
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

    def test_money_mathself(self):
        cheap_event = Event(title="I need 5 bucks",org_name="Slenderman",money_goal=5.00)
        cheap_event.save() #A test Event with a set money goal

        self.assertTrue(cheap_event.money_received == 0) # Make sure the event was prepped properly
        self.assertTrue(cheap_event.money_remaining() == 5.00)
        
        #Check that is also works in database:
        database_cheap_event = Event.objects.filter(title="I need 5 bucks")[0]
        self.assertTrue(database_cheap_event.money_received == 0 and database_cheap_event.money_remaining() == 5.00)

        database_cheap_event.add_money(Decimal('2.70')) # Simulating a pledge to test the add
        self.assertAlmostEqual(database_cheap_event.money_received, Decimal('2.70'))
        self.assertAlmostEqual(database_cheap_event.money_remaining(), Decimal('2.30'))
        

    def test_money_mathself_big(self):
        cheap_event = Event(title="I need 5000 bucks",org_name="Slenderman",money_goal=5000.00)
        cheap_event.save() #A test Event with a set money goal

        self.assertTrue(cheap_event.money_received == 0) # Make sure the event was prepped properly
        self.assertTrue(cheap_event.money_remaining() == 5000.00)
        
        #Check that is also works in database:
        database_cheap_event = Event.objects.filter(title="I need 5000 bucks")[0]
        self.assertTrue(database_cheap_event.money_received == 0 and database_cheap_event.money_remaining() == 5000.00)

        database_cheap_event.add_money(Decimal('2000')) # Simulating a pledge to test the add of a big donation
        self.assertAlmostEqual(database_cheap_event.money_received, Decimal('2000'))
        self.assertAlmostEqual(database_cheap_event.money_remaining(), Decimal('3000'))


    def test_money_mathself_3(self):
        cheap_event = Event(title="I need 20 bucks",org_name="Slenderman",money_goal=20.00)
        cheap_event.save() #A test Event with a set money goal

        self.assertTrue(cheap_event.money_received == 0) # Make sure the event was prepped properly
        self.assertTrue(cheap_event.money_remaining() == 20.00)
        
        #Check that is also works in database:
        database_cheap_event = Event.objects.filter(title="I need 20 bucks")[0]
        self.assertTrue(database_cheap_event.money_received == 0 and database_cheap_event.money_remaining() == 20.00)

        database_cheap_event.add_money(Decimal('1.254')) # Simulating a pledge to test the add of micro-donations less than 1 cent
        self.assertAlmostEqual(database_cheap_event.money_received, Decimal('1.254'))
        database_cheap_event.add_money(Decimal('1.111')) 
        self.assertAlmostEqual(database_cheap_event.money_received, Decimal('2.365'))
        
        
    def test_money_math_micro(self):
        cheap_event = Event(title="I need 20 bucks",org_name="Slenderman",money_goal=20.00)
        cheap_event.save() #A test Event with a set money goal

        self.assertTrue(cheap_event.money_received == 0) # Make sure the event was prepped properly
        self.assertTrue(cheap_event.money_remaining() == 20.00)
        
        #Check that is also works in database:
        database_cheap_event = Event.objects.filter(title="I need 20 bucks")[0]
        self.assertTrue(database_cheap_event.money_received == 0 and database_cheap_event.money_remaining() == 20.00)

        database_cheap_event.add_money(Decimal('1.111111')) # Simulating a pledge to test the add of micro-donations less than 1 cent
        self.assertAlmostEqual(database_cheap_event.money_received, Decimal('1.111111'))
        database_cheap_event.add_money(Decimal('1.111111')) 
        self.assertAlmostEqual(database_cheap_event.money_received, Decimal('2.222222'))


    def test_money_surplus(self):
        cheap_event = Event(title="I need 5 bucks",org_name="Slenderman",money_goal=5.00)
        cheap_event.save() #A test Event with a set money goal
        database_cheap_event = Event.objects.filter(title="I need 5 bucks")[0]
        database_cheap_event.add_money(Decimal('2.70')) # Simulating a pledge

        self.assertFalse(database_cheap_event.surplus()) # there is no surplus yet
        database_cheap_event.add_money(Decimal('3.50')) # add more money
        self.assertTrue(database_cheap_event.surplus()) # There should now be a surplus of 1.20
        
        #double check the right surplus of 1.20
        self.assertAlmostEqual(database_cheap_event.money_remaining(), Decimal('-1.20'))

    def test_no_money_surplus(self):
        cheap_event = Event(title="I need 5 bucks",org_name="Slenderman",money_goal=5.00)
        cheap_event.save() #A test Event with a set money goal
        database_cheap_event = Event.objects.filter(title="I need 5 bucks")[0]
        database_cheap_event.add_money(Decimal('2.70')) # Simulating a pledge

        self.assertFalse(database_cheap_event.surplus()) # there is no surplus yet
        database_cheap_event.add_money(Decimal('.25')) # add more money a few times
        database_cheap_event.add_money(Decimal('.25')) 
        database_cheap_event.add_money(Decimal('.25')) 
        database_cheap_event.add_money(Decimal('.25')) 
        database_cheap_event.add_money(Decimal('.25')) 
        self.assertFalse(database_cheap_event.surplus()) #there should still be no surplus




    def test_ordered_pledges_and_pledge_add(self):
        #Basic Event Setup
        cheap_event = Event(title="I need 5 bucks", org_name="Slenderman", money_goal=5.00)
        cheap_event.save() #A test Event with a set money goal
        database_cheap_event = Event.objects.filter(title="I need 5 bucks")[0]

        self.assertAlmostEqual(database_cheap_event.money_remaining(), Decimal('5'))
        
        #Pledge Setups & Testing
        poor_pledge = Pledge(event=database_cheap_event, payment_text='small', payment_amount=2) #2 dollars
        poor_pledge.confirm() #assume user confirms it
        poor_pledge.save()
        database_cheap_event.pledge_set.add(poor_pledge)
        database_cheap_event.add_money(poor_pledge.payment_amount) # Once confirmed, add value of pledge to the event total
        self.assertAlmostEqual(database_cheap_event.money_remaining(), Decimal('3'))

        rich_pledge = Pledge(event=database_cheap_event, payment_text='big', payment_amount=10) #10 dollars
        rich_pledge.confirm()
        rich_pledge.save() # Save the rich pledge
        database_cheap_event.pledge_set.add(rich_pledge)
        database_cheap_event.add_money(rich_pledge.payment_amount)

        #Pledge Order testing
        self.assertTrue(database_cheap_event.ordered_pledges().count() == 2) # 2 pledges in the set
        self.assertTrue(rich_pledge == database_cheap_event.ordered_pledges()[0]) # rich pledge is the most recent pledge (-date)
        self.assertTrue(poor_pledge == database_cheap_event.ordered_pledges()[1]) # poor pledge is the oldest pledge

    def test_goal_met(self):
        goalevent = Event(title="10.40 dollar goal", org_name="moneylenders", money_goal=10.40)
        goalevent.save() #A test Event with a set money goal
        database_goalevent = Event.objects.filter(title="10.40 dollar goal")[0]
        
        #confirm proper setup:
        self.assertAlmostEqual(database_goalevent.money_remaining(), Decimal('10.40'))
        self.assertFalse(database_goalevent.met())

        #confirm if goal is met or exceeded
        database_goalevent.add_money(Decimal('10.40'))
        self.assertTrue(database_goalevent.met())

        database_goalevent.add_money(Decimal('20.00'))
        self.assertTrue(database_goalevent.met()) # should still be true even above the goal.

    def test_goal_not_met_double(self):
        goalevent = Event(title="10.40 dollar goal", org_name="moneylenders", money_goal=10.40)
        goalevent.save() #A test Event with a set money goal
        database_goalevent = Event.objects.filter(title="10.40 dollar goal")[0]
        
        #confirm proper setup:
        self.assertAlmostEqual(database_goalevent.money_remaining(), Decimal('10.40'))
        self.assertFalse(database_goalevent.met())

        #confirm if goal is not met or met
        database_goalevent.add_money(Decimal('5.40'))
        self.assertFalse(database_goalevent.met())

        database_goalevent.add_money(Decimal('5.00'))
        self.assertTrue(database_goalevent.met()) # should now be true after multiple adds

    def test_goal_met_many(self):
        goalevent = Event(title="10.40 dollar goal", org_name="moneylenders", money_goal=10.40)
        goalevent.save() #A test Event with a set money goal
        database_goalevent = Event.objects.filter(title="10.40 dollar goal")[0]
        
        #confirm proper setup:
        self.assertAlmostEqual(database_goalevent.money_remaining(), Decimal('10.40'))
        self.assertFalse(database_goalevent.met())

        #confirm if goal is not met after many small donations
        database_goalevent.add_money(Decimal('0.40'))
        database_goalevent.add_money(Decimal('0.40'))
        database_goalevent.add_money(Decimal('0.40'))
        database_goalevent.add_money(Decimal('0.40'))
        database_goalevent.add_money(Decimal('0.40'))
        database_goalevent.add_money(Decimal('0.40'))
        database_goalevent.add_money(Decimal('0.40'))
        self.assertFalse(database_goalevent.met()) #should not be met yet

        database_goalevent.add_money(Decimal('12.00'))
        self.assertTrue(database_goalevent.met()) # should now be true after a big enough donation


class PledgeModelTest(TestCase):
    def test_create_pledge(self):
        blandevent = Event(title="Blank Test Event",pub_date=timezone.now()) #Blank event for testing pledge connections
        blandevent.save()
        
        self.assertFalse(Pledge.objects.exists())
        newpledge = Pledge(event=blandevent, payment_text='a donation', payment_amount=5.65, confirmed=False) #blank test pledge
        newpledge.save()

        self.assertTrue(Pledge.objects.exists()) # The event exists
        self.assertTrue(Pledge.objects.all()[0].id == newpledge.id) #Newpledge is the only pledge created (no duplicates)

    def test_confirm_pledge(self):
        blandevent = Event(title="Blank Test Event",pub_date=timezone.now()) #Blank event for testing pledge connections
        blandevent.save()
        
        newpledge = Pledge(event=blandevent,payment_text='a donation',payment_amount=5.65,confirmed=False) #blank test pledge
        newpledge.save()

        self.assertFalse(Pledge.objects.filter(event=blandevent)[0].confirmed)  #Newpledge is not yet confirmed
        newpledge.confirm() # Confirm the event as if visiting confirm view /event/pledge/{pk}/confirm
        newpledge.save()
        self.assertTrue(Pledge.objects.filter(event=blandevent)[0].confirmed) #Event is now confirmed by organizer
        

class VisitViewsTest(TestCase):
    def setUp(self):
        #Setup_Client for specific logins
        self.factory = RequestFactory()
        self.user = User.objects._create_user(
             email='cooluser@email.com', password='top_secret',is_staff=True,is_superuser=True)

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

    def test_edit_event_page_view(self):
        # Create a dummy Event #
        testevent = Event(title="New Event",pub_date=timezone.now())
        testevent.owner_id = self.user.id  # Force user to be the specific user
        testevent.save()
        ##################
        request = self.factory.get(reverse('edit_event', kwargs={'pk' : 1})) #edit the one and only event request url
        request.user = self.user  # The specific user should be able toaccess the event edit page
        
        response = event(request, testevent.id)   # server's response, should
        response.client = Client() # Create a client to attach to the reponse access the server response
        self.assertTrue(testevent.id == 1) #verify event id i.d matches pk of 1 for test
        expected_url = reverse('event', kwargs={'pk' : 1})
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        # should redirect, optional fecth commant and target status code loads the next wepage

    def test_confirm_pledge_page_view(self):
        # Create a dummy Event #
        testevent = Event(title="New Event",pub_date=timezone.now())
        testevent.owner_id = self.user.id  # Force user to be the specific user
        testevent.save()
        
        #Process a request based on self default user
        request = self.factory.get(reverse('confirm', kwargs={'pk' : 1})) #edit the one and only event request url
        request.user = self.user  # The specific user should be able toaccess the event edit page

        #Get response and attach access Client class
        response = confirm(request, 1)   # server's response
        response.client = Client() #Attach client to the reponse for test access

        expected_url = reverse('event', kwargs={'pk' : 1}) #the redirected url
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        # should redirect, optional fecth commant and target status code loads the next wepage







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
