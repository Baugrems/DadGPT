import sys, os, discord, openai, math, re
import numpy as np
from dotenv import load_dotenv

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

load_dotenv() # get variables from .env

# Get your secret keys from environmental variables. Do not hardcode these!
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
openai.api_key = os.getenv("OPENAI_API_KEY")

# every message on the server (in channels it can see) passes through here.
@client.event
async def on_message(message: discord.Message):
    # ignore messages from itself
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.channel.DMChannel):
        return
    
    if message.channel.type == discord.ChannelType.public_thread:
        return
    
    if message.channel.type == discord.ChannelType.forum:
        return

    msg = message.content

    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are DadGPT. You make groan-worthy jokes that make people cringe. All the jokes are G Rated and kid friendly. Dad jokes are your specialty. You chat like a normal assistant, but when there is an opening, you make a dad joke."},
        {"role": "user", "content": msg}
    ]
    )
    if len(completion.choices[0].message.content) < 1900:
        await message.channel.send(completion.choices[0].message.content, reference=message)
    else:
        await message.channel.send(completion.choices[0].message.content[0:1900], reference=message)
        await message.channel.send(completion.choices[0].message.content[1900:], reference=message)

##################################################################################
# Slash Commands for Admins                                                      #
##################################################################################




##################################################################################

# guards against DM traffic
async def checkDM(context):
    if context.channel.type == discord.ChannelType.private:
        await context.response.send_message("I do not respond to DMs.")
        return True
    return False


# when bot is activated, this function is run.
# Gives some basic data about itself to host machine to confirm run. 
# Sets up slash commands and initial training.
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing, 
            name="your emotions."
        )
    )

client.run(DISCORD_BOT_TOKEN)
