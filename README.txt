
# Stage Manager Application

## Overview

This application helps sound engineers and stage managers organize and manage mic inventories, stageboxes, and channel lists for live sound setups. It supports saving/loading show configurations locally and syncing channel lists between a Front of House (FOH) server and Stage client over a network.

## Features

- Manage microphone inventory with counts.
- Manage stageboxes and their inputs/outputs.
- Build and edit channel lists with mic and stagebox assignments.
- Save and load show configurations locally under `Data/Saved Shows`.
- Sync channel list updates over a Flask-based FOH API server.
- Stage client can fetch and update the current channel list from the FOH server.
- Simple GUI interface built with Tkinter.
- Example show file included: **"Rock N Roll"**.

## Directory Structure

```
Stage-Manager/
├── Data/
│   ├── Saved Shows/
│   │   └── Rock N Roll.json
│   └── Server Memory/
│       └── latest_show.json
├── mic_inventory.py
├── stagebox_manager.py
├── show_manager.py
├── foh_api.py
├── stage_requests.py
├── gui.py
├── main.py  # CLI interface (optional)
└── README.txt
```

## Setup and Installation

1. Ensure Python 3.7+ is installed.
2. Install required packages:
   ```bash
   pip install flask requests
   ```
3. Run the FOH API server:
   ```bash
   python foh_api.py
   ```
4. Run the GUI client:
   ```bash
   python gui.py
   ```

## Usage

- Use the GUI to select your role (FOH or Stage).
- FOH user can create and save shows, which are stored locally.
- Stage user can fetch the latest channel list from the FOH server, make updates, and send changes back.
- Save shows under `Data/Saved Shows` to keep different setups.
- The latest channel list in the server is saved under `Data/Server Memory/latest_show.json`.

## Example Show File

An example show file named **"Rock N Roll"** is included in the `Data/Saved Shows` folder to demonstrate the format and usage.

## License

MIT License

---

For questions or issues, please contact the developer.

