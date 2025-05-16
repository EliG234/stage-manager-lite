import json

import ttkbootstrap as ttk
import tkinter.font as tkFont
from show_manager import ShowManager
from mic_inventory import MicInventory
from stagebox_manager import StageBoxManager
import tkinter as tk
from functools import partial
from tkinter import messagebox, simpledialog
from stage_requests import send_channel_list_update, fetch_channel_list_from_server


mic_inventory = MicInventory()
stagebox_manager = StageBoxManager()
show_manager = ShowManager()


mic_models = mic_inventory.get_all_mics()
input_labels = stagebox_manager.get_all_input_labels()
output_labels = stagebox_manager.get_all_output_labels()

class StageManagerApp:
    def __init__(self, root):
        self.root = root
        self.user_role = None
        self.input_rows = []
        self.output_rows = []
        self.show_manager = ShowManager()
        self.mic_inventory = mic_inventory
        self.stagebox_manager = stagebox_manager


        self.root.title("Stage Manager - Channel List")
        window_width = 980
        window_height = 980
        self.root.geometry(f"{window_width}x{window_height}")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_vrootheight()

        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2) - 40

        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=10)
        root.option_add("*Font", default_font)


        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill="both", expand=True)



        #Input Table
        input_frame = ttk.Frame(self.main_frame)
        ttk.Label(self.main_frame, text="Input Channels", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w")
        input_frame.grid(row=1, column=0, sticky="nsew")

        input_frame.grid_columnconfigure(0, weight=0, minsize=40)

        for col in range(1, 5):
            input_frame.grid_columnconfigure(col, weight=1, uniform="equal")

        ttk.Label(input_frame, text="Ch #").grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ttk.Label(input_frame, text="Channel Name").grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ttk.Label(input_frame, text="Mic").grid(row=0, column=2, padx=5, pady=10, sticky="ew")
        ttk.Label(input_frame, text="SB Input").grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        ttk.Label(input_frame, text="Notes").grid(row=0, column=4, padx=10, pady=5, sticky="ew")


        for i in range(1, 17):
            #Channel number
            ttk.Label(input_frame, text=str(i)).grid(row=i, column=0, padx=10, pady=5, sticky="ew")

            #Channel name entry
            ch_name = ttk.Entry(input_frame, width=20)
            ch_name.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

            # Mic dropdown list
            mic_options = [""] + list(mic_inventory.get_all_mics())
            mic_var = tk.StringVar()
            mic_combo = ttk.Combobox(input_frame, textvariable=mic_var, values=mic_options, state="readonly")
            mic_combo.grid(row=i, column=2, padx=10, pady=5, sticky="ew")



            mic_combo.bind("<<ComboboxSelected>>", lambda event, var=mic_var: self.on_mic_change(var))

            #Stagebox Input dropdown

            sbi_combo = ttk.Combobox(input_frame, values=[""] + input_labels, state="readonly")
            sbi_combo.grid(row=i, column=3, padx=10, pady=5, sticky="ew")

            # Notes entry
            inotes = ttk.Entry(input_frame, width=20)
            inotes.grid(row=i, column=4, padx=10, pady=5, sticky="ew")

            self.input_rows.append({
                "channel": i,
                "name_entry": ch_name,
                "mic_var": mic_var,
                "input_combo": sbi_combo,
                "notes_entry": inotes
            })


        # Output Table
        output_frame = ttk.Frame(self.main_frame)
        ttk.Label(self.main_frame, text="Mixes / Outputs", font=("Segoe UI", 12, "bold")).grid(row=2, column=0,
                                                                                               sticky="w", pady=(20, 0))
        output_frame.grid(row=3, column=0, sticky="ew")

        output_frame.grid_columnconfigure(0, weight=0, minsize=40)

        for col in range(1, 4):
            output_frame.grid_columnconfigure(col, weight=1, uniform="equal")

        ttk.Label(output_frame, text="Mix #").grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ttk.Label(output_frame, text="Mix Name").grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ttk.Label(output_frame, text="SB Output").grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        ttk.Label(output_frame, text="Notes").grid(row=0, column=3, padx=10, pady=5, sticky="ew")

        for i in range(1, 5):
            #Mix number
            ttk.Label(output_frame, text=str(i)).grid(row=i, column=0, padx=10, pady=5, sticky="ew")

            #Mix name entry
            mix_name = ttk.Entry(output_frame, width=20)
            mix_name.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

            #Stagebox Output dropdown
            sbo_combo = ttk.Combobox(output_frame, values=[""] + output_labels, state="readonly")
            sbo_combo.grid(row=i, column=2, padx=10, pady=5, sticky="ew")

            # Notes entry
            onotes = ttk.Entry(output_frame, width=20)
            onotes.grid(row=i, column=3, padx=10, pady=5, sticky="ew")

            self.output_rows.append({
                "mix": i,
                "name_entry": mix_name,
                "output_combo": sbo_combo,
                "notes_entry": onotes
            })

        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=0, column=5, rowspan=20, padx=20, sticky="ew")
        self.role_label = ttk.Label(button_frame, text=f"Role: {self.user_role or 'None'}")
        self.role_label.pack(pady=(0, 5))
        tk.Button(button_frame, text="Select Role", command=self.prompt_user_role, width=15).pack(side="top", pady=5)
        tk.Button(button_frame, text="Load Show", command=self.load_show, width=15).pack(side=ttk.TOP, pady=5)
        tk.Button(button_frame, text="Save Show", command=self.save_show, width=15).pack(side=ttk.TOP, pady=5)
        tk.Button(button_frame, text="Send Update", command=self.update_show, width=15).pack(side=ttk.TOP, pady=5)
        tk.Button(button_frame, text="Pull Update", command=self.pull_update, width=15).pack(side=ttk.TOP, pady=5)
        tk.Button(button_frame, text="Exit", command=self.exit_app, width=15).pack(side=ttk.TOP, pady=5)

    def on_mic_change(self, var):
        mic_name = var.get()
        if not self.mic_inventory.available_mic(mic_name):
            messagebox.showwarning("Mic Unavailable", f"'{mic_name}' is not available in the mic inventory.")
            var.set("")  # Clear the selection

    def prompt_user_role(self):

        role = simpledialog.askstring("Select Role", "(FOH or STAGE):")
        if role is None:
            return  # User cancelled

        role = role.strip().upper()
        if role not in ("FOH", "STAGE"):
            messagebox.showerror("Invalid Role", "Please enter FOH or STAGE.")
            return

        self.select_user_role(role)

    def select_user_role(self, role):
        self.user_role = role
        print(f"Role '{self.user_role}' selected. Ready for Flask requests.")
        self.role_label.config(text=f"Role: {self.user_role}")
        
    def build_updated_channel_list(self):
        input_data = []
        for row in self.input_rows:
            name = row["name_entry"].get().strip()
            mic = row["mic_var"].get().split(" (")[0].strip()
            sb_input = row["input_combo"].get().strip()
            notes = row["notes_entry"].get().strip()

            if name or mic or sb_input or notes:
                input_data.append({
                    "channel": row["channel"],
                    "name": name,
                    "mic": mic,
                    "stagebox_input": sb_input,
                    "notes": notes
                })
        output_data = []
        for row in self.output_rows:
            name = row["name_entry"].get().strip()
            sb_output = row["output_combo"].get().strip()
            notes = row["notes_entry"].get().strip()

            if name or sb_output or notes:
                output_data.append({
                    "mix": row["mix"],
                    "name": name,
                    "stagebox_output": sb_output,
                    "notes": notes
                })
        return {
            "inputs": input_data,
            "outputs": output_data
        }
    def get_channel_list(self):
        return self.build_updated_channel_list()

    def populate_widgets_from_data(self, inputs, outputs):
        for i, row in enumerate(self.input_rows):
            if i < len(inputs):
                row["name_entry"].delete(0, tk.END)
                row["name_entry"].insert(0, inputs[i].get("name", ""))

                mic_model = inputs[i].get("mic", "").strip()
                if mic_model:
                    row["mic_var"].set(mic_model)
                    if mic_model not in self.mic_inventory.inventory:
                        print(f"Error: Mic model '{mic_model}' not found in inventory.")
                else:
                    row["mic_var"].set("")

                row["input_combo"].set(inputs[i].get("stagebox_input", ""))
                row["notes_entry"].delete(0, tk.END)
                row["notes_entry"].insert(0, inputs[i].get("notes", ""))
            else:
                row["name_entry"].delete(0, tk.END)
                row["mic_var"].set("")
                row["input_combo"].set("")
                row["notes_entry"].delete(0, tk.END)

        for i, row in enumerate(self.output_rows):
            if i < len(outputs):
                row["name_entry"].delete(0, tk.END)
                row["name_entry"].insert(0, outputs[i].get("name", ""))

                row["output_combo"].set(outputs[i].get("stagebox_output", ""))
                row["notes_entry"].delete(0, tk.END)
                row["notes_entry"].insert(0, outputs[i].get("notes", ""))
            else:
                row["name_entry"].delete(0, tk.END)
                row["output_combo"].set("")
                row["notes_entry"].delete(0, tk.END)

    def load_show(self):
        show_name = simpledialog.askstring("Load Show", "Enter show name:")
        if not show_name:
            return

        input_list = []
        output_list = []

        data = self.show_manager.load_show(
            show_name,
            self.mic_inventory,
            self.stagebox_manager,
            input_list,
            output_list
        )
        self.populate_widgets_from_data(data["inputs"], data["outputs"])
        messagebox.showinfo("Success", f"Show '{show_name}' Loaded successfully.")

    def save_show(self):
        show_name = simpledialog.askstring("Save Show", "Enter show name:")
        if not show_name:
            return

        channel_data = self.build_updated_channel_list()


        for input_entry in channel_data["inputs"]:
            mic_model = input_entry.get("mic", "").strip()
            if not mic_model:
                messagebox.showerror("Error", f"Mic model is missing for channel {input_entry.get('channel')}")
                return
            if mic_model not in self.mic_inventory.get_all_mics():
                messagebox.showerror("Error",
                                     f"Mic model '{mic_model}' not found in inventory for channel {input_entry.get('channel')}")
                return


        self.show_manager.save_show(
            show_name,
            self.mic_inventory,
            self.stagebox_manager,
            channel_data["inputs"],
            channel_data["outputs"]
        )
        messagebox.showinfo("Success", f"Show '{show_name}' saved successfully.")

    def update_show(self):
        try:
            updated_channel_list = self.build_updated_channel_list()
            success = send_channel_list_update(updated_channel_list)

            if success:
                messagebox.showinfo("Success", "Channel list updated on FOH server.")
            else:
                messagebox.showerror("Error", "Failed to update channel list on FOH server.")

        except Exception as e:
            print(f"Error sending update: {e}")
            messagebox.showerror("Error", f"Error sending update: {e}")

    def pull_update(self):
        channel_list = fetch_channel_list_from_server()
        if channel_list:
            inputs = channel_list.get("inputs", [])
            outputs = channel_list.get("outputs", [])
            self.populate_widgets_from_data(inputs, outputs)
            messagebox.showinfo("Success", "Channel list loaded from FOH server.")
        else:
            messagebox.showerror("Error", "Failed to load channel list from FOH server.")

    def exit_app(self):
        if messagebox.askokcancel("Exit", "Leaving so soon?"):
            self.root.destroy()

if __name__ == "__main__":

    root = ttk.Window(themename="darkly")
    app = StageManagerApp(root)
    root.mainloop()


