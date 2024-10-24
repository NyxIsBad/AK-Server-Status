import discord
from discord.ext import commands
import configparser
from state import *

config = configparser.ConfigParser()

try:
    config.read('secrets.ini')
except:
    # make a new file
    config['BOT'] = {
        'token': 'YOUR_TOKEN',
        'prefix': 'YOUR_PREFIX',
        'client_id': 'YOUR_CLIENT_ID',
    }
    config['CHANNELS'] = {
        'channels': 'CHANNEL_IDS',
    }
    with open('secrets.ini', 'w') as configfile:
        config.write(configfile)
    print('Please fill out the secrets.ini file')

token = config['BOT']['token']
prefix = config['BOT']['prefix']
client_id = config['BOT']['client_id']

channels = list(map(int, config['CHANNELS']['channels'].split(',')))

# clear the log file
open('status.log', 'w').close()

intents=discord.Intents.default()
intents.messages = True 
# print invite link
print(f"https://discord.com/oauth2/authorize?client_id={client_id}&permissions={intents.value}&scope=bot")
client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command('help')

@client.event 
async def on_ready():
    print('Bot is ready')
    activity = discord.Game(name=f"{prefix}help", type=3)
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_message(message):
    print(f"Received message: {message.content}")
    await client.process_commands(message)

@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title="Help", description=f"Use {prefix}help <command> for more info on a command.", color=0x00ff00)
    embed.add_field(name="Commands", value="status", inline=False)
    embed.add_field(name="Prefix", value="ak!", inline=False)
    await ctx.send(embed=embed)

@help.command()
async def status(ctx):
    embed = discord.Embed(title="Status", description="Check the status of the channels.", color=0x00ff00)
    await ctx.send(embed=embed)

@help.command()
async def setchannel(ctx):
    embed = discord.Embed(title="Set Channel", description=f"Set the channel to monitor. Syntax {prefix}setchannel <channel_id>", color=0x00ff00)
    await ctx.send(embed=embed)

@client.event 
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used.")

@client.command()
async def status(ctx):
    await ctx.send(f"Channel 1: {'online' if check_server(ip_address, ports[0]) else 'offline or unreachable'}")
    await ctx.send(f"Channel 2: {'online' if check_server(ip_address, ports[1]) else 'offline or unreachable'}")
    await ctx.send(f"Channel 3: {'online' if check_server(ip_address, ports[2]) else 'offline or unreachable'}")
    await ctx.send(f"Channel 4: {'online' if check_server(ip_address, ports[3]) else 'offline or unreachable'}")

async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')



client.run(token)
