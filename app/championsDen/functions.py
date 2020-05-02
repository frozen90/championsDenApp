import requests
import random
import json
from .models import Global_Stats,Profile,Course

DEV_API_KEY = 'RGAPI-6892c100-e755-4b44-a634-122038a9c2a7'
SINGLE_MATCH_URL_REQ = "https://eun1.api.riotgames.com/lol/match/v4/matches/"


def player_stats(tier, position):

    tier_to_be_fetched = tier
    player_position = position

    top_players_lp = requests.get("https://eun1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/"+ tier_to_be_fetched + "/I?page=1&api_key=" + DEV_API_KEY)
    top_players_lp_json = top_players_lp.json()

    leader = top_players_lp_json[0]
    second = top_players_lp_json[1]
    third = top_players_lp_json[2]


    leader_acc_id_req = requests.get("https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+ leader['summonerName'] +"?api_key=" + DEV_API_KEY)
    leader_acc_id = leader_acc_id_req.json()
    leader_matches_list = requests.get("https://eun1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + leader_acc_id['accountId'] + "?endIndex=100&api_key=" + DEV_API_KEY)
    second_acc_id_req = requests.get("https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+ leader['summonerName'] +"?api_key=" + DEV_API_KEY)
    second_acc_id = leader_acc_id_req.json()
    second_matches_list = requests.get("https://eun1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + second_acc_id['accountId'] + "?endIndex=100&api_key=" + DEV_API_KEY)
    third_acc_id_req = requests.get("https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+ second['summonerName'] +"?api_key=" + DEV_API_KEY)
    third_acc_id = leader_acc_id_req.json()
    third_matches_list = requests.get("https://eun1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + second_acc_id['accountId'] + "?endIndex=100&api_key=" + DEV_API_KEY)

    counter = 0
    game_id = []
    for game in leader_matches_list.json()['matches']:
        if counter < 10:
            if game['queue'] == 420:
                if game['role'] == position or game['lane'] == position:
                    game_id.append(game['gameId'])
                    counter += 1


    for game in second_matches_list.json()['matches']:
        if counter < 10:
            if game['queue'] == 420:
                if game['role'] == position or game['lane'] == position:
                    game_id.append(game['gameId'])
                    counter += 1


    for game in third_matches_list.json()['matches']:
        if counter < 10:
            if game['queue'] == 420:
                if game['role'] == position or game['lane'] == position:
                    game_id.append(game['gameId'])
                    counter += 1



    stats_list = []
    match_details_list = []
    for details in game_id:

        match_details_request = requests.get("https://" + "eun1"+ ".api.riotgames.com/lol/match/v4/matches/" + str(details) + "?api_key=" + DEV_API_KEY)
        match_details_list += [match_details_request.json()]


    for single_match in match_details_list:
        for details in single_match['participantIdentities']:
            if details['player']['accountId'] == leader_acc_id['accountId'] or details['player']['accountId'] == third_acc_id['accountId'] or details['player']['accountId'] == third_acc_id['accountId']:
                game_duration = round(single_match['gameDuration']/60,2)
                if game_duration <= 0:
                    game_duration = 1;

                total_team_damage = 0
                total_team_kills = 0
                if details['participantId'] <= 5:
                    total_team_damage = single_match['participants'][0]['stats']['totalDamageDealtToChampions'] + single_match['participants'][1]['stats']['totalDamageDealtToChampions'] + single_match['participants'][2]['stats']['totalDamageDealtToChampions'] + single_match['participants'][3]['stats']['totalDamageDealtToChampions'] + single_match['participants'][4]['stats']['totalDamageDealtToChampions']
                    total_team_kills = single_match['participants'][0]['stats']['kills'] + single_match['participants'][1]['stats']['kills'] + single_match['participants'][2]['stats']['kills'] + single_match['participants'][3]['stats']['kills'] + single_match['participants'][4]['stats']['kills']
                else:
                    total_team_damage = single_match['participants'][5]['stats']['totalDamageDealtToChampions'] + single_match['participants'][6]['stats']['totalDamageDealtToChampions'] + single_match['participants'][7]['stats']['totalDamageDealtToChampions'] + single_match['participants'][8]['stats']['totalDamageDealtToChampions'] + single_match['participants'][9]['stats']['totalDamageDealtToChampions']
                    total_team_kills = single_match['participants'][5]['stats']['kills'] + single_match['participants'][6]['stats']['kills'] + single_match['participants'][7]['stats']['kills'] + single_match['participants'][8]['stats']['kills'] + single_match['participants'][9]['stats']['kills']


                if total_team_kills <= 0:
                    total_team_kills = 1

                if total_team_damage <= 0:
                    total_team_damage = 1

                divisor = 0
                if single_match['participants'][details['participantId'] - 1]['stats']['deaths'] == 0:
                    divisor = 1
                else:
                    divisor = single_match['participants'][details['participantId'] - 1]['stats']['deaths']

                stats_list += [{
                 "kills":single_match['participants'][details['participantId'] - 1]['stats']['kills'],
                 "total_CC_dealt":single_match['participants'][details['participantId'] - 1]['stats']['totalTimeCrowdControlDealt'],
                 "totalHeal":single_match['participants'][details['participantId'] - 1]['stats']['totalHeal'],
                 "CC":single_match['participants'][details['participantId'] - 1]['stats']['timeCCingOthers'],
                 "deaths":single_match['participants'][details['participantId'] - 1]['stats']['deaths'],
                 "assist":single_match['participants'][details['participantId'] - 1]['stats']['assists'],
                 "KDA":round((single_match['participants'][details['participantId'] - 1]['stats']['kills'] + single_match['participants'][details['participantId'] - 1]['stats']['assists']) / divisor ,2),
                 "vis_per_minute":round((single_match['participants'][details['participantId'] - 1]['stats']['visionScore']/game_duration),2),
                 "total_cs":single_match['participants'][details['participantId'] - 1]['stats']['totalMinionsKilled'],
                 "cs_per_min":round((single_match['participants'][details['participantId'] - 1]['stats']['totalMinionsKilled']/game_duration),2),
                 "damage_per_minute":int(round((single_match['participants'][details['participantId'] - 1]['stats']['totalDamageDealtToChampions']/game_duration),0)),
                 "dmg_percentage_per_team":int(round((single_match['participants'][details['participantId'] - 1]['stats']['totalDamageDealtToChampions']/total_team_damage)*100,0)),
                 "kill_participation":int(round(((single_match['participants'][details['participantId'] - 1]['stats']['kills'] + single_match['participants'][details['participantId'] - 1]['stats']['assists'])/total_team_kills)*100,0)),
                 }]



    delta_kda = 0
    delta_total_CC = 0
    delta_total_heal = 0
    delta_vis_per_minute = 0
    delta_total_cs = 0
    delta_cs_per_min = 0
    delta_dmg_per_minute = 0
    delta_dmg_percentage = 0
    delta_kill_participation = 0
    for single_stat in stats_list:

        delta_kda += single_stat['KDA']
        delta_total_CC += single_stat['total_CC_dealt']
        delta_total_heal += single_stat['totalHeal']
        delta_vis_per_minute += single_stat['vis_per_minute']
        delta_total_cs += single_stat['total_cs']
        delta_cs_per_min += single_stat['cs_per_min']
        delta_dmg_per_minute += single_stat['damage_per_minute']
        delta_dmg_percentage += single_stat['dmg_percentage_per_team']
        delta_kill_participation += single_stat['kill_participation']


    delta_stats = {
        "kda":(delta_kda/10),
        "CC":(delta_total_CC/10),
        "totalHeal":(delta_total_heal/10),
        "vis_per_min":(delta_vis_per_minute/10),
        "total_cs":(delta_total_cs/10),
        "cs_per_min":(delta_cs_per_min/10),
        "dmg_per_min":(delta_dmg_per_minute/10),
        "dmg_percentage":(delta_dmg_percentage/10),
        "kill_participation":(delta_kill_participation/10)
    }





    return delta_stats



def single_player_stats(user,position):

    user = user
    user_profile = Profile.objects.get(user=user)
    summoner_name = user_profile.summoner_name
    position = position


    player_acc_id_req = requests.get("https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+ summoner_name +"?api_key=" + DEV_API_KEY)
    player_acc_id = player_acc_id_req.json()
    player_matches_list = requests.get("https://eun1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + player_acc_id['accountId'] + "?endIndex=100&api_key=" + DEV_API_KEY)


    counter = 0
    game_id = []
    for game in player_matches_list.json()['matches']:
        if counter < 10:
            if game['queue'] == 420:
                if game['role'] == position or game['lane'] == position:
                    game_id.append(game['gameId'])
                    counter += 1






    stats_list = []
    match_details_list = []
    for details in game_id:

        match_details_request = requests.get("https://" + "eun1"+ ".api.riotgames.com/lol/match/v4/matches/" + str(details) + "?api_key=" + DEV_API_KEY)
        match_details_list += [match_details_request.json()]


    for single_match in match_details_list:
        for details in single_match['participantIdentities']:
            if details['player']['accountId'] == player_acc_id['accountId']:
                game_duration = round(single_match['gameDuration']/60,2)
                if game_duration <= 0:
                    game_duration = 1;

                total_team_damage = 0
                total_team_kills = 0
                if details['participantId'] <= 5:
                    total_team_damage = single_match['participants'][0]['stats']['totalDamageDealtToChampions'] + single_match['participants'][1]['stats']['totalDamageDealtToChampions'] + single_match['participants'][2]['stats']['totalDamageDealtToChampions'] + single_match['participants'][3]['stats']['totalDamageDealtToChampions'] + single_match['participants'][4]['stats']['totalDamageDealtToChampions']
                    total_team_kills = single_match['participants'][0]['stats']['kills'] + single_match['participants'][1]['stats']['kills'] + single_match['participants'][2]['stats']['kills'] + single_match['participants'][3]['stats']['kills'] + single_match['participants'][4]['stats']['kills']
                else:
                    total_team_damage = single_match['participants'][5]['stats']['totalDamageDealtToChampions'] + single_match['participants'][6]['stats']['totalDamageDealtToChampions'] + single_match['participants'][7]['stats']['totalDamageDealtToChampions'] + single_match['participants'][8]['stats']['totalDamageDealtToChampions'] + single_match['participants'][9]['stats']['totalDamageDealtToChampions']
                    total_team_kills = single_match['participants'][5]['stats']['kills'] + single_match['participants'][6]['stats']['kills'] + single_match['participants'][7]['stats']['kills'] + single_match['participants'][8]['stats']['kills'] + single_match['participants'][9]['stats']['kills']


                if total_team_kills <= 0:
                    total_team_kills = 1

                if total_team_damage <= 0:
                    total_team_damage = 1

                divisor = 0
                if single_match['participants'][details['participantId'] - 1]['stats']['deaths'] == 0:
                    divisor = 1
                else:
                    divisor = single_match['participants'][details['participantId'] - 1]['stats']['deaths']

                stats_list += [{
                 "kills":single_match['participants'][details['participantId'] - 1]['stats']['kills'],
                 "total_CC_dealt":single_match['participants'][details['participantId'] - 1]['stats']['totalTimeCrowdControlDealt'],
                 "totalHeal":single_match['participants'][details['participantId'] - 1]['stats']['totalHeal'],
                 "CC":single_match['participants'][details['participantId'] - 1]['stats']['timeCCingOthers'],
                 "deaths":single_match['participants'][details['participantId'] - 1]['stats']['deaths'],
                 "assist":single_match['participants'][details['participantId'] - 1]['stats']['assists'],
                 "KDA":round((single_match['participants'][details['participantId'] - 1]['stats']['kills'] + single_match['participants'][details['participantId'] - 1]['stats']['assists']) / divisor ,2),
                 "vis_per_minute":round((single_match['participants'][details['participantId'] - 1]['stats']['visionScore']/game_duration),2),
                 "total_cs":single_match['participants'][details['participantId'] - 1]['stats']['totalMinionsKilled'],
                 "cs_per_min":round((single_match['participants'][details['participantId'] - 1]['stats']['totalMinionsKilled']/game_duration),2),
                 "damage_per_minute":int(round((single_match['participants'][details['participantId'] - 1]['stats']['totalDamageDealtToChampions']/game_duration),0)),
                 "dmg_percentage_per_team":int(round((single_match['participants'][details['participantId'] - 1]['stats']['totalDamageDealtToChampions']/total_team_damage)*100,0)),
                 "kill_participation":int(round(((single_match['participants'][details['participantId'] - 1]['stats']['kills'] + single_match['participants'][details['participantId'] - 1]['stats']['assists'])/total_team_kills)*100,0)),
                 }]



    delta_kda = 0
    delta_total_CC = 0
    delta_total_heal = 0
    delta_vis_per_minute = 0
    delta_total_cs = 0
    delta_cs_per_min = 0
    delta_dmg_per_minute = 0
    delta_dmg_percentage = 0
    delta_kill_participation = 0
    for single_stat in stats_list:

        delta_kda += single_stat['KDA']
        delta_total_CC += single_stat['total_CC_dealt']
        delta_total_heal += single_stat['totalHeal']
        delta_vis_per_minute += single_stat['vis_per_minute']
        delta_total_cs += single_stat['total_cs']
        delta_cs_per_min += single_stat['cs_per_min']
        delta_dmg_per_minute += single_stat['damage_per_minute']
        delta_dmg_percentage += single_stat['dmg_percentage_per_team']
        delta_kill_participation += single_stat['kill_participation']


    delta_stats = {
        "kda":(delta_kda/10),
        "CC":(delta_total_CC/10),
        "totalHeal":(delta_total_heal/10),
        "vis_per_min":(delta_vis_per_minute/10),
        "total_cs":(delta_total_cs/10),
        "cs_per_min":(delta_cs_per_min/10),
        "dmg_per_min":(delta_dmg_per_minute/10),
        "dmg_percentage":(delta_dmg_percentage/10),
        "kill_participation":(delta_kill_participation/10)
    }


    return delta_stats








def skill_algorithm(stats,position):

    user_stats = stats
    global_stats = Global_Stats.objects.get(position=position)
    #weakness
    kda = False;
    cs_per_min = False;
    total_dmg_healed = False;
    CC_applied = False;
    dmg_per_min = False;
    vis_per_min = False;
    suggested_path = []
    print(user_stats['kda'])
    print(global_stats.kda)


    # Check for weakness

    if position == "DUO_CARRY" or position == "MID" or position == "TOP" or position == "JUNGLE":

        if position == "DUO_CARRY":
            position = "BOT"
        if position == "MID":
            position = "MID"
        if position == "TOP":
            position = "TOP"
        if position == "JUNGLE":
            position = "JUNGLE"


        kda_percentage = (user_stats['kda']/ global_stats.kda) * 100
        if kda_percentage < 75:
            kda = True;
            suggested_path.append(Course.objects.filter(tags__contains='kda'))
        else:
            kda = False;

        cs_per_min_percentage = (user_stats['cs_per_min']/global_stats.cs_per_min) * 100

        if cs_per_min_percentage < 80:
            cs_per_min = True
            suggested_path.append(Course.objects.filter(tags__contains='cs'))

        else:
            cs_per_min = False

        dmg_per_min_percentage = (user_stats['dmg_per_min']/global_stats.dmg_per_min) * 100


        if dmg_per_min_percentage < 80:
            dmg_per_min = True
            suggested_path.append(Course.objects.filter(tags__contains='dmg'))
        else:
            dmg_per_min = False

        vis_per_min_percentage = (user_stats['vis_per_min']/global_stats.vis_per_min) * 100
        if vis_per_min_percentage < 90:
            vis_per_min = True
            suggested_path.append(Course.objects.filter(tags__contains='vis'))

        else:
            vis_per_min = False




        suggested_path.append(Course.objects.filter(role=position))
        results = {"kda":kda,
        "kda_percentage": kda_percentage,
         "cs_per_min":cs_per_min,
         "cs_per_min_percentage": cs_per_min_percentage,
         "dmg_per_min":dmg_per_min,
         "dmg_per_min_percentage":dmg_per_min_percentage,
         "vis_per_min":vis_per_min,
         "vis_per_min_percentage":vis_per_min_percentage,
         "suggested_path": suggested_path}

        return results

    else:

        kda_percentage = (user_stats['kda']/ global_stats.kda) * 100
        if kda_percentage < 75:
            kda = True;
            suggested_path.append(Course.objects.filter(tags__contains='kda'))

        else:
            kda = False;

        total_dmg_healed_percentage = (user_stats['totalHeal']/global_stats.total_dmg_healed) * 100
        if total_dmg_healed_percentage < 80:
            total_dmg_healed = True
            suggested_path.append(Course.objects.filter(tags__contains='heal'))
        else:
            total_dmg_healed = False

        CC_applied_percentage = (user_stats['CC']/global_stats.CC_applied) * 100
        if CC_applied_percentage < 80:
            CC_applied = True
            suggested_path.append(Course.objects.filter(tags__contains='cc'))
        else:
            CC_applied = False

        vis_per_min_percentage = (user_stats['vis_per_min']/global_stats.vis_per_min) * 100
        if vis_per_min_percentage < 90:
            vis_per_min = True
            suggested_path.append(Course.objects.filter(tags__contains='vis'))
        else:
            vis_per_min = False


        results = {"kda":kda,
        "kda_percentage": kda_percentage,
         "total_dmg_healed":total_dmg_healed,
         "total_dmg_healed_percentage": total_dmg_healed,
         "CC_applied":CC_applied,
         "CC_applied_percentage":CC_applied_percentage,
         "vis_per_min":vis_per_min,
         "vis_per_min_percentage":vis_per_min_percentage,
         "suggested_path": suggested_path}

        return results
