from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateField('Creation Date')

#!hello

class Post(models.Model):
    url = models.CharField(max_length=200)

    def __str__(self):
        pass