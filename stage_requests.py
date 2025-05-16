import requests
from bottle import response

FOH_API_URL = "http://localhost:5000"

def fetch_channel_list_from_server():
    try:
        response = requests.get(f"{FOH_API_URL}/channel_list")
        if response.status_code == 200:
            channel_list = response.json()
            print("Channel List received:", response.json())
            for ch, info in channel_list.items():
                print(f"{ch}: {info}")
            return channel_list
        else:
            print(f"Failed to get channel list: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to FPH server: {e}")

def send_channel_list_update(updated_list):
    try:
        response = requests.post(f"{FOH_API_URL}/update_channel_list", json=updated_list)
        if response.status_code == 200:
            print("Update sent successfully")
            return True
        else:
            print(f"Failed to send update: {response.status_code}, {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to FOH server: {e}")
        return False

if __name__ == "__main__":
    fetch_channel_list_from_server()