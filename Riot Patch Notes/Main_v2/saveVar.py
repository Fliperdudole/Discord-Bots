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