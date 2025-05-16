class MicInventory:
    def __init__(self):
        self.inventory = {"Shure sm58", "Shure sm81", "Shure sm57", "Audix D6", "Audix D2", "Audix D4", "DI Box"}

    def available_mic(self, model):
        if model not in self.inventory:
            print(f"Error: Mic model '{model}' not found in inventory.")
            return False
        return True

    def to_dict(self):
        return list(self.inventory)

    def load_inventory(self, data):
        self.inventory = set(data)

    def get_all_mics(self):
        return list(self.inventory)
