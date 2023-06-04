import os

DEFAULT_CHANNEL_FILE = 'default_channel.txt'





def save_default_channel(CHANNEL_ID):
    # Open the file in write mode and save the default channel ID
    with open(DEFAULT_CHANNEL_FILE, 'w') as file:
        file.write(str(CHANNEL_ID))





def load_default_channel():
    # Check if the file exists
    if os.path.isfile(DEFAULT_CHANNEL_FILE):
        # Open the file and read the default channel ID
        with open(DEFAULT_CHANNEL_FILE, 'r') as file:
            channel_id = file.read().strip()
            if channel_id:
                return int(channel_id)

    return None


# Function to read the last patch number from the file
def read_last_patch(LAST_PATCH_FILE):
    if os.path.exists(LAST_PATCH_FILE):
        with open(LAST_PATCH_FILE, 'r') as file:
            try:
                current_patch = int(file.read())
                return current_patch
            except ValueError:
                pass
    return 1

# Function to write the current patch number to the file
def write_last_patch(LAST_PATCH_FILE,patch_number):
    with open(LAST_PATCH_FILE, 'w') as file:
        file.write(str(patch_number))
