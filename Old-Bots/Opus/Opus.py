#
#  Opus.py
#  Opus, a different kind of bot.
#
#  Created by CDFalcon on 12/22/17.
#  Copyright (c) 2017 CDFalcon. All rights reserved.
#
#-----------------------------------------------------------------------------

from pypubg import core
import discord
from datetime import datetime
import random
import pdb
import re
import os
import time
import io

#Creates Folders. Use 'somefolder/newfile' to create a new file inside a folder
if not os.path.isdir('misc'):
    os.makedirs('misc')
if not os.path.isdir('reports'):
    os.makedirs('reports')
if not os.path.isdir('channels'):
    os.makedirs('channels')
if not os.path.isdir('streamers'):
    os.makedirs('streamers')
if (not os.path.isfile('misc/authorized.txt')):
    f = io.open('misc/authorized.txt', 'w')
    f.write('<@199240002171961344>')
    f.close
if (not os.path.isfile('channels/currentChannels.txt')):
    f = io.open('channels/currentChannels.txt', 'w')
    f.close
if (not os.path.isfile('misc/giveawayRoles.txt')):
    f = io.open('misc/giveawayRoles.txt', 'w')
    f.close
if (not os.path.isfile('reports/unkickableRoles.txt')):
    f = io.open('reports/unkickableRoles.txt', 'w')
    f.close

#Connects
client = discord.Client()

@client.event
async def on_ready():
    print('Long Live Opus')
    print(client.user.id)

#To welcome new users
@client.event
async def on_member_join(member):

    if member == client.user:
        return

    else:
        await member.send("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =\n Hey <@" + str(member.id) + ">, welcome to our humble Discord server, the **Kinetic Gaming Community*. I am **Opus, a Discord bot**. I keep things running smoothly around here.\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = == = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =\n Please stop by the #welcome Channel to read our house rules. Once you finish with that, head on down to #opus-info to learn all about yours truly and our unique channel management system. Most importantly of all, **keep bringing home that chicken dinner!**")
        await member.add_roles(discord.utils.get(member.guild.roles, name=('Member')))

#Always checks to see if it needs to delete a channel whenever someone leaves a channel
@client.event
async def on_voice_state_update(user, previous, current):
    with io.open('channels/currentChannels.txt', 'r') as f:
        currentChannels = f.readlines()

    #Checks to see if the channel is empty
    with io.open('channels/currentChannels.txt', 'w') as f:
        for channelName in currentChannels:
            if channelName != '' and channelName != '\n':
                if len((discord.utils.get(user.guild.voice_channels, name=channelName.strip('\n'))).members) == 0:
                    #If so, delete
                    await (discord.utils.get(user.guild.voice_channels, name=channelName.strip('\n'))).delete()
                    os.remove('channels/' + channelName.strip('\n') + '.txt')
                
                #If not, rewrite back to file
                else:
                    f.write(channelName)
                    
    #Needs better code, fix later
    previous = previous.channel
    current = current.channel

    try:
        if previous.category_id == (discord.utils.get(user.guild.categories, name='Duos').id) or previous.category_id == (discord.utils.get(user.guild.categories, name='Squads').id):
            if len(previous.members) == 0:
                await previous.delete()
    #bad
    except:
        print("user connected")

    numbers = '1234567890'
    channelNumber = int(''.join(random.sample(numbers, 5)))

    if current == discord.utils.get(user.guild.voice_channels, name='Auto Duos'):
        categorySnowflake = discord.utils.get(user.guild.categories, name='Duos')
        channelName = 'Duo #' + str(channelNumber)
        playerLimit = 2

    elif current == discord.utils.get(user.guild.voice_channels, name='Auto Squads'):
        categorySnowflake = discord.utils.get(user.guild.categories, name='Squads')
        channelName = 'Squad #' + str(channelNumber)
        playerLimit = 4

    else:
        return
        
    for channel in user.guild.voice_channels:
        if channel.category_id == (discord.utils.get(user.guild.categories, name='Duos').id) and channelName.startswith("Duo"):
            if len(channel.members) < channel.user_limit:
                await user.move_to(channel)
                return

        elif channel.category_id == (discord.utils.get(user.guild.categories, name='Squads').id) and channelName.startswith("Squad"):
            if len(channel.members) < channel.user_limit:
                await user.move_to(channel)
                return
    
    await user.guild.create_voice_channel(channelName, category = categorySnowflake)
    await user.move_to(discord.utils.get(user.guild.voice_channels, name=channelName))
    await (discord.utils.get(user.guild.voice_channels, name=channelName)).edit(user_limit = int(playerLimit))


#Whenever someone posts anything, check to see if it is a command
@client.event
async def on_message(message):

    #No messaging itself
    if message.author == client.user:
        return

    #If the message appears to be a command
    if message.content.startswith('<@393828678766821376>'):

        #Removes the mention to get just the command
        command = message.content.format(message).replace('<@393828678766821376> ', '', 1)

        try:

            #All commmands go here
            if command == 'help':
                await message.delete()
                await message.author.send('**Help Menu Requested: Ask and Ye Shall Receive.**\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =\n**How to communicate with yours truely:**\n*Ya like jazz?* Solid pickup-line if you ask me. Still, most likely not the best way to talk. In order to get my attention, you need to (ready for it?) *mention* me. Wow. Amazing. <insert applause here>. Yea it is not hard m8. Literally just start any normal message with <@393828678766821376> and it becomes a request in my eyes.')
                await message.author.send('\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =\n**How to understand to attached request list:**\nEach request is read with the following syntax: *request/argument(s)/userInput(like the text for reports and such)*.\nExample Request: <@393828678766821376> report/Bob/for being a scrub\n')
                await message.author.send('= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =\n**Current Requests (listed alphabetically):**\n\n')
                await message.author.send('createchannel:\n*Usage: <@393828678766821376> createchannel/channelName/userLimit/channelType\nDescription: Creates a voice channel. If no user limit is needed, please enter 0 for the argument. Channel types: public and private. For private channels, set a password by setting the channeType to* **private:password** *. If you are in a voice channel when you run this command, you will automatically join the new channel.*\n\n')
                await message.author.send('getreports:\n*Usage: <@393828678766821376> getreports/user\nDescription: Sends all reports on a certain user to requester.* **Admin Only**\n\n')
                await message.author.send('joinchannel:\n*Usage: <@393828678766821376> joinchannel/channelName/password\nDescription: Allows you to join private Custom Voice Channels* **Important:** *You MUST be in a voice channel before using this command, otherwise Discord considers you not connected and cannot move you into the channel!*\n\n')
                await message.author.send('report:\n*Usage: <@393828678766821376> report/user/reportText\nDescription: Reports a user anonymously. One report per user per report-ee. After 5 reports, the owner is notified and will look into the problem. After 10 reports, the user is autokicked.*\n\n')
                await message.author.send('roll:\n*Usage: <@393828678766821376> roll\nDescription: Randomly chooses a winner for a giveaway as long as they have a certain role or higher (current: Trusted Member).* **Admin Only**\n\n')
                await message.author.send('streaming:\n*Usage: <@393828678766821376> streaming\nDescription: Posts an announcement advertising your channel to possible viewers. Requires a 1 time setup to use.* **Streamer Only**\n\n')
                
            #Report a user
            elif command.startswith('report'):
                await message.delete()
                #Breaks apart command. Will fail if the user did not report correctly
                (command, user, reportText) = command.split('/')

                #User ID from nickname
                userID = discord.utils.get(message.guild.members, name=user).id

                #For if the user has no history of reports
                if (not os.path.isfile('reports/' + str(userID) + '.txt')):
                    with io.open('reports/' + str(userID) + '.txt', 'w') as f:
                        f.write('1\nReport author: {0.author.mention}\n'.format(message) + 'Submitted at: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\nReport text: ' + reportText)
                        f.close
                    await message.author.send('Thanks for submitting your report on <@' + str(userID) + '>. Our Administration will attempt to quickly resolve this matter.')

                else:
                    #Opens user report file
                    with io.open('reports/' + str(userID) + '.txt', 'r') as f:
                        if ('Report author: {0.author.mention}'.format(message)) in f.read():
                            f.close
                            await message.author.send('Sorry pal, but it appears as though you have already submitted a report on this user. No need to notify us again, we are already aware of the situation.')
                            return
                        else:
                            #Needed because we called f.read above... bad code, fix
                            f.close
                            with io.open('reports/' + str(userID) + '.txt', 'r') as f:
                                #The number of current reports is stored at the top of the file
                                currentReports = int(f.readline().strip('\n')) + 1
                                f.close

                                #Notifies the people in misc/authorized.txt when the report count gets above 5
                                if currentReports > 4:
                                    hasRole = 0
                                    toBeKicked = discord.utils.get(message.guild.members, name=user)
                                    if currentReports == 10:
                                        with io.open('reports/unkickableRoles.txt', 'r') as f:
                                            for line in f:
                                                if discord.utils.get(message.guild.roles, name=line.strip('\n')) in toBeKicked.roles:
                                                    hasRole = hasRole + 1
                                            #For when they are not a mod
                                            if hasRole == 0:                                               
                                                #await toBeKicked.send('You have been auto-kicked via <@393828678766821376> Auto Moderation. Feel free to discuss your reports with an Admin or Mod if you feel they are unfair.')
                                                await message.guild.kick(toBeKicked)
                                                f.close()
                                                with io.open('misc/misc/authorized.txt', 'r') as f:
                                                    for line in f:
                                                        await message.guild.get_member(int(line.strip('<').strip('@').strip('>').strip('\n'))).send(('User ' + str(toBeKicked) + ' reached more than 10 reports and was kicked. Sending reports.'))
                                                        with io.open('reports/' + str(userID) + '.txt', 'r') as f:
                                                            currentReportsLine = 'Current number of reports on this user: ' + str(currentReports)
                                                            next(f)
                                                            await message.author.send(currentReportsLine)
                                                            for line in f:
                                                                await message.author.send(line.format(message))
                                                            f.close
                                                            
                                            #For when they are a mod
                                            else:
                                                with io.open('misc/authorized.txt', 'r') as f:
                                                    for line in f:
                                                        await message.guild.get_member(int(line.strip('<').strip('@').strip('>').strip('\n'))).send(('User ' + str(toBeKicked) + ' has reached over 10 reports, but was not Auto-Kicked due to their roles. Please use **<@393828678766821376> getreports/' + user + '** to view reports on this user.'))                                               
                                    elif currentReports == 5:
                                        with io.open('misc/authorized.txt', 'r') as f:
                                            for line in f:
                                                await message.guild.get_member(int(line.strip('<').strip('@').strip('\n').strip('>'))).send(('User ' + str(toBeKicked) + ' has reached 5 reports. Please use **<@393828678766821376> getreports/' + user + '** to view reports on this user.'))
                                                                           
                                with io.open('reports/' + str(userID) + '.txt', 'r') as f:
                                    next(f)
                                    lines = f.readlines()
                                    f.close

                                    with io.open('reports/' + str(userID) + '.txt', 'w') as f:
                                        #Rewrites our new first line
                                        f.write(str(currentReports) + '\n')
                                        for line in lines:
                                            f.write(line)
                                        f.write('\nReport author: {0.author.mention}\n'.format(message) + 'Submitted at: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\nReport text: ' + reportText)
                                        f.close
                                    
                                    await message.author.send('Thanks for submitting your report on <@' + str(userID) + '>. Our Administration will attempt to quickly resolve this matter.')

            #For admins to get reports
            elif command.startswith('getreports'):
                await message.delete()
                (command, user) = command.split('/')
                userID = discord.utils.get(message.guild.members, name=user).id

                with io.open('misc/authorized.txt', 'r') as f:
                    #Checks to see if the author is an admin (or CDF)
                    if ('{0.author.mention}'.format(message)) in f.read():
                        f.close
                        #If the user has reports
                        if (os.path.isfile('reports/' + str(userID) + '.txt')):
                            await message.author.send('**You got it boss. Reports incoming.**')
                            with io.open('reports/' + str(userID) + '.txt', 'r') as f:
                                currentReports = 'Current number of reports on this user: ' + f.readline().strip('\n')
                                await message.author.send(currentReports)
                                lines = f.readlines()
                                for line in lines:
                                    await message.author.send(line.format(message))
                                f.close
                        else:
                             await message.author.send('No reports exist for <@' + str(userID) + '>.')
                    else:
                        await message.author.send('You are not authorized to view reports for this user. Nice try, but I choose who has power in these parts...')

            #For when a user wants to create a voice channel. Here we go.
            elif command.startswith('createchannel'):
                await message.delete()
                (command, channelName, playerLimit, channelType) = command.split('/')

                channelName = re.sub('[^A-z0-9 -]', '', channelName).lower().replace(' ', '')

                #Checks to see if the channel name is avalible
                with io.open('channels/currentChannels.txt', 'r') as f:
                    if channelName in f.read():
                        await message.author.send('**Sorry m8, looks like that channel name is taken! Try again with another name.**')
                        f.close
                        return               

                with io.open('channels/' + channelName + '.txt', 'w') as f:
                    #Check to see if the channel is private
                    if 'private' in channelType:
                        #Trys to split:
                        try:
                            (channelType, password) = channelType.split(':')
                            password = re.sub('[^A-z0-9 -]', '', password).lower().replace(' ', '')
                            f.write(password)
                        except:
                            await message.author.send('Error #1: You failed to enter an argument, in this case the password for your private server. Remember, set the channel type to **private:password** to create a private channel.')
                            f.close
                            os.remove('channels/' + channelName + '.txt')
                            return
                    elif 'public' in channelType:
                        print('public channel created')
                    #Improper Channel Type
                    else:
                        await message.author.send('Error #1: You failed to enter an argument, in this case the channelType. Remember, only two channelType exist: **public** and **private:password**')
                        f.close
                        os.remove('channels/' + channelName + '.txt')
                        return
                        
                with io.open('channels/currentChannels.txt', 'a') as f:
                    f.write('\n' + channelName)

                #Creates the actual voice channel
                if channelType == 'public':
                    await message.guild.create_voice_channel(channelName, category = discord.utils.get(message.guild.categories, name='Custom Voice Channels'))
                    await message.author.move_to(discord.utils.get(message.guild.voice_channels, name=channelName))
                    await message.author.send('Alrighty, looks like you are all set. If you were not in a voice channel before you sent this command, go ahead and quickly join your channel.')
                    LFG = discord.utils.get(message.guild.text_channels, name='looking-to-play')
                    await LFG.send('Hey @here, <@' + str(message.author.id) + '> is opening a public voice channel. Therefore, **' + channelName + '** is requesting some **stone-cold-killers!**')

                if channelType == 'private':
                    permOverwrites = {
                        message.guild.default_role: discord.PermissionOverwrite(connect=False),
                        discord.utils.get(message.guild.roles, name='Admin'): discord.PermissionOverwrite(connect=True),
                        }
                    await message.guild.create_voice_channel(channelName, overwrites = permOverwrites, category = discord.utils.get(message.guild.categories, name='Custom Voice Channels'))
                    await message.author.send('Alrighty, looks like you are all set. If you were not in a voice channel before you sent this command, go ahead and join using **<@393828678766821376> joinchannel/' + channelName + '/' + password + '**')
                    await message.author.move_to(discord.utils.get(message.guild.voice_channels, name=channelName))
                    
                newchannel = discord.utils.get(message.guild.voice_channels, name=channelName.strip('\n'))
                if playerLimit != 0:
                    await newchannel.edit(user_limit = int(playerLimit))
                    
            #For joining a private channel. User needs to be connected to a voice channel for this to work
            elif command.startswith('joinchannel'):
                await message.delete()
                (command, channelName, password) = command.split('/')

                #Checks to see if channel exists
                with io.open('channels/currentChannels.txt', 'r') as f:
                    if channelName not in f.read():
                        await message.author.send('Error #2: You are attempting to join, look up, or edit a channel/role/member that does not appear to exist on this Discord server. Please try again with a correct name, and as always use **<@393828678766821376> help** to view the full command list.')
                        f.close
                        return

                with io.open('channels/' + channelName + '.txt', 'r') as f:                
                    storedPassword = f.readline()
                    if storedPassword == password:
                        await message.author.move_to(discord.utils.get(message.guild.voice_channels, name=channelName))
                                                                 
                    else:
                        await message.author.send('**Sorry m8, looks like your password is incorrect. Did you not see the sign? The Girl Scouts of America voice channel is 3 channels down...**')

            #Posts an announcement that this streamer is going live.
            elif command.startswith('streaming'):
                await message.delete()
                if discord.utils.get(message.guild.roles, name='Streamer') not in message.author.roles:
                    await message.author.send('Sorry m8, you need to have the streamer role to use this command.')
                    
                else:
                    #If they have setup their stream already
                    if (os.path.isfile('streamers/' + str(message.author.id) + '.txt')):
                        with io.open('streamers/' + str(message.author.id) + '.txt', 'r') as f:                   
                            await message.channel.send('Hey @everyone, {0.author.mention} is going live! If you have some free time, go check out their stream: '.format(message) + f.readline().strip('\n'))
                            
                    else:
                        await message.author.send('Looks like you have not setup your stream yet! Please use **<@393828678766821376> setupstream yourstreamlink**. IMPORTANT: **Notice the space instead of backslash between the request and link. This request has different syntax than the rest.** Also, **yourstreamlink** needs to be the link to your twitch stream, with no errors whatsoever. If you make a mistake typing the link, just reuse the command.')
                        
            #For streamers that have not already setup their stream
            elif command.startswith('setupstream'):
                await message.delete()
                (command, link) = command.split(' ')
                await message.author.send('Good to go! Your link is ' + link)
                with io.open('streamers/' + str(message.author.id) + '.txt', 'w') as f:
                    f.write(link)

            #For giveaway commands and such. Choose a random winner from a set of people that have approved roles (in misc/giveawayRoles.txt)
            elif command.startswith('roll'):
                await message.delete()

                with io.open('misc/authorized.txt', 'r') as f:
                    #Checks to see if the author is an admin (or CDF)
                    if ('{0.author.mention}'.format(message)) not in f.read():
                        f.close
                        await message.author.send('You are not authorized to host serverwide giveaways. Nice try, but I choose who has power around these parts.')
                        return

                #Clears or creates file
                f = io.open('misc/drawing.txt', 'w')
                f.close
                
                with io.open('misc/giveawayRoles.txt', 'r') as f:
                    for line in f:
                        for person in message.guild.members:
                            if discord.utils.get(message.guild.roles, name=line.strip('\n')) in person.roles:
                                with io.open('misc/drawing.txt', 'a') as f:
                                    f.write("<@" + str(person.id) + ">" + '\n')
                                    f.close

                lines = open('misc/drawing.txt').read().splitlines()
                winner = random.choice(lines)
                await message.channel.send('Hey @here, ' + winner + ' just won our giveaway. Congrats! Check your DMs for info on how to redeem your prize.')

            #Stat tracking for PUBG
            elif command.startswith('linkstats'):
                await message.delete()
                return

            #Yippe, someone likes me
            elif command.startswith('good bot'):
                await message.channel.send('{0.author.mention}'.format(message) + ' good human.')

            #Someone hates me
            elif command.startswith('bad bot'):
                await message.channel.send('{0.author.mention}'.format(message) + ' **thats what she said** *;)*')
                
            #For those special people
            else:
                await message.channel.send('**M8, I need some of what you are smoking... That request is not even close to existing. Use ** *<@393828678766821376> help* ** to see what requests I can respond to. **')

        except ValueError:
            await message.author.send('Error #1: You either gave too few arguments, too many arguments, or a letter/character instead of a number in your request. Please try again with proper syntax, and as always use **<@393828678766821376> help** to view the full command list. \n**Exception:** you may receive this error after using the **createchannel** request. If you still received a confirmation message, then you entered an incorrect value for the playerLimit arguement. Your channel was still created, but will not have a playerLimit.')
        except AttributeError:
            await message.author.send('Error #2: You are attempting to join, look up, or edit a channel/role/member that does not appear to exist on this Discord server. Please try again with a correct name (caps and special characters do count), and as always use **<@393828678766821376> help** to view the full command list.')
        except discord.Forbidden:
            await message.channel.send('Error #3: I do not appear to have admin permissions. Please try again after I receive my glorious perms, and as always use **<@393828678766821376> help** to view the full command list. \n**Exception:** you will receive this message if you try to communicate with me through DMs. **Remember**, due to some jacked up bot restrictions put in place by Discord, I cannot receive any messages you send via DMs. Instead, use **any text channel in the Discord server** to send me requests.')
        except:
            print('Something went wrong')
                                                                                                                      
client.run('MzkzODI4Njc4NzY2ODIxMzc2.DR7dFA.lK78_9MOuWIe2t0_Kxx_vPvgi7k')
