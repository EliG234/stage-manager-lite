import json
import os


def convert_sets_to_lists(obj):
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {key: convert_sets_to_lists(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_sets_to_lists(item) for item in obj]
    return obj

class ShowManager:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_path = os.path.join(script_dir, "Data", "Saved Shows")

        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def save_show(self, show_name, mic_inventory, stagebox_manager, input_list, output_list):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        # Convert mic_inventory to dictionary
        mic_inventory_dict = mic_inventory.to_dict()

        # Convert stagebox Data, inputs, and outputs using the helper function
        stageboxes = convert_sets_to_lists(stagebox_manager.stageboxes)  # Use the correct function here
        inputs = convert_sets_to_lists(input_list)
        outputs = convert_sets_to_lists(output_list)

        # Debugging: Print the types of each part to check for any sets
        print(f"mic_inventory_dict type: {type(mic_inventory_dict)}")
        print(f"stageboxes type: {type(stageboxes)}")
        print(f"inputs type: {type(inputs)}")
        print(f"outputs type: {type(outputs)}")

        # Prepare the final Data dictionary
        data = {
            "mic_inventory": mic_inventory_dict,
            "stageboxes": stageboxes,
            "inputs": inputs,
            "outputs": outputs
        }

        # Debugging: Check if any sets remain
        print(f"Data after conversion: {data}")

        # Save the Data to a JSON file
        path = os.path.join(self.base_path, f"{show_name}.json")
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Show Data saved to {path}")

    def load_show(self, show_name, mic_inventory, stagebox_manager, input_list, output_list):
        path = os.path.join(self.base_path, f"{show_name}.json")
        if not os.path.isfile(path):
            print(f"Show file '{path}' does not exist.")
            return None

        try:
            with open(path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error reading JSON from {path}: {e}")
            return None

        mic_inventory.load_inventory(data.get("mic_inventory", {}))

        stagebox_manager.stageboxes.clear()
        stagebox_manager.stageboxes.update(data.get("stageboxes", {}))

        input_list.clear()
        input_list.extend(data.get("inputs", []))

        output_list.clear()
        output_list.extend(data.get("outputs", []))

        print(f"Show Data loaded from {path}")

        return data
