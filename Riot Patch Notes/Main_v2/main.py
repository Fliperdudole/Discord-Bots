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
        
        await LeaguePN.check_League_Patch(CHANNEL_ID, MAX_PATCH, client)

    while ValorantPN.checking_patch:
        await ValorantPN.check_Valorant_Patch(CHANNEL_ID, MAX_PATCH, client)









# Run the bot
client.run(TOKEN)