# Run Python GUI inside GitHub codespaces

This repository provides setup scripts and examples that make it possible to run Python GUI applications inside GitHub Codespaces.

It uses:

- Xvfb: to create a virtual display in a headless environment
- noVNC: to stream the desktop directly in your browser

This is especially useful for running and testing GUI libraries like Pygame, Tkinter, or other Python GUI frameworks inside Codespaces.

## Getting Started

Clone this repo and open in codespace.

Once you open your codespace, run the command below to give you the access to execute the bash file

```bash
chmod +x start-gui.sh

```

The command below will be used to run the bash file (which the start the virtual desktop

```bash
./start-gui.sh
```

Once your bash script is running, 
1. Navigate to the port tab and switch the `port 6080` visibility to `public`
2. Open the `port 6080` exposed url in a seperate tab or click it directly from the port tab
3. If the GUI has not started automatically, click `vnc.html` or `vnc_auto.html`
4. Once your GUI loads, go back to your codespace, open a new terminal instance and run your python script

```bash
python3 your_script.py
```

All should be running fine. Once your python file is running, check the gui tab to see you code output


### Note

- ALSA audio warnings can be ignored — Codespaces doesn’t provide sound output.
- Press ESC or close the window in the GUI to exit your app cleanly.
- You can adapt this setup for any GUI toolkit, not just Pygame.
