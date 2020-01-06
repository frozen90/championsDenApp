from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
# Create your views here.

API_KEY = 'RGAPI-ad7ca1bd-3af7-4f48-aa27-fd670a51d501'
REGIONS = {'BR1','EUN1','EUW1','JP1','KR','LA1','LA2','NA1','OC1','TR1','RU'}

def landingpage(request):

    return HttpResponse('Hello welcome in landingpage')


def getSummoner(request):

    if request.POST:
        username = request.POST.get('name_field')
        region = request.POST.get('region')
        response = requests.get("https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + username + "?api_key=" + API_KEY)
        summonerData = response.json()
        matches = requests.get("https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + summonerData['accountId'] + "?api_key=" + API_KEY)
        matchesData = matches.json()

        try:

            summoner = {
            'id': summonerData['id'],
            'accountID': summonerData['accountId'],
            'puuid': summonerData['puuid'],
            'name': summonerData['name'],
            'profileIcon': summonerData['profileIconId'],
            'revisionDate': summonerData['revisionDate'],
            'summonerLevel': summonerData['summonerLevel']}
            return render(request, 'summoner.html',{'summoner': summoner, 'userRegion': region,'regions': REGIONS, 'matches' : matchesData})

        except:
            data = summonerData['status']
            errormessage = data['message']
            return render(request, 'summoner.html',{'errormessage': errormessage, 'regions': REGIONS})

    return render(request, 'summoner.html', {'regions': REGIONS})
