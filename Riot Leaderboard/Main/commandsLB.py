# Import libraries
import os
import discord
from discord.ext import commands

import requests


@commands.command()
async def track(ctx, *,account_name):   
    account_name = account_name.strip()


    base_url="https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    url_account= account_name.replace(" ", "%20")
    combined_url = base_url + url_account
    api_url = combined_url + '?api_key=' + os.getenv('RIOT_LB_API')

    #await ctx.send(f'{api_url} is the url')

    #await ctx.send(f'{account_name} is being tracked')

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an exception if the response contains an error status code
        # Process the response if no error occurred
    except requests.exceptions.HTTPError as err:
        error_data = err.response.json().get("status")
        error_message = error_data.get("message")
        error_code = error_data.get("status_code")
        await ctx.send(f'Error code {error_code}: {error_message}. Contact Fliperdudole for further questions')
    except requests.exceptions.RequestException as err:
        await ctx.send("An error occurred during the request.")




    








async def setup(bot):
    bot.add_command(track)    