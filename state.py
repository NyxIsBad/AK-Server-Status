import datetime, socket, time
import aiohttp, json, asyncio

status = [-1]*4
# Usage
ip_address = '34.66.112.227'
ports = [6543, 6544, 6545, 6546]

async def send_embed_via_webhook(title="AK Server Status", description="", color=0x00ff00, fields: list = [], content="", URLs = []):
    embed = {
        "title": title,
        "description": description,
        "color": color,  # Green color
        "fields": fields
    }
    
    payload = {
        "username": "AK Server Status",
        "avatar_url": "https://cdn.discordapp.com/attachments/1299007089766568016/1299007221166823424/ak.png",
        "content": content,
        "embeds": [embed]
    }

    async with aiohttp.ClientSession() as session:
        for URL in URLs:
            async with session.post(URL, json=payload) as response:
                if response.status == 204:  # Discord sends 204 No Content on success
                    print("Successfully sent embed via webhook")
                else:
                    print(f"Failed to send embed. Status code: {response.status}")
                    print(await response.text())  # Get detailed response if needed

def check_server(ip, port, timeout=2):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)  # Set a timeout for the connection attempt
        try:
            sock.connect((ip, port))
            return True  # Server is online
        except (socket.timeout, ConnectionRefusedError):
            return False  # Server is offline or refused the connection
        
def webhook_state(urls):
    if len(urls) <= 0:
        print("No webhook URLs provided. Exiting...")
        return
    print("Checking the status of the channels")
    # Check that we are in fact connected to the internet
    while True:
        try:
            socket.gethostbyname('google.com')
            print("Internet connection detected")
            break
        except socket.gaierror:
            print("No internet connection detected, retrying...")
            time.sleep(60)
    
    while True:
        payload = ''
        states = []
        for i, port in enumerate(ports):
            state = 1 if check_server(ip_address, port) else 0
            cur_time = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')
            
            if status[i] == -1:
                status[i] = state
                print(f"Channel {i+1} starts as {'online' if state == 1 else 'offline or unreachable'} at {cur_time} UTC")
                payload += f"Channel {i+1} starts as {'online' if state == 1 else 'offline or unreachable'} at {cur_time} UTC\n"
            elif status[i] == state:
                pass
            else:
                status[i] = state
                print(f"Channel {i+1} is now {'online' if state == 1 else 'offline or unreachable'} at {cur_time} UTC")
                payload += f"Channel {i+1} is now {'online' if state == 1 else 'offline or unreachable'} at {cur_time} UTC\n"
            states.append(state)
        if len(payload) > 0:
            asyncio.run(send_embed_via_webhook(title=f"Channel {i+1} Status", description=payload, color=0x00ff00 if sum(states) == 4 else 0xff0000, URLs=urls))
        else: 
            print("No changes in the status of the channels")
        time.sleep(120)  # Check every 2 minutes