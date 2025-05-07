import socket
import json
import os

class FOHServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.channel_list = {}  # Channel data to be sent to the STAGE

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
            print("FOH server started. Waiting for STAGE to connect...")

            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")

                # Send the initial channel list to the client
                self.send_channel_list(conn)

                # Wait for the STAGE to send updates
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    self.handle_client_update(data)
                    print("Updated channel list received.")
                    self.send_channel_list(conn)

    def send_channel_list(self, conn):
        # Send current channel list as a JSON object
        channel_data = json.dumps(self.channel_list)
        conn.sendall(channel_data.encode())

    def handle_client_update(self, data):
        # Handle the incoming data from the client (STAGE)
        updated_data = json.loads(data.decode())
        self.channel_list = updated_data  # Update the channel list with the new data

    def save_show(self, show_name):
        # Save the current channel list to a file
        with open(f"Data/{show_name}.json", "w") as file:
            json.dump(self.channel_list, file)
        print(f"Show {show_name} saved.")

    def load_show(self, show_name):
        # Load the channel list from a file
        try:
            with open(f"Data/{show_name}.json", "r") as file:
                self.channel_list = json.load(file)
            print(f"Show {show_name} loaded.")
        except FileNotFoundError:
            print(f"Error: {show_name} not found.")


# Run the server
foh_server = FOHServer()
foh_server.start_server()
