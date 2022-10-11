#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""#########################################################
############################################################
### Interface with Polar H10 sensor.                     ###
###                                                      ###
### Thanks to                                            ###
### https://github.com/pareeknikhil/biofeedback/tree/master/Polar%20Device%20Data%20Stream/ECG ###
### https://github.com/diegotsouza/ecg_processing        ###
### https://github.com/mmuramatsu/Heart-rate-collector   ###
###                                                      ###
### Author: Daniel Dantas                                ###
### Last edited: Jan 2022                                ###
############################################################
#########################################################"""

#from importlib import reload

import pprint
import signal
import asyncio
import os
import time
from datetime import datetime

import bleak
from bleak import BleakClient
from bleak import BleakScanner

import Data
import Plot
import const as k
import utils


MODEL_NBR_UUID = '00002a24-0000-1000-8000-00805f9b34fb'
MANUFACTURER_NAME_UUID = '00002a29-0000-1000-8000-00805f9b34fb'
BATTERY_LEVEL_UUID = '00002a19-0000-1000-8000-00805f9b34fb'
HEART_RATE = '00002a37-0000-1000-8000-00805f9b34fb'

## UUID for connection establsihment with device ##
PMD_SERVICE = "FB005C80-02E7-F387-1CAD-8ACD2D8DF0C8"
## UUID for Request of stream settings ##
PMD_CONTROL = "FB005C81-02E7-F387-1CAD-8ACD2D8DF0C8"
## UUID for Request of start stream ##
PMD_DATA = "FB005C82-02E7-F387-1CAD-8ACD2D8DF0C8"
## UUID for Request of ECG Stream ##
ECG_WRITE = bytearray([0x02, 0x00, 0x00, 0x01, 0x82, 0x00, 0x01, 0x01, 0x0E, 0x00])
## Polar H10 ECG sampling frequency for reference. Value can not be changed.
ECG_SAMPLING_FREQ = 130

FLAG_INTERRUPT = False
FLAG_SAVE_RR = True
FLAG_SAVE_ECG = True
FLAG_PLOT_RR = True
FLAG_PLOT_ECG = True


class Polar():
  def __init__(self):
    self.data_rr = Data.Data(k.TYPE_RR)
    self.data_ecg = Data.Data(k.TYPE_ECG)
    self.plot = Plot.Plot()

    self.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(self.loop)


  ## \brief Handles the interrupt signal.
  #
  #  @param sig
  #  @param frame
  def signal_handler(self, sig, frame):
    print('\b\bKeyboard interrupt received...')
    global FLAG_INTERRUPT
    FLAG_INTERRUPT = True

  ## \brief Print exception message preceded with file and function name.
  #
  #  @param msg Exception message.
  #  @param func Function name.
  #  @param file File name. Caller may use __file__.
  def print_exception(self, msg, func, file):
    print("Exception at %s: %s: %s" % (os.path.basename(file), func, msg))

  ## \brief Print message preceded with file and function name.
  #
  #  @param msg Message.
  #  @param func Function name.
  #  @param file File name. Caller may use __file__.
  def print_message(self, msg, func, file):
    print("%s: %s: %s" % (os.path.basename(file), func, msg))


  ## \brief Query uuids and display results.
  #
  #  @param d Device.
  async def print_uuids(self, d):
    uuids = d.metadata["uuids"]
    uuids = [MODEL_NBR_UUID, \
             MANUFACTURER_NAME_UUID, \
             BATTERY_LEVEL_UUID, \
             HEART_RATE] + uuids
    try:
      async with BleakClient(d.address) as client:
        if (not client.is_connected):
          raise Exception("Unable to connect to device at %s" % d.address)
        # Connected
        services = await client.get_services()
        print("Services: ", services.services)
        for s in uuids:
          print("%s: %s" % (s, bleak.uuids.uuidstr_to_str(s)))
          try:
            result = await client.read_gatt_char(s)
            if (s == BATTERY_LEVEL_UUID):
              print(int(result[0]))
            else:
              print(result)
          except Exception as e:
            self.print_exception(e, "print_uuids", __file__)
        # Will disconnect
      await client.disconnect()

    except Exception as e:
      self.print_exception(e, "print_uuids", __file__)

  ## \brief Print details about device.
  #
  #  @param d Device.
  def print_device(self, d):
    msg = "Device <<%s>> at <<%s>>" % (d.name, d.address)
    self.print_message(msg, "print_device", __file__)
    print("Name:     ", d.name)
    print("Address:  ", d.address)
    print("RSSI:     ", d.rssi)
    print("Details:  ")
    pprint.pprint(d.details)
    print("Metadata: ")
    pprint.pprint(d.metadata)
    
    #loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    self.loop.run_until_complete(self.print_uuids(d))
    #asyncio.run(self.print_uuids(d))

  ## \brief Parse the packet with ECG data received from the Polar device.
  #
  # Parse the packet with ECG data received from the Polar device into numeric
  # values and stores it in a Data object.
  #
  #  @param sender Parameter required in functions called by client.start_notify
  #  @param packet Bytearray with heart rate measurement received from the Polar device.
  #        data (bytearray): Heart rate measurement received from the device
  #            Byte 0 - if 0x00 then packet is not empty.
  #            Byte 1..8 - Timestamp from Polar internal clock.
  #            Byte 10..12, 13..15 etc - INT24 ECG potential in microvolts.
  def parse_ecg(self, sender, packet):
    if packet[0] == 0x00:

      """
      if self.data_ecg.t0 == Data.TIME_UNINITIALIZED:
        # Sets t0 to current time
        self.data_ecg.t0 = time.time()
        t = 0.0
      else:
        t = time.time() - self.data_ecg.t0
      """

      timestamp = self.convert_to_unsigned_long(packet, 1, 8)
      step = 3
      samples = packet[10:]
      offset = 0
      t = time.time()
      while offset < len(samples):
        ecg = self.convert_array_to_signed_int(samples, offset, step)
        offset += step
        self.data_ecg.time.extend([t])
        self.data_ecg.timestamp.extend([timestamp])
        self.data_ecg.values_ecg.extend([ecg])


  def convert_array_to_signed_int(self, data, offset, length):
    return int.from_bytes(
      bytearray(data[offset : offset + length]), byteorder="little", signed=True,
    )


  def convert_to_unsigned_long(self, data, offset, length):
    return int.from_bytes(
      bytearray(data[offset : offset + length]), byteorder="little", signed=False,
    )


  ## \brief Parse the packet with heart rate data received from the Polar device.
  #
  # Parse the packet with heart rate data received from the Polar device into numeric
  # values and stores it in a Data object.
  #
  #  @param sender Parameter required in functions called by client.start_notify
  #  @param packet Bytearray with heart rate measurement received from the Polar device.
  #      Byte 0 - Flags:
  #          Bit 0 - Heart rate value format: 0 -> UINT8 bpm, 1 -> UINT16 bpm
  #          Bit 1..2 - Sensor contact status
  #          Bit 3 - Energy expended status
  #          Bit 4 - RR-interval: 0 -> No values are preent, 1 -> One or more
  #          values are present
  #          Bit 5, 6 and 7 - Unused
  #      Byte 1 - UINT8 BPM
  #      Byte 2..3, 4..5 etc - UINT16 RR intervals
  def parse_rr(self, sender, packet):
    # If the 4th bit of the bytearray is 1 then RR reads were sent
    print(len(packet), sep="")
    if (packet[0] & 0b00010000):

      """
      if self.data_rr.t0 == Data.TIME_UNINITIALIZED:
        # Sets t0 to current time
        self.data_rr.t0 = time.time()
        t = 0.0
      else:
        t = time.time() - self.data_rr.t0
      """

      t = time.time()

      # packet[1] is the HR read
      hr = packet[1]

      # packet[2:4] is the RR interval times 1/1024s
      # Convert the bytes to UINT16
      len_packet = len(packet)
      i = 2
      while (i < len_packet):
        rr = int.from_bytes(packet[2:4], byteorder='little', signed=False)
        self.data_rr.time.append(t)
        self.data_rr.heart_rate.append(hr)
        self.data_rr.rr_interval.append(rr)
        print("i = %d, rr = %f" %(i, rr))
        i += 2


  ## \brief Receive RR data from Polar sensor
  #
  #  @param mac MAC Address of Device.
  #  @param filename File where RR data will be stored.
  async def receive_rr(self, mac, filename=''):
    # Listen to the SIGINT signal
    signal.signal(signal.SIGINT, self.signal_handler)
    try:
      async with BleakClient(mac) as client:
        if (not client.is_connected):
          raise Exception("Unable to connect to device at %s" % mac)
        # Connected
        await client.start_notify(HEART_RATE, self.parse_rr)
        while not FLAG_INTERRUPT:
          await asyncio.sleep(0.1)
          if FLAG_SAVE_RR and filename != '':
            self.data_rr.save_raw_data(filename)
          if(self.data_rr.time != []):
            self.data_rr.clear()
        # Will disconnect
        await client.stop_notify(HEART_RATE)
        await client.disconnect()

    except Exception as e:
      self.print_exception(e, "receive_rr", __file__)

  ## \brief Receive ECG data from Polar sensor
  #
  #  @param mac MAC Address of Device.
  #  @param filename File where ECG data will be stored.
  async def receive_ecg(self, mac, filename=''):
    # Listen to the SIGINT signal
    signal.signal(signal.SIGINT, self.signal_handler)
    try:
      async with BleakClient(mac) as client:
        if (not client.is_connected):
          raise Exception("Unable to connect to device at %s" % mac)
        # Connected
        att_read = await client.read_gatt_char(PMD_CONTROL)
        await client.write_gatt_char(PMD_CONTROL, ECG_WRITE)
        await client.start_notify(PMD_DATA, self.parse_ecg)
        while not FLAG_INTERRUPT:
          await asyncio.sleep(0.1)
          if FLAG_SAVE_ECG and filename != '':
            self.data_ecg.save_raw_data(filename)
          if(self.data_ecg.time != []):
            self.data_ecg.clear()

        # Will disconnect
        await client.stop_notify(PMD_DATA)
        await client.stop_notify(HEART_RATE)
        await client.disconnect()

    except Exception as e:
      self.print_exception(e, "receive_ecg", __file__)

  ## \brief Receive ECG and RR data from Polar sensor
  #
  #  @param mac MAC Address of Device.
  #  @param filename_rr File where RR data will be stored.
  #  @param filename_ecg File where ECG data will be stored.
  async def receive_both(self, mac, filename_rr='', filename_ecg=''):
    # Listen to the SIGINT signal
    signal.signal(signal.SIGINT, self.signal_handler)
    try:
      async with BleakClient(mac) as client:
        if (not client.is_connected):
          raise Exception("Unable to connect to device at %s" % mac)
        # Connected
        att_read = await client.read_gatt_char(PMD_CONTROL)
        await client.write_gatt_char(PMD_CONTROL, ECG_WRITE)
        await client.start_notify(PMD_DATA, self.parse_ecg)
        await client.start_notify(HEART_RATE, self.parse_rr)
        while not FLAG_INTERRUPT:
          await asyncio.sleep(0.2)
          if (FLAG_PLOT_ECG):
            self.plot.plot_incremental(self.data_ecg.values_ecg, k.TYPE_ECG)
          if (FLAG_PLOT_RR):
            self.plot.plot_incremental(self.data_rr.heart_rate, k.TYPE_RR)
          if FLAG_SAVE_ECG and filename_ecg != '':
            self.data_ecg.save_raw_data(filename_ecg)
          if FLAG_SAVE_RR and filename_rr != '':
            self.data_rr.save_raw_data(filename_rr)
          if(self.data_ecg.time != []):
            self.data_ecg.clear()
          if(self.data_rr.time != []):
            self.data_rr.clear()

        # Will disconnect
        await client.stop_notify(PMD_DATA)
        await client.disconnect()

    except Exception as e:
      self.print_exception(e, "receive_both", __file__)

  ## \brief Scan and list nearby bluetooth devices.
  #
  #  Scan nearby devices and return those containing the
  #  string received as parameter in their name.
  #
  #  Return list of devices with type bleak.backends.device.BLEDevice
  #
  #  @param name String to search in device name
  async def list_devices(self, name="", timeout=10.0):
    self.print_message("Scanning devices.", "list_devices", __file__)

    result = []
    devices = await BleakScanner.discover(timeout=timeout)
    for d in devices:
      if (d.name.find(name) < 0):
        continue
      msg = "Found device <<%s>> at <<%s>>" % (d.name, d.address)
      self.print_message(msg, "list_devices", __file__)
      result.append(d)
    return result

  ## \brief Llist nearby Polar devices.
  #
  #  Scan nearby devices and return those containing the
  #  string "Polar" in the name.
  #
  #  Return list of devices with type bleak.backends.device.BLEDevice
  #
  def list_devices_polar(self, timeout=10.0):
    #loop = asyncio.get_event_loop()
    result = self.loop.run_until_complete(self.list_devices("Polar", timeout))
    #result = asyncio.run(self.list_devices("Polar", timeout))
    return result

def main():
  polar = Polar()
  devices = polar.list_devices_polar()
  ## Run as follows to find single specific device.
  #devices = asyncio.run(polar.list_devices("Polar H10 4F5F6B2C"))
  msg = "Found %d device(s)" % (len(devices))
  polar.print_message(msg, "main", __file__)
  for d in devices:
    pass
    polar.print_device(d)

  if (len(devices) == 0):
    polar.print_message("Returning", "main", __file__)
    return

  if (FLAG_PLOT_RR or FLAG_PLOT_ECG):
    polar.plot.init()

  d = devices[0]

  filename_rr = "/tmp/rr.tsv"
  utils.remove(filename_rr)
  #asyncio.run(polar.receive_rr(d.address, filename_rr))

  filename_ecg = "/tmp/ecg.tsv"
  utils.remove(filename_ecg)
  #asyncio.run(polar.receive_ecg(d.address, filename_ecg))

  #asyncio.run(polar.receive_both(d.address, filename_rr, filename_ecg))
  polar.loop.run_until_complete(polar.receive_both(d.address, filename_rr, filename_ecg))

  return devices

if __name__ == '__main__':
  main()
