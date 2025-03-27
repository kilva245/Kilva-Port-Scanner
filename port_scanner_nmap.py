#!/usr/bin/env python3
# Use these commands in Kali to install required software:
#  sudo apt install python3-pip
#  pip install python-nmap
#  pip install colorama

# Import nmap so we can use it for the scan
import nmap
# We need to create regular expressions to ensure that the input is correctly formatted.
import re
# for set color to first text when run the script (for banner in basic header)
from colorama import init, Fore
# for banner in basic header
import pyfiglet
import time  # Importing time module to use for sleep functionality
import threading  # Importing threading module to create and manage threads

# Regular Expression Pattern to recognise IPv4 addresses.
ip_add_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

# Initialize colorama
init()

# Basic user interface header
banner = pyfiglet.figlet_format("kilva")
print(Fore.RED + banner)
print(Fore.RED + "\n****************************************************************")
print(Fore.RED + "\n* Copyright of kilva, 2025                              *")
print(Fore.RED + "\n****************************************************************")
print(Fore.RESET)  # Reset color to default

open_ports = []
# Ask user to input the ip address they want to scan.
while True:
    ip_add_entered = input(Fore.GREEN + "\nEnter target ip: ")
    if ip_add_pattern.search(ip_add_entered):
        print(Fore.GREEN + f"{ip_add_entered} is a valid ip address")
        break

while True:
    port_input = input(Fore.GREEN + "Please enter the port you want to scan (0-65535): ")
    if port_input.isdigit() and 0 <= int(port_input) <= 65535:
        port = int(port_input)
        break
    else:
        print(Fore.RED + "Invalid port number. Please enter a number between 0 and 65535.")

# Function to display loading animation
def loading_animation():
    while not stop_loading:
        for char in "|/-\\":
            print(Fore.GREEN + f"\rScanning port {port}... {char}", end="")
            time.sleep(0.1)  # Pause for a short duration to create the loading effect

# Create an instance of the PortScanner
nm = nmap.PortScanner()

# Start loading animation in a separate thread
stop_loading = False
loading_thread = threading.Thread(target=loading_animation)  # Create a new thread for the loading animation
loading_thread.start()  # Start the loading animation thread

try:
    # Scan the specified IP address for the specified port
    result = nm.scan(ip_add_entered, str(port))
    # Extract the port status from the returned object
    port_status = result['scan'][ip_add_entered]['tcp'][port]['state']
    stop_loading = True  # Stop the loading animation
    loading_thread.join()  # Wait for the loading thread to finish
    print(Fore.GREEN + f"\nPort {port} is {port_status}")  # Port status in green
except Exception as e:
    stop_loading = True  # Stop the loading animation
    loading_thread.join()  # Wait for the loading thread to finish
    print(Fore.RED + f"\nCannot scan port {port}. Error: {e}")  # Error message in red
finally:
    print(Fore.RESET)  # Reset color to default