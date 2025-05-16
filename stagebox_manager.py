class StageBoxManager:
    def __init__(self):
        self.stageboxes = {
            "SB1": {"inputs": ["I1", "I2", "I3", "I4"], "outputs": ["O1", "O2"]},
            "SB2": {"inputs": ["I1", "I2", "I3", "I4"], "outputs": ["O1", "O2"]},
            "SB3": {"inputs": ["I1", "I2", "I3", "I4"], "outputs": ["O1", "O2"]},
            "SB4": {"inputs": ["I1", "I2", "I3", "I4"], "outputs": ["O1", "O2"]}
        }

    def view_stagebox_list(self):
        if not self.stageboxes:
            print("No stageboxes found.")
        else:
            for name, data in self.stageboxes.items():
                available_inputs = len(data["inputs"])
                available_outputs = len(data["outputs"])
                print(f"Stagebox: {name}, Inputs: {available_inputs}, Outputs: {available_outputs}")

    def available_input(self, stagebox, input_num):
        # Check if input exists and is not already in use
        if stagebox in self.stageboxes:
            input_label = f"{stagebox}-I{input_num}"
            return input_label not in self.get_all_input_labels()  # Check if it's available
        return False

    def available_output(self, stagebox, output_num):
        # Check if output exists and is not already in use
        if stagebox in self.stageboxes:
            output_label = f"{stagebox}-O{output_num}"
            return output_label not in self.get_all_output_labels()  # Check if it's available
        return False

    def used_input(self, stagebox, input_num):
        # Directly assign input, no checking needed.
        return f"{stagebox}-I{input_num}" in self.get_all_input_labels()

        total = self.stageboxes[stagebox]["outputs"]["total"]
        used = self.stageboxes[stagebox]["outputs"]["used"]

        if used < total:
            return True
        else:
            print(f"No available outputs on {stagebox}")
            return False

    def mark_used_output(self, stagebox, output_num):
        # Directly use output without tracking it.
        return f"{stagebox}-O{output_num}" in self.get_all_output_labels()

    def release_output(self, stagebox, output_num):
        if stagebox in self.stageboxes and self.stageboxes[stagebox]["outputs"]['used'] > 0:
            self.stageboxes[stagebox]["outputs"]['used'] -= 1
            print(f"Released one output from {stagebox}: now {self.stageboxes[stagebox]["outputs"]['used']} used out of {self.stageboxes[stagebox]["outputs"]['total']}")
            return True
        else:
            print(f"Output from {stagebox} cannot be released or is already empty!")
            return False

    def get_all_input_labels(self):
        input_labels = []
        for stagebox in self.stageboxes:
            for input_label in self.stageboxes[stagebox]["inputs"]:
                input_labels.append(f"{stagebox}-{input_label}")
        return input_labels

    def get_all_output_labels(self):
        output_labels = []
        for stagebox in self.stageboxes:
            for output_label in self.stageboxes[stagebox]["outputs"]:
                output_labels.append(f"{stagebox}-{output_label}")
        return output_labels

