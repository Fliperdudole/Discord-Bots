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

start_time = datetime.now()  # Set the program start time

prev_prompt = ''



async def check_and_print_roles(guild, role_names):
    role_status = {}

    for role_name in role_names:
        existing_role = discord.utils.get(guild.roles, name=role_name)
        role_status[role_name] = existing_role is not None

    return role_status

# Usage example in your code:
async def create_notify_role():
    print("\n\033[33mRole Check:\033[0m")
    for guild in client.guilds:
        role_names = [ValorantPN.role_name, LeaguePN.role_name]  # Array for role names

        # Check if both roles exist in the server
        role_status = await check_and_print_roles(guild, role_names)

        if role_status[ValorantPN.role_name] and role_status[LeaguePN.role_name]:
            print(f"✅ Both roles ({ValorantPN.role_name} and {LeaguePN.role_name}) already exist in server '{guild.name}'")
        else:
            for role_name, exists in role_status.items():
                if exists:
                    print(f"✅ Role {role_name} already exists in server '{guild.name}'")
                else:
                    # Role doesn't exist, create it
                    new_role = await guild.create_role(name=role_name, hoist=True, mentionable=True)
                    print(f"✅ Created role {new_role.name} in server '{guild.name}'")



async def check_server_status():
    current_day = datetime.today().weekday()
    current_time = datetime.now().strftime("%I:%M:%S %p")  # Use %I:%M:%S %p for 12-hour format
    runtime = datetime.now() - start_time

    if current_day in (1, 3):  # Tuesday or Thursday
        server_status = "\033[92m online\033[0m"
    else:
        server_status = "\033[91m offline\033[0m"

    new_line = f"\033[33mServer Status:\033[0m{server_status} ({current_time}) - Runtime: {runtime.total_seconds():.2f} seconds"
    return new_line






# Function to check if the day is the day that Patch Notes usually come out for their respective game
async def schedule_timers(notif_channel):
    tuesday_checks = 0
    tuesday_done = False
    thursday_checks = 0
    thursday_done = False

    global prev_prompt

    while True:
        current_day = datetime.today().weekday()
        current_time = datetime.now().strftime("%H:%M:%S")

        if current_day in (1, 3):  # Tuesday or Thursday
            # Tuesday at 1 PM
            if current_day == 1 and tuesday_checks < MAX_PATCH:
                
                target_time = datetime.now().replace(hour=11, minute=18, second=0)
                wait_time = (target_time - datetime.now()).total_seconds()

                if wait_time <= 0:
                    print("\n\033[33mGame Check:\033[0m")
                    await ValorantPN.check_Valorant_Patch(notif_channel, tuesday_done, client)
                    print(f"\033[31mValorant\033[0m Tuesday check is done\n")
                    tuesday_done = False
                    await LeaguePN.check_League_Patch(notif_channel, MAX_PATCH, client)
                    print(f"\033[34mLeague Of Legends\033[0m Tuesday check is done\n")
                    tuesday_checks += 1

            # Thursday at 1 PM
            elif current_day == 3 and thursday_checks < MAX_PATCH:
                target_time = datetime.now().replace(hour=13, minute=0, second=0)
                wait_time = (target_time - datetime.now()).total_seconds()

                if wait_time <= 0:
                    print("\n\033[33mGame Check:\033[0m")
                    await ValorantPN.check_Valorant_Patch(notif_channel, thursday_done, client)
                    print(f"\033[31mValorant\033[0m Thursday check is done\n")
                    thursday_done = False
                    await LeaguePN.check_League_Patch(notif_channel, thursday_done, client)
                    print(f"\033[34mLeague Of Legends\033[0m Thursday check is done\n")
                    thursday_checks += 1

        status = await check_server_status()
        print(status, end="\r")
        prev_prompt = status

        await asyncio.sleep(10)





@client.event
async def on_ready():
    global CHANNEL_ID

    server_count = len(client.guilds)
    total_members = sum(guild.member_count for guild in client.guilds)

    print(f"\033[33mServer List ({server_count} Servers, {total_members} Members):\033[0m")

    for guild in client.guilds:
        print(f"{guild.name} ({guild.member_count} Members)")

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