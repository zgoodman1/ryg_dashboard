from sqlite3 import Timestamp
from django.db import models
from django.forms import DateField

# Create your models here.
class Green_by_date(models.Model):
    date = models.DateField()
    percentage = models.DecimalField(decimal_places=5, max_digits=7)

class Green_by_team(models.Model):
    team = models.CharField(max_length=200)
    percentage = models.DecimalField(decimal_places=5, max_digits=7)

class Emot_by_date(models.Model):
    date = models.DateField()
    emotion = models.CharField(max_length=200)
    percentage = models.DecimalField(decimal_places=5, max_digits=7)

class Num_check_ins(models.Model):
    date = models.DateField()
    check_ins = models.IntegerField()