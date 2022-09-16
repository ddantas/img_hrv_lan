#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""#########################################################
############################################################
### Record audio data.                                   ###
###                                                      ###
### Author: Mario Muramatsu, Daniel Dantas               ###
### Last edited: Sep 2022                                ###
############################################################
#########################################################"""

import pyaudio
import wave
import time
import os
import sys
import asyncio
import signal
import threading

import Plot
import const as k

FLAG_INTERRUPT = False
FLAG_SAVE_AUDIO = True
FLAG_PLOT_AUDIO = True

class AudioDevice():
  # Audio class based on pyAudio and Wave
  def __init__(self):
    self.rate = 44100
    self.frames_per_buffer = 5000
    self.channels = 2
    self.format = pyaudio.paInt16
    self.audio = pyaudio.PyAudio()
    self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer = self.frames_per_buffer)
    self.audio_frames = []

    if (FLAG_PLOT_AUDIO):
      with_audio = True
      self.plot = Plot.Plot(with_audio)
      self.plot.init()
      time.sleep(0.1)

  ## \brief Handles the interrupt signal.
  #
  #  @param sig
  #  @param frame
  def signal_handler(self, sig, frame):
    print('\b\bKeyboard interrupt received...')
    global FLAG_INTERRUPT
    FLAG_INTERRUPT = True

  # Audio starts being recorded
  def receive(self, filename):
    signal.signal(signal.SIGINT, self.signal_handler)
    self.stream.start_stream()
    while not FLAG_INTERRUPT:
      data = self.stream.read(self.frames_per_buffer) 
      self.audio_frames.append(data)
      print(len(self.audio_frames))
      if (FLAG_PLOT_AUDIO):
        self.plot.plot_incremental(data, k.TYPE_AUDIO)
    if (FLAG_SAVE_AUDIO):
      self.stop(filename)

  # Finishes the audio recording therefore the thread too    
  def stop(self, filename):
    if FLAG_INTERRUPT:
      self.stream.stop_stream()
      self.stream.close()
      self.audio.terminate()

      waveFile = wave.open(filename, 'wb')
      waveFile.setnchannels(self.channels)
      waveFile.setsampwidth(self.audio.get_sample_size(self.format))
      waveFile.setframerate(self.rate)
      waveFile.writeframes(b''.join(self.audio_frames))
      waveFile.close()      

  # Launches the audio recording function using a thread
  def start(self, filename):
    audio_thread = threading.Thread(target=self.receive(filename))
    audio_thread.start()

def main():
    audiodev = AudioDevice()

    # Start
    print('Start monitoring.')
    print('Start recording.')
    filename = "AudioDevice.wav"
    #asyncio.run(audiodev.receive(filename))
    audiodev.start(filename)
    time.sleep(1)
    #audiodev.stop_audio_recording('test')
    print('Stop recording.')
    

"""#########################################################
############################################################
### Main function                                        ###
############################################################
#########################################################"""


if __name__ == '__main__':
    main()
