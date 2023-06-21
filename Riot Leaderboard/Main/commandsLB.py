# Import libraries
import os
import discord
from discord.ext import commands
from tabulate import tabulate

import requests

RIOT_API = "RGAPI-b8a2896e-8bd0-4d4f-bdb3-f625a8b9b67a"


@commands.command()
async def track(ctx, *,account_name):
    account_name = account_name.strip()
    url_account_name= account_name.replace(" ", "%20")
    

    try:
        account_puuid, summoner_id = await getPlayer_PUUID(ctx, url_account_name)
        winrate,kda,total_damage = await getPlayer_Match_Data(ctx, account_puuid)
        user_rank, user_lp = await getSummoner_Data(ctx, summoner_id)
        await printSummoner_Data(ctx, account_name, user_rank, user_lp, winrate ,kda, total_damage)

    
    
    
    
    
    
    
    except requests.exceptions.HTTPError as err:
        error_data = err.response.json().get("status")
        error_message = error_data.get("message")
        error_code = error_data.get("status_code")
        await ctx.send(f'Error code {error_code}: {error_message}. Contact Fliperdudole for further questions')
    except requests.exceptions.RequestException as err:
        await ctx.send("An error occurred during the request.")
    


async def getPlayer_PUUID(ctx, url_account_name ):   
   

    base_url="https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    
    combined_url = base_url + url_account_name
    api_key = '?api_key=' + RIOT_API

    api_url = combined_url + api_key

    #await ctx.send(f'API URL: {api_url}')

    

    
    response = requests.get(api_url)
    response.raise_for_status()  # Raises an exception if the response contains an error status code
    # Process the response if no error occurred
    
    
    account_info = response.json()
    #await ctx.send(f'Account Info: {account_info}')
    account_puuid = account_info['puuid']
    #await ctx.send(f'Account PUUID: {account_puuid}')
    summoner_id = account_info['id']
    
    return account_puuid, summoner_id
        
        

async def getPlayer_Match_Data(ctx, puuid):
    #print(puuid)
    match_type = "type=ranked"
    base_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?{match_type}&start=0&count=20"
    api_key_v1 = '&api_key=' +  RIOT_API

    api_url = base_url + api_key_v1
    #await ctx.send(f'MATCH ID API URL: {api_url}')
    response = requests.get(api_url)
    match_ids = response.json()
    
    kill_count = 0
    death_count = 0
    assist_count = 0
    
    kda_count = 0
    win_count = []
    total_damage_count = 0
    past_games = 20
    
    for x in range(past_games):
        recent_match_ID = match_ids[x]
        #await ctx.send(f'Recent Match ID: {recent_match_ID}')
        
        api_key_v2 = '?api_key=' +  RIOT_API

        match_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{recent_match_ID}" + api_key_v2

        match_response = requests.get(match_url)
        match_data = match_response.json()

        #await ctx.send(f'MATCH JSON URL: {match_url}')
        
        # A list of all the participants puuids
        participants = match_data['metadata']['participants']
        # Now, find where in the data our players puuid is found
        player_index = participants.index(puuid)

        player_data = match_data['info']['participants'][player_index]

        #summoner = player_data['summonerName']
        k = player_data['kills']
        d = player_data['deaths']
        a = player_data['assists']
        kda = round(float(player_data['challenges']['kda']), 2)
        win = bool(player_data['win'])
        total_damage = int(player_data['totalDamageDealtToChampions'])
        #print(f"KDA: {kda} - Win?: {win}")
        
        kill_count += k
        death_count += d
        assist_count += a


        kda_count += kda
        win_count.append(win)
        total_damage_count += total_damage
    
    
    kda = (kill_count + assist_count) / death_count
    win = (sum(win_count) / past_games) * 100
    
    
    
    
    

    kills = kill_count / past_games
    deaths = death_count / past_games
    assists = assist_count / past_games

    print(f"Total | Kills:{kill_count} Deaths: {death_count} Assists: {assist_count}")
    print(f"Average | Kills:{kills} Deaths: {deaths} Assists: {assists} KDA: {kda:.2f}")

    

    table = [
        ["Total", f"Kills: {kill_count}", f"Deaths: {death_count}", f"Assists: {assist_count}"],
        ["Average", f"Kills: {kills}", f"Deaths: {deaths}", f"Assists: {assists}", f"KDA: {kda:.2f}"]
    ]

    formatted_table = f'```\n{tabulate(table, headers=["", "Kills", "Deaths", "Assists", "KDA"], tablefmt="presto")}```'

    await ctx.send(formatted_table)




    return win,kda,total_damage_count

    
  

    

async def getSummoner_Data(ctx, summoner_id):
    base_url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    api_key = '?api_key=' +  RIOT_API
    api_url = base_url + api_key

    response = requests.get(api_url)
    user_data = response.json()
    #print(user_data) 
    user_tier = user_data[0]['tier']
    user_division = user_data[0]['rank']

    
    user_rank = user_tier +" "+ user_division
    user_lp = user_data[0]['leaguePoints']
    return user_rank, user_lp





async def printSummoner_Data(ctx, account_name, user_rank, user_lp, winrate, kda, total_damage):
    winrate_formatted = f"{winrate}%"
    kda_formatted = f"{kda:.2f}"
    total_damage_formatted = f"{total_damage/1000:.2f}k"
    



    table = [
        [account_name, user_rank, winrate_formatted, kda_formatted, total_damage_formatted]
    ]

    formatted_table = f'```\n{tabulate(table, headers=["Name", "Rank", "Winrate", "KDA", "Total Damage"])}```'
    await ctx.send(formatted_table)

    








async def setup(bot):
    bot.add_command(track)    