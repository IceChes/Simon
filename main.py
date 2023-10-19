import sounddevice as sd
import whisper
import os
from scipy.io.wavfile import write
from playsound import playsound
import random
import serial
import time
from pocketsphinx import LiveSpeech

def removePunctuation(str):
  return str.replace(",", "").replace(".", "").lower() # This function removes punctuation/capitalization from an input string.

audioFiles_unknown = ["Lines/unknown1.wav", "Lines/unknown2.wav", "Lines/unknown3.wav", "Lines/unknown4.wav"] # Configure random audio files.
audioFiles_notNow = ["Lines/notnow1.wav", "Lines/notnow2.wav", "Lines/notnow3.wav", "Lines/notnow4.wav"]

esp32 = serial.Serial(port=input("ESP32 port: "), baudrate=115200, timeout=1) # Define the ESP32

def espWrite(input):
    esp32.write(input.encode('utf-8') + b'\n')

def espRead():
    readData = esp32.readline()
    return readData

keywords = {  # Define recognized keywords. They don't have to be categorized like this, it's mostly for me.
  # On/Off
  1: 'on',
  2: 'off',
  3: 'disable',
  4: 'enable',
  5: 'activate',
  6: 'deactivate',
  # Stop/Start
  7: 'start',
  8: 'stop',
  9: 'continue',
  10: 'cancel',
  11: 'pause',
  12: 'resume',
  # Stop NOW
  13: 'emergency',
  14: 'halt',
  # Nodes
  15: 'printer',
  16: 'job',
  17: 'computer',
  18: 'car',
  19: 'lights',
  20: 'lights',
  # Shutdown
  21: 'shut',
  22: 'down',
  23: 'shutdown'
  
    # Additional keywords can be placed in here using the following format:
    # number: 'keyword'
    # Keywords can be the names of nodes, trigger words, or other things you want Simon to respond to.
    # Keywords must be 1 word. 
}

model = whisper.load_model("base") # Load a moderately sized Whisper model.
freq = 44100 # Input audio frequency.
duration = 4 # Input audio window. Making this too small increases the likelihood for input sentences to be cut off, too large and the audio will take a while to record.

print("Ready.") # The model takes a bit to load in so this is nice to have.

while True: # Start program loop.

    speech = LiveSpeech(keyphrase='simon', kws_threshold=1e-12)

    for phrase in speech:

        recording = sd.rec(int(duration * freq), samplerate=freq, channels=1) # Record mono audio with the defined parameters.

        playsound('Lines/standby.wav')

        print("Standing by.") # Let the user know that Simon is ready.

        sd.wait() # Wait for the audio to record.

        write("/dev/shm/question1.wav", freq,recording) # Write the audio to RAM.

        result = model.transcribe("/dev/shm/question1.wav") # Transcribe the audio using Whisper.

        print(result["text"]) # Print out what Whisper heard.

        # Clean up input and split into tokens.
        input = result["text"] 
        inputFiltered = removePunctuation(input)
        splitInput = inputFiltered.split() 

        foundStrings = set(splitInput) & set(keywords.values())  # Compare the split input and keyword dictionary.

        if {'off', 'disable'}.intersection( # This checks for "off" OR "disable" AND "light" OR "lights".
            set(foundStrings)) and {'light', 'lights'}.intersection( 
            set(foundStrings)) in foundStrings:
            playsound('Lines/nodelights2.wav')
            espWrite('0')

        elif {'on', 'enable'}.intersection(
            set(foundStrings)) and {'light', 'lights'}.intersection( 
            set(foundStrings)) in foundStrings:
            playsound('Lines/nodelights2.wav')
            espWrite('0')

        elif 'shut' in foundStrings and 'down' in foundStrings or {'shutdown'}.intersection(set(foundStrings)) : # This checks for "shut" AND "down" OR "shutdown".
            playsound('Lines/powerdown1.wav')
            exit()

    
    # This space intentionally left blank for readability when adding new code.
    
    
    
    
    
    
    
    
    
    
    
    
        else: # Simon did not detect a valid command after you addressed him. 
            print("No command detected.")
            audioFile = random.choice(audioFiles_unknown)
            playsound(audioFile)

    os.remove("/dev/shm/question1.wav")