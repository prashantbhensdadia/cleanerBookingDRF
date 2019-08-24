import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User as user
from django.dispatch import receiver
import os, time

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone_no, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not phone_no:
            raise ValueError('The given email must be set')
        user = self.model(phone_no=phone_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_no, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_no, password, **extra_fields)

    def create_superuser(self, phone_no, password,  **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_no, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = None
    first_name = models.CharField(blank=True, null=True, max_length=20)
    last_name = models.CharField(blank=True, null=True, max_length=20)
    phone_no = models.CharField(unique = True, max_length = 10)
    created_at = models.DateTimeField(auto_now_add = True)
    modified_at = models.DateTimeField(auto_now = True)
    
    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = ['password']

    objects = UserManager()

class City(models.Model):
    name = models.CharField(blank=False, null=False, max_length = 50)

    def __str__(self):
        return self.name

class Cleaner(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    city = models.ForeignKey('City', blank=False, null=False)

    def __str__(self):
        return self.first_name + " " +self.last_name

class Appointment(models.Model):
    user = models.ForeignKey('User', blank=False, null=False)
    cleaner = models.ForeignKey('Cleaner', blank=False, null=False)
    time = models.DateTimeField()