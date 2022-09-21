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

  ## \brief Handles the interrupt signal.
  #
  #  @param sig
  #  @param frame
  def signal_handler(self, sig, frame):
    print('\b\bKeyboard interrupt received...')
    global FLAG_INTERRUPT
    FLAG_INTERRUPT = True

  ## \brief Start receiving audio signal
  #
  #  @param filename
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

  ## \brief Stop receiving audio signal and and save it to file.
  #
  #  @param filename
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

  ## \brief Launch the audio recording function using a thread
  def start(self, filename):
    audio_thread = threading.Thread(target=self.receive(filename))
    audio_thread.start()

  ## \brief Scan audio input devices and return them in a list.
  def scan_devices(self):
    p = self.audio
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    result = []
    for i in range(0, numdevices):
      print("device[%d]" % i)
      if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
        string = "%02d - %s" % (i, p.get_device_info_by_host_api_device_index(0, i).get('name'))
        result.append(string)
    return(result)

  def init_plot(self):
    print("AudioDevice.init_plot")
    if (FLAG_PLOT_AUDIO):
      with_audio = True
      self.plot = Plot.Plot(with_audio)
      self.plot.init()
      time.sleep(0.1)


def main():  
    audiodev = AudioDevice()
    audiodev.init_plot()

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
