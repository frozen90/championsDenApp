import requests
import random
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, ProfileForm
from .models import Profile
from .decorators import unathenticated_user, allowed_users
from django.http import JsonResponse
import datetime
# Create your views here.

API_KEY = 'RGAPI-02fed81c-4a81-4ee2-b9e8-ffd734628a90'
REGIONS = {'BR1','EUN1','EUW1','JP1','KR','LA1','LA2','NA1','OC1','TR1','RU'}

def index(request):
    names = ("bob", "dan", "jack", "lizzy", "susan")

    items = []
    for i in range(100):
        items.append({
            "name": random.choice(names),
            "age": random.randint(20,80),
            "url": "https://example.com",
        })

    context = {}
    context["items_json"] = json.dumps(items)

    return render(request, 'list.html', context)

#!!!! Login View !!!!#
@unathenticated_user
def user_login(request):






    if request.POST:
        username = request.POST.get('username_field')
        password = request.POST.get('password_field')
        user = authenticate(username=username, password=password)

        if user is not None:

            login(request,user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:

                return redirect('homepage')

        else:

            context = {"page_name":"Login", "message":"Username/Password Incorrect"}
            return render(request, 'login.html', context)

    context = {"page_name":"Login"}
    return render(request, 'login.html', context)

#!!!! Logout View !!!!#
def user_logout(request):
    logout(request)
    context = {"page_name":"Homepage"}

    return redirect('/', context)

#!!!! Register View !!!!#
def register_page(request):
    form = CreateUserForm()
    profile_form = ProfileForm()
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            group = Group.objects.get(name='user')
            user.groups.add(group)




            messages.success(request, 'Account was created for ' + username)
            return redirect('login')


    context = {"page_name":"Register", 'form':form, 'profile_form':profile_form}

    return render(request, 'register.html', context)

#!!!! Homepage View !!!!#
def landingpage(request):
    context = {"page_name":"Index"}

    return render(request, 'index.html', context )


#!!!! Summoner_Dashboard View !!!!#
@login_required(login_url='login',redirect_field_name="next")
@allowed_users(allowed_roles=['admin','user'])
def summoner_dashboard(request):

    user = request.user
    region = user.profile.region
    summoner_name = user.profile.summoner_name

    # RIOT API CALLS # 







    context = {"page_name":"Summoner Dashboard", "champion1_path":"images/MissFortune_icon.png"}

    return  render(request, 'dashboard.html', context)


def getSummoner(request):
    if request.POST:

        username = request.POST.get('name_field')
        region = request.POST.get('region')
        response = requests.get("https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + username + "?api_key=" + API_KEY)
        summonerData = response.json()
        matches = requests.get("https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + summonerData['accountId'] + "?endIndex=10&api_key=" + API_KEY)
        matchesData = matches.json()
        singleGameInfo = []
        for everyMatch in matchesData['matches']:

            singleGame = requests.get("https://" + region + ".api.riotgames.com/lol/match/v4/matches/" + str(everyMatch['gameId']) + "?api_key=" + API_KEY)
            singleGameData = singleGame.json()
            singleGameInfo += singleGameData




        try:

            summoner = {
            'id': summonerData['id'],
            'accountID': summonerData['accountId'],
            'puuid': summonerData['puuid'],
            'name': summonerData['name'],
            'profileIcon': summonerData['profileIconId'],
            'revisionDate': summonerData['revisionDate'],
            'summonerLevel': summonerData['summonerLevel']}
            return render(request, 'summoner.html',{'summoner': summoner, 'userRegion': region,'regions': REGIONS, 'matches' : matchesData, 'games': singleGameInfo, })

        except:
            data = summonerData['status']
            errormessage = data['message']
            return render(request, 'summoner.html',{'errormessage': errormessage, 'regions': REGIONS})

    return render(request, 'summoner.html', {'regions': REGIONS})



#!!!! Video Player View !!!!#
def video_player(request):
    context = {"page_name":"Video"}

    return render(request, 'video2.html', context)


#!!!! Tutor_DASHBOARD View !!!!#

def tutor(request):
    context = {"page_name":"Tutor"}

    return render(request, 'tutor.html', context)


#!!!! Courses Search View !!!!#
def courses(request):
    context = {"page_name":"Courses", "n":"range(1,1000000000000000)"}

    return render(request, 'courses.html', context)


#!!!! Single Course  View !!!!#
def course(request):
    context = {"page_name":"Course"}

    return render(request, 'course.html', context)

#!!!!  Course Creator  View !!!!#
def course_creator(request):
    context = {"page_name":"Course Creator"}

    return render(request, 'create-a-course.html')

def unathorized(request):

    return render(request,'401.html')



#!!! REST API'S !!!#

def check(request):
    if request.GET['role'] and request.GET['type']:
        timestamp = 1586900538779
        dt_object = datetime.datetime.fromtimestamp(1586899044)
        current_time = datetime.datetime.now()

        difference = current_time - dt_object


        current_user = request.user.profile.region
        print(difference)
        data = {'change': dt_object}
        return JsonResponse(data);


    data = {'name':'Vitor'}

    return JsonResponse(data)
