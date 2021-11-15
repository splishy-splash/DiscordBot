import os
from discord.ext import commands
import GoogleAPI
import Scheduler
import IdiomOTD


with open('token.txt', 'r') as f:
    DiscordBotToken = f.readline()

with open('channel_id.txt', 'r') as f:
    channel_id = int(f.readline())

calendarId = 'primary'

client = commands.Bot(command_prefix='!')
scheduler = Scheduler.start_scheduler()


async def send_msg(channelID, text):
    channel = client.get_channel(channelID)
    await channel.send(text)


@client.event
async def on_ready():
    print("discord bot reporting for duty!!")


@client.command()
async def get_schedule(ctx):
    formatted_events = ''
    for i in GoogleAPI.check_schedule(GoogleAPI.google_auth(), 'primary'):
        formatted_events += i
    await ctx.send(formatted_events)


@client.command()
async def idiom(ctx):
    await ctx.send(IdiomOTD.idiomoftheday())


@client.command()
async def add_meeting(ctx, *args):
    await ctx.send(GoogleAPI.add_to_schedule(GoogleAPI.google_auth(), ' '.join(args)))


while True:
    client.run(DiscordBotToken)
