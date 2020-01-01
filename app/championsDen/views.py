from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
# Create your views here.

API_KEY = 'RGAPI-38c91693-1ece-40fa-ac67-0df42a1c13f7'


def landingpage(request):

    return HttpResponse('Hello welcome in landingpage')


def getSummoner(request):
    response = requests.get('https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/amfetaminator200?api_key=' + API_KEY)
    summonerData = response.json()
    print(summonerData)
    level = summonerData['summonerLevel']
    return HttpResponse(level
    )
