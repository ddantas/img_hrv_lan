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

interrupt_flag = False

data_rr = Data.Data(Data.TYPE_RR)
data_ecg = Data.Data(Data.TYPE_ECG)

## \brief Handles the interrupt signal.
#
#  @param sig
#  @param frame
def signal_handler(sig, frame):
  print('\b\bKeyboard interrupt received...')
  global interrupt_flag
  interrupt_flag = True


## \brief Print exception message preceded with file and function name.
#
#  @param msg Exception message.
#  @param func Function name.
#  @param file File name. Caller may use __file__.
def print_exception(msg, func, file):
  print("Exception at %s: %s: %s" % (os.path.basename(file), func, msg))

## \brief Print message preceded with file and function name.
#
#  @param msg Message.
#  @param func Function name.
#  @param file File name. Caller may use __file__.
def print_message(msg, func, file):
  print("%s: %s: %s" % (os.path.basename(file), func, msg))


## \brief Query uuids and display results.
#
#  @param d Device.
async def print_uuids(d):
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
          print(result)
        except Exception as e:
          print_exception(e, "print_uuids", __file__)
      # Will disconnect
    await client.disconnect()
    
  except Exception as e:
    print_exception(e, "print_uuids", __file__)

################################
## REVISAR INICIO

## Bit conversion of the Hexadecimal stream
def parse_ecg(sender, data):
  if data[0] == 0x00:
    if data_ecg.t0 == Data.TIME_UNINITIALIZED:
      # Sets t0 to current time
      data_ecg.t0 = time.time()
      t = 0.0
    else:
      t = time.time() - data_ecg.t0
    timestamp = convert_to_unsigned_long(data, 1, 8)
    step = 3
    samples = data[10:]
    offset = 0
    while offset < len(samples):
      ecg = convert_array_to_signed_int(samples, offset, step)
      offset += step
      data_ecg.time.extend([t])
      data_ecg.timestamp.extend([timestamp])
      data_ecg.values_ecg.extend([ecg])

    if(data_ecg.time != []):
      print("data_ecg.time length: %d" % len(data_ecg.time))
      print("data_ecg.time: " + str(data_ecg.time))
      print("data_ecg.timestamp length: %d" % len(data_ecg.timestamp))
      print("data_ecg.timestamp: " + str(data_ecg.timestamp))
      print("data_ecg.values_ecg length: %d" % len(data_ecg.values_ecg))
      print("data_ecg.values_ecg: " + str(data_ecg.values_ecg))


def convert_array_to_signed_int(data, offset, length):
    return int.from_bytes(
        bytearray(data[offset : offset + length]), byteorder="little", signed=True,
    )


def convert_to_unsigned_long(data, offset, length):
    return int.from_bytes(
        bytearray(data[offset : offset + length]), byteorder="little", signed=False,
    )


def parse_rr(sender, data):
    '''
    Parse the data receive from the device into numeric values and stores it in
    a Data object.

    Parameters:
        data (bytearray): Heart rate measurement received from the device
            Byte 0 - Flags:
                Bit 0 - Heart rate value format: 0 -> UINT8 bpm, 1 -> UINT16 bpm
                Bit 1..2 - Sensor contact status
                Bit 3 - Energy expended status
                Bit 4 - RR-interval: 0 -> No values are preent, 1 -> One or more
                values are present
                Bit 5, 6 and 7 - Unused
            Byte 1 - UINT8 BPM
            Byte 2..5 - UINT16 RR intervals
    '''
    # If the 4th bit of the bytearray is 1 then RR reads were sent
    if (data[0] & 0b00010000):

        if data_rr.t0 == Data.TIME_UNINITIALIZED:
            # Sets t0 to current time
            data_rr.t0 = time.time()
            t = 0.0
        else:
            t = time.time() - data_rr.t0

        data_rr.time.append(t)

        # data[1] is the HR read
        hr = data[1]
        data_rr.values_hr.append(hr)

        # data[2:4] is the RR interval
        # Convert the bytes in UINT16
        rr = int.from_bytes(data[2:4], byteorder='little', signed=False)
        data_rr.values_rr.append(rr)

        print(f'Time: {t} s,   Heart rate: {hr} bpm,       RR-interval: {rr} ms')

################################
## REVISAR FIM


## \brief Receive RR data from Polar sensor
#
#  @param d Device.
#  @param filename File where RR data will be stored.
async def receive_rr(d, filename):
  # Listen to the SIGINT signal
  signal.signal(signal.SIGINT, signal_handler)
  try:
    async with BleakClient(d.address) as client:
      if (not client.is_connected):
        raise Exception("Unable to connect to device at %s" % d.address)
      # Connected
      await client.start_notify(HEART_RATE, parse_rr)
      while not interrupt_flag:
        await asyncio.sleep(0.1)
        data_rr.save_raw_data(filename)
        if(data_rr.time != []):
          data_rr.clear()
      # Will disconnect
      await client.stop_notify(HEART_RATE)
      await client.disconnect()
    
  except Exception as e:
    print_exception(e, "receive_rr", __file__)

## \brief Receive ECG data from Polar sensor
#
#  @param d Device.
#  @param filename File where ECG data will be stored.
async def receive_ecg(d, filename):
  # Listen to the SIGINT signal
  signal.signal(signal.SIGINT, signal_handler)
  try:
    async with BleakClient(d.address) as client:
      if (not client.is_connected):
        raise Exception("Unable to connect to device at %s" % d.address)
      # Connected
      att_read = await client.read_gatt_char(PMD_CONTROL)
      await client.write_gatt_char(PMD_CONTROL, ECG_WRITE)
      await client.start_notify(PMD_DATA, parse_ecg)
      while not interrupt_flag:
        await asyncio.sleep(0.1)
        data_ecg.save_raw_data(filename)
        if(data_ecg.time != []):
          data_ecg.clear()

      # Will disconnect
      await client.stop_notify(PMD_DATA)
      await client.stop_notify(HEART_RATE)
      await client.disconnect()

  except Exception as e:
    print_exception(e, "receive_both", __file__)

## \brief Receive ECG and RR data from Polar sensor
#
#  @param d Device.
#  @param filename_rr File where RR data will be stored.
#  @param filename_ecg File where ECG data will be stored.
async def receive_both(d, filename_rr, filename_ecg):
  # Listen to the SIGINT signal
  signal.signal(signal.SIGINT, signal_handler)
  try:
    async with BleakClient(d.address) as client:
      if (not client.is_connected):
        raise Exception("Unable to connect to device at %s" % d.address)
      # Connected
      att_read = await client.read_gatt_char(PMD_CONTROL)
      await client.write_gatt_char(PMD_CONTROL, ECG_WRITE)
      await client.start_notify(PMD_DATA, parse_ecg)
      await client.start_notify(HEART_RATE, parse_rr)
      while not interrupt_flag:
        await asyncio.sleep(0.1)
        data_ecg.save_raw_data(filename_ecg)
        data_rr.save_raw_data(filename_rr)
        if(data_ecg.time != []):
          data_ecg.clear()
        if(data_rr.time != []):
          data_rr.clear()

      # Will disconnect
      await client.stop_notify(PMD_DATA)
      await client.disconnect()

    
  except Exception as e:
    print_exception(e, "connect", __file__)

## \brief Print details about device.
#
#  @param d Device.
def print_device(d):
  msg = "Device <<%s>> at <<%s>>" % (d.name, d.address)
  print_message(msg, "print_device", __file__)
  print("Name:     ", d.name)
  print("Address:  ", d.address)
  print("RSSI:     ", d.rssi)
  print("Details:  ")
  pprint.pprint(d.details)
  print("Metadata: ")
  pprint.pprint(d.metadata)
  
  #loop = asyncio.get_event_loop()
  #loop.run_until_complete(print_uuids(d))
  asyncio.run(print_uuids(d))

## \brief Scan and list nearby bluetooth devices.
#
#  Scan nearby devices and return those containing the
#  string received as parameter in their name.
#
#  Return list of devices with type bleak.backends.device.BLEDevice
#
#  @param name String to search in device name
async def list_devices(name=""):
  print_message("Scanning devices.", "list_devices", __file__)

  result = []
  devices = await BleakScanner.discover()
  for d in devices:
    if (d.name.find(name) < 0):
      continue
    msg = "Found device <<%s>> at <<%s>>" % (d.name, d.address)
    print_message(msg, "list_devices", __file__)
    result.append(d)
  return result

## \brief Llist nearby Polar devices.
#
#  Scan nearby devices and return those containing the
#  string "Polar" in the name.
#
#  Return list of devices with type bleak.backends.device.BLEDevice
#
def list_devices_polar():
  #loop = asyncio.get_event_loop()
  #result = loop.run_until_complete(list_devices("Polar"))
  result = asyncio.run(list_devices("Polar"))
  return result

def main():
  devices = list_devices_polar()
  msg = "Found %d device(s)" % (len(devices))
  print_message(msg, "main", __file__)
  for d in devices:
    pass
    #print_device(d)

  if (len(devices) == 0):
    print_message("Returning", "main", __file__)
    return

  d = devices[0]

  filename_rr = "/tmp/rr.tsv"
  Data.Data.remove(filename_rr)
  #asyncio.run(receive_rr(d, filename_rr))

  filename_ecg = "/tmp/ecg.tsv"
  Data.Data.remove(filename_ecg)
  #asyncio.run(receive_ecg(d, filename_ecg))

  asyncio.run(receive_both(d, filename_rr, filename_ecg))
  
  #task = asyncio.create_task(receive_rr(d))
  #await asyncio.gather(task)

  #loop = asyncio.get_event_loop()
  #loop.run_until_complete(receive_rr(d))
 
  return devices
  
    

if __name__ == '__main__':
  main()
