import time
import datetime
import socket
import discord
import os
import asyncio
import configparser

# Load token and channel ID from secrets.ini
config = configparser.ConfigParser()
config.read('secrets.ini')
DISCORD_TOKEN = config.get('discord', 'token')
CHANNEL_ID = config.getint('discord', 'channel_id')

# Function to check if the server is online
def check_server(ip, port, timeout=2):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((ip, port))
            return True  # Server is online
        except (socket.timeout, ConnectionRefusedError):
            return False  # Server is offline or unreachable

# Define a subclass of discord.Client for the bot
class MyDiscordBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user.name}')
        self.channel = self.get_channel(CHANNEL_ID)
        await self.monitor_servers()

    # Coroutine to monitor the server statuses
    async def monitor_servers(self):
        ip_address = '34.66.112.227'
        ports = [6543, 6544, 6545, 6546]
        status = [-1] * len(ports)

        while True:
            for i, port in enumerate(ports):
                state = 1 if check_server(ip_address, port) else 0
                cur_time = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')

                # If the status has changed, send a message
                if status[i] == -1:
                    status[i] = state
                    await self.channel.send(
                        f"Channel {i+1} starts as {'online' if state == 1 else 'offline or unreachable'} at {cur_time} UTC"
                    )
                elif status[i] != state:
                    status[i] = state
                    await self.channel.send(
                        f"Channel {i+1} is now {'online' if state == 1 else 'offline or unreachable'} at {cur_time} UTC"
                    )
            # Check every 60 seconds
            await asyncio.sleep(60)

# Initialize and run the bot
if __name__ == '__main__':
    # Check internet connection
    try:
        socket.gethostbyname('google.com')
        print("Internet connection detected")
    except socket.gaierror:
        print("No internet connection detected")
        os._exit(0)

    intents = discord.Intents.default()
    bot = MyDiscordBot(intents=intents)
    bot.run(DISCORD_TOKEN)
