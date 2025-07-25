import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
import os
import subprocess

class ourwindow(Gtk.ApplicationWindow):

    def __init__(self, application):
        super().__init__(application=application, title="Demonstration of PyObject GUI Application Creation")
        self.set_default_size(1920, 1080)

        # Correct button creation for GTK 4
        button1 = Gtk.Button.new_with_label("Execute")
        button1.set_size_request(100, 50)
        button1.set_halign(Gtk.Align.CENTER)
        button1.set_valign(Gtk.Align.CENTER)
        button1.set_css_classes(["button", "secondary"])
        button1.set_tooltip_text("Click this button to execute a command with elevated privileges")
        button1.connect("clicked", self.whenbutton1_clicked)
        
        # create a table view with test data
        # Create a ListStore with test data
        store = Gtk.ListStore(int, str, str, bool)
        store.append([1, "Server 1", "20ms", False])
        store.append([2, "Server 2", "30ms", False])
        store.append([3, "Server 3", "40ms", False])

        # Create a TreeView and set its model
        tree = Gtk.TreeView(model=store)

        # Add columns to the TreeView
        renderer_text = Gtk.CellRendererText()

        column_id = Gtk.TreeViewColumn("Id", renderer_text, text=0)
        tree.append_column(column_id)

        column_author = Gtk.TreeViewColumn("Server Name", renderer_text, text=1)
        tree.append_column(column_author)

        column_price = Gtk.TreeViewColumn("Ping", renderer_text, text=2)
        tree.append_column(column_price)

        # Add a button column to the TreeView
        # Use Gtk.CellRendererToggle for the toggle button column
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_toggle_toggled, store)

        column_toggle = Gtk.TreeViewColumn("Action", renderer_toggle, active=3)
        tree.append_column(column_toggle)

        # Add the TreeView to the box
  

        # Create a vertical box container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_vexpand(True)
        vbox.set_hexpand(True)


        # Add the TreeView to the box after the button
        vbox.append(tree)
        vbox.append(button1)

        # Center the TreeView
        tree.set_size_request(800, 600)
        tree.set_halign(Gtk.Align.CENTER)
        tree.set_valign(Gtk.Align.CENTER)

        # Center the button
        button1.set_halign(Gtk.Align.CENTER)
        button1.set_valign(Gtk.Align.CENTER)

        # Set the box as the child of the window
        self.set_child(vbox)

    def whenbutton1_clicked(self, button):
        try:
            command = ["pkexec", "echo", "Hello, World!"]
            output = subprocess.check_output(
                command,
                text=True,
                stderr=subprocess.STDOUT,
                env=os.environ.copy()
            )
            print(f"Command output: {output}")
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}: {e.output}")
        except FileNotFoundError:
            print("pkexec not found. Please ensure it is installed.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            print("Success")

    def on_toggle_toggled(self, widget, path, store):
        # Toggle the state of the button for the selected row
        store[path][3] = not store[path][3]
        print(f"Toggle button state changed for row {path}: {store[path][3]}")

class MyApp(Gtk.Application):

    def __init__(self):
        super().__init__(application_id="com.example.myapp")

    def do_activate(self):
        win = ourwindow(self)
        win.present()


app = MyApp()
app.run()
