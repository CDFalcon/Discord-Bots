# Some people might find this useful, it assigns everyone in your discord a certain
# if they don't already have it.

import discord
from discord.ext import commands
from discord.ext.commands import Bot

bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    pass
@bot.event
async def on_message(message):
    if message.content.startswith('?update'):
        await message.delete()
        role = discord.utils.get(message.guild.roles, name ="role name here")
        
        for member in message.guild.members:
            try:
                await member.add_roles(role)
                print(" added")
            except:
                print ("failed")

bot.run("xxxxxxxxxxxxxxxxxxxxxxxx")
    
