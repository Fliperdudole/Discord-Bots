import os
import requests
import discord
import asyncio
from datetime import datetime, timedelta

# Max number of times Patch can be checked
MAX_PATCH = 2

# Discord bot token
TOKEN = 'MTExNDAzMTQ2NTIwMjcyNDg5NQ.GJ_8nc.wRuejjtz7b3DQGyZOeDfLbR-Qr-b-RNMHwBluY'

# Channel ID where the notifications will be sent
CHANNEL_ID = 805998967589830730

# URL of the website to check for updates
URL_TEMPLATE = 'https://www.leagueoflegends.com/en-us/news/game-updates/patch-{}-{}-notes/'

# File to store the last patch number
LAST_PATCH_FILE = 'last_league_patch.txt'



# Function to read the last patch number from the file
def read_last_patch():
    if os.path.exists(LAST_PATCH_FILE):
        with open(LAST_PATCH_FILE, 'r') as file:
            try:
                current_patch = int(file.read())
                return current_patch
            except ValueError:
                pass
    return 1

# Function to write the current patch number to the file
def write_last_patch(patch_number):
    with open(LAST_PATCH_FILE, 'w') as file:
        file.write(str(patch_number))


current_patch = read_last_patch()


# Season number 
current_season = 13


patch_tries = 0




# Function to check for updates and send notifications
async def check_for_updates():
    global current_patch, patch_tries
    
    # Generate the URL for the current patch
    url = URL_TEMPLATE.format(current_season,current_patch)
    
    
    # Fetch the webpage
    response = requests.get(url)

    # Check if the page exists (returns 200 status code)
    if response.status_code == 200:
        # Get the role name to mention
        role_name = 'League-Patch-Notes'  
        
        message = f"Patch Notes {current_season}.{current_patch} is out!\n{url}"
        channel = client.get_channel(CHANNEL_ID)
        
        if channel is None:
            print("The channel was not found.")
            return
        
        try:
            role = discord.utils.get(channel.guild.roles, name=role_name)
            if role:
                message = f"{role.mention}\n{message} "
                
            await channel.send(message)
        except discord.Forbidden:
            print("The bot doesn't have permission to send messages in the channel.")
            return
        
        # Increment the current patch number
        current_patch += 1
        write_last_patch(current_patch)
    else:
        

        
        print(f"No update found for patch {current_season}.{current_patch}.")
        current_patch += 1
        patch_tries += 1
        
        # Check if the current patch exceeds a limit
        if patch_tries > MAX_PATCH:
            print("Reached the maximum patch limit.")
            
            current_patch -= 3
            write_last_patch(current_patch)
            print(f"Reseting patch back to last successful patch {current_season}.{current_patch}")
            await waitThurs()
            return

            
        
            

# Initialize the Discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)


# Event triggered when the bot has connected to Discord
@client.event
async def on_ready():
    print('Bot connected to Discord.')
    
    while True:
        await check_for_updates()
        await asyncio.sleep(2)  # Wait for 2 seconds before checking again


# Get the current day of the week and waits till 7am
async def waitThurs():
    print("Waiting for Thursday at 7am")
    today = datetime.now().date()
    weekday = today.weekday()  # Monday is 0 and Sunday is 6

    # Calculate the days remaining until Thursday (weekday 3)
    days_until_thursday = (3 - weekday) % 7  # Adjusted to Thursday

    # Calculate the time until Thursday at 7 AM
    next_thursday = today + timedelta(days=days_until_thursday)
    next_thursday_7am = datetime.combine(next_thursday, datetime.min.time()) + timedelta(hours=7)  # Thursday at 7 AM
    time_until_thursday_7am = next_thursday_7am - datetime.now()

    # Schedule the check_for_updates() function to run on the next Thursday at 7 AM
    await asyncio.sleep(time_until_thursday_7am.total_seconds())
    await check_for_updates()




# Run the bot
client.run(TOKEN)
