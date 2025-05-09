import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter.font as tkFont

root = ttk.Window(themename="darkly")
root.title("Stage Manager - Channel List")
window_width = 825
window_height = 980
root.geometry(f"{window_width}x{window_height}")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_vrootheight()

x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2) - 40

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(family="Segoe UI", size=10)
root.option_add("*Font", default_font)

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

#Input Table
input_frame = ttk.Frame(main_frame)
ttk.Label(main_frame, text="Input Channels", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w")
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
    mic_combo = ttk.Combobox(input_frame, values=["", 'Mic 1', 'Mic 2', 'Mic 3'], state="readonly")
    mic_combo.grid(row=i, column=2, padx=10, pady=5, sticky="ew")

    #Stagebox Input dropdown
    sbi_combo = ttk.Combobox(input_frame, values=["", 'SB1-1', 'SB1-2', 'SB1-3', 'SB1-4'], state="readonly")
    sbi_combo.grid(row=i, column=3, padx=10, pady=5, sticky="ew")

    # Notes entry
    inotes = ttk.Entry(input_frame, width=20)
    inotes.grid(row=i, column=4, padx=10, pady=5, sticky="ew")

#Output Table
output_frame = ttk.Frame(main_frame)
ttk.Label(main_frame, text="Mixes / Outputs", font=("Segoe UI", 12, "bold")).grid(row=2, column=0, sticky="w", pady=(20, 0))
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
    sbo_combo = ttk.Combobox(output_frame, values=["", 'SB1-1', 'SB1-2', 'SB1-3', 'SB1-4'], state="readonly")
    sbo_combo.grid(row=i, column=2, padx=10, pady=5, sticky="ew")

    # Notes entry
    onotes = ttk.Entry(output_frame, width=20)
    onotes.grid(row=i, column=3, padx=10, pady=5, sticky="ew")
root.mainloop()
