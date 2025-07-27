import requests 
import os
import json
def get_server_info(api='https://api.steampowered.com/ISteamApps/GetSDRConfig/v1/?appid=730'):
        print("Get server list")
        try:
            response = requests.get(api, timeout=20)
            response.raise_for_status()  # Raise an exception for bad status codes
            server_info_json = response.json()
            print("Successfully fetched server info.")
            return server_info_json
        except requests.exceptions.RequestException as e:
            print(f"Error fetching server info: {e}")
            return None
server_info = json.load(get_server_info())
for server in server_info:
    print(server)
