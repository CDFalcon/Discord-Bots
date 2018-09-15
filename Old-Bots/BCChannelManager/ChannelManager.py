#
#  manager2.py
#
#  Created by CDFalcon on 1/14/18.
#  Copyright (c) 2017 CDFalcon. All rights reserved.
#
#-----------------------------------------------------------------------------

from pypubg import core
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext import commands
from datetime import datetime
import random
import settings

#connects with the Bot extension
managerbot = commands.Bot(command_prefix='.')

async def log(server, message):

    managerlog = (discord.utils.get(server.text_channels, id=settings.MANAGER_LOG_ID))
    await managerlog.send(message)

async def battlecord():

    return managerbot.get_guild(settings.BATTLECORD)

#event
@managerbot.event
#when the bot connects and is ready
async def on_ready():
    print('Ready')
    #sets bot to current version
    await managerbot.change_presence(game=discord.Game(name=(settings.VERSION + " - CDFalcon")))
    
@managerbot.event
#whenever someone joins voice channels
async def on_voice_state_update(member, previous, current):
                             
    #created a new channel
    if current.channel == discord.utils.get(member.guild.voice_channels, id=settings.CHANNEL_CREATOR_ID):

        numbers = '1234567890'
        channelNumber = int(''.join(random.sample(numbers, 4)))
    
        newchannel = await member.guild.create_voice_channel(channelNumber, category = discord.utils.get(member.guild.categories, id=settings.PRIVATE_CHANNEL_CATEGORY_ID))
        await member.move_to(newchannel)
        
        managerlog = (discord.utils.get(member.guild.text_channels, id=settings.MANAGER_LOG_ID))
        await managerlog.send("```Event: Private Channel Created\nMember: " + str(member) + "\nDate: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "```")
        await member.send(settings.CREATION_SUCCESS)
        
    #if it is an empty public channel, delete it
    try:
        if previous.channel.category_id == settings.PRIVATE_CHANNEL_CATEGORY_ID:
            if len(previous.channel.members) == 0:
                await previous.channel.delete()
                
    #if it is not, do nothing
    except:
        pass

@managerbot.command(pass_context=True)
#edits current voice channel             
async def edit(context, *args):

    server = await battlecord()
    editor = context.author.id
    editor = discord.utils.get(server.members, id = editor)

    isDM = False
    try:
        await context.message.delete()
    except:
        isDM = True
        
    if not args:
        return await context.author.send(settings.HELP_MENU)
    
    else:
        target = args[0]       
    if len(args) < 2:
        return await context.author.send(settings.ERROR_1)
    if target not in ['max', 'bitrate', 'name']:
        return await context.author.send(settings.ERROR_2)   
    value = args[1]

    try:
        if not (editor.voice.channel.category_id == settings.PRIVATE_CHANNEL_CATEGORY_ID):
            return await context.author.send(settings.ERROR_4)
    except:
        return await context.author.send(settings.ERROR_5)

    try:
        if target == 'max':
            await editor.voice.channel.edit(user_limit = value)
    except:
        await context.author.send(settings.ERROR_3)
        
    if target == 'bitrate':
        try:
            await editor.voice.channel.edit(bitrate = value)
        except:
            return await context.author.send(settings.ERROR_3)
        
    elif target == 'name':
        #for channel in 
        await editor.voice.channel.edit(name = value)

    elif target != 'max':
        return await context.author.send(settings.ERROR_3)
    
    await context.author.send(settings.SUCCESS)

    if isDM == False:
        await context.author.send(settings.ERROR_6)
        
    return await log(server, ("```Event: Channel Edited\nMember: " + str(context.author) + "\nEdit: " + target + "\nDate: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "```"))
        

@managerbot.command(pass_context=True)
#edits current voice channel             
async def join(context, *args):

    server = await battlecord()
    joiner = context.author.id
    joiner = discord.utils.get(server.members, id = joiner)

    isDM = False
    try:
        await context.message.delete()
    except:
        isDM = True
        
    if not args:
        return await context.author.send(settings.HELP_MENU)

    else:
        channelName = args[0]

    try:
        if (joiner.voice.channel.category_id != 0):
            try:
                if not ((discord.utils.get(server.voice_channels, name=channelName.strip('\n'))).category_id == settings.PRIVATE_CHANNEL_CATEGORY_ID):
                    return await context.author.send(settings.ERROR_2)
            except:
                return await context.author.send(settings.ERROR_2)
    except:
        return await context.author.send(settings.ERROR_5)

    try:
        await joiner.move_to(discord.utils.get(server.voice_channels, name=channelName))

    except:
        return await context.author.send(settings.ERROR_3)
    
    await context.author.send(settings.SUCCESS)

    if isDM == False:
        await context.author.send(settings.ERROR_6)

    return await log(server, ("```Event: Channel Joined\nMember: " + str(context.author) + "\nChannel: " + channelName + "\nDate: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "```"))
        
managerbot.run(settings.BOT_TOKEN)
