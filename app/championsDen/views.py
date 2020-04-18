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
import datetime, time
from time import strftime
from time import gmtime
# Create your views here.

CHAMPION_ICON_IMG_PATH = "http://ddragon.leagueoflegends.com/cdn/10.8.1/img/champion/"
static_champ_list_req = requests.get("http://ddragon.leagueoflegends.com/cdn/10.8.1/data/en_US/champion.json")
static_champ_list = static_champ_list_req.json()
POSITION_DICT = {"MIDDLE":"MID","BOTTOM":"ADC","DUO_CARRY":"ADC", "DUO_SUPPORT":"SUPPORT", "TOP":"TOP", "JUNGLE":"JUNGLE"}
CHAMP_DICT = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    CHAMP_DICT[row['key']] = row['id']


QUEUE_ID = {400:"Draft Pick", 420:"Ranked Solo/Duo", 430:"Blind Pick", 440:"Ranked Flex", 450:"Aram", 700:"Clash"}
API_KEY = 'RGAPI-6683789b-d0da-4ac3-b717-746490ee1b30'
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


    # RIOT API CALLS #
    # CALL FOR SUMMONER DETAILS #
    summoner_details_request = requests.get("https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + "amfetaminator200" + "?api_key=" + API_KEY)
    summoner_details = summoner_details_request.json()
    summoner_name = summoner_details['name']
    #print(summoner_details)
    profileIconId = summoner_details['profileIconId']
    profile_icon_path = "profile_icon/" + str(profileIconId) + ".png"
    summoner_id = summoner_details['id']
    summoner_account_id = summoner_details['accountId']
    summoner_puuid = summoner_details['puuid']
    summoner_level = summoner_details['summonerLevel']
    # Getting last played date and time #
    summoner_revision_date = summoner_details['revisionDate']
    to_str = str(summoner_revision_date)
    timestamp = ""
    counter = 0
    for i in to_str:
        if counter < 10:
            timestamp += i
            counter += 1
        else:
            pass

    last_seen_date = datetime.datetime.fromtimestamp(int(timestamp))
    time_difference = datetime.datetime.now() - last_seen_date
    #print(time_difference)
    last_played_date = ""
    if time_difference.days > 0:
        last_played_date = str(time_difference.days) + " days ago"
    else:
        last_played_hours = str(time_difference)
        if last_played_hours[1] == ":":
            last_played_date = last_played_hours[0:1] + " hours ago"
        else:
            last_played_date = last_played_hours[0:2] + " hours ago"

    # Getting current rank and LP Points #
    # CALL FOR CURRENT RANK AND LP #
    rank_details_request = requests.get("https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + summoner_id + "?api_key=" + API_KEY)
    rank_details_json = rank_details_request.json()
    if rank_details_json == []:
        # IF PLAYER IS UNRANKED #
        current_tier = "UNRANKED"
        ranked_helmet_path = "ranked_helmets/UNRANKED.webp"
        context = {
        "page_name":"Summoner Dashboard",
        "champion1_path":"images/MissFortune_icon.png",
        "profile_icon":profile_icon_path,
        "summoner_name":summoner_name,
        "last_played":last_played_date,
        "ranked_helmet_path": ranked_helmet_path,
        "current_tier":current_tier,
        "summoner_level": summoner_level

        }
    else:
        # IF PLAYER HAVE RANK #
        rank_details = rank_details_json[0]
        #print(rank_details)
        current_tier = rank_details['tier']
        current_rank = rank_details['rank']
        if current_tier == "MASTER" or current_tier == "GRANDMASTER" or current_tier =="CHALLENGER":
            current_rank = ""
            current_tier = rank_details['tier']
        current_lp = rank_details['leaguePoints']
        current_lp_str = str(current_lp)+ " " + "LP"
        current_wins = rank_details['wins']
        current_loses = rank_details['losses']
        css_color_class = current_tier + current_rank
        css_icon_color = current_tier
        ranked_helmet_path = "ranked_helmets/" + current_tier + current_rank + ".webp"
        #print(css_color_class)
        total_matches = current_wins + current_loses
        current_win_ratio = round((current_wins/total_matches) * 100, 2)

        # CALL FOR MATCHES DETAILS #

        #request_match_details = requests.get("https://eun1.api.riotgames.com/lol/match/v4/matches/2447297054?api_key=RGAPI-6683789b-d0da-4ac3-b717-746490ee1b30")
        last_matches_request = requests.get("https://"+ region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoner_account_id + "?api_key=" + API_KEY)
        last_matches_list = last_matches_request.json()
        #print(last_matches_list)
        game_details_list = []
        counter = 0
        for game_details in last_matches_list['matches']:

            if counter < 10:
                game_details_list += [game_details]
                counter += 1
            else:
                break

        # GETTING MATCH DETAILS FROM API CALL #
        match_details_list = []
        for every_game_id in game_details_list:

            match_details_request = requests.get("https://" + region + ".api.riotgames.com/lol/match/v4/matches/" + str(every_game_id['gameId']) + "?api_key=" + API_KEY)
            match_details_list += [match_details_request.json()]


        #print(match_details_list)

        # GETTING PLAYER STATS FROM MATCH DETAILS #
        player_stats_list = []
        counter = 0
        for single_match in match_details_list:
            position = game_details_list[counter]
            counter += 1
            for details in single_match['participantIdentities']:
                if details['player']['accountId'] == summoner_account_id:
                    player_role = ""
                    role = single_match['participants'][details['participantId'] - 1]['timeline']['role']
                    lane = single_match['participants'][details['participantId'] - 1]['timeline']['lane']
                    if role == "DUO" or role == "SOLO" or role == "NONE":
                        player_role = lane
                    else:
                        player_role = role


                    #print(player_role)
                    game_duration = round(single_match['gameDuration']/60,2)
                    game_duration_minutes = strftime("%M:%S", gmtime(single_match['gameDuration']))
                    total_team_damage = 0
                    if details['participantId'] <= 5:
                        total_team_damage = single_match['participants'][0]['stats']['totalDamageDealtToChampions'] + single_match['participants'][1]['stats']['totalDamageDealtToChampions'] + single_match['participants'][2]['stats']['totalDamageDealtToChampions'] + single_match['participants'][3]['stats']['totalDamageDealtToChampions'] + single_match['participants'][4]['stats']['totalDamageDealtToChampions']
                    else:
                        total_team_damage = single_match['participants'][5]['stats']['totalDamageDealtToChampions'] + single_match['participants'][6]['stats']['totalDamageDealtToChampions'] + single_match['participants'][7]['stats']['totalDamageDealtToChampions'] + single_match['participants'][8]['stats']['totalDamageDealtToChampions'] + single_match['participants'][9]['stats']['totalDamageDealtToChampions']
                    #print(every_match['participants'][player_id['participantId'] - 1])

                    player_stats_list += [{"gameId":single_match['gameId'],
                     "kills":single_match['participants'][details['participantId'] - 1]['stats']['kills'],
                     "deaths":single_match['participants'][details['participantId'] - 1]['stats']['deaths'],
                     "assist":single_match['participants'][details['participantId'] - 1]['stats']['assists'],
                     "win":single_match['participants'][details['participantId'] - 1]['stats']['win'],
                     "KDA":round((single_match['participants'][details['participantId'] - 1]['stats']['kills'] + single_match['participants'][details['participantId'] - 1]['stats']['assists']) / single_match['participants'][details['participantId'] - 1]['stats']['deaths'],2),
                     "champion_icon":CHAMPION_ICON_IMG_PATH + CHAMP_DICT[str(single_match['participants'][details['participantId'] - 1]['championId'])] + ".png",
                     "role":POSITION_DICT[player_role],
                     "game_type":QUEUE_ID[single_match['queueId']],
                     "game_duration":game_duration_minutes,
                     "vis_per_minute":round((single_match['participants'][details['participantId'] - 1]['stats']['visionScore']/game_duration),2),
                     "total_cs":single_match['participants'][details['participantId'] - 1]['stats']['totalMinionsKilled'],
                     "cs_per_min":round((single_match['participants'][details['participantId'] - 1]['stats']['totalMinionsKilled']/game_duration),2),
                     "damage_per_minute":round((single_match['participants'][details['participantId'] - 1]['stats']['totalDamageDealtToChampions']/game_duration),2),
                     "dmg_percentage_per_team":int(round((single_match['participants'][details['participantId'] - 1]['stats']['totalDamageDealtToChampions']/total_team_damage)*100,0)),
                     }]




        print(player_stats_list)



        #request_match_details_json = request_match_details.json()
        #player_match_details = []

        #print(reques_match_details_json['participantIdentities'])
        #for every_participant in request_match_details_json['participantIdentities']:
            #if every_participant['player']['summonerName'] == summoner_name:
                #player_match_details = request_match_details_json['participants'][every_participant['participantId'] - 1]


        #print(player_match_details['stats'])
        #print(CHAMP_DICT[str(player_match_details['championId'])])

        context = {
                "page_name":"Summoner Dashboard",
                "champion1_path":"images/MissFortune_icon.png",
                "profile_icon":profile_icon_path,
                "summoner_name":summoner_name,
                "last_played":last_played_date,
                "current_tier": current_tier,
                "current_rank": current_rank,
                "current_lp": current_lp_str,
                "current_wins": current_wins,
                "current_loses": current_loses,
                "current_win_ratio":current_win_ratio,
                "css_color_class": css_color_class,
                "css_icon_color": css_icon_color,
                "ranked_helmet_path": ranked_helmet_path,
                "summoner_level": summoner_level,
                "matches_list": player_stats_list,

                    }

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
