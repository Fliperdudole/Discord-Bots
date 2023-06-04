#Programmer: Brandon Sandoval
#Date Started: 6/3/23
#Purpose: This helper file will contain all the necessary variables/functions in order 
#         for the main file to work for the specified game

import saveVar
import requests


# URL for the League Patch Notes website
URL = 'https://www.leagueoflegends.com/en-us/news/game-updates/patch-{}-{}-notes/'
 
# File to store the last patch number
LAST_PATCH_FILE = 'last_league_patch.txt'

# Number of tries done to check patch
patch_tries = 0

# Variable to check current patch to prevent recurring updates 
current_patch = saveVar.read_last_patch(LAST_PATCH_FILE)

# Current season/act
current_season = 13

# Get the role name to mention
role_name = 'League-Patch-Notes'

# amended League url
league_url = URL.format(current_season, current_patch)

# League response code
league_response = requests.get(league_url)




checking_patch = True