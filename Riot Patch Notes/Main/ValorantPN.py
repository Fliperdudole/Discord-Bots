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
LAST_PATCH_FILE = 'last_valorant_patch.txt'

# Number of tries done to check patch
patch_tries = 0

# Variable to check current patch to prevent recurring updates
current_patch = saveVar.read_last_patch(LAST_PATCH_FILE)

# Current season/act
current_season = 6

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

# Used as a bool flag
checking_patch = True


# This function, using the requests module, checks the website and sends in the notfication channel
async def check_Valorant_Patch(CHANNEL_ID, MAX_PATCH, client):
    global current_patch, patch_tries, checking_patch

    # Pads the number
    pad_num = await pad_patch_num(current_patch)

    url = URL.format(current_season,pad_num)

    # Request the website through HTML
    response = requests.get(url)

    # Check if the page exists (returns 200 status code)
    if response.status_code == 200:

        leagueMessage= f"Patch Notes {current_season}.{pad_num} is out!\n{url}"

        channel = client.get_channel(CHANNEL_ID)
        
        # if the role exists then send a message mentioning the role
        try:
            role = discord.utils.get(channel.guild.roles, name=role_name)
            if role:
                message = f"{role.mention}\n{leagueMessage} "
                
            await channel.send(message)
            
        except discord.Forbidden:# Bot doesnt have the right permissions in the server to send messages
            print("The bot doesn't have permission to send messages in the channel.")
            return
        
        current_patch += 1

        # Save the last patch in a text file
        saveVar.write_last_patch(LAST_PATCH_FILE,current_patch)

    else:

        # Prints in the terminal that no update was found
        print(f"No update found for patch {current_season}.{current_patch}.")
        
        current_patch +=1
        saveVar.write_last_patch(LAST_PATCH_FILE,current_patch)
        
        patch_tries +=1

        # Check if the current patch exceeds a limit as Riot likes to jump patches at times
        if patch_tries > MAX_PATCH:
            print("Reached the maximum patch limit.")
            
            current_patch -= 3
            saveVar.write_last_patch(LAST_PATCH_FILE,current_patch)
            print(f"Reseting patch back to last successful patch {current_season}.{current_patch}")
            
            checking_patch=False
            return 
