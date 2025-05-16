Stage Manager App
=================

This is a Python-based application designed for stage and FOH engineers to manage microphone inventory, stageboxes, and input/output assignments across a live show. It includes a GUI interface and local server communication for role-based workflows.

----------------------------
Features
----------------------------
- Assign microphones to stage inputs and outputs using dropdown menus.
- View and edit channel lists in a clean GUI interface.
- Save and load shows locally (stored in 'Data/Saved Shows').
- Server memory stores the latest show in 'Data/Server Memory/latest_show.json'.
- Role selection: STAGE or FOH.
- Example show provided: "Rock N Roll.json".

----------------------------
Running the Application
----------------------------
1. Make sure you have Python 3.10 or later installed.
2. Install required packages (in terminal or PyCharm terminal):

   pip install flask requests ttkthemes

3. Start the local server:
   In one terminal window or tab, run:
   python foh_api.py

   This will start a Flask server on http://localhost:5000 used to send/receive show data.

4. Launch the GUI:
   In another terminal window or run configuration, launch the GUI:
   python gui.py

----------------------------
File Structure
----------------------------

Stage-Manager/
│
├── gui.py                  # GUI application entry point
├── show_manager.py         # Logic for saving/loading show data
├── foh_api.py              # Local Flask server for channel data sync
├── stage_requests.py       # Client interface to send/fetch data from server
│
├── Data/
│   ├── Saved Shows/        # Local saved shows (e.g. "Rock N Roll.json")
│   └── Server Memory/      # Server memory file (latest_show.json)
│
├── README.txt              # You're reading it!

----------------------------
Notes
----------------------------
- Make sure to run both the server and GUI simultaneously for full functionality.
- Shows are saved as .json files and can be shared or backed up easily.
- If any microphone is missing or invalid, saving will prompt for corrections.
- The server stores the *latest* show to be retrieved or overwritten as needed.
