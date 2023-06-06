# Import libraries
import discord
from discord.ext import commands

# Helper libraries
import ValorantPN
import LeaguePN
import saveVar



# This function sets the channel ID to whereever it was called from
async def channel_set(ctx, default_channel_id):
    if ctx.message.content.lower() == "!setchannel":# This response allows the user to set the channel they want the notifications in
        
        default_channel_id = ctx.message.channel.id
        await ctx.send('Notifcations will now be sent here.') 
        print("Notification Channel Updated to: ",ctx.message.channel,"\n")


        # save updated default channel
        saveVar.save_default_channel(default_channel_id)

    
    return None




# This command calls function 'channel_set()"
@commands.command()
async def setchannel(ctx):                                   # This command sets the Channel ID where the user calls the command
    print("Command", ctx.message.content,"has been recieved and sent by",ctx.message.author)
    await channel_set(ctx, default_channel_id)     

# Load the default channel ID when the commands starts
default_channel_id = saveVar.load_default_channel()     



# This command gives the user the notification role for the respective game
@commands.command()
async def valorant(ctx):
    if ctx.message.content.lower() == "!valorant":
        print("Command", ctx.message.content,"has been recieved and sent by",ctx.message.author,"\n")
        giveRole = ValorantPN.role_name
        role = discord.utils.get(ctx.message.guild.roles, name=giveRole)
        if role: # if the user calls the command then give them the role
            try:
                await ctx.message.author.add_roles(role)
                # Currently set to DM's but if you want the message in general do "ctx.message.channel.send"
                await ctx.message.author.send(f'Role "{giveRole}" has been assigned to {ctx.message.author.mention}.')
                return
            # if the bot doesn't have permission then print
            except discord.Forbidden:
                await ctx.message.channel.send("I don't have permission to assign roles.")
                return
            
        else: #  if the user doesn't have the role then let them know 
            await ctx.message.channel.send(f'Role "{giveRole}" not found.')
            return
    # Processes the command through Discord's API
    await commands.process_commands(ctx.message)   


# This command removes the notification role for the respective game from the user
@commands.command()
async def rmvalorant(ctx):
    if ctx.message.content.lower() == "!rmvalorant":
        print("Command", ctx.message.content,"has been recieved and sent by",ctx.message.author,"\n")
        removeRole = ValorantPN.role_name
        role = discord.utils.get(ctx.message.guild.roles, name=removeRole)
        if role: # if the user has the role then remove
            try:
                await ctx.message.author.remove_roles(role)
                # Currently set to DM's but if you want the message in general do "ctx.message.channel.send"
                await ctx.message.author.send(f'Role "{removeRole}" has been removed from {ctx.message.author.mention}.')
                return
            # if the bot doesn't have permission then print
            except discord.Forbidden:
                await ctx.message.channel.send("I don't have permission to remove roles.")
                return
            
        else:   #  if the user doesn't have the role then let them know 
            await ctx.message.channel.send(f'Role "{removeRole}" not found.')
            return
    # Processes the command through Discord's API
    await commands.process_commands(ctx.message)   



# This command gives the user the notification role for the respective game
@commands.command()
async def league(ctx):
    if ctx.message.content.lower() == "!league":
        print("Command", ctx.message.content,"has been recieved and sent by",ctx.message.author,"\n")
        giveRole = LeaguePN.role_name
        role = discord.utils.get(ctx.message.guild.roles, name=giveRole)
        if role: # if the user calls the command then give them the role
            try:
                await ctx.message.author.add_roles(role)
                # Currently set to DM's but if you want the message in general do "ctx.message.channel.send"
                await ctx.message.author.send(f'Role "{giveRole}" has been assigned to {ctx.message.author.mention}.')
                return
            # if the bot doesn't have permission then print
            except discord.Forbidden:
                await ctx.message.channel.send("I don't have permission to assign roles.")
                return
            
        else: #  if the user doesn't have the role then let them know 
            await ctx.message.channel.send(f'Role "{giveRole}" not found.')
            return
    # Processes the command through Discord's API
    await commands.process_commands(ctx.message)   


# This command removes the notification role for the respective game from the user
@commands.command()
async def rmleague(ctx):
    if ctx.message.content.lower() == "!rmleague":
        print("Command", ctx.message.content,"has been recieved and sent by",ctx.message.author,"\n")
        removeRole = LeaguePN.role_name
        role = discord.utils.get(ctx.message.guild.roles, name=removeRole)
        if role: # if the user has the role then remove
            try:
                await ctx.message.author.remove_roles(role)
                # Currently set to DM's but if you want the message in general do "ctx.message.channel.send"
                await ctx.message.author.send(f'Role "{removeRole}" has been removed from {ctx.message.author.mention}.')
                return
            # if the bot doesn't have permission then print
            except discord.Forbidden:
                await ctx.message.channel.send("I don't have permission to remove roles.")
                return
            
        else:   #  if the user doesn't have the role then let them know 
            await ctx.message.channel.send(f'Role "{removeRole}" not found.')
            return
    # Processes the command through Discord's API
    await commands.process_commands(ctx.message)   



# This is a help command as I was too lazy to mess with Discord's default help command
@commands.command()
async def helpPN(ctx):
    if ctx.message.content.lower() == "!helppn":
        print("Command", ctx.message.content,"has been recieved and sent by",ctx.message.author,"\n")
        await ctx.message.channel.send("These are the current commands I can receive!")
        await ctx.message.channel.send("!setchannel - Set the notifications channel")
        await ctx.message.channel.send("!valorant - Add the Valorant-Patch-Notes role to receive notifications")
        await ctx.message.channel.send("!rmvalorant - Remove the Valorant-Patch-Notes role")

        await ctx.message.channel.send("!league - Add the League-Patch-Notes role to receive notifications")
        await ctx.message.channel.send("!rmleague - Remove the League-Patch-Notes role")

        

# This is a setup function to add the commands to the bot which is then loaded from the main file
async def setup(bot):
    bot.add_command(valorant)
    bot.add_command(rmvalorant)
    bot.add_command(league)
    bot.add_command(rmleague)

    bot.add_command(setchannel)

    bot.add_command(helpPN)