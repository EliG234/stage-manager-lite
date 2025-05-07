class MicInventory:
    def __init__(self):
        self.inventory = {
            "Shure sm58": 8,
            "Shure sm81": 2,
            "Shure sm57": 4
        }

        self.in_use = {model: 0 for model in self.inventory}

    def available_mic(self, model):
        if model not in self.inventory:
            print(f"Error: Mic model '{model}' not found in inventory.")
            return False
        else:
            used = self.in_use.get(model, 0)
            total = self.inventory[model]
            return used < total

    def used_mic(self, model):
        if self.available_mic(model):
            self.in_use[model] += 1
            return True
        else:
            return False

    def release_mic(self, model):
        if self.in_use.get(model, 0) > 0:
            self.in_use[model] -= 1

    def to_dict(self):
        return self.inventory.copy()

    def load_inventory(self, data):
        self.inventory = data.copy()
