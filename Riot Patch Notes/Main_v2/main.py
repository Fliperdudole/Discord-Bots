#Programmer: Brandon Sandoval
#Date Started: 6/3/23
#Purpose: This main file will have variables passed in from other files, depending on the game, and 
# check if the URL has been updated, if the URL is valid then it will post them to a discord server channel 
# and notify all users with a certain role name



# import libraries
import os
import requests
import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

# These are the helper files
import commandsPN      # This file contains all commands of the program 
import LeaguePN      # This file will have the variables needed for League Patch notes
import ValorantPN    # This file will have the variables needed for Valorant Patch notes
import saveVar       # This file will save the variables in case the bot goes down

# Initialize the Discord client
#intents = discord.Intents.default()

client = commands.Bot(command_prefix='!', intents=discord.Intents.all(),)



# Discord bot token, using OS environment variables
TOKEN = os.getenv('RIOT_PN_TOKEN') 

# Channel ID set to none but will have a default and can be set
CHANNEL_ID = None

# Max number of future Patches to check
MAX_PATCH = 2



async def check_League_Patch():

    url = LeaguePN.URL.format(LeaguePN.current_season,LeaguePN.current_patch)
    
    response = requests.get(url)

    # Check if the page exists (returns 200 status code)
    if response.status_code == 200:

        leagueMessage= f"Patch Notes {LeaguePN.current_season}.{LeaguePN.current_patch} is out!\n{url}"

        channel = client.get_channel(CHANNEL_ID)
        
        try:
            role = discord.utils.get(channel.guild.roles, name=LeaguePN.role_name)
            if role:
                message = f"{role.mention}\n{leagueMessage} "
                
            await channel.send(message)
        except discord.Forbidden:
            print("The bot doesn't have permission to send messages in the channel.")
            return
        
        LeaguePN.current_patch += 1
        saveVar.write_last_patch(LeaguePN.LAST_PATCH_FILE,LeaguePN.current_patch)

    else:

        print(f"No update found for patch {LeaguePN.current_season}.{LeaguePN.current_patch}.")
        
        LeaguePN.current_patch +=1
        saveVar.write_last_patch(LeaguePN.LAST_PATCH_FILE,LeaguePN.current_patch)
        
        LeaguePN.patch_tries +=1

        # Check if the current patch exceeds a limit
        if LeaguePN.patch_tries > MAX_PATCH:
            print("Reached the maximum patch limit.")
            
            LeaguePN.current_patch -= 3
            saveVar.write_last_patch(LeaguePN.LAST_PATCH_FILE,LeaguePN.current_patch)
            print(f"Reseting patch back to last successful patch {LeaguePN.current_season}.{LeaguePN.current_patch}")
            
            LeaguePN.checking_patch=False
            return 

    





async def check_Valorant_Patch():
    
    pad_num = await ValorantPN.pad_patch_num(ValorantPN.current_patch)

    url = ValorantPN.URL.format(ValorantPN.current_season,pad_num)
    #print(url)
    response = requests.get(url)

    # Check if the page exists (returns 200 status code)
    if response.status_code == 200:

        leagueMessage= f"Patch Notes {ValorantPN.current_season}.{pad_num} is out!\n{url}"

        channel = client.get_channel(CHANNEL_ID)
        
        try:
            role = discord.utils.get(channel.guild.roles, name=ValorantPN.role_name)
            if role:
                message = f"{role.mention}\n{leagueMessage} "
                
            await channel.send(message)
        except discord.Forbidden:
            print("The bot doesn't have permission to send messages in the channel.")
            return
        
        ValorantPN.current_patch += 1
        saveVar.write_last_patch(ValorantPN.LAST_PATCH_FILE,ValorantPN.current_patch)

    else:

        print(f"No update found for patch {ValorantPN.current_season}.{ValorantPN.current_patch}.")
        
        ValorantPN.current_patch +=1
        saveVar.write_last_patch(ValorantPN.LAST_PATCH_FILE,ValorantPN.current_patch)
        
        ValorantPN.patch_tries +=1

        # Check if the current patch exceeds a limit
        if ValorantPN.patch_tries > MAX_PATCH:
            print("Reached the maximum patch limit.")
            
            ValorantPN.current_patch -= 3
            saveVar.write_last_patch(ValorantPN.LAST_PATCH_FILE,ValorantPN.current_patch)
            print(f"Reseting patch back to last successful patch {ValorantPN.current_season}.{ValorantPN.current_patch}")
            
            ValorantPN.checking_patch=False
            return 







@client.event
async def on_ready():
    global CHANNEL_ID
    print("Patch Notes Bot is online!")

    CHANNEL_ID = saveVar.load_default_channel()


    await client.load_extension('commandsPN')
    
    if CHANNEL_ID is None:                                   # Checks if default channel isn't set
        CHANNEL_ID = client.guilds[0].text_channels[0].id    # Sets Channel to channel that it joined to
        print("Default Channel ID Set:", CHANNEL_ID)
        
        saveVar.save_default_channel(CHANNEL_ID)             # Saves Channel ID in default_channel.txt
    else:
        print("Channel ID is set to",CHANNEL_ID)             # Shows Channel ID


    while LeaguePN.checking_patch:
        
        await check_League_Patch()

    while ValorantPN.checking_patch:
        await check_Valorant_Patch()









# Run the bot
client.run(TOKEN)