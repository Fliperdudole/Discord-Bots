#Programmer: Brandon Sandoval
#Date Started: 6/3/23
#Purpose: This main file will have variables passed in from other files, depending on the game, and 
# check if the URL has been updated, if the URL is valid then it will post them to a discord server channel 
# and notify all users with a certain role name



# Import libraries
import os
import discord
from discord.ext import commands
import asyncio
from datetime import datetime

# These are the helper files
#import commandsPN   # This file contains all commands of the program 
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

async def create_notify_role():
    guild = client.guilds[0]  # Change this to the desired guild or fetch it by ID
    role_names = [ValorantPN.role_name,LeaguePN.role_name] # Array for role names
   
    
    for role in role_names:

        # Check if the role already exists
        create_role = discord.utils.get(guild.roles, name=role)
        
        if create_role is None: # Role doesn't exist, create it
            # hoist = shown on the server, mentionable = mentionable in server
            role = await guild.create_role(name=role, hoist=True, mentionable=True)
            print(f"Created role: {role.name}")
        else:
            print(f"Role already exists: {role}")







# Function to check if the day is the day that Patch Notes usually come out for their respective game
async def schedule_timers():
    tuesday_checks = 0
    thursday_checks = 0

    while True:
        # Get the current weekday (Monday is 0 and Sunday is 6)
        current_day = datetime.today().weekday()

        if current_day == 1 and tuesday_checks <= MAX_PATCH:
            # Tuesday at 1 PM
            target_time = datetime.now().replace(hour=13, minute=0, second=0)
            wait_time = (target_time - datetime.now()).total_seconds()

            if wait_time > 0:
                await asyncio.sleep(wait_time)

            await ValorantPN.check_Valorant_Patch(CHANNEL_ID, MAX_PATCH, client)
            tuesday_checks += 1

        elif current_day == 3 and thursday_checks <= MAX_PATCH:
            # Thursday at 1 PM
            target_time = datetime.now().replace(hour=13, minute=0, second=0)
            wait_time = (target_time - datetime.now()).total_seconds()

            if wait_time > 0:
                await asyncio.sleep(wait_time)

            await LeaguePN.check_League_Patch(CHANNEL_ID, MAX_PATCH, client)
            thursday_checks += 1

        # Reset counters on Monday
        if current_day == 0:
            tuesday_checks = 0
            thursday_checks = 0

        await asyncio.sleep(600)  # Wait 10 minutes before checking again
        current_time = datetime.now().strftime("%H:%M:%S")  # Format current time as HH:MM:SS
        print("Bot was \033[92monline\033[0m as of:", current_time)



@client.event
async def on_ready():
    global CHANNEL_ID
    print("Patch Notes Bot is \033[92monline\033[0m") # puts the word "online" in green!


    # Saves the Channel ID in a file
    CHANNEL_ID = saveVar.load_default_channel()

    # Loads commands from file "commandsPN.py"
    await client.load_extension('commandsPN')

    await create_notify_role()
    
    if CHANNEL_ID is None:                                   # Checks if default channel isn't set
        guild = client.guilds[0]
        channel = guild.text_channels[0]
        CHANNEL_ID = channel.id                              # Sets Channel to channel that it joined to
        print(f"Default Channel ID Set to: {channel.name} (Server: {guild.name})\n")
        
        saveVar.save_default_channel(CHANNEL_ID)             # Saves Channel ID in default_channel.txt
    else:
        guild = client.guilds[0]  
        channel = guild.get_channel(CHANNEL_ID)
        print(f"Notification Channel set to: {channel.name} (Server: {guild.name})\n")             # Shows Channel ID

    await schedule_timers()








# Run the bot
client.run(TOKEN)