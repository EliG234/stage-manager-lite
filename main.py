from mic_inventory import MicInventory
from show_manager import ShowManager
from stagebox_manager import StageBoxManager
import os

def send_update(message):
    print(f"[UPDATE SENT]: {message}")

def main_menu():
    print("\nWelcome to Channel List Manager!")
    print("Please select user type:")
    print("1. FOH")
    print("2. Stage Manager")
    print("3. Exit")
    return input("Enter # of choice: ").strip()


def user_menu():
    print("Main Menu:")
    print("1. Mic Inventory")
    print("2. Stagebox Manager")
    print("3. Save Show")
    print("4. Load Show")
    print("5. Exit")
    return input("Enter # of choice: ").strip()

def mic_inventory_menu():
    print("\nMic Inventory")
    print("1. View Mic List")
    print("2. Back")
    return input("Enter # of choice: ").strip()

def stagebox_menu():
    print("\nStagebox Manager")
    print("1. View Stagebox List")
    print("2. Back")
    return input("Enter # of choice: ").strip()

def run_cli():
    mic_inventory = MicInventory()
    stagebox_manager = StageBoxManager()
    show_manager = ShowManager()

    while True:
        user = main_menu()
        if user == "1" or user == "2":
            break
        elif user == "3":
            print("Goodbye!")
            return
        else:
            print(" Invalid choice. Please try again...")

    while True:
        choice = user_menu()

        if choice == "1":
            while True:
                mic_choice = mic_inventory_menu()
                if mic_choice == "1":
                    print("Mic Inventory:")
                    for model, count in mic_inventory.inventory.items():
                        print(f"{model}: {count}")
                elif mic_choice == "2":
                    break
                else:
                    print(" Invalid choice. Please try again...")

        elif choice == "2":
            while True:
                sb_choice = stagebox_menu()
                if sb_choice == "1":
                    print("Stagebox List:")
                    stagebox_manager.view_stagebox_list()
                elif sb_choice == "2":
                    break
                else:
                    print(" Invalid choice. Please try again...")

        elif choice == "3":
           show_name = input("Enter show name: ").strip()
           show_manager.save_show(show_name, mic_inventory, stagebox_manager)
           send_update("Show saved")

        elif choice == "4":
            show_files = [
                f for f in os.listdir(show_manager.base_path)
                if f.endswith(".json")
            ]

            if not show_files:
                print("No saved shows found.")
                continue

            print("\nAvailable shows:")
            for idx, filename in enumerate(show_files, 1):
                print(f"{idx}. {filename}")

            try:
                selected = int(input("Select a show to load (by number): ").strip())
                if 1 <= selected <= len(show_files):
                    show_name = show_files[selected - 1].replace(".json", "")
                    show_manager.load_show(show_name, mic_inventory, stagebox_manager)
                    send_update(f"'{show_name}' loaded.")
                else:
                    print("Invalid selection.")

            except ValueError:
                print("Please enter a valid number.")

        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again...")

if __name__ == "__main__":
    run_cli()
