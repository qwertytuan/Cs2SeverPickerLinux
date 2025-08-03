#!/usr/bin/python3
import gi
gi.require_version('Gtk', '4.0')
<<<<<<< Updated upstream
from gi.repository import Gtk, Gdk
=======
from gi.repository import Gtk, GLib
>>>>>>> Stashed changes
import os
import subprocess
import requests
import random
import re
import asyncio
import threading

class ourwindow(Gtk.ApplicationWindow):

    def __init__(self, application):
        super().__init__(application=application, title="CS2 Server Picker Linux")
        self.set_default_size(1200, 800)
        self.getServerInfo()

        # Correct button creation for GTK 4
        self.toggle_all_button = Gtk.Button.new_with_label("Select All")
        self.toggle_all_button.set_size_request(120, 50)
        self.toggle_all_button.set_halign(Gtk.Align.CENTER)
        self.toggle_all_button.set_valign(Gtk.Align.CENTER)
        self.toggle_all_button.set_css_classes(["button", "secondary"])
        self.toggle_all_button.set_tooltip_text("Click to select/unselect all servers")
        self.toggle_all_button.connect("clicked", self.on_toggle_all_clicked)
        
        # Store reference to the store for the toggle all functionality
        self.store = None
        
        # create a table view with test data
        # Create a ListStore with test data (all string columns except id and boolean)
<<<<<<< Updated upstream
        # Added a color column for row highlighting and text color
        store = Gtk.ListStore(int, str, str, str, str, bool, str, str)
=======
        store = Gtk.ListStore(int, str, str, str, str, str, bool)
>>>>>>> Stashed changes
        self.store = store  # Store reference for toggle all functionality
        server_data = self.serverData()
        if server_data:
            for i, server in enumerate(server_data):
                if len(server) >= 4:
                    key, name, ip_list, random_ip = server
                    # Convert IP list to string for display
                    ip_list_str = ', '.join(ip_list) if ip_list else "No IPs"
<<<<<<< Updated upstream
                    # Add row with default dark background and white text
                    store.append([i, key, name, ip_list_str, random_ip, False, "#202023", "white"])
=======
                    store.append([i, key, name, ip_list_str, random_ip, "N/A", False])
>>>>>>> Stashed changes
        else:
            print("No server data available to display.")
            return
    
        # Create a TreeView and set its model
        tree = Gtk.TreeView(model=store)
        
        # Make column separations more visible
        tree.set_grid_lines(Gtk.TreeViewGridLines.VERTICAL)
        tree.set_enable_tree_lines(True)
        
        # Add rounded corners using CSS
        self.apply_rounded_corners_css(tree)

        # Add columns to the TreeView
        renderer_text = Gtk.CellRendererText()

        column_id = Gtk.TreeViewColumn("Id", renderer_text, text=0, background=6, foreground=7)
        tree.append_column(column_id)

        column_key = Gtk.TreeViewColumn("Server Key", renderer_text, text=1, background=6, foreground=7)
        tree.append_column(column_key)

        column_name = Gtk.TreeViewColumn("Server Name", renderer_text, text=2, background=6, foreground=7)
        tree.append_column(column_name)
        
        column_random_ip = Gtk.TreeViewColumn("Random IP", renderer_text, text=4, background=6, foreground=7)
        tree.append_column(column_random_ip)

        column_ping = Gtk.TreeViewColumn("Ping (ms)", renderer_text, text=5)
        tree.append_column(column_ping)

        # Add a button column to the TreeView
        # Use Gtk.CellRendererToggle for the toggle button column
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_toggle_toggled, store)

<<<<<<< Updated upstream
        column_toggle = Gtk.TreeViewColumn("Action", renderer_toggle, active=5)
        column_toggle.add_attribute(renderer_toggle, "cell-background", 6)
=======
        column_toggle = Gtk.TreeViewColumn("Action", renderer_toggle, active=6)
>>>>>>> Stashed changes
        tree.append_column(column_toggle)

        # Create a ScrolledWindow for the TreeView to make it scrollable
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_child(tree)
        
        # Set size constraints for the scrolled window
        # 80% width of window and 50% height of window
        scrolled_window.set_size_request(int(1200 * 0.8), int(800 * 0.5))
        scrolled_window.set_halign(Gtk.Align.CENTER)
        scrolled_window.set_valign(Gtk.Align.START)

        # Create a vertical box container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_vexpand(True)
        vbox.set_hexpand(True)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)

        # Add the ScrolledWindow (containing TreeView) to the box
        vbox.append(scrolled_window)
        vbox.append(self.toggle_all_button)

        # Add Ping All button
        self.ping_all_button = Gtk.Button.new_with_label("Ping All Servers")
        self.ping_all_button.connect("clicked", self.on_ping_all_clicked)
        vbox.append(self.ping_all_button)

        # Center the button
        self.toggle_all_button.set_halign(Gtk.Align.CENTER)
        self.toggle_all_button.set_valign(Gtk.Align.CENTER)
        self.ping_all_button.set_halign(Gtk.Align.CENTER)
        self.ping_all_button.set_valign(Gtk.Align.CENTER)

        # Set the box as the child of the window
        self.set_child(vbox)

    def on_toggle_all_clicked(self, button):
        """Toggle all servers between selected and unselected state"""
        if not self.store:
            return
            
        # Check if any items are currently selected
        has_selected = False
        for row in self.store:
            if row[6]:  # Check the boolean column (index 6)
                has_selected = True
                break
        
        # If any are selected, unselect all. If none are selected, select all
        new_state = not has_selected
        
        for row in self.store:
<<<<<<< Updated upstream
            row[5] = new_state
            # Update row color based on selection state
            if new_state:
                row[6] = "lightcoral"  # Background color when selected
                row[7] = "black"       # Text color when selected
            else:
                row[6] = "#202023"     # Default background color
                row[7] = "white"       # Default text color
=======
            row[6] = new_state
>>>>>>> Stashed changes
        
        # Update button text based on current state
        if new_state:
            self.toggle_all_button.set_label("Unselect All")
            print("All servers selected")
        else:
            self.toggle_all_button.set_label("Select All")
            print("All servers unselected")
        
        # Print all selected rows
        self.print_selected_servers()


    def on_toggle_toggled(self, widget, path, store):
        # Toggle the state of the button for the selected row
<<<<<<< Updated upstream
        store[path][5] = not store[path][5]
        # Update row color based on selection state
        if store[path][5]:
            store[path][6] = "lightcoral"  # Background color when selected
            store[path][7] = "black"       # Text color when selected
        else:
            store[path][6] = "#202023"     # Default background color
            store[path][7] = "white"       # Default text color
        
        print(f"Toggle button state changed for row {path}: {store[path][5]}")
=======
        store[path][6] = not store[path][6]
        print(f"Toggle button state changed for row {path}: {store[path][6]}")
>>>>>>> Stashed changes
        # Get server info for this row
        server_key = store[path][1]
        server_name = store[path][2]
        random_ip = store[path][4]
        print(f"Selected server: {server_name} ({server_key}) - IP: {random_ip}")
        
        # Update the toggle all button text based on current selection state
        self.update_toggle_all_button_text()
        
        # Print all selected rows when individual toggle changes
        self.print_selected_servers()
        
    
    def update_toggle_all_button_text(self):
        """Update the toggle all button text based on current selection state"""
        if not self.store:
            return
            
        selected_count = 0
        total_count = len(self.store)
        
        for row in self.store:
            if row[6]:  # Check the boolean column (index 6)
                selected_count += 1
        
        if selected_count == 0:
            self.toggle_all_button.set_label("Select All")
        elif selected_count == total_count:
            self.toggle_all_button.set_label("Unselect All")
        else:
            self.toggle_all_button.set_label(f"Unselect ({selected_count}/{total_count})")

    def print_selected_servers(self):
        """Print all currently selected servers"""
        if not self.store:
            return
        
        selected_servers = []
        for row in self.store:
            if row[6]:  # Check if selected (boolean column index 6)
                server_info = {
                    'id': row[0],
                    'key': row[1],
                    'name': row[2],
                    'ip_addresses': row[3],
                    'random_ip': row[4],
                    'ping': row[5],
                    'selected': row[6]
                }
                selected_servers.append(server_info)
        
        print(f"\n=== SELECTED SERVERS ({len(selected_servers)}) ===")
        if selected_servers:
            for server in selected_servers:
                print(f"ID: {server['id']}")
                print(f"  Key: {server['key']}")
                print(f"  Name: {server['name']}")
                print(f"  Random IP: {server['random_ip']}")
                print(f"  Ping: {server['ping']}")
                print(f"  All IPs: {server['ip_addresses']}")
                print("  ---")
        else:
            print("No servers currently selected")
        print("=" * 40)
        
    def apply_rounded_corners_css(self, tree):
        """Apply CSS for rounded corners to the TreeView"""
        css_provider = Gtk.CssProvider()
        css = """
        treeview {
            border-radius: 12px;
            border: 2px solid #404040;
            background: #202023;
        }
        
        """
        css_provider.load_from_data(css.encode('utf-8'))
        
        # Apply the CSS to the TreeView
        tree.get_style_context().add_provider(
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
    
    def getServerInfo(self, api='https://api.steampowered.com/ISteamApps/GetSDRConfig/v1/?appid=730'):
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

    def serverData(self):
        server_info = self.getServerInfo()
        all_server = []
        # Clean the information to servers datas
        if not server_info or "pops" not in server_info:
            return None
        pops = server_info["pops"]
        for pop_key, pop_data in pops.items():
            all_ip = []
            server = []
            pop_description = pop_data.get("desc", "N/A")
            server.append(pop_key)
            server.append(pop_description)
            relays = pop_data.get("relays", [])
            for relay in relays:
                ipv4 = relay.get("ipv4")
                if ipv4:
                    all_ip.append(ipv4)
            if all_ip:
                server.append(all_ip)
                random_ip = random.choice(all_ip)
                server.append(random_ip)
                all_server.append(server)  # Only add servers that have IPs
        if all_server:
            return all_server

    # --- Start of new/modified methods for async ping ---

    def on_ping_all_clicked(self, button):
        """Handler for the 'Ping All Servers' button."""
        ips = [row[4] for row in self.store]
        
        def run_async_pings_in_thread():
            """Runs the asyncio event loop in a separate thread."""
            async def get_pings(ips):
                """Gathers all async ping tasks."""
                tasks = [self.get_ping_async(ip) for ip in ips]
                return await asyncio.gather(*tasks)

            # Run the async function and get results
            results = asyncio.run(get_pings(ips))
            
            # Schedule UI update on the main GTK thread
            GLib.idle_add(self.update_ping_results, results)

        # Create and start the thread
        ping_thread = threading.Thread(target=run_async_pings_in_thread)
        ping_thread.daemon = True  # Allows main program to exit even if thread is running
        ping_thread.start()

    def update_ping_results(self, results):
        """Updates the ListStore with ping results on the main thread."""
        ip_to_ping = {ip: ping for ip, ping in results}
        for row in self.store:
            ip = row[4]
            ping = ip_to_ping.get(ip)
            if ping is not None:
                row[5] = f"{ping:.2f}"
            else:
                row[5] = "Failed"
        print("Ping results updated in the UI.")

    async def get_ping_async(self, ip):
        """Asynchronously pings a single IP address and returns the average ping time."""
        print(f"Pinging {ip}...")
        try:
            proc = await asyncio.create_subprocess_exec(
                'ping', '-c', '3', '-W', '5', ip,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10)

            if proc.returncode == 0:
                output = stdout.decode()
                avg_line = re.search(r'rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms', output)
                if avg_line:
                    avg_ping = float(avg_line.group(2))
                    print(f"Ping to {ip}: {avg_ping:.2f} ms")
                    return ip, avg_ping
                else:
                    print(f"Could not parse ping result for {ip}")
                    return ip, None
            else:
                print(f"Ping failed for {ip}: {stderr.decode().strip()}")
                return ip, None
        except asyncio.TimeoutError:
            print(f"Ping timeout for {ip}")
            return ip, None
        except (subprocess.CalledProcessError, OSError) as e:
            print(f"Error pinging {ip}: {e}")
            return ip, None
    

class MyApp(Gtk.Application):

    def __init__(self):
        super().__init__(application_id="com.example.myapp")

    def do_activate(self):
        win = ourwindow(self)
        win.present()


app = MyApp()
app.run()
