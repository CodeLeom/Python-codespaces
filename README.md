# Run Python GUI inside GitHub codespaces

> This repository contains setup scripts and examples that make it possible to run Python GUI applications inside GitHub Codespaces.
> It uses `Xvfb` to create a virtual display and `noVNC` to stream the desktop directly to your browser.
> This is especially useful for running and testing libraries like Pygame, Tkinter, or other Python GUI frameworks in a headless environment like Codespaces.


Clone this repo and open in codespace.

Once you open your codespace, run the command below to give you the access to execute the bash file

```bash
chmod +x start-gui.sh

```

The command below will be used to run the bash file

```bash
./start-gui.sh
```

Once your bash script is running, 
1. Navigate to the port tab and switch the port visibility to public
2. open the url in a seperate tab or click it directly from the port tab
3. If the GUI has not started, click `vnc.html` or `vnc_auto.html`
4. Once your GUI loads, go back to your codespace, open a new terminal instance and run your python script


All should be running fine. Once your python file is running, check the gui tab to see you code running
