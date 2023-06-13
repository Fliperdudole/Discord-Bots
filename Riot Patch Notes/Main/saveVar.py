# Import library
import os

# Channel text file
DEFAULT_CHANNEL_FILE = 'default_channel.txt'




# This function saves and writes the default channel to the file
def save_default_channels(default_channels):
    with open(DEFAULT_CHANNEL_FILE, 'w') as file:
        for server_id, channel_id in default_channels.items():
            file.write(f"{server_id},{channel_id}\n")




# This function loads and reads the default channel from the file
def load_default_channels():
    default_channels = {}
    try:
        with open(DEFAULT_CHANNEL_FILE, 'r') as file:
            lines = file.readlines()
            for line in lines:
                server_id, channel_id = line.strip().split(',')
                default_channels[server_id] = channel_id
    except FileNotFoundError:
        print(f"Default channel file '{DEFAULT_CHANNEL_FILE}' not found.")
    return default_channels


# Function to get default notification channel for a server
def get_default_channel(server_id, default_channels):
    if server_id in default_channels:
        return default_channels[server_id]
    else:
        return None

# Function to update default notification channel for a server
def update_default_channel(server_id, channel_id, default_channels):
    default_channels[server_id] = channel_id
    save_default_channels(default_channels)


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