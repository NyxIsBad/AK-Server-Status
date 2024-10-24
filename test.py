import discord
from discord.ext import commands
import configparser
from state import *
config = configparser.ConfigParser()
config.read('secrets.ini')

token = config['BOT']['token']
prefix = config['BOT']['prefix']

channels = list(map(int, config['CHANNELS']['channels'].split(',')))

# get bitwise permissions
print(discord.Intents.default().value)