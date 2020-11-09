""" Test cases for User sub-app of tinyfunds"""
from django.test import TestCase
from .models import UserManager, User  #from users directory, overloaded user term

# Time mangement
from django.utils import timezone
import datetime
import pdb


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

        

    def test_join_time(self):
        newsuper = User(email="super@super.com",name="superman",bio="moderator for site",is_staff=True,is_superuser=True)
        newsuper.save() # save superuser to SQL database

        #creting a basic user without superuser permissions
        basicuser = User(email="basic@email.com",name="normalman",bio="basic site user") # default values should not be a super user
        basicuser.save()

        #Testing field creation timing
        self.assertTrue(newsuper.date_joined < timezone.now()) #Time should exist
        self.assertTrue(newsuper.date_joined < basicuser.date_joined) #superuser should have been created before the basic user
    
    def test_abs_url(self):
        basicuser = User(email="basic@email.com",name="normalman",bio="basic site user")
        basicuser.save()
        print(basicuser.get_absolute_url())
        self.assertTrue(basicuser.get_absolute_url() == "/users/1/")

        basicuser_2 = User(email="basic_1@email.com",name="normal",bio="basic site user second")
        basicuser_2.save()
        self.assertTrue(basicuser_2.get_absolute_url() == "/users/2/")
    
    def test_add_money_normal(self):
        basicuser = User(email="basic@email.com",name="normalman",bio="basic site user")
        basicuser.save()

        basicuser.add_money(100)
        self.assertTrue(basicuser.total_donated == 100)
    
    def test_add_money_negative(self):
        basicuser = User(email="basic@email.com",name="normalman",bio="basic site user")
        basicuser.save()

        basicuser.add_money(-1)
        self.assertTrue(basicuser.total_donated == 0)
    
    def test_get_level_one(self):
        basicuser = User(email="basic@email.com",name="normalman",bio="basic site user")
        basicuser.save()

        basicuser.add_money(5)

        self.assertTrue(basicuser.get_level() == 1)
    
    def test_get_level_two(self):
        basicuser = User(email="basic@email.com",name="normalman",bio="basic site user")
        basicuser.save()

        basicuser.add_money(10)

        self.assertTrue(basicuser.get_level() == 2)

    
    def test_get_level_three(self):
        basicuser = User(email="basic@email.com",name="normalman",bio="basic site user")
        basicuser.save()

        basicuser.add_money(20)

        self.assertTrue(basicuser.get_level() == 3)
    
    def test_get_level_four(self):
        basicuser = User(email="basic@email.com",name="normalman",bio="basic site user")
        basicuser.save()

        basicuser.add_money(30)

        self.assertTrue(basicuser.get_level() == 4)
    
    def test_get_level_color_one(self):
        basicuser = User(email="basic@email.com",name="normalman",bio="basic site user")
        basicuser.save()

        self.assertTrue(basicuser.get_level_color() == "")

    def test_get_level_color_two_to_four(self):
        basicuser = User(email="basic@email.com",name="normalman",bio="basic site user")
        basicuser.save()

        basicuser.add_money(20)

        self.assertTrue(basicuser.get_level_color() == "9,150,9")
    
    def test_get_level_color_two_to_four(self):
        basicuser = User(email="basic@email.com",name="normalman",bio="basic site user")
        basicuser.save()

        basicuser.add_money(20)

        self.assertTrue(basicuser.get_level_color() == "9,150,9") 

    def test_get_level_color_five_to_nine(self):
        basicuser = User(email="basic@email.com",name="normalman",bio="basic site user")
        basicuser.save()
        
        basicuser.add_money(50)
        
        self.assertTrue(basicuser.get_level_color() == "24,150,24")
    
    def test_get_level_color_above_ten(self):
        basicuser = User(email="basic@email.com",name="normalman",bio="basic site user")
        basicuser.save()
        
        basicuser.add_money(100)
        
        self.assertTrue(basicuser.get_level_color() == "88,150,155")
    
    
    




    

    
    
    





    






    









    