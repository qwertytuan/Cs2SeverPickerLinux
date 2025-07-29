#!/usr/bin/python3
import requests
import os
import json
import subprocess
import random
import re

def getServerInfo(api='https://api.steampowered.com/ISteamApps/GetSDRConfig/v1/?appid=730'):
    print("Fetching server list...")
    try:
        response = requests.get(api, timeout=20)
        response.raise_for_status()  # Raise an exception for bad status codes
        server_info_json = response.json()
        print("Successfully fetched server info.")
        return server_info_json
    except requests.exceptions.RequestException as e:
        print(f"Error fetching server info: {e}")
        return None

def serverData():
    server_info = getServerInfo()
    all_server = []
    # Clean the infomation to servers datas
    pops = server_info["pops"]
    for pop_key,pop_data in pops.items():
        all_ip = []
        server=[]
        pop_description = pop_data["desc"]
        #print(f"Server key: {pop_key}")
        server.append(pop_key)
        #print(f"Server name: {pop_description}")
        server.append(pop_description)
        relays = pop_data.get("relays",[])
        for relay in relays:
            ipv4 = relay["ipv4"]
            all_ip.append(ipv4)
            #print(f"Ip: {ipv4}")
        if all_ip:
            server.append(all_ip)
            random_ip = random.choice(all_ip)
            server.append(random_ip)
            all_server.append(server)  # Only add servers that have IPs
        #else:
            #print("No IPs found for this server.")
        #if server:
            #print(server)
        #print("--------------------------------")
    if all_server:
        return all_server

def getPing(ip):
    print(f"Pinging {ip}...")
    try:
        # Use ping command with 3 packets and 5 second timeout
        result = subprocess.run(
            ['ping', '-c', '3', '-W', '5', ip],
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )
        
        if result.returncode == 0:
            # Parse the output to extract average ping time
            output = result.stdout
            # Look for the line with statistics (avg/min/max/mdev)
            avg_line = re.search(r'rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms', output)
            if avg_line:
                avg_ping = float(avg_line.group(2))
                print(f"Ping to {ip}: {avg_ping:.2f} ms")
                return avg_ping
            else:
                print(f"Could not parse ping result for {ip}")
                return None
        else:
            print(f"Ping failed for {ip}: {result.stderr.strip()}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"Ping timeout for {ip}")
        return None
    except (subprocess.CalledProcessError, OSError) as e:
        print(f"Error pinging {ip}: {e}")
        return None
    
    
    
data = serverData()
# Test pinging a few servers with their random IPs
print(f"Total servers found: {len(data)}")
for i, server in enumerate(data):  
    if len(server) >= 4:  # Ensure server has all elements [key, name, ip_list, random_ip]
        key, name, ip_list, random_ip = server
        print(f"Index: {i} ,Server Key: {key}, Name: {name}, IPs: {ip_list}, Random IP: {random_ip}")
