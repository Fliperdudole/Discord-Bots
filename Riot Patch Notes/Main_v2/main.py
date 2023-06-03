#Programmer: Brandon Sandoval
#Date Started: 6/3/23
#Purpose: This main file will have variables passed in from other files, depending on the game, and 
# check if the URL has been updated, if the URL is valid then it will post them to a discord server channel 
# and notify all users with a certain role name



# import libraries
import os
import discord
import requests
import asyncio
from datetime import datetime, timedelta

# These are the helper files
import responses     # Will be used to create variables based off responses of user's
import LeaguePN      # This file will have the variables needed for League Patch notes
import ValorantPN    # This file will have the variables needed for Valorant Patch notes


# Discord bot token, using OS environment variables
TOKEN = os.getenv('RIOT_PN_TOKEN') 

# Channel ID set to none but will have a default and can be set
CHANNEL_ID = None













async def on_ready():
    print("Patch Notes Bot is online!")

    if CHANNEL_ID is None:
        CHANNEL_ID = client.guilds[0].text_channels[0].id
        print('Default Channel Set:', CHANNEL_ID)
































































# Run the bot
client.run(TOKEN)