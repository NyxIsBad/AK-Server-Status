import datetime, socket, time

status = [-1]*4
# Usage
ip_address = '34.66.112.227'
ports = [6543, 6544, 6545, 6546]

def check_server(ip, port, timeout=2):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)  # Set a timeout for the connection attempt
        try:
            sock.connect((ip, port))
            return True  # Server is online
        except (socket.timeout, ConnectionRefusedError):
            return False  # Server is offline or refused the connection
        
async def state():
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
        for i, port in enumerate(ports):
            state = 1 if check_server(ip_address, port) else 0
            cur_time = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')
            with open('status.log', 'a') as f:
                # check if state is different from last time
                if status[i] == -1:
                    status[i] = state
                    print(f"Channel {i+1} starts as {'online' if state == 1 else 'offline or unreachable'} at {cur_time} UTC")
                    f.write(f"Channel {i+1} starts as {'online' if state == 1 else 'offline or unreachable'} at {cur_time} UTC\n")
                elif status[i] == state:
                    f.write(f'Channel {i+1} is still {'online' if state == 1 else 'offline or unreachable'} at {cur_time} UTC\n')
                else:
                    status[i] = state
                    print(f"Channel {i+1} is now {'online' if state == 1 else 'offline or unreachable'} at {cur_time} UTC")
                    f.write(f"Channel {i+1} is now {'online' if state == 1 else 'offline or unreachable'} at {cur_time} UTC\n")
        time.sleep(120)  # Check every 2 minutes