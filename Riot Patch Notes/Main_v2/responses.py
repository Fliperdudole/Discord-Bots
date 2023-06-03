import saveVar


async def channel_set(message, default_channel_id):
    if message.content.lower() == "!setchannel":# This response allows the user to set the channel they want the notifications in
        
        default_channel_id = message.channel.id
        await message.channel.send('Default channel updated.') 


        # save updated default channel
        saveVar.save_default_channel(default_channel_id)

    
    return None