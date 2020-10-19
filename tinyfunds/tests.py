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
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sites.models import Site
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.urls import reverse

#AllAuth install at tinyfunds proj: env/bin/...ajango-allauth/allauth/.../socialaccount/tests.py
from allauth.account import app_settings as account_settings
from allauth.account.models import EmailAddress
from allauth.account.utils import user_email, user_username
from allauth.tests import MockedResponse, TestCase, mocked_response
from allauth.utils import get_user_model
from allauth.socialaccount import app_settings, providers
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialLogin
from allauth.socialaccount.views import signup

# A Generic test-class to ensure that manage.py testing is working and finds a file
# Self:Note, tests must start with keyword test_name or they won't work
#classes should also contain the word Test as a convention to run
class FirstTest(TestCase): 
    def test_first_test(self):
        self.assertTrue("Hello" == "Hello")
        self.assertTrue("world" == "world")
        self.assertFalse(False) # yes, I actually just wrote this.


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