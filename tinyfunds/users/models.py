from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user

    def __str__(self):
        return "gamerg8"

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    bio = models.CharField(max_length=254, null=True, blank=True)
    pfp = models.CharField(max_length=1024, null=False, blank=False, default="https://avatars2.githubusercontent.com/u/3195011?s=460&u=f421eadccb78b212d516b6b38cab7f2de97522e4&v=4")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    total_donated = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)
    total_hours_pledged = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=0)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
        
    def add_money(self, amount):
        if amount > 0:
            self.total_donated+=amount

    def add_hours(self, amount):
        if amount > 0:
            self.total_hours_pledged+=amount

    def get_level(self):
        return int((self.total_donated/10 + self.total_hours_pledged) + 1)

    def get_level_color(self):
        level = self.get_level()
        if (level > 10):
            return "{},150,{}".format((level*8)%200, (level*5+100)%200)
        elif (level > 5):
            return "{},150,{}".format((level*4)%50, (level*4)%50)
        elif (level == 1):
            return ""
        else:
            return "{},150,{}".format((level*3)%20, (level*3)%20)

    def __str__(self):
        return self.email
