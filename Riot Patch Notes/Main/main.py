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
MAX_PATCH = 1



prev_prompt = ''

async def create_notify_role():
    for guild in client.guilds:
        role_names = [ValorantPN.role_name, LeaguePN.role_name]  # Array for role names

        for role in role_names:
            # Check if the role already exists
            existing_role = discord.utils.get(guild.roles, name=role)

            if existing_role is None:  # Role doesn't exist, create it
                # hoist = shown on the server, mentionable = mentionable in server
                new_role = await guild.create_role(name=role, hoist=True, mentionable=True)
                print(f"Created role '{new_role.name}' in server '{guild.name}'")
            else:
                print(f"Role '{existing_role.name}' already exists in server '{guild.name}'")




# Function to check if the day is the day that Patch Notes usually come out for their respective game
async def schedule_timers(notif_channel):
    tuesday_checks = 0
    tuesday_done = False
    thursday_checks = 0
    thursday_done = False

    global prev_prompt

    while True:
        # Get the current weekday (Monday is 0 and Sunday is 6)
        current_day = datetime.today().weekday()

        if current_day == 1 and tuesday_checks < MAX_PATCH:
            # Tuesday at 1 PM
            target_time = datetime.now().replace(hour=12, minute=0, second=0)
            wait_time = (target_time - datetime.now()).total_seconds()

            if wait_time > 0:
                await asyncio.sleep(wait_time)
            print(f"\ntuesday checks: {tuesday_checks}")
            await ValorantPN.check_Valorant_Patch(notif_channel, tuesday_done, client)
            tuesday_done=False
            await LeaguePN.check_League_Patch(notif_channel, MAX_PATCH, client)
            tuesday_checks += 1

        elif current_day == 1 and thursday_checks < MAX_PATCH:
            # Thursday at 1 PM
            target_time = datetime.now().replace(hour=17, minute=44, second=0)
            wait_time = (target_time - datetime.now()).total_seconds()

            if wait_time > 0:
                await asyncio.sleep(wait_time)

            await ValorantPN.check_Valorant_Patch(notif_channel, thursday_done, client)
            thursday_done = False
            await LeaguePN.check_League_Patch(notif_channel, thursday_done, client)
            thursday_checks += 1

        # Reset counters on Monday
        if current_day == 0:
            tuesday_checks = 0
            tuesday_done = False

            thursday_checks = 0
            thursday_done = False


        await asyncio.sleep(10 )  # Wait 10 minutes before checking again
        current_time = datetime.now().strftime("%H:%M:%S")  # Format current time as HH:MM:SS
        print(prev_prompt, end="\r")
        new_line = f"Bot was \033[92monline\033[0m as of: {current_time}"
        print(new_line, end="\r")
        prev_prompt = new_line



@client.event
async def on_ready():
    global CHANNEL_ID
    print("Patch Notes Bot is \033[92monline\033[0m")  # puts the word "online" in green!

    print("Bot is connected to the following servers:")
    for guild in client.guilds:
        print(guild.name)
    print()

    notif_channel = saveVar.load_default_channels()

    # Loads commands from file "commandsPN.py"
    await client.load_extension('commandsPN')

    await create_notify_role()

    for guild in client.guilds:
        guild_id = str(guild.id)
        channel_id = notif_channel.get(guild_id)
        if channel_id is None:
            # Get the first available text channel in the guild
            channel = discord.utils.get(guild.text_channels)
            if channel is not None:
                notif_channel[guild_id] = channel.id
                saveVar.update_default_channel(guild_id, channel.id, notif_channel)
                print(f"Default Channel ID Set to: {channel.name} (Server: {guild.name})")
            else:
                print(f"No available text channels in the server: {guild.name}")

    await schedule_timers(notif_channel)








# Run the bot
client.run(TOKEN)