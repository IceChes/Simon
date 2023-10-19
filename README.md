# Simon
Simon is a voice assistant platform. 

# Features

- Lightweight idle.
- Cross-platform.
- Totally modular.
- Based on widely available parts and libraries.

# Installation

Please don't install Simon yet if you don't want to do development with it. It's not finished.

To install Simon on Linux, run the installer script. To install Simon on Windows... figure it out I guess.

`./installer.sh`

The installer grabs all necessary python packages via pip. If you are on Arch Linux, you probably need to make a venv for Simon before you run the installer.

`python -m venv Simon`

`source Simon/bin/activate`

Exit the venv with 

`deactivate`

Once Simon is installed, run it with 

`python main.py`

You will need to connect a serial device to your computer and then specify the port in the console. This is an annoyance now but later will be part of wireless device support.

# Editing main.py

Simon is designed to be edited. To add new commands, there are 3 steps.

- Add the new keywords in the `keywords` dictionary. Keywords must be 1 word in length.
- Add the conditions for running a command based on the input keyword. Examples of ways to do this are outlined in the comments of main.py.
- Add the function you want to run if the condition is satisfied.

# Adding New Voice Lines

Simon's voice lines were made by using XTTS and a sample of Vega from Doom Eternal. For copyright reasons I'm not sure if I'm allowed to distribute the original sample source but you can clip one of his lines yourself if you'd like.

The lines were then filtered through Audacity with a -0.8 hard clipping distortion value, and a small amount of reverb. The distortion is to cover up the slurring of words and glitches present in XTTS.

You can add new wav files to the "Lines" directory and play them in main.py using playsound.