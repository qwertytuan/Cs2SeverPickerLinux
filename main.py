#!/usr/bin/python3
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk
import iptables_manager as iptbl
import request

class ServerPickerWindow(Gtk.ApplicationWindow):

    def __init__(self, application):
        super().__init__(application=application, title="CS2 Server Picker Linux")
        self.set_default_size(1200, 800)

        # Button to select/deselect all servers
        self.toggle_all_button = Gtk.Button.new_with_label("Select All")
        self.toggle_all_button.set_size_request(120, 50)
        self.toggle_all_button.set_halign(Gtk.Align.CENTER)
        self.toggle_all_button.set_valign(Gtk.Align.CENTER)
        self.toggle_all_button.set_css_classes(["button", "secondary"])
        self.toggle_all_button.set_tooltip_text("Click to select/unselect all servers")
        self.toggle_all_button.connect("clicked", self.on_toggle_all_clicked)
        
        # Button to block selected IPs
        self.block_selected_button = Gtk.Button.new_with_label("Block Selected IPs")
        self.block_selected_button.set_size_request(120, 50)
        self.block_selected_button.set_halign(Gtk.Align.CENTER)
        self.block_selected_button.set_valign(Gtk.Align.CENTER)
        self.block_selected_button.set_css_classes(["button", "secondary"])
        self.block_selected_button.set_tooltip_text("Click to block selected server IPs")
        self.block_selected_button.connect("clicked", self.on_block_selected_clicked)
        
        # Store reference to the store for the toggle all functionality
        self.store = None
        
        # create a table view with test data
        # Create a ListStore with test data (all string columns except id and boolean)
        # Added a color column for row highlighting and text color
        store = Gtk.ListStore(int, str, str, str, str, bool, str, str)
        self.store = store  # Store reference for toggle all functionality
        server_data = request.get_server_data()
        if server_data:
            for i, server in enumerate(server_data):
                if len(server) >= 4:
                    key, name, ip_list, random_ip = server
                    # Convert IP list to string for display
                    ip_list_str = ', '.join(ip_list) if ip_list else "No IPs"
                    # Add row with default dark background and white text
                    store.append([i, key, name, ip_list_str, random_ip, False, "#202023", "white"])
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

        # Add a button column to the TreeView
        # Use Gtk.CellRendererToggle for the toggle button column
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_toggle_toggled, store)

        column_toggle = Gtk.TreeViewColumn("Action", renderer_toggle, active=5)
        column_toggle.add_attribute(renderer_toggle, "cell-background", 6)
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
        vbox.append(self.block_selected_button)

        # Center the button
        self.toggle_all_button.set_halign(Gtk.Align.CENTER)
        self.toggle_all_button.set_valign(Gtk.Align.CENTER)

        self.block_selected_button.set_halign(Gtk.Align.CENTER)
        self.block_selected_button.set_valign(Gtk.Align.CENTER)

        # Set the box as the child of the window
        self.set_child(vbox)

    # Toggle all servers between selected and unselected state
    def on_toggle_all_clicked(self, button):
        """Toggle all servers between selected and unselected state"""
        if not self.store:
            return
            
        # Check if any items are currently selected
        has_selected = False
        for row in self.store:
            if row[5]:  # Check the boolean column (index 5)
                has_selected = True
                break
        
        # If any are selected, unselect all. If none are selected, select all
        new_state = not has_selected
        
        for row in self.store:
            row[5] = new_state
            # Update row color based on selection state
            if new_state:
                row[6] = "lightcoral"  # Background color when selected
                row[7] = "black"       # Text color when selected
            else:
                row[6] = "#202023"     # Default background color
                row[7] = "white"       # Default text color
        
        # Update button text based on current state
        if new_state:
            self.toggle_all_button.set_label("Unselect All")
            print("All servers selected")
        else:
            self.toggle_all_button.set_label("Select All")
            print("All servers unselected")
        
        # Print all selected rows
        self.print_selected_servers()

    # Toggle button handler for individual rows
    def on_toggle_toggled(self, widget, path, store):
        # Toggle the state of the button for the selected row
        store[path][5] = not store[path][5]
        # Update row color based on selection state
        if store[path][5]:
            store[path][6] = "lightcoral"  # Background color when selected
            store[path][7] = "black"       # Text color when selected
        else:
            store[path][6] = "#202023"     # Default background color
            store[path][7] = "white"       # Default text color
        
        print(f"Toggle button state changed for row {path}: {store[path][5]}")
        # Get server info for this row
        server_key = store[path][1]
        server_name = store[path][2]
        random_ip = store[path][4]
        print(f"Selected server: {server_name} ({server_key}) - IP: {random_ip}")
        
        # Update the toggle all button text based on current selection state
        self.update_toggle_all_button_text()
        
        # Print all selected rows when individual toggle changes
        self.print_selected_servers()

    # Update the toggle all button text based on current selection state
    def update_toggle_all_button_text(self):
        """Update the toggle all button text based on current selection state"""
        if not self.store:
            return
            
        selected_count = 0
        total_count = len(self.store)
        
        for row in self.store:
            if row[5]:  # Check the boolean column (index 5)
                selected_count += 1
        
        if selected_count == 0:
            self.toggle_all_button.set_label("Select All")
        elif selected_count == total_count:
            self.toggle_all_button.set_label("Unselect All")
        else:
            self.toggle_all_button.set_label(f"Unselect ({selected_count}/{total_count})")
    
    # Print all currently selected servers
    def print_selected_servers(self):
        """Print all currently selected servers"""
        if not self.store:
            return
        
        selected_servers = []
        for row in self.store:
            if row[5]:  # Check if selected (boolean column index 5)
                server_info = {
                    'id': row[0],
                    'key': row[1],
                    'name': row[2],
                    'ip_addresses': row[3],
                    'random_ip': row[4],
                    'selected': row[5]
                }
                selected_servers.append(server_info)
        
        print(f"\n=== SELECTED SERVERS ({len(selected_servers)}) ===")
        if selected_servers:
            for server in selected_servers:
                print(f"ID: {server['id']}")
                print(f"  Key: {server['key']}")
                print(f"  Name: {server['name']}")
                print(f"  Random IP: {server['random_ip']}")
                print(f"  All IPs: {server['ip_addresses']}")
                print("  ---")
        else:
            print("No servers currently selected")
        print("=" * 40)
     
    # Add CSS for rounded corners to the TreeView   
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
    
    # Block selected IPs using iptables
    def on_block_selected_clicked(self, button):
        """Block all selected server IPs using iptables"""
        if not self.store:
            print("No server data available to block.")
            return
        
        selected_servers_to_block = []
        selected_servers_to_unblock = []
        for row in self.store:
            if row[5]:  # Selected servers
                # Convert IP addresses string back to list for iptables manager
                ip_addresses = row[3].split(', ') if row[3] != "No IPs" else []
                server_data = [row[1], row[2], ip_addresses, row[4]]  # [key, name, ip_list, random_ip]
                selected_servers_to_block.append(server_data)
                print(f"Blocking server: {row[2]} ({row[1]}) - IP: {row[4]}")
            else:  # Unselected servers
                # Convert IP addresses string back to list for iptables manager
                ip_addresses = row[3].split(', ') if row[3] != "No IPs" else []
                server_data = [row[1], row[2], ip_addresses, row[4]]  # [key, name, ip_list, random_ip]
                selected_servers_to_unblock.append(server_data)
                print(f"Unblocking server: {row[2]} ({row[1]}) - IP: {row[4]}")

        if not selected_servers_to_block:
            print("No servers selected to block.")

        if not selected_servers_to_unblock:
            print("No servers selected to unblock.")
        
        # Block the selected servers using iptables
        if selected_servers_to_block:
            iptbl.block_ips_for_servers(selected_servers_to_block)
            print(f"Blocked {len(selected_servers_to_block)} servers")
                                            
        # Unblock the unselected servers using iptables
        if selected_servers_to_unblock:
            iptbl.unblock_ips_for_servers(selected_servers_to_unblock)
            print(f"Unblocked {len(selected_servers_to_unblock)} servers")


class Cs2ServerPickerApp(Gtk.Application):

    def __init__(self):
        super().__init__(application_id="com.example.cs2serverpicker")

    def do_activate(self):
        win = ServerPickerWindow(self)
        win.present()

app = Cs2ServerPickerApp()
app.run()
