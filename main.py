#!/usr/bin/python3
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, Gio, GObject
import iptables_manager as iptbl
import request

class ServerData(GObject.Object):
    """GObject to hold server data for the list store"""
    
    def __init__(self, id, key, name, ip_list_str, random_ip, selected=False):
        super().__init__()
        self.id = id
        self.key = key
        self.name = name
        self.ip_list_str = ip_list_str
        self.random_ip = random_ip
        self.selected = selected
        self.background_color = "#202023"
        self.text_color = "white"

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
        
        # Create a Gio.ListStore for server data
        self.store = Gio.ListStore.new(ServerData)
        
        # Get server data and populate the store
        server_data = request.get_server_data()
        if server_data:
            for i, server in enumerate(server_data):
                if len(server) >= 4:
                    key, name, ip_list, random_ip = server
                    # Convert IP list to string for display
                    ip_list_str = ', '.join(ip_list) if ip_list else "No IPs"
                    # Create ServerData object and append to store
                    server_obj = ServerData(i, key, name, ip_list_str, random_ip, False)
                    self.store.append(server_obj)
        else:
            print("No server data available to display.")
            return

        # Create selection model
        self.selection_model = Gtk.NoSelection.new(self.store)
        
        # Create ColumnView
        column_view = Gtk.ColumnView.new(self.selection_model)
        
        # Apply CSS styling
        self.apply_rounded_corners_css(column_view)
        
        # Add columns to the ColumnView
        
        # ID Column
        id_factory = Gtk.SignalListItemFactory()
        id_factory.connect("setup", self.setup_id_column)
        id_factory.connect("bind", self.bind_id_column)
        id_column = Gtk.ColumnViewColumn.new("ID", id_factory)
        column_view.append_column(id_column)
        
        # Server Key Column
        key_factory = Gtk.SignalListItemFactory()
        key_factory.connect("setup", self.setup_key_column)
        key_factory.connect("bind", self.bind_key_column)
        key_column = Gtk.ColumnViewColumn.new("Server Key", key_factory)
        column_view.append_column(key_column)
        
        # Server Name Column
        name_factory = Gtk.SignalListItemFactory()
        name_factory.connect("setup", self.setup_name_column)
        name_factory.connect("bind", self.bind_name_column)
        name_column = Gtk.ColumnViewColumn.new("Server Name", name_factory)
        column_view.append_column(name_column)
        
        # Random IP Column
        ip_factory = Gtk.SignalListItemFactory()
        ip_factory.connect("setup", self.setup_ip_column)
        ip_factory.connect("bind", self.bind_ip_column)
        ip_column = Gtk.ColumnViewColumn.new("Random IP", ip_factory)
        column_view.append_column(ip_column)
        
        # Toggle Column
        toggle_factory = Gtk.SignalListItemFactory()
        toggle_factory.connect("setup", self.setup_toggle_column)
        toggle_factory.connect("bind", self.bind_toggle_column)
        toggle_column = Gtk.ColumnViewColumn.new("Action", toggle_factory)
        column_view.append_column(toggle_column)

        # Create a ScrolledWindow for the ColumnView to make it scrollable
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_child(column_view)
        
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

    # Column setup and bind methods for ColumnView
    def setup_id_column(self, factory, list_item):
        label = Gtk.Label()
        list_item.set_child(label)

    def bind_id_column(self, factory, list_item):
        label = list_item.get_child()
        server = list_item.get_item()
        label.set_text(str(server.id))

    def setup_key_column(self, factory, list_item):
        label = Gtk.Label()
        list_item.set_child(label)

    def bind_key_column(self, factory, list_item):
        label = list_item.get_child()
        server = list_item.get_item()
        label.set_text(server.key)

    def setup_name_column(self, factory, list_item):
        label = Gtk.Label()
        list_item.set_child(label)

    def bind_name_column(self, factory, list_item):
        label = list_item.get_child()
        server = list_item.get_item()
        label.set_text(server.name)

    def setup_ip_column(self, factory, list_item):
        label = Gtk.Label()
        list_item.set_child(label)

    def bind_ip_column(self, factory, list_item):
        label = list_item.get_child()
        server = list_item.get_item()
        label.set_text(server.random_ip)

    def setup_toggle_column(self, factory, list_item):
        toggle = Gtk.CheckButton()
        toggle.connect("toggled", self.on_toggle_toggled)
        list_item.set_child(toggle)

    def bind_toggle_column(self, factory, list_item):
        toggle = list_item.get_child()
        server = list_item.get_item()
        toggle.set_active(server.selected)
        toggle.server_data = server  # Store reference to server data

    # Toggle all servers between selected and unselected state
    def on_toggle_all_clicked(self, button):
        """Toggle all servers between selected and unselected state"""
        if not self.store:
            return
            
        # Check if any items are currently selected
        has_selected = False
        for i in range(self.store.get_n_items()):
            server = self.store.get_item(i)
            if server.selected:
                has_selected = True
                break
        
        # If any are selected, unselect all. If none are selected, select all
        new_state = not has_selected
        
        for i in range(self.store.get_n_items()):
            server = self.store.get_item(i)
            server.selected = new_state
            # Update row color based on selection state
            if new_state:
                server.background_color = "lightcoral"  # Background color when selected
                server.text_color = "black"            # Text color when selected
            else:
                server.background_color = "#202023"     # Default background color
                server.text_color = "white"             # Default text color
        
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
    def on_toggle_toggled(self, widget):
        # Get the server data from the widget
        server = getattr(widget, 'server_data', None)
        if not server:
            return
            
        # Toggle the state
        server.selected = widget.get_active()
        
        # Update row color based on selection state
        if server.selected:
            server.background_color = "lightcoral"  # Background color when selected
            server.text_color = "black"             # Text color when selected
        else:
            server.background_color = "#202023"     # Default background color
            server.text_color = "white"             # Default text color
        
        print(f"Toggle button state changed for server {server.id}: {server.selected}")
        print(f"Selected server: {server.name} ({server.key}) - IP: {server.random_ip}")
        
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
        total_count = self.store.get_n_items()
        
        for i in range(total_count):
            server = self.store.get_item(i)
            if server.selected:
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
        for i in range(self.store.get_n_items()):
            server = self.store.get_item(i)
            if server.selected:
                server_info = {
                    'id': server.id,
                    'key': server.key,
                    'name': server.name,
                    'ip_addresses': server.ip_list_str,
                    'random_ip': server.random_ip,
                    'selected': server.selected
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
     
    # Add CSS for rounded corners to the ColumnView   
    def apply_rounded_corners_css(self, column_view):
        """Apply CSS for rounded corners to the ColumnView"""
        css_provider = Gtk.CssProvider()
        css = """
        columnview {
            border-radius: 12px;
            border: 2px solid #404040;
            background: #202023;
        }
        
        """
        css_provider.load_from_data(css.encode('utf-8'))
        
        # Apply the CSS to the ColumnView
        column_view.get_style_context().add_provider(
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
        
        for i in range(self.store.get_n_items()):
            server = self.store.get_item(i)
            if server.selected:  # Selected servers
                # Convert IP addresses string back to list for iptables manager
                ip_addresses = server.ip_list_str.split(', ') if server.ip_list_str != "No IPs" else []
                server_data = [server.key, server.name, ip_addresses, server.random_ip]  # [key, name, ip_list, random_ip]
                selected_servers_to_block.append(server_data)
                print(f"Blocking server: {server.name} ({server.key}) - IP: {ip_addresses}")
            else:  # Unselected servers
                # Convert IP addresses string back to list for iptables manager
                ip_addresses = server.ip_list_str.split(', ') if server.ip_list_str != "No IPs" else []
                server_data = [server.key, server.name, ip_addresses, server.random_ip]  # [key, name, ip_list, random_ip]
                selected_servers_to_unblock.append(server_data)
                print(f"Unblocking server: {server.name} ({server.key}) - IP: {ip_addresses}")

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
