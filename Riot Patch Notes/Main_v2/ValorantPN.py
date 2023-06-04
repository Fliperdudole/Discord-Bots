#Programmer: Brandon Sandoval
#Date Started: 6/3/23
#Purpose: This helper file will contain all the necessary variables/functions in order 
#         for the main file to work for the specified game


import saveVar

# URL for the Valorant Patch Notes website
URL = 'https://playvalorant.com/en-us/news/game-updates/valorant-patch-notes-{}-{}/'

# File to store the last patch number
LAST_PATCH_FILE = 'last_valorant_patch.txt'

# Number of tries done to check patch
patch_tries = 0

# Variable to check current patch to prevent recurring updates
current_patch = saveVar.read_last_patch(LAST_PATCH_FILE)

# Current season/act
current_season = 6

# Get the role name to mention
role_name = 'Valorant-Patch-Notes' 

async def pad_patch_num(num):
     # Nums 1-9 have to have a padded 0 in order for the link to work (ex.1 = 01)
    if num >= 1 and num <=9:
        padded_number = str(num).zfill(2)

    else:
        padded_number = str(num)
    return padded_number


checking_patch = True