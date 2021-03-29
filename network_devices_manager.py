import tkinter as tk
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

        default_font = tk.font.nametofont("TkFixedFont")
        default_font.configure(size=8)

        # Define graphic elements
        self.master = master
        self.master.option_add("*Font", default_font)
        self.master.title("Imperium - Tools - Network Devices Manager")

        self.label_functions = tk.Label(master, text="Device commands")

        self.entry_host = tk.Entry(master, textvariable=self.host)
        self.entry_name = tk.Entry(master, textvariable=self.device_name)
        self.entry_username = tk.Entry(master, textvariable=self.username)
        self.entry_password = tk.Entry(master, textvariable=self.password)

        self.button_add_device = tk.Button(master, text="Add", command=self.add_device)
        self.button_refresh_status = tk.Button(master, text="Refresh", command=self.refresh_status)
        self.button_connect = tk.Button(master, text="Connect", command=self.login)
        self.button_remove_device = tk.Button(master, text="Delete", command=self.remove_device)
        self.button_exec_1 = tk.Button(master, text="Show run", command=self.show_runn_config)
        self.button_exec_2 = tk.Button(master, text="Show interfaces", command=self.show_runn_config)
        self.button_exec_3 = tk.Button(master, text="Show details", command=self.show_runn_config)
        self.button_exec_4 = tk.Button(master, text="Show version", command=self.show_runn_config)
        self.button_exec_5 = tk.Button(master, text="Show hardware", command=self.show_runn_config)
        self.button_exec_6 = tk.Button(master, text="Backup run", command=self.show_runn_config)
        self.button_exec_7 = tk.Button(master, text="Backup startup", command=self.show_runn_config)

        self.scroll_devices = tk.Scrollbar(master)

        self.list_devices = tk.Listbox(master, selectmode=tk.SINGLE, xscrollcommand=self.scroll_devices.set)

        # Stick elements to the window
        self.label_functions.grid(row=0, column=5, sticky=tk.W+tk.E)

        self.entry_host.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.entry_name.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.entry_username.grid(row=7, column=0, sticky=tk.W+tk.E)
        self.entry_password.grid(row=7, column=1, sticky=tk.W+tk.E)

        self.button_add_device.grid(row=0, column=2, sticky=tk.W+tk.E)
        self.button_refresh_status.grid(row=0, column=3, sticky=tk.W+tk.E)
        self.button_connect.grid(row=7, column=2, sticky=tk.W+tk.E)
        self.button_remove_device.grid(row=7, column=3, sticky=tk.W+tk.E)
        self.button_exec_1.grid(row=1, column=5, sticky=tk.W+tk.E)
        self.button_exec_2.grid(row=2, column=5, sticky=tk.W+tk.E)
        self.button_exec_3.grid(row=3, column=5, sticky=tk.W+tk.E)
        self.button_exec_4.grid(row=4, column=5, sticky=tk.W+tk.E)
        self.button_exec_5.grid(row=5, column=5, sticky=tk.W+tk.E)
        self.button_exec_6.grid(row=6, column=5, sticky=tk.W+tk.E)
        self.button_exec_7.grid(row=7, column=5, sticky=tk.W+tk.E)

        self.scroll_devices.grid(row=1, column=3, rowspan=6, sticky=tk.N+tk.S)
        self.list_devices.grid(row=1, columnspan=3, rowspan=6, sticky=tk.W+tk.E)

        # Init state of GUI elements
        self.list_devices.insert(0, 'IP'.center(16) + 'NAME'.center(20) + 'STATUS'.center(12))

        # Define app variables
        self.devices = []

    def add_device (self):
        host = str(self.host.get())
        name = str(self.device_name.get())
        self.list_devices.insert(tk.END, host.ljust(16) + name.ljust(2))

        device = Device(host, name)
        self.devices.append(device)

    def refresh_status (self):
        pass   

    def login (self):
        selection = self.list_devices.curselection()
        if selection and selection[0] != 0:
            host = self.devices[selection[0] - 1].host
            username = self.username.get()
            password = self.password.get()

            self.client = Client(host, username, password)
            self.client._connect()
            return self.client

    def remove_device (self):
        selection = self.list_devices.curselection()
        if selection and selection[0] != 0:
            self.list_devices.delete(selection[0])
            self.devices.pop(selection[0] - 1)

    def show_runn_config (self):
        print(self.client.execute("show run"))

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()