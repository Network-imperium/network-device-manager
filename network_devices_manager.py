import json
import tkinter as tk
from datetime import datetime
from tkinter.font import Font
from ssh_executor import *

class Device:
    def __init__ (self, host, name):
        self.host = host
        self.name = name

class MainApp:
    def __init__ (self, master): 
        # Define Tk variables
        self.host = tk.StringVar(value="IPv4 address")
        self.device_name = tk.StringVar(value="Device name")
        self.username = tk.StringVar(value="Auth username")
        self.password = tk.StringVar(value="Password")
        self.command = tk.StringVar(value="Device commands")

        default_font = tk.font.nametofont("TkFixedFont")
        default_font.configure(size=8)

        # Define app variables
        self.current_device = None
        self.devices = []
        self.commands = ["Refresh", "Save run", "Save startup", "Save version", "Run terminal"]

        # Define graphic elements
        self.master = master
        self.master.option_add("*Font", default_font)
        self.master.title("Imperium - Tools - Network Devices Manager")

        self.entry_host = tk.Entry(master, textvariable=self.host)
        self.entry_name = tk.Entry(master, textvariable=self.device_name)
        self.entry_username = tk.Entry(master, textvariable=self.username)
        self.entry_password = tk.Entry(master, textvariable=self.password)

        self.button_add_device = tk.Button(master, text="Add", command=self.add_device)
        self.button_connect = tk.Button(master, text="Connect", command=self.login)
        self.button_remove_device = tk.Button(master, text="Delete", command=self.remove_device)

        self.scroll_devices = tk.Scrollbar(master)

        self.list_devices = tk.Listbox(master, selectmode=tk.SINGLE, xscrollcommand=self.scroll_devices.set)

        self.menu_commands = tk.OptionMenu(master, self.command, *self.commands)

        # Stick elements to the window
        self.entry_host.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.entry_name.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.entry_username.grid(row=7, column=0, sticky=tk.W+tk.E)
        self.entry_password.grid(row=7, column=1, sticky=tk.W+tk.E)

        self.button_add_device.grid(row=0, column=2, sticky=tk.W+tk.E)
        self.button_connect.grid(row=7, column=2, sticky=tk.W+tk.E)
        self.button_remove_device.grid(row=7, column=3, columnspan=2, ipadx="40px", sticky=tk.W+tk.E)

        self.scroll_devices.grid(row=1, column=4, rowspan=6, sticky=tk.N+tk.S)
        self.list_devices.grid(row=1, columnspan=4, rowspan=6, sticky=tk.W+tk.E)

        self.menu_commands.grid(row=0, column=3, columnspan=2, sticky=tk.W+tk.E)

        # Init state of GUI elements
        self.list_devices.insert(0, 'IP'.center(16) + 'NAME'.center(24) + 'STATUS'.center(14))
        self.command.trace("w", self.execute_command)
        self.load_config_json()

    def load_config_json (self):
        try:
            with open("ndm_config.json", "r+") as file:
                for device in json.loads(file.read()):
                    host = device['host']
                    name = device['name']
                    self.list_devices.insert(tk.END, host.ljust(16) + name.ljust(24))
                    
                    device = Device(host, name)
                    self.devices.append(device)
        except IOError:
            print("File not accessible")

    def update_config_json (self):
        with open("ndm_config.json", "w") as file:
            file.write(json.dumps([device.__dict__ for device in self.devices]))
            file.close()

    def add_device (self):
        host = str(self.host.get())
        name = str(self.device_name.get())
        self.list_devices.insert(tk.END, host.ljust(16) + name.ljust(24))

        device = Device(host, name)
        self.devices.append(device)

        self.update_config_json()

    def execute_command (self, *args):
        command = self.command.get()
        if command == self.commands[0]:
            self.refresh_status()

        if command == self.commands[1]:
            self.execute_save_run()
        
        self.command.set("Device commands")

    def login (self):
        selection = self.list_devices.curselection()
        if selection and selection[0] != 0:
            self.current_device = self.devices[selection[0] - 1]
            username = self.username.get()
            password = self.password.get()

            self.client = Client(self.current_device.host, username, password)
            self.client._connect()
            return self.client

    def remove_device (self):
        selection = self.list_devices.curselection()
        if selection and selection[0] != 0:
            self.list_devices.delete(selection[0])
            self.devices.pop(selection[0] - 1)

            self.update_config_json()

    def refresh_status (self):
        pass   

    def execute_save_run (self):
        if self.client:
            config = [lie.replace('\n', '') for line in self.client.execute("show run")]
            filename = self.current_device.name + '_' + str(datetime.now().date()).replace('-','')
            with open(filename, "w") as file:
                file.write(''.join(config))
                file.close()

