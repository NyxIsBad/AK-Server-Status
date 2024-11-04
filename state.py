import datetime, socket, time
import aiohttp, json, asyncio

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
    # Each channel in `status` will be a tuple (state, consecutive_count)
    status = [(-1, 0)] * 4  # Initialize as offline with 0 consecutive occurrences
    
    # Usage
    ip_address = '34.66.112.227'
    ports = [6543, 6544, 6545, 6546]
    timer = 120  # Check every 2 minutes by default

    # Send initial status
    asyncio.run(send_embed_via_webhook(title="AK Server Status", description="Starting the server status monitoring", color=0x0000ff, URLs=urls))
    
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
        for i, port in enumerate(ports):
            state = 1 if check_server(ip_address, port) else 0
            cur_time = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')
            
            # Unpack previous state and consecutive count
            prev_state, consecutive_count = status[i]

            if prev_state == -1:
                # Initialize the first state without sending a notification
                status[i] = (state, 1)
                payload += f"Channel {i+1} starts as {'online' if state == 1 else 'offline or unreachable'} at {cur_time} UTC\n"
            elif prev_state == state:
                # If the state has not changed, increment the consecutive count
                consecutive_count += 1
                status[i] = (state, consecutive_count)
                
                # Send a notification only if the state is the same twice in a row
                if consecutive_count == 2:
                    payload += f"Channel {i+1} is {'online' if state == 1 else 'offline or unreachable'} at {cur_time} UTC\n"
                    timer = 120 # reset the timer
            else:
                # check for wifi issues
                try:
                    socket.gethostbyname('google.com')
                except socket.gaierror:
                    time.sleep(60)
                    continue
                # State changed, reset consecutive count
                status[i] = (state, 1)
                payload += f"Channel {i+1} is now {'online' if state == 1 else 'offline or unreachable'} at {cur_time} UTC\n"
                timer = 30 # we need to double check on a state change
            
            all_online = sum([state for state, _ in status]) == 4

        # Only send a webhook if there are updates
        if len(payload) > 0:
            asyncio.run(send_embed_via_webhook(
                title="Aura Kingdom Server Status",
                description=payload,
                color=0x00ff00 if all_online else 0xff0000,
                URLs=urls
            ))
        else: 
            print("No changes in the status of the channels")
        
        # every hour, send a message to the webhook to show that the bot is still running
        if datetime.datetime.now().minute == 0 or True:
            asyncio.run(send_embed_via_webhook(
                title="Aura Kingdom Server Status",
                description=f"Hourly check: channel states are {'all online' if all_online else 'at least partially offline or unreachable'}\nChannel 1 has been {'online' if status[0][0] == 1 else 'offline or unreachable'} for {status[0][1]} counts\nChannel 2 has been {'online' if status[1][0] == 1 else 'offline or unreachable'} for {status[1][1]} counts\nChannel 3 has been {'online' if status[2][0] == 1 else 'offline or unreachable'} for {status[2][1]} counts\nChannel 4 has been {'online' if status[3][0] == 1 else 'offline or unreachable'} for {status[3][1]} counts",
                color=0x0000ff,
                URLs=urls
            ))

        time.sleep(timer)  # Check every 2 minutes
