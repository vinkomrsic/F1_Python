# 🏎️ F1_Python — Formula 1 Data CLI Tool
![Python](https://img.shields.io/badge/python-3.9+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python-based command-line interface (CLI) tool to explore Formula 1 race data using the [FastF1](https://github.com/theOehrly/Fast-F1) API.  
Built for data nerds, racing fans, and anyone who wants to analyze F1 sessions without touching a browser.

---

## Features

- View official session results (positions, driver names, team, time)
- Display lap times for any driver in a session
- Graph lap times with pit stop and fastest lap highlighting
- Interactive CLI navigation
- Handles missing or incomplete data gracefully
- Supports all race results (older races may be inaccurate) 
- Supports lap times from 2018 onward

---

## Screenshots

<img src="https://github.com/user-attachments/assets/3ac3b517-475e-4c80-8a78-0b657212413b" alt="CLI Screenshot" width="500">

<img src="https://github.com/user-attachments/assets/f5222537-7e73-4902-8448-64c4297b8e21" alt="Lap Time Graph" width="800">

---

## Installation

1. Clone the repo:

    ```bash
    git clone https://github.com/vinkomrsic/F1_Python.git
    cd F1_Python
    ```

2. (Optional) Set up a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the tool:

    ```bash
    python main.py
    ```

---

## To Do

- [ ] Add CSV export of lap data
- [ ] Compare two drivers
- [ ] Add command-line arguments (non-interactive mode)
- [ ] Package as CLI tool (`f1tool`)

## Author

Made by [@vinkomrsic](https://github.com/vinkomrsic)  
Feedback, pull requests, or memes welcome.
