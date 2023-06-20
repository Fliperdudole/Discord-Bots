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

    await ctx.send(f'{api_url} is the url')

    await ctx.send(f'{account_name} is being tracked')

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an exception if the response contains an error status code
        # Process the response if no error occurred
    except requests.exceptions.HTTPError as err:
        error_code = err.response.status_code
        if error_code == 400:
            print("Bad request error (400)")
        elif error_code == 401:
            print("Unauthorized error (401)")
        elif error_code == 403:
            print("Forbidden error (403)")
        elif error_code == 404:
            print("Data not found error (404)")
        elif error_code == 405:
            print("Method not allowed error (405)")
        elif error_code == 415:
            print("Unsupported media type error (415)")
        elif error_code == 429:
            print("Rate limit exceeded error (429)")
        elif error_code == 500:
            print("Internal server error (500)")
        elif error_code == 502:
            print("Bad gateway error (502)")
        elif error_code == 503:
            print("Service unavailable error (503)")
        elif error_code == 504:
            print("Gateway timeout error (504)")
        else:
            print("An HTTP error occurred with status code:", error_code)
    except requests.exceptions.RequestException as err:
        print("An error occurred during the request:", err)



    








async def setup(bot):
    bot.add_command(track)    