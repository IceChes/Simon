# Simon
Simon is a modular personal assistant that runs on any Linux PC. It requires fairly powerful hardware but should run on most modern SBCs.

Simon will listen for the wake word “Simon”, and then transcribe whatever you say in the following 4 seconds into a command. It will then translate the command into a function depending on what words the command contains. If it doesn’t hear a command, it will say that it didn’t hear you, and wait another 4 seconds. If it doesn’t hear anything in the following 4 seconds, it will go back into idle mode.

The functions Simon executes are serial commands that communicate with an ESP32 dongle, which in turn communicates with a mesh of “nodes”. This part is still in early development so I won’t go too far into it yet.

Simon relies on 5 core components.
- Voice recognition system
- ESP32 MQTT mesh (unfinished)
- Voice line database
- Voice parsing script (unfinished)

Each component will be detailed below.

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

# How it Works
## Voice Recognition
The voice recognition system relies on two submodules - Whisper by OpenAI, and PocketSphinx. Sphinx looks for the keyword “Simon”, and Whisper transcribes any command following “Simon”. The advantage to doing this is that Sphinx is fairly lightweight so it can run in real time, and then Whisper’s highly accurate but more resource intensive model can be run when the code word is detected. This is fairly similar to how common devices like Amazon Alexa work.

## ESP32 MQTT Mesh
This part of Simon is UNFINISHED. The ESP32 MQTT mesh will form a network of interconnected devices that Simon can interact with. 

## Voice Line Database
The voice line database is a folder containing each voice sound file Simon plays. Due to the slow nature of most AI text to speech, Simon cannot synthesize text on-the-fly.

Adding voice lines is as simple as dragging in new wav files and adding them to main.py. The difficult part is synthesizing new voice lines.

When I synthesized Simon’s voice, I used Coqui TTS with the XTTS model. I used a line from Vega in Doom Eternal for the reference voice. The resulting audio was filtered through Audacity with -0.8 hard clipping distortion and a small amount of reverb. You can use the same process to synthesize similar voice lines. I will not be sharing the original sample I used due to copyright concerns.

## Voice Parsing Script
After you say “simon”, Whisper will activate and record for 4 seconds. After the 4 second window has passed, Whisper will transcribe what you said. Then it will clean the transcription of punctuation and capitals, and split it into words. Then it will run through an if-then-else search tree looking to see if your input contains certain combinations of keywords. 

All key phrases should be designed to take less than 4 seconds to say. Simon does not have any ability to detect if you stop talking. Also, because of the search tree system, Simon does not listen for exact phrases and should be much more reliable than a typical assistant in detecting what you say.

# Hacking
## Editing main.py
main.py is the central speech recognition and parsing loop. It contains the list of words recognized by Simon, what words form what commands, and what commands execute what functions. 

To add keywords, edit the `keywords` dict and add whatever keywords you would like, prefixed by an index number for the dict. Keywords must be a single word.

To add a search tree entry, go down to the search tree and take a close look at the search tree functions. You’ll notice some patterns.

To search for a keyword, use `‘<keyword>’ in foundStrings`

For example:

```python
elif ‘off’ in foundStrings:
	turnOff()
```

To search for multiple keywords, use two of the above conditions chained with an and statement.

```python
elif ‘off’ in foundStrings and ‘turn’ in foundStrings:
	turnOff()
```

To search for a keyword, or a different keyword, use `{keyword1, keyword2}.intersection(set(foundStrings))`

You can add more than 2 keywords, like in this example, which activates if it hears “off”, “disable”, or “deactivate”.

```python
if {'off', 'disable', ‘deactivate’}.intersection(set(foundStrings)):
	turnOff()
```

You can combine 2 general keyword searches like this, which looks for “off”, “disable”, or deactivate”, and also “light” or “lights”.

```python
if {'off', 'disable', ‘deactivate’}.intersection(set(foundStrings)) and {‘lights’, ‘light’}.intersection(set(foundStrings)):
	turnOffLights()
```

You can combine general and specific keyword searches like in this condition, which searches for “off”, “disable”, or “deactivate” in addition to “light”.

```python
if {'off', 'disable', ‘deactivate’}.intersection(set(foundStrings)) and ‘light’ in foundStrings:
	turnOffLights()
```

**IMPORTANT - It is not recommended that you make any commands that can be triggered with only a single phrase to prevent accidental triggering.**

## Editing Simon_Hub_Config.h

The Simon Hub node software is not finished , so neither are the docs for it. It is also not part of this repo yet.

The Hub Node firmware is a simple piece of software that contains only AP hosting, and a very large switch case function. The switch case acts as a search tree to process serial inputs from main.py. 

The config file is the important part. It defines all of the functions run when a new serial command is received. Simply add the function to be run under the corresponding serial input. The serial input must be triggered by something in main.py, probably a conditional. Writing conditionals is outlined above.
