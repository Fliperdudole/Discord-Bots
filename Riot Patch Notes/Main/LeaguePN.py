#Programmer: Brandon Sandoval
#Date Started: 6/3/23
#Purpose: This helper file will contain all the necessary variables/functions in order 
#         for the main file to work for the specified game


# Import libraries
import saveVar
import discord
import requests


# URL for the League Patch Notes website
URL = 'https://www.leagueoflegends.com/en-us/news/game-updates/patch-{}-{}-notes/'
 
# File to store the last patch number
LAST_PATCH_FILE = 'last_league_patch.txt'

# Variable to check current patch to prevent recurring updates 
current_patch = saveVar.read_last_patch(LAST_PATCH_FILE)

# Current season/act
current_season = 13

# Get the role name to mention
role_name = 'League-Patch-Notes'

# amended League url
league_url = URL.format(current_season, current_patch)

# League response code
league_response = requests.get(league_url)



# This function, using the requests module, checks the website and sends in the notfication channel
async def check_League_Patch(notif_channel, is_done, client):
    global current_patch


    for patch_attempt in range(3):
                #print(f"\nattempt: {patch_attempt}")

                temp_patch = current_patch + patch_attempt
                #print(f"temp:{temp_patch}")
                url = URL.format(current_season,temp_patch)
                #print(f"url: {url}")
                response = requests.get(url)

                if response.status_code == 200:

                    leagueMessage= f"Patch Notes {current_season}.{temp_patch} is out!\n{url}"
                    
                    for server_id, channel_id in notif_channel.items():
                        channel = client.get_guild(int(server_id)).get_channel(int(channel_id))

                        # if the role exists then send a message mentioning the role
                        try:
                            role = discord.utils.get(channel.guild.roles, name=role_name)
                            if role:
                                message = f"{role.mention}\n{leagueMessage} "
                            await channel.send(message)
                        except discord.Forbidden:
                            print("The bot doesn't have permission to send messages in the channel.")
                    #print(f"before: {current_patch}")
                    current_patch = temp_patch + 1
                    saveVar.write_last_patch(LAST_PATCH_FILE,current_patch)
                    #print(f"after: {current_patch}")
                    is_done = True
                    return is_done 
                    

                else:
                    print(f"No update found for patch {current_season}.{temp_patch}.")
    if response.status_code != 200:
        temp_patch = current_patch
        saveVar.write_last_patch(LAST_PATCH_FILE,temp_patch)

        print("Reached the maximum patch limit.")
        print(f"Reseting patch back to last successful patch {current_season}.{temp_patch}")
        return




