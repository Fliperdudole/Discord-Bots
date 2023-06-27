#Programmer: Brandon Sandoval
#Date Started: 6/3/23
#Purpose: This helper file will contain all the necessary variables/functions in order 
#         for the main file to work for the specified game



# Import libraries
import saveVar
import discord
import requests



# URL for the Valorant Patch Notes website
URL = 'https://playvalorant.com/en-us/news/game-updates/valorant-patch-notes-{}-{}/'

# File to store the last patch number
LAST_PATCH_FILE = './DATA/last_valorant_patch.txt'


# Variable to check current patch to prevent recurring updates
current_patch = saveVar.read_last_patch(LAST_PATCH_FILE)

# Current season/act
current_season = 7

# Get the role name to mention
role_name = 'Valorant-Patch-Notes' 



# This function pads the num 1-9
async def pad_patch_num(num):
     # Nums 1-9 have to have a padded 0 in order for the link to work (ex.1 = 01)
    if num >= 1 and num <=9:
        padded_number = str(num).zfill(2)

    else:
        padded_number = str(num)
    return padded_number


# This function, using the requests module, checks the website and sends in the notfication channel
async def check_Valorant_Patch(notif_channel, is_done, client):
    global current_patch

    for patch_attempt in range(3):
            #print(f"\nattempt: {patch_attempt}")

            temp_patch = current_patch + patch_attempt
            #print(f"temp:{temp_patch}")
            pad_num = await pad_patch_num(temp_patch)
            #print(f"pad num: {pad_num}")
            url = URL.format(current_season,pad_num)
            #print(f"url: {url}")
            response = requests.get(url)

            if response.status_code == 200:

                leagueMessage= f"Patch Notes {current_season}.{pad_num} is out!\n{url}"
                 
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


