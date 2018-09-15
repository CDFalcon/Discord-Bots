# One of the earlier renditions of the Automated Channel Feature trend I started. 
# Horrible, horrible code. Sorry sorry sorry.

import discord
from datetime import datetime
import random
import pdb
import re
import os
import time
import io

#Connects
client = discord.Client()

@client.event
async def on_ready():
    print('LFG bot')
    print(client.user.id)

#Sorts users into channels
@client.event
async def on_voice_state_update(user, previous, current):

    previous = previous.channel
    current = current.channel
    
    if previous.category_id == (discord.utils.get(user.guild.categories, name='Duos').id) or previous.category_id == (discord.utils.get(user.guild.categories, name='Squads').id):
        if len(previous.members) == 0:
            await previous.delete()

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
        if channel.category_id == (discord.utils.get(user.guild.categories, name='Duos').id) or channel.category_id == (discord.utils.get(user.guild.categories, name='Squads').id):
            if len(channel.members) < channel.user_limit:
                await user.move_to(channel)
                return
    
    await user.guild.create_voice_channel(channelName, category = categorySnowflake)
    await user.move_to(discord.utils.get(user.guild.voice_channels, name=channelName))
    await (discord.utils.get(user.guild.voice_channels, name=channelName)).edit(user_limit = int(playerLimit))
    
                                                                                                                    
client.run('xxxxxxxxxxxxxxxxx')
