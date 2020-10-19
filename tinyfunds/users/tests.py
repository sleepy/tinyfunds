""" Test cases for User sub-app of tinyfunds"""
from django.test import TestCase
from .models import UserManager, User  #from users directory, overloaded user term

# Time mangement
from django.utils import timezone
import datetime


"""Basic test case to test our testing procedures"""
class UsersFirstTest(TestCase): 
    def test_first_test(self):
        self.assertTrue("Hello" == "Hello")
        self.assertTrue("world" == "world")
        self.assertFalse(False) # yes, I actually just wrote this.

"""Test Cases for User sub-app Models"""
class UserModelTest(TestCase):
    #create a basic new user data entry with default pfp and permissions
    def test_create_normal_users(self):
        #Creation of a User Object for Fields Testing
        newuser = User(email="newuseremail@email.com", name="newuser's_name",bio="New User's Bio. I like Kittens.", is_staff=False, last_login=timezone.now())
        self.assertTrue(newuser.email == "newuseremail@email.com")
        self.assertTrue(newuser.name == "newuser's_name")
        self.assertTrue(newuser.bio == "New User's Bio. I like Kittens.")
        self.assertTrue(newuser.is_superuser == False) # Check default values properly instantiated
        
        newuser.save() #Saves newuser object to the SQL database
        self.assertTrue(newuser.date_joined < timezone.now()) #join time should be instantiated in the past
        
        #Direct SQL creation of another user object
        User.objects.create(email="email@gmail.com",name="Talos",bio="true king of skyrim")
        
        self.assertTrue(User.objects.exists()) #Objects should exist
        self.assertTrue(User.objects.filter(name="Talos").exists())
        self.assertTrue(User.objects.filter(name="newuser's_name").exists())
        self.assertFalse(User.objects.filter(name="NOT_A_NAME").exists())
        
        #No query set is created here , but could do q = User.objects.somefilter. and q2 = q1.filter()...
        self.assertTrue(User.objects.filter(email__contains="email.com").exists())
        self.assertFalse(User.objects.filter(email__contains="email.NOT").exists())

        #Testing Specific Object finding, since email organization matches
        self.assertTrue(newuser in User.objects.filter(email__contains="@email.com"))

    def test_create_superuser(self):
        newsuper = User(email="super@super.com",name="superman",bio="moderator for site",is_staff=True,is_superuser=True)
        newsuper.save() # save superuser to SQL database

        #creting a basic user without superuser permissions
        basicuser = User(email="basic@email.com",name="normalman",bio="basic site user") # default values should not be a super user
        basicuser.save()

        #Check Model instantiation permissions
        self.assertTrue(newsuper in User.objects.filter(is_superuser=True))
        self.assertFalse(basicuser in User.objects.filter(is_superuser=True))

        #Testing field creation timing
        self.assertTrue(newsuper.date_joined < timezone.now()) 
        self.assertTrue(newsuper.date_joined < basicuser.date_joined)
