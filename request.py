#!/usr/bin/python3
import requests
import os
import json
import random

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
        print(f"Server key: {pop_key}")
        server.append(pop_key)
        print(f"Server name: {pop_description}")
        server.append(pop_description)
        relays = pop_data.get("relays",[])
        for relay in relays:
            ipv4 = relay["ipv4"]
            all_ip.append(ipv4)
            print(f"Ip: {ipv4}")
        if all_ip:
            server.append(all_ip)
            random_ip = random.choice(all_ip)
            print(f"Random ip in list: {random_ip}")
        else:
            print("No IPs found for this server.")
        if server:
            print(server)
        print("--------------------------------")
        all_server.append(server)
    if all_server:
        return all_server

data= serverData()
for item in data:
          print(f"Server in array: {item}")
