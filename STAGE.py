import socket
import json
import tkinter as tk
from tkinter import simpledialog

class STAGEClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.channel_list = {}

    def connect_to_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))

            # Receive the initial channel list
            self.receive_channel_list(client_socket)

            # Create GUI for STAGE
            self.create_gui(client_socket)

    def receive_channel_list(self, client_socket):
        data = client_socket.recv(1024)
        self.channel_list = json.loads(data.decode())

    def send_channel_list(self, client_socket):
        updated_data = json.dumps(self.channel_list)
        client_socket.sendall(updated_data.encode())

    def create_gui(self, client_socket):
        # GUI setup
        root = tk.Tk()
        root.title("STAGE Manager")

        def load_show():
            # Ask user for show name to load
            show_name = simpledialog.askstring("Input", "Enter show name to load:")
            self.receive_channel_list(client_socket)  # Receive new data from the server
            self.display_channel_list()

        def save_show():
            # Ask user for show name to save
            show_name = simpledialog.askstring("Input", "Enter show name to save:")
            self.send_channel_list(client_socket)
            print(f"Show {show_name} saved on FOH")

        def display_channel_list():
            # Display the channel list in the GUI
            for widget in frame.winfo_children():
                widget.destroy()
            for channel, details in self.channel_list.items():
                label = tk.Label(frame, text=f"{channel}: {details}")
                label.pack()

        # Frame to hold the channel list
        frame = tk.Frame(root)
        frame.pack()

        # Load and Save buttons
        load_button = tk.Button(root, text="Load Show", command=load_show)
        load_button.pack()
        save_button = tk.Button(root, text="Save Show", command=save_show)
        save_button.pack()

        display_channel_list()  # Display the current list

        root.mainloop()


# Run the client
stage_client = STAGEClient()
stage_client.connect_to_server()
