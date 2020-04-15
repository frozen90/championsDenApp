from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.
REGION_CHOICES =(
    ("BR1", "Brazil"),
    ("EUN1", "EU Nordic East"),
    ("EUW1", "EU West"),
    ("JP1", "Japan"),
    ("KR", "Korea"),
    ("LA1", "Latin America 1"),
    ("LA2", "Latin America 2"),
    ("NA1", "North America"),
    ("OC1", "Oceania"),
    ("TR1", "Turkey"),
    ("RU", "Russia"),

)

class Profile(models.Model):

    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    summoner_name = models.CharField( max_length=100);
    region = models.CharField(max_length=4, choices=REGION_CHOICES);

    def __str__(self):
        return self.user.username
