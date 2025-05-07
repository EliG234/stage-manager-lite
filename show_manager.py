import json
import os

class ShowManager:
    def __init__(self):
        self.base_path = "Data"

    def save_show(self, show_name, mic_inventory, stagebox_manager):
        data = {
            "mic_inventory": mic_inventory.to_dict(),
            "stagebox_manager": {
                "inputs": list(stagebox_manager.stageboxes),
            }
        }
        path = os.path.join(self.base_path, f"{show_name}.json")
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Show data saved to {path}")

    def load_show(self, show_name, mic_inventory, stagebox_manager):
        path = os.path.join(self.base_path, f"{show_name}.json")
        with open(path, "r") as f:
            data = json.load(f)

        mic_inventory.load_inventory(data["mic_inventory"])

        # Load stagebox data only
        stagebox_manager.stageboxes.clear()
        for stagebox_name in data["stagebox_manager"]["inputs"]:
            if isinstance(stagebox_name, str):
                stagebox_data = {
                    "name": stagebox_name,
                    "inputs": 4,  # Default number of inputs
                    "outputs": 2  # Default number of outputs
                }
                stagebox_manager.stageboxes[stagebox_name] = stagebox_data
            else:
                print(f"Invalid data found in stagebox manager: {stagebox_name}")
        print("Show data loaded successfully.")
