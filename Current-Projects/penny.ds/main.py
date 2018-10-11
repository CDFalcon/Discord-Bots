from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext import commands

from wit import Wit

import pdb
import re
import os
from datetime import datetime
import io
import subprocess

import wix_ai
from settings import *
import misc

import sys
import json
import requests
import pprint

#Setup#
#==============================#

bot = commands.Bot(command_prefix="penny.")
bot.remove_command('help')

#Functions#
#==============================#

async def create_bash(message):
    bash = await message.guild.create_text_channel("bash-shell")
    await bash.set_permissions(message.guild.default_role, read_messages = False)
    await bash.send(message.author.mention+" `, here is a private bash shell channel for you. Remember, start all commands with 'penny.bash '`\n`In you case you needed it, this channel's id is` **" + str(bash.id) + "**")
    

async def is_admin(message):
    if message.author.id == admin_id:
        return True
    await message.channel.send(message.author.mention+"`, you appear to attempting to use an administrator-only command.`")
    return False

#Events#
#==============================#

@bot.event
async def on_ready():
    print("#"*50+"\nStartup completed at "+str(datetime.now())+"\n"+"#"*50)
    await bot.change_presence(activity=discord.Game(name=("github.com/CDFalcon")))

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    
    if message.author == bot.user:
        return
    if message.content.startswith("penny."):
        return
    
    wit_response = wit.message(message.content)
    print("Recieved data: " + str(wit_response))
    wit_response = wix_ai.manage_request(wit_response)

    if wit_response == "error":
        await message.channel.send("`Sorry, I didn\'t understand your message. Try using simple English, or ask someone with experience in using me for help.`")

    elif wit_response[0] == "search":
        results = misc.google_search(wit_response[1], google_api, google_cse, num=wit_response[2])
        response_message = "\n`Here are the first 5 results for` **\"" + wit_response[1] + "**\"\n"
        for i in range(wit_response[2]):
            response_message += "`Title:` " + results[i]['title'] + "\n`Link:` " + results[i]['link'] + "\n"
        await message.author.send(response_message)
        await message.channel.send("`Sent search results for  `** " + str(wit_response[1]) + "**`  to  `" + message.author.mention + ".")

    elif wit_response[0] == "ban":
        if await is_admin(message):
            try:
                await discord.utils.get(message.guild.members, name = wit_response[1]).ban(reason="Banned via admin request.")
                await message.channel.send("`Banned  `@" + str(wit_response[1]) + "`  by  `" + message.author.mention + "'s `request.`")
            except:
                await message.channel.send("`Something went wrong `" + message.author.mention)

    elif wit_response[0] == "kick":
        if await is_admin(message):
            try:
                await discord.utils.get(message.guild.members, name = wit_response[1]).kick(reason="Kicked via admin request.")
                await message.channel.send("`Kicked  `@" + str(wit_response[1]) + "`  by  `" + message.author.mention + "'s `request.`")
            except:
                await message.channel.send("`Something went wrong `" + message.author.mention)

    elif wit_response[0] == "open":
        if wit_response[1] == "terminal":
            if await is_admin(message):
                await create_bash(message)
                await message.channel.send("`Done and done `" + message.author.mention)

    elif wit_response[0] == "close":
        pass

    elif wit_response[0] == "say":
        if await is_admin(message):
            try:
                if wit_response[2] == "default.channel":
                    pass
            except:
                pass
            
    elif "greetings" in wit_response:
        try:
            await message.channel.send("`Hi `" + message.author.mention + "`, I am Penny, a rather clever Discord bot with a natural language AI to help me translate your messages. AMA!`")
        except:
            pass

#Commands#
#==============================#
        
@bot.command(pass_context=True)       
async def bash(context, *args):
    try:
        result = subprocess.check_output(args, shell=False)
        await context.channel.send("`Command output: `\n" + str(result))
    except:
        await context.channel.send("`Something went wrong `" + context.author.mention)

#Other#
#==============================#
        
if __name__ == '__main__':
    wit = Wit(access_token=wit_token)
    bot.run(ds_token)


    
