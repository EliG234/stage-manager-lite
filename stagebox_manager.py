class StageBoxManager:
    def __init__(self):
        self.stageboxes = {
            "SB1": {
                "inputs": {"total": 4, "used": set()},
                "outputs": {"total": 2, "used": 0}
            },
            "SB2": {
                "inputs": {"total": 4, "used": set()},
                "outputs": {"total": 2, "used": 0}
            },
            "SB3": {
                "inputs": {"total": 4, "used": set()},
                "outputs": {"total": 2, "used": 0}
            },
            "SB4": {
                "inputs": {"total": 4, "used": set()},
                "outputs": {"total": 2, "used": 0}
            }
        }

    def view_stagebox_list(self):
        if not self.stageboxes:
            print("No stageboxes found.")
        else:
            for name, data in self.stageboxes.items():
                print(f"Stagebox: {name}, Inputs: {data['inputs']['total']}, Outputs: {data['outputs']['total']}")


    def available_input(self, stagebox, input_num):
        return (
            stagebox in self.stageboxes and
            0 < input_num <= self.stageboxes[stagebox]["inputs"]["total"] and
            input_num not in self.stageboxes[stagebox]["inputs"]["used"]
        )

    def used_input(self, stagebox, input_num):
        if self.available_input(stagebox, input_num):
            self.stageboxes[stagebox]["inputs"]["used"].add(input_num)
            used = len(self.stageboxes[stagebox]["inputs"]["used"])
            total = self.stageboxes[stagebox]["inputs"]["total"]
            print(f"Used {stagebox}-{input_num}: {used} used out of {total}")
            return True
        else:
            print(f"Input line {stagebox}-{input_num} not available!")
            return False

    def release_input(self, stagebox, input_num):
        if stagebox not in self.stageboxes:
            print(f"Stagebox {stagebox} not found.")
            return False

        if input_num in self.stageboxes[stagebox]["inputs"]["used"]:
            self.stageboxes[stagebox]["inputs"]["used"].remove(input_num)
            print(f"Released input {stagebox}-{input_num}")
            return True
        else:
            print(f"Input {stagebox}-{input_num} not marked as used.")
            return False

    def available_output(self, stagebox, output_num):
        if stagebox not in self.stageboxes:
            print(f"Stagebox {stagebox} not found in outputs")
            return False

        total = self.stageboxes[stagebox]["outputs"]["total"]
        used = self.stageboxes[stagebox]["outputs"]["used"]

        if used < total:
            return True
        else:
            print(f"No available outputs on {stagebox}")
            return False

    def mark_used_output(self, stagebox, output_num):
        if stagebox not in self.stageboxes:
            print(f"Stagebox {stagebox} not found in outputs!")
            return False

        if not self.available_output(stagebox, output_num):
            print(f"Output {stagebox}-{output_num} not available!")
            return False

        self.stageboxes[stagebox]["outputs"]["used"] += 1
        used = self.stageboxes[stagebox]["outputs"]["used"]
        total = self.stageboxes[stagebox]["outputs"]["total"]
        print(f"Used {stagebox}-{output_num}: {used} used out of {total}")
        return True

    def release_output(self, stagebox, output_num):
        if stagebox in self.stageboxes and self.stageboxes[stagebox]["outputs"]['used'] > 0:
            self.stageboxes[stagebox]["outputs"]['used'] -= 1
            print(f"Released one output from {stagebox}: now {self.stageboxes[stagebox]["outputs"]['used']} used out of {self.stageboxes[stagebox]["outputs"]['total']}")
            return True
        else:
            print(f"Output from {stagebox} cannot be released or is already empty!")
            return False
