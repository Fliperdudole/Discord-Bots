#Programmer: Brandon Sandoval
#Date Started: 6/19/23
#Date Finished: TBA
# Purpose: This main file will have variables passed in from other files, depending on the game, and 
# check if the URL has been updated, if the URL is valid then it will post them to a discord server channel 
# and notify all users with a certain role name

# Import libraries
import os
import discord
from discord.ext import commands
import asyncio
from datetime import datetime

client = commands.Bot(command_prefix='!', intents=discord.Intents.all(),)


# Discord bot token, using OS environment variables
TOKEN = os.getenv('RIOT_LB_TOKEN') 
