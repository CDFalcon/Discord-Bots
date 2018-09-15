#
#  main.py
#
#  Created by CDFalcon on 4/18/18.
#  Copyright (c) 2018 CDFalcon. All rights reserved.
#
#Imports#
#-----------------------------------------------------------------------------#

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext import commands
from datetime import datetime
import random

import settings

#Classwork#
#-----------------------------------------------------------------------------#

tag = commands.Bot(command_prefix='?')
tag.remove_command("help")

#Functions#
#-----------------------------------------------------------------------------#

async def isAuthorized(context):
    
    hasRoles = False
    for role in settings.ADMIN_ROLES:
        if discord.utils.get(context.guild.roles, name=role) in context.author.roles:
            hasRoles = True
        
    return hasRoles

async def isHubAdmin(context, *args):
    
    try:
        await context.message.delete()
    except:
        await context.author.send(settings.ERROR__WRONG_CHANNEL)
        return False #21

    if len(args) != 2:
        await context.author.send(settings.ERROR__INVALID_ARGS)
        return False

    partner = args[0]

    try:
        if (discord.utils.get(context.guild.roles, name = partner + " Admin")) not in context.author.roles:
            await context.author.send(settings.ERROR__NOT_HUB_ADMIN)
            return False
    except:
        return await context.author.send(settings.ERROR__INVALID_ARGS)

    return True

#Events#
#-----------------------------------------------------------------------------#

@tag.event
async def on_ready():
    print("Ready")
    await tag.change_presence(game=discord.Game(name=(settings.VERSION))) #50

@tag.event
async def on_voice_state_update(member, previous, current):
                             
    if current.channel == discord.utils.get(member.guild.voice_channels, id=settings.DY_CHAN_ID):
        
        numbers = '1234567890'
        channelNumber = int(''.join(random.sample(numbers, 5)))
    
        await member.guild.create_voice_channel(str(channelNumber), category = discord.utils.get(member.guild.categories, id=settings.DY_CAT_ID))
        await member.move_to(discord.utils.get(member.guild.voice_channels, name=str(channelNumber)))
                
    try:
        if previous.channel.category_id == settings.DY_CAT_ID:
            if len(previous.channel.members) == 0:
                await previous.channel.delete()
    except:
        pass

#General Commands#
#-----------------------------------------------------------------------------#
    
@tag.command(pass_context=True)            
async def help(context):
    try:
        await context.author.send(settings.HELP_MENU)
        await context.message.delete()
    except:
        await context.author.send(settings.ERROR__WRONG_CHANNEL)

@tag.command(pass_context=True)            
async def join(context, *args):

    try:
        await context.message.delete()
    except:
        return await context.author.send(settings.ERROR__WRONG_CHANNEL)

    if not args or len(args) > 2:
        return await context.author.send(settings.ERROR__INVALID_ARGS)

    password = 0
    
    if len(args) == 2:
        password = args[1]

    partner = args[0]
    partnerRole = (discord.utils.get(context.guild.roles, name = partner))

    try:
        if partnerRole.color != discord.Color.dark_blue():
            return await context.author.send(settings.ERROR__INVALID_HUB)
    except:
        return await context.author.send(settings.ERROR__INVALID_HUB)

    try:
        if (discord.utils.get(context.guild.channels, name = partner + " password")).id != int(password):
            return await context.author.send(settings.ERROR__WRONG_PASSWORD) #91
    except:
        pass

    if (discord.utils.get(context.guild.roles, name = "Banned from " + partner)) not in context.author.roles:
        await context.author.send(settings.JOIN_MESSAGE_START + partner + settings.JOIN_MESSAGE_END)
        return await context.author.add_roles(partnerRole)

    else:
        return await context.author.send("**You are banned from **`" + partner + "` **and therefore cannot join.**")

@tag.command(pass_context=True)            
async def leave(context, *args):

    try:
        await context.message.delete()
    except:
        return await context.author.send(settings.ERROR__WRONG_CHANNEL)

    if len(args) != 1:
        return await context.author.send(settings.ERROR__INVALID_ARGS)

    partnerRole = (discord.utils.get(context.guild.roles, name = args[0]))

    try:
        await context.author.remove_roles(partnerRole) #111
    except:
        return await context.author.send(ERROR__INVALID_HUB)

    return await context.author.send(settings.LEAVE_MESSAGE_START + args[0] + settings.LEAVE_MESSAGE_END)
       
#Hub Admin Commands#
#-----------------------------------------------------------------------------#

@tag.command(pass_context=True)            
async def createPassword(context, *args):

    if await isHubAdmin(context, *args) == False:
        return

    partner = args[0]

    try:
        await (discord.utils.get(context.guild.channels, name = partner + " password")).delete()
    except:
         await context.author.send("**No current password found, creating a new password.**")
    try:
        if len(args) != 2:
            newPassword = await context.guild.create_voice_channel(partner + " password", category = (discord.utils.get(context.guild.categories, id = settings.PASSWORD_ID)))
            return await context.author.send("**Your new password is **`" + str(newPassword.id) + "`**.**")
        elif args[1] == "true":
            return await context.author.send("**Password deleted.**")
    except: #130
        return await context.author.send(settings.ERROR__INVALID_ARGS)

@tag.command(pass_context=True)            
async def ban(context, *args):

    if await isHubAdmin(context, *args) == False:
        return
    
    partner = args[0]

    try:
        await (discord.utils.get(context.guild.members, name = args[1])).add_roles(discord.utils.get(context.guild.roles, name = "Banned from " + partner))
        await (discord.utils.get(context.guild.members, name = args[1])).remove_roles(discord.utils.get(context.guild.roles, name = partner))
        await (discord.utils.get(context.guild.members, name = args[1])).remove_roles(discord.utils.get(context.guild.roles, name = partner + " Mod"))
    except:
        return await context.author.send(settings.ERROR__INVALID_ARGS)

    await context.author.send("`" + args[1] + "` **has been banned from your hub.**")

@tag.command(pass_context=True) #143           
async def unban(context, *args):
    
    if await isHubAdmin(context, *args) == False:
        return

    partner = args[0]
    
    try:
        await (discord.utils.get(context.guild.members, name = args[1])).remove_roles(discord.utils.get(context.guild.roles, name = "Banned from " + partner))
    except:
        return await context.author.send(settings.ERROR__INVALID_ARGS)

    await context.author.send("`" + args[1] + "` **has been unbanned from your hub.**")

@tag.command(pass_context=True)            
async def mod(context, *args):

    if await isHubAdmin(context, *args) == False:
        return
    
    partner = args[0]

    try:
        await (discord.utils.get(context.guild.members, name = args[1])).add_roles(discord.utils.get(context.guild.roles, name = partner + " Mod"))
        await (discord.utils.get(context.guild.members, name = args[1])).remove_roles(discord.utils.get(context.guild.roles, name = partner))
    except:
        return await context.author.send(settings.ERROR__INVALID_ARGS)

    await context.author.send("`" + args[1] + "` **has been added as a mod for your hub.**")

@tag.command(pass_context=True)            
async def unmod(context, *args):
    
    if isHubAdmin(context, *args) == False:
        return

    partner = args[0]
    
    try:
        await (discord.utils.get(context.guild.members, name = args[1])).remove_roles(discord.utils.get(context.guild.roles, name = partner + " Mod"))
    except:
        return await context.author.send(settings.ERROR__INVALID_ARGS) #172

    await context.author.send("`" + args[1] + "` **has been removed as a mod from your hub.**")

@tag.command(pass_context=True)            
async def hide(context, *args):
    
    if await isHubAdmin(context, *args) == False:
        return

    partner = args[0]
    
    try:
        channelToBeHidden = (discord.utils.get(context.guild.channels, name = args[1])) 
        if channelToBeHidden.category == discord.utils.get(context.guild.categories, name = partner):
            await channelToBeHidden.set_permissions(discord.utils.get(context.guild.roles, name = partner), read_messages = False, read_message_history = False, connect = False)
    except:
        return await context.author.send(settings.ERROR__INVALID_ARGS)

    await context.author.send("**Channel hidden.**")

@tag.command(pass_context=True)            
async def unhide(context, *args):
    
    if await isHubAdmin(context, *args) == False:
        return

    partner = args[0] #190
    
    try:
        channelToBeHidden = (discord.utils.get(context.guild.channels, name = args[1]))
        if channelToBeHidden.category == discord.utils.get(context.guild.categories, name = partner):
            await channelToBeHidden.set_permissions(discord.utils.get(context.guild.roles, name = partner), read_messages = True, read_message_history = True, connect = True)
    except:
        return await context.author.send(settings.ERROR__INVALID_ARGS)

    await context.author.send("**Channel unhidden.**")
    
 
#TAG Admin Commands#
#-----------------------------------------------------------------------------#

@tag.command(pass_context=True)            
async def addPartner(context, *args):

    try: #200
        if(await isAuthorized(context)):
            await context.message.delete()
        else:
            return await author.context.send(settings.ERROR__NOT_TAG_ADMIN)
    except:
        return await context.author.send(settings.ERROR__WRONG_CHANNEL)

    if not args:
        return await context.author.send(settings.ERROR__INVALID_ARGS)
    else:
        newPartner = args[0]
        
    if len(args) < 2 or len(args) > 3:
        return await context.author.send(settings.ERROR__INVALID_ARGS)
    
    firstAdmin = (discord.utils.get(context.guild.members, name = args[1]))

    if len(args) == 3:
        if args[2] == "true":
            password = await context.guild.create_voice_channel(newPartner + " password", category=(discord.utils.get(context.guild.categories, id = settings.PASSWORD_ID)))
            await firstAdmin.send("Your hub's password is `" + str(password.id) + "`.")
        else:
            await context.author.send(settings.ERROR__INVALID_ARGUMENT)

    await firstAdmin.send(settings.NEW_HUB_MESSAGE)
    
    newCategory = await context.guild.create_category(newPartner)
    
    newAdminRole = await context.guild.create_role(name = newPartner + " Admin", color = discord.Color.red())
    await firstAdmin.add_roles(newAdminRole)
    newRole = await context.guild.create_role(name = newPartner, color = discord.Color.dark_blue())
    newModRole = await context.guild.create_role(name = newPartner + " Mod", color = discord.Color.dark_purple())
    newBanRole = await context.guild.create_role(name = "Banned from " + newPartner, color = discord.Color.greyple())
    
    await newCategory.set_permissions(context.guild.default_role, read_messages = False, read_message_history = False, connect = False)
    await newCategory.set_permissions(newAdminRole, read_messages = True, read_message_history = True, connect = True, manage_channels = True, manage_messages = True, move_members = True)
    await newCategory.set_permissions(newModRole, read_messages = True, read_message_history = True, connect = True, manage_messages = True)
    await newCategory.set_permissions(newRole, read_messages = True, read_message_history = True, connect = True)
    await newCategory.set_permissions(newBanRole, read_messages = False, read_message_history = False, connect = False)
    
    await context.guild.create_text_channel("General Chat", category = newCategory)
    recruit = await context.guild.create_text_channel(newPartner + "-recruitment", category = (discord.utils.get(context.guild.categories, id = settings.RECRUIT_CAT_ID)))

    await recruit.set_permissions(newModRole, manage_messages = True)
    await recruit.set_permissions(newAdminRole, manage_messages= True)

@tag.command(pass_context=True) 
async def removePartner(context, *args):

    try:
        if(await isAuthorized(context)):
            await context.message.delete()
        else:
            return await context.author.send(settings.ERROR__NOT_TAG_ADMIN)
    except:
        return await context.author.send(settings.ERROR__WRONG_CHANNEL)

    if not args:
        return await context.author.send(settings.ERROR__INVALID_ARGS)
    else:
        partner = args[0]

    if len(args) > 1: #260
        return await context.author.send(settings.ERROR__INVALID_ARGS)

    try:
        await (discord.utils.get(context.guild.roles, name = partner)).delete()
        await (discord.utils.get(context.guild.roles, name = (partner + " Admin"))).delete()
        await (discord.utils.get(context.guild.roles, name = (partner + " Mod"))).delete()
        await (discord.utils.get(context.guild.roles, name = ("Banned from " + partner))).delete()
    except:
        return await context.author.send(settings.ERROR__INVALID_HUB)

    category = (discord.utils.get(context.guild.categories, name = partner))
    
    for channel in context.guild.channels:
        if channel.category == category:
            await channel.delete()

    try:
        await (discord.utils.get(context.guild.channels, name = partner + " password")).delete()
    except:
        pass

    try:
        await (discord.utils.get(context.guild.channels, name = partner + "-recruitment")).delete()
    except:
        pass

    return await category.delete()

#Script Start#
#-----------------------------------------------------------------------------#

tag.run(settings.BOT_TOKEN) #283
