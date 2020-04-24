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
from .forms import CreateUserForm, ProfileForm, CreateCourseForm
from .models import Profile, Course, Course_Section, Message, Feedback
from .decorators import unathenticated_user, allowed_users
from django.http import JsonResponse
from django.urls import reverse
import datetime, time
from time import strftime
from time import gmtime
import pandas as pd
from star_ratings.models import Rating
import stripe
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template.defaultfilters import register






stripe.api_key = "sk_test_Q8PFwzlQAZvMItaPbMUBHV9s000rGISHUB"

CHAMPION_ICON_IMG_PATH = "tiles/"
static_champ_list_req = requests.get("http://ddragon.leagueoflegends.com/cdn/10.8.1/data/en_US/champion.json")
static_champ_list = static_champ_list_req.json()
POSITION_DICT = {"MIDDLE":"MID","BOTTOM":"ADC","DUO_CARRY":"ADC", "DUO_SUPPORT":"SUPPORT", "TOP":"TOP", "JUNGLE":"JUNGLE", "NONE":"JUNGLE"}
SINGLE_MATCH_URL_REQ = "https://eun1.api.riotgames.com/lol/match/v4/matches/"
CHAMP_DICT = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    CHAMP_DICT[row['key']] = row['id']


QUEUE_ID = {400:"Draft Pick", 420:"Ranked Solo", 430:"Blind Pick", 440:"Ranked Flex", 450:"Aram", 700:"Clash"}
API_KEY = 'RGAPI-16f7535d-655f-4330-a66a-21716158cd5e'
REGIONS = {'BR1','EUN1','EUW1','JP1','KR','LA1','LA2','NA1','OC1','TR1','RU'}

### CUSTOM TEMPLATE TAG ###

#custom template tag
@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group =  Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False

    return group in user.groups.all()

### VIEWS ####


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
            return redirect('login_link')


    context = {"page_name":"Register", 'form':form, 'profile_form':profile_form}

    return render(request, 'register.html', context)

#!!!! Homepage View !!!!#
def landingpage(request):
    context = {"page_name":"Index"}

    return render(request, 'index.html', context )


#!!!! Summoner_Dashboard View !!!!#
@login_required(login_url='login_link',redirect_field_name="next")
@allowed_users(allowed_roles=['admin','user'])
def summoner_dashboard(request):

    page_name = request.user.profile.summoner_name + " Dashboard"
    user = request.user
    new_messages = Message.objects.filter(receiver=user,new_message=True)
    new_messages_number = len(new_messages)
    region = user.profile.region
    summoner_name = user.profile.summoner_name


    # RIOT API CALLS #
    # CALL FOR SUMMONER DETAILS #
    summoner_details_request = requests.get("https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name + "?api_key=" + API_KEY)
    summoner_details = summoner_details_request.json()

    try:
        if summoner_details['status']['status_code']:
            context = {"message":summoner_details['status']['message']}
            return  render(request, 'dashboard.html', context)
    except:
        pass



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
    rank_pre_process = rank_details_request.json()
    rank_details_json = []

    for rank_solo in rank_pre_process:
        if rank_solo['queueType'] == "RANKED_SOLO_5x5":
            rank_details_json = rank_solo


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
        rank_details = rank_details_json
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
        last_matches_request = requests.get("https://eun1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoner_account_id + "?endIndex=10&api_key=" + API_KEY)
        last_matches_list = last_matches_request.json()
        print(last_matches_list)
        game_details_list = []
        #print(game_details_list)
        counter = 0
        for game_details in last_matches_list['matches']:
                game_details_list += [game_details]
                counter += 1


        # GETTING MATCH DETAILS FROM API CALL #
        match_details_list = []
        for every_game_id in game_details_list:

            match_details_request = requests.get("https://" + region + ".api.riotgames.com/lol/match/v4/matches/" + str(every_game_id['gameId']) + "?api_key=" + API_KEY)
            match_details_list += [match_details_request.json()]


        #print(match_details_list)

        # GETTING PLAYER STATS FROM MATCH DETAILS #
        player_stats_list = []
        last_matches_recent_champions = []
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
                    if game_duration <= 0:
                        game_duration = 1;

                    game_duration_minutes = strftime("%M:%S", gmtime(single_match['gameDuration']))
                    total_team_damage = 0
                    total_team_kills = 0
                    if details['participantId'] <= 5:
                        total_team_damage = single_match['participants'][0]['stats']['totalDamageDealtToChampions'] + single_match['participants'][1]['stats']['totalDamageDealtToChampions'] + single_match['participants'][2]['stats']['totalDamageDealtToChampions'] + single_match['participants'][3]['stats']['totalDamageDealtToChampions'] + single_match['participants'][4]['stats']['totalDamageDealtToChampions']
                        total_team_kills = single_match['participants'][0]['stats']['kills'] + single_match['participants'][1]['stats']['kills'] + single_match['participants'][2]['stats']['kills'] + single_match['participants'][3]['stats']['kills'] + single_match['participants'][4]['stats']['kills']
                    else:
                        total_team_damage = single_match['participants'][5]['stats']['totalDamageDealtToChampions'] + single_match['participants'][6]['stats']['totalDamageDealtToChampions'] + single_match['participants'][7]['stats']['totalDamageDealtToChampions'] + single_match['participants'][8]['stats']['totalDamageDealtToChampions'] + single_match['participants'][9]['stats']['totalDamageDealtToChampions']
                        total_team_kills = single_match['participants'][5]['stats']['kills'] + single_match['participants'][6]['stats']['kills'] + single_match['participants'][7]['stats']['kills'] + single_match['participants'][8]['stats']['kills'] + single_match['participants'][9]['stats']['kills']
                    #print(every_match['participants'][player_id['participantId'] - 1])

                    if total_team_kills <= 0:
                        total_team_kills = 1

                    if total_team_damage <= 0:
                        total_team_damage = 1


                    last_matches_recent_champions += [{"champ":CHAMP_DICT[str(single_match['participants'][details['participantId'] - 1]['championId'])]}]
                    divisor = 0
                    if single_match['participants'][details['participantId'] - 1]['stats']['deaths'] == 0:
                        divisor = 1
                    else:
                        divisor = single_match['participants'][details['participantId'] - 1]['stats']['deaths']

                    player_stats_list += [{"game_url":SINGLE_MATCH_URL_REQ + str(single_match['gameId']) + "?api_key=" + API_KEY,
                     "kills":single_match['participants'][details['participantId'] - 1]['stats']['kills'],
                     "deaths":single_match['participants'][details['participantId'] - 1]['stats']['deaths'],
                     "assist":single_match['participants'][details['participantId'] - 1]['stats']['assists'],
                     "win":single_match['participants'][details['participantId'] - 1]['stats']['win'],
                     "KDA":round((single_match['participants'][details['participantId'] - 1]['stats']['kills'] + single_match['participants'][details['participantId'] - 1]['stats']['assists']) / divisor ,2),
                     "champion_icon":CHAMPION_ICON_IMG_PATH + CHAMP_DICT[str(single_match['participants'][details['participantId'] - 1]['championId'])] + "_0.jpg",
                     "role":str("laneicons/" + str(POSITION_DICT[player_role]) + ".png"),
                     "game_type":QUEUE_ID[single_match['queueId']],
                     "game_duration":game_duration_minutes,
                     "vis_per_minute":round((single_match['participants'][details['participantId'] - 1]['stats']['visionScore']/game_duration),2),
                     "total_cs":single_match['participants'][details['participantId'] - 1]['stats']['totalMinionsKilled'],
                     "cs_per_min":round((single_match['participants'][details['participantId'] - 1]['stats']['totalMinionsKilled']/game_duration),2),
                     "damage_per_minute":int(round((single_match['participants'][details['participantId'] - 1]['stats']['totalDamageDealtToChampions']/game_duration),0)),
                     "dmg_percentage_per_team":int(round((single_match['participants'][details['participantId'] - 1]['stats']['totalDamageDealtToChampions']/total_team_damage)*100,0)),
                     "kill_participation":int(round(((single_match['participants'][details['participantId'] - 1]['stats']['kills'] + single_match['participants'][details['participantId'] - 1]['stats']['assists'])/total_team_kills)*100,0)),
                     "champ_name":CHAMP_DICT[str(single_match['participants'][details['participantId'] - 1]['championId'])]
                     }]






        #print(player_stats_list)
        sorted_list = []
        for e in last_matches_recent_champions:
            sorted_list.append(e['champ'])

        my_count = pd.Series(sorted_list).value_counts().reset_index().values.tolist()
        #print(sorted_list)
        #print(my_count)
        most_recent_champ_occ = 0
        most_recent_champ = ""
        second_most_recent_champ_occ = 0
        second_most_recent_champ = ""
        third_most_recent_champ_occ = 0
        third_most_recent_champ = ""
        for v in my_count:
            if v[1] > most_recent_champ_occ:
                most_recent_champ = v[0]
                most_recent_champ_occ = v[1]
            elif v[1] > second_most_recent_champ_occ:
                second_most_recent_champ = v[0]
                second_most_recent_champ_occ = v[1]
            elif v[1] > third_most_recent_champ_occ:
                third_most_recent_champ_occ = v[1]
                third_most_recent_champ = v[0]
            else:
                pass



        most_recent_champ_icon = ""
        most_recent_champ_wins = 0
        most_recent_champ_loses = 0
        most_recent_champ_total_kills = 0
        most_recent_champ_total_deaths = 0
        most_recent_champ_total_assists = 0
        second_recent_champ_icon = ""
        second_recent_champ_wins = 0
        second_recent_champ_loses = 0
        second_recent_champ_total_kills = 0
        second_recent_champ_total_deaths = 0
        second_recent_champ_total_assists = 0
        third_recent_champ_icon = ""
        third_recent_champ_wins = 0
        third_recent_champ_loses = 0
        third_recent_champ_total_kills = 0
        third_recent_champ_total_deaths = 0
        third_recent_champ_total_assists = 0





        for champ_stats in player_stats_list:
            if champ_stats['champ_name'] == most_recent_champ:
                most_recent_champ_total_kills += champ_stats['kills']
                most_recent_champ_total_assists += champ_stats['assist']
                most_recent_champ_total_deaths += champ_stats['deaths']
                most_recent_champ_icon = champ_stats['champion_icon']

                if champ_stats['win'] == True:
                    most_recent_champ_wins += 1
                elif champ_stats['win'] == False:
                    most_recent_champ_loses += 1

            elif champ_stats['champ_name'] == second_most_recent_champ:
                second_recent_champ_total_kills += champ_stats['kills']
                second_recent_champ_total_deaths += champ_stats['deaths']
                second_recent_champ_total_assists += champ_stats['assist']
                second_recent_champ_icon = champ_stats['champion_icon']

                if champ_stats['win'] == True:
                    second_recent_champ_wins += 1
                elif champ_stats['win'] == False:
                    second_recent_champ_loses += 1

            elif champ_stats['champ_name'] == third_most_recent_champ:
                third_recent_champ_total_kills += champ_stats['kills']
                third_recent_champ_total_deaths += champ_stats['deaths']
                third_recent_champ_total_assists += champ_stats['assist']
                third_recent_champ_icon = champ_stats['champion_icon']

                if champ_stats['win'] == True:
                    third_recent_champ_wins += 1
                else:
                    third_recent_champ_loses += 1

        if most_recent_champ_total_deaths == 0:
            most_KDA = round((most_recent_champ_total_kills + most_recent_champ_total_assists)/1,2)
        else:
            most_KDA = round((most_recent_champ_total_kills + most_recent_champ_total_assists)/most_recent_champ_total_deaths,2)

        if second_recent_champ_total_deaths == 0:
            second_KDA = round((second_recent_champ_total_kills + second_recent_champ_total_assists)/1,2)
        else:
            second_KDA = round((second_recent_champ_total_kills + second_recent_champ_total_assists)/second_recent_champ_total_deaths,2)

        if third_recent_champ_total_deaths == 0:
            third_KDA = round((third_recent_champ_total_kills + third_recent_champ_total_assists)/1,2)
        else:
            third_KDA = round((third_recent_champ_total_kills + third_recent_champ_total_assists)/third_recent_champ_total_deaths,2)

        most_win_rate = 0
        second_win_rate = 0
        third_win_rate = 0

        if most_recent_champ_wins == 0:
            most_win_rate = 0
        else:
            most_win_rate = round((most_recent_champ_wins/(most_recent_champ_loses + most_recent_champ_wins))*100,0)

        if second_recent_champ_wins == 0:
            second_win_rate = 0

        else:
            second_win_rate = round((second_recent_champ_wins /(second_recent_champ_loses + second_recent_champ_wins))*100,0)

        if third_recent_champ_wins == 0:
            third_win_rate = 0
        else:
            third_win_rate = round((third_recent_champ_wins/(third_recent_champ_loses + third_recent_champ_wins))*100,0)

        most_recent_champ_total_stats = {
            "champion_icon":most_recent_champ_icon,
            "wins":most_recent_champ_wins,
            "loses":most_recent_champ_loses,
            "win_rate":most_win_rate,
            "KDA": most_KDA

        }
        second_recent_champ_total_stats = {
            "champion_icon":second_recent_champ_icon,
            "wins":second_recent_champ_wins,
            "loses":second_recent_champ_loses,
            "win_rate":second_win_rate,
            "KDA": second_KDA

        }
        third_recent_champ_total_stats = {
            "champion_icon":third_recent_champ_icon,
            "wins":third_recent_champ_wins,
            "loses":third_recent_champ_loses,
            "win_rate":third_win_rate,
            "KDA": third_KDA

        }





        #request_match_details_json = request_match_details.json()
        #player_match_details = []

        #print(reques_match_details_json['participantIdentities'])
        #for every_participant in request_match_details_json['participantIdentities']:
            #if every_participant['player']['summonerName'] == summoner_name:
                #player_match_details = request_match_details_json['participants'][every_participant['participantId'] - 1]


        #print(player_match_details['stats'])
        #print(CHAMP_DICT[str(player_match_details['championId'])])

        context = {
                "page_name": page_name,
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
                "most_recent_champ":most_recent_champ_total_stats,
                "second_recent_champ":second_recent_champ_total_stats,
                "third_recent_champ":third_recent_champ_total_stats,
                "new_messages_number":new_messages_number,

                    }

    return  render(request, 'dashboard.html', context)


#!!!! Video Player View !!!!#
@xframe_options_exempt
def video_player(request,pk):

    user = request.user
    id = pk
    course = Course.objects.get(id=id)
    course_access = list(course.users_with_access.values('username'))
    user_has_access = False

    for e in course_access:
        if user.username == e['username']:
            user_has_access = True;
        else:
            pass

    if user_has_access == True:

        sections = Course_Section.objects.filter(course_id=course)

        context = {"page_name":"Video", "sections":sections}

        return render(request, 'video2.html', context)

    else:
        return  redirect('course',pk=course.id)


#!!!! Tutor_DASHBOARD View !!!!#

def tutor(request):

    user = request.user
    new_messages = Message.objects.filter(receiver=user,new_message=True)
    number_of_messages = len(new_messages)
    page_name = request.user.username + " Dashboard"
    last_login = user.last_login
    tutor_pic = user.tutor.profile_pic
    courses_set = Course.objects.filter(course_author=request.user.username).order_by('-last_updated')[:3]
    course_details = []

    for i in courses_set:
        try:
            rating = i.ratings.get()
            average = round(rating.average,2)
        except:
            average = 0


        course_details += [{
            "course_id":i.id,
            "course_name":i.course_name,
            "views":i.views,
            "ratings":average,
            "image_field":i.image_field,
            "buys":i.buys
        }]

    context = {"page_name":page_name,"last_login":last_login, "course_set":course_details,"tutor_pic":tutor_pic,"number_of_messages":number_of_messages}

    return render(request, 'tutor.html', context)


#!!!! Courses Search View !!!!#
def courses(request):

    courses_set = Course.objects.all()
    course_details = []

    for i in courses_set:
        try:
            rating = i.ratings.get()
            average = round(rating.average,2)
        except:
            average = 0


        course_details += [{
            "course_id":i.id,
            "course_name":i.course_name,
            "views":i.views,
            "ratings":average,
            "image_field":i.image_field,
            "price":i.price
        }]

    context = {"page_name":"Courses", "courses":course_details }

    return render(request, 'courses.html', context)


#!!!! Single Course  View !!!!#
@login_required(login_url='login_link',redirect_field_name="next")
def course(request,pk):
    course = Course.objects.get(pk=pk)
    course.views = course.views + 1
    course.save()
    user = request.user


    course_access = list(course.users_with_access.values('username'))
    user_has_access = False
    for e in course_access:
        if user.username == e['username']:
            print(e)
            user_has_access = True;
        else:
            pass


    try:
        ratings = course.ratings.get()
    except:
        ratings = 0

    sections = Course_Section.objects.filter(course_id=course)
    section_counter = len(sections)
    rank = course.rank
    rank_list = rank.split(',')
    print(rank_list)



    context = {"page_name":"Course", "course":course, "ratings":ratings, "course_access":user_has_access,"sections":sections,"section_counter":section_counter,"recommended_ranks":rank_list, "user":user}

    return render(request, 'course.html', context)

#!!!!  Course Creator  View !!!!#

def course_creator(request):

    course_form = CreateCourseForm()
    if request.method == "POST":
        course_form = CreateCourseForm(request.POST,request.FILES)

        if course_form.is_valid():
            course = course_form.save()
            course.course_author = request.user.username
            course.save()

            return redirect('section_creator',pk=course.id)

        else:
            context = {"page_name":"Course Creator","form":course_form}



    context = {"page_name":"Course Creator","form":course_form}

    return render(request, 'create-a-course.html', context )

#!!! Section Creator View !!!!#
def section_creator(request, pk):

    courses = []
    course = Course.objects.get(pk=pk)


    if request.POST:
        counter = request.POST.get('counter')
        for i in range(int(counter)):
                i += 1
                video_url = request.POST.get('section' + str(i) + '_video_url')
                print(video_url)
                section_title = request.POST.get('section' + str(i) +'_section_title')
                print(section_title)
                section_description = request.POST.get('section' + str(i) +'_section_description')
                print(section_description)

                section = Course_Section(course_id=course,section_title=section_title,video_url=video_url,section_description=section_description,order=i)
                section.save()





    context = {"page_name":"Section Creator","course":course,"courses":courses}

    return render(request, 'section_creator.html',context)


#!!! Tutor Application View !!!#
def tutor_application(request):

    context = {'page_name':"How it works"}
    return render(request,'how_it_works.html', context)


def unathorized(request):

    return render(request,'401.html')



#!!! REST API'S !!!#

def charge(request):
    amount = 5
    if request.method == 'POST':
        print('Data:', request.POST)
        course_id = request.POST['course_id']
        price = float(request.POST['course_price'])
        customer = stripe.Customer.create(
        email=request.POST['email'],
        name=request.POST['user_id'],
        source=request.POST['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount= int(price) * 100,
            currency='eur',
            description="payment for a course"
        )
        user = User.objects.get(id=request.POST['user_id'])
        course = Course.objects.get(id=course_id)
        course.users_with_access.add(user)
        course.buys = course.buys + 1
        course.save()



    return redirect('course' ,pk=course_id)



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



#!!! COURSE SUBSCRIPTION !!!#
def course_subscription(request, instruction, pk):

    course = Course.objects.get(pk=pk)
    if instruction == 'subscribe':
        Course.subscribe(request.user,course)

    elif instruction == 'unsubscribe':
        Course.unsubscribe(request.user, course)

    return redirect('homepage')


def course_detail(request):

    user = request.user
    course = Course.objects.get(pk=1)
    course_title = course.course_name
    course_access = list(course.users_with_access.values('username'))
    user_has_access = False
    for e in course_access:
        if user.username == e['username']:
            print(e)
            user_has_access = True;
        else:
            pass



    return render(request,'change-course.html',{"course":course, "course_access":user_has_access})
