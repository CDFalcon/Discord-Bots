import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext import commands
import praw
import pdb
import re
import os
import time
from datetime import datetime
import io
import settings

# Connect to Reddit
reddit = praw.Reddit('BrowserBot1')

#Connect to Discord
redditbot = commands.Bot(command_prefix='rb.')
redditbot.remove_command('help')

@redditbot.event
#when the bot connects and is ready
async def on_ready():
    print('Ready')
    #sets bot to current version
    await redditbot.change_presence(game=discord.Game(name=("rb.help - " + settings.GITHUB)))

@redditbot.command(pass_context=True)
#help menu             
async def parse(context, *args):

    #Verifies args
    if not args:
        return await context.author.send(settings.ERROR_1)     
    if len(args) < 3:
        return await context.author.send(settings.ERROR_1)

    await context.channel.send("`Parsing Reddit, please wait. Results will be sent via DM.`")
    
    settings.SUB = args[0]
    settings.POST_NUMBER = int(args[1])
    settings.MIN_UPVOTES = int(args[2])
    settings.KEYWORD = args[3]
    
    #for i in range(settings.POST_NUMBER):
    for submission in (reddit.subreddit(settings.SUB)).hot(limit=settings.POST_NUMBER):
        if re.search(settings.KEYWORD, submission.title, re.IGNORECASE):
            if submission.score > settings.MIN_UPVOTES:
                message = ("**=======================**\n\n\n")
                message += ("`Title: `" + submission.title.encode('ascii', 'ignore').decode('ascii') + '\n' + '\n')
                message += ("`Score: `" + str(submission.score) + '\n' + '\n')
                message += ("`Post ID: `" + str(submission.id) + '\n' + '\n')
                message += ("`Text:` " + submission.selftext.encode('ascii', 'ignore').decode('ascii') + '\n' + '\n')
                message += ("`URL:` " + submission.url + '\n' + '\n')
                message += ("**=======================**\n\n\n")
                await context.author.send(message)
    await context.author.send("```Finished!```")

@redditbot.command(pass_context=True)
#help menu             
async def help(context):
    await context.author.send(settings.HELP)

redditbot.run(settings.DISCORD_TOKEN)
