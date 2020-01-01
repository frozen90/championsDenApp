from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
# Create your views here.

API_KEY = 'RGAPI-5ccb450e-29d5-4696-b60d-481a4047e541'


def landingpage(request):

    return HttpResponse('Hello welcome in landingpage')


def getSummoner(request):

    if request.POST:
        username = request.POST.get('name_field')
        response = requests.get("https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + username + "?api_key=" + API_KEY)
        summonerData = response.json()
        try:

            summoner = {
            'id': summonerData['id'],
            'accountID': summonerData['accountId'],
            'puuid': summonerData['puuid'],
            'name': summonerData['name'],
            'profileIcon': summonerData['profileIconId'],
            'revisionDate': summonerData['revisionDate'],
            'summonerLevel': summonerData['summonerLevel']}
            return render(request, 'summoner.html',{'summoner': summoner})

        except: 
            data = summonerData['status']
            errormessage = data['message']
            return render(request, 'summoner.html',{'errormessage': errormessage})

    return render(request, 'summoner.html')
