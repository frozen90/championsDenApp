from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Course
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


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','username', 'password1', 'password2',]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('summoner_name', 'region')



class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_name','role','tags','experience','rank','price','image_field')
