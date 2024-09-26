import time
import datetime
import socket
import os
from infi.systray import SysTrayIcon

FILE_NAME = 'status.log'

def check_server(ip, port, timeout=2):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)  # Set a timeout for the connection attempt
        try:
            sock.connect((ip, port))
            return True  # Server is online
        except (socket.timeout, ConnectionRefusedError):
            return False  # Server is offline or refused the connection

# Menu Tray
menu_options = ()
systray = SysTrayIcon("icon.ico", "AK Channel Monitor", menu_options, on_quit=lambda x: os._exit(0))
systray.start()

status = [-1]*4

# Clear the status log
open(FILE_NAME, 'w').close()

# Check that we are in fact connected to the internet
try:
    socket.gethostbyname('google.com')
except socket.gaierror:
    with open(FILE_NAME, 'w') as f:
        f.write("No internet connection detected\n")
    os._exit(0)

# Usage
ip_address = '34.66.112.227'
ports = [6543, 6544, 6545, 6546]

while True:
    with open(FILE_NAME, 'a') as f:
        for i, port in enumerate(ports):
            cur_time = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')
            if check_server(ip_address, port) and status[i] != 1:
                f.write(f"Channel {i+1} is now online at {cur_time} UTC\n")
                status[i] = 1
            elif not check_server(ip_address, port) and status[i] != 0:
                f.write(f"Channel {i+1} is now offline or unreachable at {cur_time} UTC\n")
                status[i] = 0
    time.sleep(10)  # Wait for 5 seconds before checking again