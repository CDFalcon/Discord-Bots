#
#  Opus2.py
#
#  Created by CDFalcon on 1/14/18.
#  Copyright (c) 2018 CDFalcon. All rights reserved.
#
#-----------------------------------------------------------------------------

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext import commands
from datetime import datetime
import random
import settings

#connects with the Bot extension
opusbot = commands.Bot(command_prefix='?')

async def kickMember(member):
    try:
        await member.guild.create_voice_channel("DCing")
        await member.move_to(discord.utils.get(member.guild.voice_channels, name="DCing"))
        return await (discord.utils.get(member.guild.voice_channels, name="DCing")).delete()
    except:
        await log(context, ("```Event: Failed Kick\nDate: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "```"))

async def isAuthorized(context):
    
    hasRoles = False
    for role in settings.ADMIN_ROLES:
        if discord.utils.get(context.guild.roles, name=role) in context.author.roles:
            hasRoles = True
            
    if hasRoles == False:
        await context.author.send(settings.ERROR_4)
        
    return hasRoles

async def log(context, message):

    opuslog = (discord.utils.get(context.author.guild.text_channels, id=settings.OPUS_LOG_ID))
    await opuslog.send(message)

#event
@opusbot.event
#when the bot connects and is ready
async def on_ready():
    print('Ready')
    #sets bot to current version
    await opusbot.change_presence(game=discord.Game(name=("?opus - " + settings.VERSION)))

@opusbot.event
#whenever a DCing joins our server
async def on_member_join(member):

    await member.send(settings.JOIN_MESSAGE)
    await member.add_roles(discord.utils.get(context.guild.roles, name=('Unverified')))
    
@opusbot.event
#whenever someone joins voice channels
async def on_voice_state_update(member, previous, current):
                             
    #created a new channel
    if current.channel == discord.utils.get(member.guild.voice_channels, id=settings.CHANNEL_CREATOR_ID):
        
        numbers = '1234567890'
        channelNumber = int(''.join(random.sample(numbers, 5)))
    
        await member.guild.create_voice_channel(settings.NEW_PUBLIC_CHANNEL_NAME + str(channelNumber), category = discord.utils.get(member.guild.categories, id=settings.PUBLIC_CHANNEL_CATEGORY_ID))
        await member.move_to(discord.utils.get(member.guild.voice_channels, name=settings.NEW_PUBLIC_CHANNEL_NAME + str(channelNumber)))
        
        opuslog = (discord.utils.get(member.guild.text_channels, id=settings.OPUS_LOG_ID))
        await opuslog.send("```Event: New Channel\nMember: " + str(member) + "\nDate: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "```")
        
    #if it is an empty public channel, delete it
    try:
        if previous.channel.category_id == settings.PUBLIC_CHANNEL_CATEGORY_ID or previous.channel.category_id == settings.PRIVATE_CHANNEL_CATEGORY_ID:
            if len(previous.channel.members) == 0:
                await previous.channel.delete()
                
    #if it is not, do nothing
    except:
        pass

#new command
@opusbot.command(pass_context=True)
#help menu             
async def opus(context):
    try:
        await context.author.send(settings.HELP_MENU)
        await context.message.delete()
    except:
        await context.author.send(settings.ERROR_6)

@opusbot.command(pass_context=True)
#whenever a member joins, see if they accept our rules
async def accept(context):

    try:
        await context.message.delete()
    except:
        await context.author.send(settings.ERROR_6)
    
    
    if (discord.utils.get(context.guild.roles, name="Member")) not in context.author.roles:
        await context.author.add_roles(discord.utils.get(context.guild.roles, name=('Member')))
        await context.author.remove_roles(discord.utils.get(context.guild.roles, name=('Unverified')))
        #moves them to a new channel, then deletes the channel, which DC's them from the voice channels
        await kickMember(context.author)
        await context.author.send("```Thanks for accepting our rules! From all of the staff, we hope you enjoy your time here.```")
        await log(context, ("```Event: Member joined and accepted the rules\nMember: " + str(context.author) + "\nDate: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "```"))
    else:
        await context.author.send("```You already have accepted our rules, no need for a second time!```")
        await kickMember(context.author)

@opusbot.command(pass_context=True)
#edits current voice channel             
async def edit(context, *args):

    try:
        await context.message.delete()
    except:
        return await context.author.send(settings.ERROR_6)

    if not args:
        return await context.author.send(settings.ERROR_1)
    else:
        target = args[0]       
    if len(args) < 2:
        return await context.author.send(settings.ERROR_1)
    if target not in ['max', 'bitrate', 'name', 'type']:
        return await context.author.send(settings.ERROR_2)   
    value = args[1]

    try:
        if not (context.author.voice.channel.category_id == settings.PUBLIC_CHANNEL_CATEGORY_ID or context.author.voice.channel.category_id == settings.PRIVATE_CHANNEL_CATEGORY_ID):
            return await context.author.send(settings.ERROR_4)
    except:
        return await context.author.send(settings.ERROR_5)

    try:
        if target == 'max':
            await context.author.voice.channel.edit(user_limit = value)
    except:
        await context.author.send(settings.ERROR_3)
        
    if target == 'bitrate':
        try:
            await context.author.voice.channel.edit(bitrate = value)
        except:
            return await context.author.send(settings.ERROR_3)
    elif target == 'name':
        await context.author.voice.channel.edit(name = value)

    elif target == 'type':

        currentName = str(context.author.voice.channel)
        currentMaxPlayers = context.author.voice.channel.user_limit
        currentBitrate = context.author.voice.channel.bitrate

        if value == 'private':            
            newChannel = await context.guild.create_voice_channel(currentName, category = discord.utils.get(context.guild.categories, id=settings.PRIVATE_CHANNEL_CATEGORY_ID))

        elif value == 'public':
            newChannel = await context.guild.create_voice_channel(currentName, category = discord.utils.get(context.guild.categories, id=settings.PUBLIC_CHANNEL_CATEGORY_ID))

        else:
            return await context.author.send(settings.ERROR_3)

        await context.author.move_to(newChannel)
        await newChannel.edit(bitrate = currentBitrate)
        await newChannel.edit(user_limit = currentMaxPlayers)
        await log(context, ("```Event: Channel Edited\nMember: " + str(context.author) + "\nEdit: " + target + "\nDate: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "```"))
        

@opusbot.command(pass_context=True)
#edits current voice channel             
async def join(context, *args):

    try:
        await context.message.delete()
    except:
        return await context.author.send(settings.ERROR_6)

    if not args:
        return await context.author.send(settings.ERROR_1)

    else:
        channelName = args[0]

    try:
        if not ((discord.utils.get(context.guild.voice_channels, name=channelName).category_id == settings.PUBLIC_CHANNEL_CATEGORY_ID) or ((discord.utils.get(context.guild.voice_channels, name=channelName)).category_id) == settings.PRIVATE_CHANNEL_CATEGORY_ID):
            return await context.author.send(settings.ERROR_4)
    except:
        return await context.author.send(settings.ERROR_5)

    try:
        await context.author.move_to(discord.utils.get(context.guild.voice_channels, name=channelName))

    except:
        return await context.author.send(settings.ERROR_3)

@opusbot.command(pass_context=True)
#edits current voice channel             
async def kick(context, *args):

    try:
        await context.message.delete()
    except:
        return await context.author.send(settings.ERROR_6)

    if not args:
        return await context.author.send(settings.ERROR_1)
    else:
        target = args[0]

    target = discord.utils.get(context.guild.members, name=target)

    if await isAuthorized(context) == False:
        return
        
    else:
        try:
            if target.voice.channel != None:
                await kickMember(target)
                await log(context, ("```Event: Member kicked from channel\nMember: " + str(context.author) + "\nTarget: " + str(target) + "\nDate: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "```"))
            else:
                await context.author.send(settings.ERROR_2)
        except:
            await context.author.send(settings.ERROR_2)

@opusbot.command(pass_context=True)
#chooses a random member from the server            
async def roll(context, *args):

    try:
        await context.message.delete()
    except:
        return await context.author.send(settings.ERROR_6)

    if await isAuthorized(context) == False:
        return

    if not args:
        return await context.author.send(settings.ERROR_1)

    winner = []
    for member in context.guild.members:
        for role in args:
            try:
                if (discord.utils.get(context.guild.roles, name=role)) in member.roles:
                    winner.insert(0, str(member))
            except:
                return await context.author.send(settings.ERROR_3)
                
    try:
        winnerwinner = random.choice(winner)
    except:
        return await context.author.send(settings.ERROR_1)
    
    await context.message.channel.send(settings.GIVEAWAY_MESSAGE + str(winnerwinner))
    await log(context, ("```Event: roll\nMember: " + str(context.author) + "\nWinner: " + str(winnerwinner) + "\nDate: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "```"))

@opusbot.command(pass_context=True)
#DM's a set group of roles a message set by the user
async def tell(context, *args):

    try:
        await context.message.delete()
    except:
        return await context.author.send(settings.ERROR_6)

    if await isAuthorized(context) == False:
        return

    if not args or len(args) < 2:
        return await context.author.send(settings.ERROR_1)

    roles = []

    for role in args:
        roles.insert(0, role)

    message = roles[0]
    del roles[0]

    toReceive = []

    for member in context.guild.members:
        for role in roles:
            try:
                if discord.utils.get(context.guild.roles, name = role) in member.roles:
                    if member not in toReceive:
                        toReceive.insert(0, member)
            except:
                return await context.author.send(settings.ERROR_3)

    for member in toReceive:
        try:
            await member.send("```Message from " + str(context.author) + "```\n" + message)
        except:
            await context.author.send("```Member " + str(member) + " did not receive your message due to their privacy settings.")

    logContent = "```Event: tell\nMember: " + str(context.author) + "\nMessaged roles:"

    for role in roles:
        logContent = logContent + (" <" + str(role) + ">")

    await log(context, (logContent + "\nMessage content: " + message + "\nDate: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "```"))

@opusbot.command(pass_context=True)
#edits current voice channel             
async def invites(context, *args):

    try:
        await context.message.delete()
    except:
        return await context.author.send(settings.ERROR_6)
    
    if not args or len(args) > 1:
        return await context.author.send(settings.ERROR_1)

    member = args[0]

    totalUsedInvites = 0

    for invitation in (await context.guild.invites()):
        try:
            if invitation.inviter == (discord.utils.get(context.guild.members, name=member)):
                totalUsedInvites += invitation.uses               
        except:
            return await context.author.send(settings.ERROR_3)

    await context.author.send(str("```" + str(discord.utils.get(context.guild.members, name=member))) + " has brought a total of " + str(totalUsedInvites) + " new player(s) to the server with their current active links." + "```")
    await log(context, ("```Event: invites\nMember: " + str(context.author) + "\nTarget: " + str(discord.utils.get(context.guild.members, name=member)) + "\nTotal invites: " + str(totalUsedInvites) + "\nDate: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "```"))

@opusbot.command(pass_context=True)
#edits current voice channel             
async def channel(context, *args):

    try:
        await context.message.delete()
    except:
        return await context.author.send(settings.ERROR_6)

    if not args or len(args) > 1:
        return await context.author.send(settings.ERROR_1)

    target = args[0]

    if await isAuthorized(context) == False:
        return

    if not args or len(args) > 1:
        return await context.author.send(settings.ERROR_1)

    try:
        for member in (context.author.voice.channel.members):
            if member != context.author:
                if target == "mute":
                    await member.edit(mute=True)
                if target == "unmute":
                    await member.edit(mute=False)
    except:
        return await context.author.send(settings.ERROR_5)

    await log(context, ("```Event: VoiceState change\nMember: " + str(context.author) + "\nTarget: " + target + "\nDate: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "```"))
        
opusbot.run(settings.BOT_TOKEN)
