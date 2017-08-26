import discord
from discord.ext import commands
import logging
import asyncio
import requests
import json
import os
import time
from operator import attrgetter


startup_extensions = ["stats"]
bot = commands.Bot(command_prefix="/")

# @bot.event
# async def on_server_join(server):
#     print("test")
#     print("Joining server: {0.id} ({0.name})".format(server))

@bot.event
async def on_ready():
    print("Logged in as:")
    print(bot.user.name)
    print(bot.user.id)
    print("======================")
    for server in bot.servers:
        print("server name: {} | server ID: {}".format(server, server.id))

@bot.command(pass_context=True)
async def exit(ctx):
    if ctx.message.author.id == "104441268863533056":
        await bot.logout()
    else:
        await bot.say("You don't have that kind of power...")
        
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    
bot.run("")


