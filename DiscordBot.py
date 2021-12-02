from discord.ext import commands

#These are local modules
import GoogleAPI
import IMDb
import IdiomOTD
import Scheduler
import weather

with open('token.txt', 'r') as f:
    DiscordBotToken = f.readline()

with open('channel_id.txt', 'r') as f:
    channel_id = int(f.readline())


calendarId = 'primary'

client = commands.Bot(command_prefix='!')
scheduler = Scheduler.start_scheduler()


@client.command()
async def imdb(ctx, *args):
    await ctx.send(IMDb.parse_input(args))


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



@scheduler.scheduled_job('interval', hours=24, start_date='2021-12-01 16:00:00')
async def check_for_snow():
    channel = client.get_channel(channel_id)
    await channel.send(weather.post_weather())


@client.command()
async def snow(ctx, *args):
    await ctx.send(weather.post_weather(args))

while True:
    client.run(DiscordBotToken)
