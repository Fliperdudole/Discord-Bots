import saveVar


async def channel_set(ctx, default_channel_id):
    if ctx.message.content.lower() == "!setchannel":# This response allows the user to set the channel they want the notifications in
        
        default_channel_id = ctx.message.channel.id
        await ctx.send('Notifcations will now be sent here.') 
        print("Notification Channel Updated to: ",ctx.message.channel)


        # save updated default channel
        saveVar.save_default_channel(default_channel_id)

    
    return None