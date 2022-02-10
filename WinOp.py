#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""#########################################################
############################################################
### Basic user interface in tkinter.                     ###
###                                                      ###
### Author: Daniel Dantas                                ###
### Last edited: August 2018                             ###
############################################################
#########################################################"""


# python 3
import tkinter as tk
from tkinter import ttk
import cv2
import tkinter.messagebox
import tkinter.filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
    NavigationToolbar2Tk)

import math as m
import os
import threading
import time
import datetime as dt

from PIL import Image
from PIL import ImageTk

from LanDevice import *
import Plot
import Data

WIN_TITLE = "Operator Window"
IMG_DATA_SIZE = struct.calcsize('>L')
DEBUG = 1

## \brief HrvScreen class
# Class responsible for using a connected client to receive, save and plot the ECG and RR data.
class HrvScreen(tk.Frame):

    ## \brief Object constructor.
    #  @param self The object pointer.
    #  @param window The object root, which will always be a Frame inside of a tkinter.Tk() object.
    #  @param client The Client which will receive the bluetooth data.
    #  @param path The path where the program will save the received bluetooth data.
    #  @param name The name of the object, used to differentiate between different files.
    def __init__(self, window, client, path, name='subj'):
        super().__init__(window)
        self.client = client
        self.window = window
        self.recording = False
        self.is_receiving_data = False
        self.name = name
        self.path = path
        self.filename_ecg = self.path + self.name + '_ecg.tsv'
        self.filename_rr = self.path + self.name + '_rr.tsv'
        self.plot = Plot.Plot()
        self.init_plot()
        self.hrv_plot = FigureCanvasTkAgg(self.plot.fig, master=self.window)
        self.hrv_plot.get_tk_widget().grid(padx=50, pady=(0,50))

    ## \brief Initiate the plotting figure where the ECG and RR data will be displayed.
    #  @param self The object pointer.
    def init_plot(self):
        self.plot.fig = Figure(figsize=(5,3))
        self.plot.ax_rr = self.plot.fig.add_subplot(211)
        self.plot.ax_ecg = self.plot.fig.add_subplot(212)

    ## \brief Use its client to receive the ECG and RR data, save it to the disk, and plot it on the screen.
    #  @param self The object pointer.
    def display_hrv_plot(self):
        self.is_receiving_data = True
        while self.is_receiving_data:
            try:
                packet = self.client.recv_values()
                data = packet.decode_packet()
                print(self.name[-1], end="")

                if data.datatype == Data.TYPE_ECG:

                    if self.recording:
                        data.save_raw_data(self.filename_ecg)

                    self.plot.plot_incremental(data.values_ecg, Plot.TYPE_ECG)

                    if(data.time != []):
                        data.clear()

                else:
                    if self.recording:
                        data.save_raw_data(self.filename_rr)

                    self.plot.plot_incremental(data.values_hr, Plot.TYPE_RR)

                    if(data.time != []):
                        data.clear()

                self.hrv_plot.draw()


            except Exception as e:
                self.is_receiving_data = False
                break


    ## \brief Set a flag to tell the display thread to start recording.
    #  @param self The object pointer.
    def start_recording(self):
        self.recording = True

    def stop_recording(self):
        self.recording = False

    ## \brief Set a flag to tell the display thread to stop running.
    #  @param self The object pointer.
    def cleanup(self):
        self.is_receiving_data = False

    def reset_screen(self, path):
        self.path = path
        self.filename_ecg = self.path + self.name + '_ecg.tsv'
        self.filename_rr = self.path + self.name + '_rr.tsv'

## \brief CamScreen class
# Class responsible for using a connected client to receive, save and display the video streaming data.
class CamScreen(tk.Frame):

    def __init__(self, window, client, path, name='subj'):
        super().__init__(window)
        self.is_receiving_video = False
        self.recording = False
        self.client = client
        self.window = window
        self.name = name
        self.path = path
        self.cap = cv2.VideoWriter(self.path + self.name + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30.0, (640,480))
        self.width = 600
        self.height = 480
        self.frame = tk.Frame(self.window, bg='black', height=480, width=600)
        self.frame.grid_propagate(False)
        self.frame.grid(padx=50, pady=50)
        self.screen = tk.Label(self.frame, width=self.width, height=self.height, bg='black')
        self.screen.grid()

    ## \brief Use its client to receive the video streaming data, save it to the disk, and display it on the screen.
    #  @param self The object pointer.
    def display_frames(self):

        self.is_receiving_video = True

        while self.is_receiving_video:

            frame = self.client.recv_frame(IMG_DATA_SIZE)

            if len(frame) == 0:
                self.is_receiving_video = False
                # self.screen.config(image='', bg='black')
                break

            if self.recording:
                self.cap.write(frame)

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            self.screen.config(image=imgtk)
            self.screen.imgtk = imgtk

        self.screen.config(image='', bg='black')

    # ## \brief Set a flag to tell the display thread to start recording.
    # #  @param self The object pointer.
    def start_recording(self):
        self.recording = True

    def stop_recording(self):
        self.recording = False

    ## \brief Set a flag to tell the display thread to stop running and release the VideoCapture object.
    #  @param self The object pointer.
    def cleanup(self):
        self.is_receiving_video = False
        self.cap.release()

    def reset_screen(self, path):
        self.path = path
        self.cap = cv2.VideoWriter(self.path + self.name + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30.0, (640,480))


class WinMainTk(tk.Frame):

    ## \brief Object constructor.
    #  @param self The object pointer.
    #  @param root The object root, usualy created by calling tkinter.Tk().
    def __init__(self, root):

        self.frame = tk.Frame.__init__(self, root)
        self.stop = False
        self.root = root
        self.client1 = Client()
        self.client2 = Client()
        self.scanner = Client()

        self.set_dir_name()        

        self.create_frame_main()

        self.create_frame_toolbox()

  
    ## \brief Log all desired events to stdout and a file using a specific template.
    #  @param text The text that will be written.
    def log(self, text):
        now = datetime.datetime.now()
        log_template = f'{now} Log:'
        print(log_template + text)

        with open(self.path + 'log.txt', 'a') as log:
            print(log_template + text, file=log)

    ## \brief Set automatically to what directory the received data (video and [ECG,RR]) will be saved to.
    #  @param self The object pointer.
    def set_dir_name(self):

        if not os.path.isdir('./data'):
            os.mkdir('./data')

        if DEBUG:
            if not os.path.isdir('./data/DEBUG'):
                os.mkdir('./data/DEBUG')      

            self.path = 'data/DEBUG/'
            self.log(f"saving the recordings at {self.path}")
            return

        dirs = os.listdir('./data')

        if 'DEBUG' in dirs:
            dirs.remove('DEBUG')

        dirs.sort()

        num = 0
        for d in dirs:
            dir_num = int(d)
            if dir_num > num+1:
                break
            num+=1

        new_dir = num+1
        path =f'./data/{new_dir:03d}/'
        self.path = path 
        os.mkdir(self.path)

        self.log(f"saving the recordings at {self.path}")


    ## \brief Create main frame, composed by two frames.
    #  Create main frame, composed by two frames, one contains two CamScreens and two HrvScreens
    #  and the other one contains a toolbox for all the program's functionalities.
    #
    #  @param self The object pointer.
    def create_frame_main(self):
        self.frame_main = tk.Frame(self.root)

        self.frame_main.grid(row=0, column=0, stick='nsew')

        self.frame1_parent = tk.Frame(self.frame_main, height=600, width=600)
        self.frame2_parent = tk.Frame(self.frame_main, height=600, width=600)

        self.frame1_parent.grid(row=0, column=0, stick='nsew')
        self.frame2_parent.grid(row=0, column=1, stick='nsew')

        self.screen1 = CamScreen(self.frame1_parent, self.client1, self.path, name='subj1')
        self.screen1.grid(row=0, column=0)
        
        self.hrv_plot1 = HrvScreen(self.frame1_parent, self.client1, self.path, name='subj1')
        self.hrv_plot1.grid(row=1, column=0)

        self.screen2 = CamScreen(self.frame2_parent, self.client2, self.path, name='subj2')
        self.screen2.grid(row=0, column=0)

        self.hrv_plot2 = HrvScreen(self.frame2_parent, self.client2, self.path, name='subj2')
        self.hrv_plot2.grid(row=1, column=0)

    ## \brief Create toolbox frame, with buttons and entry fields to use the tools.
    #  @param self The object pointer.
    def create_frame_toolbox(self):
        self.frame_right = tk.Frame(self.root)
        self.frame_right.grid(row=0, column=1, stick='nswe', ipadx=5)

        self.root.columnconfigure(1, weight=0, minsize=200)

        BUTTON_WIDTH = 45
        IPADY = 3

        self.selected_host_cam1 = tk.StringVar()
        self.selected_host_cam2 = tk.StringVar()

        self.selected_host_polar1 = tk.StringVar()
        self.selected_host_polar2 = tk.StringVar()

        # self.btn_scan = tk.Button(self.frame_right, text="Scan the network", padx=3, width=BUTTON_WIDTH,
        #                             command=lambda: self.start_scan('network'))

        self.btn_scan = tk.Button(self.frame_right, text="Scan the network", padx=3, width=BUTTON_WIDTH,
                                    command=lambda: self.reset_capture())

        self.scan_at = tk.Label(self.frame_right,text="\nScan specific host", padx=3)
        self.btn_scan_at = tk.Button(self.frame_right, text="Scan host", padx=3, width=BUTTON_WIDTH,
                                    command=lambda: self.start_scan('specific'))
        self.scan_entry = tk.Entry(self.frame_right, width=BUTTON_WIDTH)

        self.select_cam1_label = tk.Label(self.frame_right,text="\nCAM 1", padx=3)
        self.select_cam2_label = tk.Label(self.frame_right,text="\nCAM 2", padx=3)

        self.select_polar1_label = tk.Label(self.frame_right,text="\nPolar 1", padx=3)
        self.select_polar2_label = tk.Label(self.frame_right,text="\nPolar 2", padx=3)

        self.btn_select_cam1 = tk.Button(self.frame_right, text="Select host", padx=3, width=BUTTON_WIDTH, 
                                            command=lambda : self.select_host_cam(1))
        self.btn_select_cam2 = tk.Button(self.frame_right, text="Select host", padx=3, width=BUTTON_WIDTH, 
                                            command=lambda : self.select_host_cam(2))

        self.btn_select_polar1 = tk.Button(self.frame_right, text="Select Polar device", padx=3, width=BUTTON_WIDTH, 
                                            command=lambda : self.select_host_polar(1))
        self.btn_select_polar2 = tk.Button(self.frame_right, text="Select Polar device", padx=3, width=BUTTON_WIDTH, 
                                            command=lambda : self.select_host_polar(2))

        self.select_routine_label = tk.Label(self.frame_right,text="\nRoutine\nNo file selected", padx=3)
        self.btn_routine = tk.Button(self.frame_right, text="Select routine file", padx=3, width=BUTTON_WIDTH, 
                                        command=self.select_routine_file)

        self.schedule_time_label = tk.Label(self.frame_right, text="\nSelect routine start in seconds", padx=3)

        self.schedule_time = tk.Entry(self.frame_right, width=BUTTON_WIDTH)
        self.schedule_time.insert(0, '10')

        self.btn_schedule = tk.Button(self.frame_right, text="Schedule routine start", padx=3, width=BUTTON_WIDTH, 
                                        command=self.schedule_routine)

        self.combo_box_cam1 = ttk.Combobox(self.frame_right, width=BUTTON_WIDTH, textvariable=self.selected_host_cam1)
        self.combo_box_cam1['state'] = 'readonly'

        self.combo_box_cam2 = ttk.Combobox(self.frame_right, width=BUTTON_WIDTH, textvariable=self.selected_host_cam2)
        self.combo_box_cam2['state'] = 'readonly'

        self.combo_box_polar1 = ttk.Combobox(self.frame_right, width=BUTTON_WIDTH, textvariable=self.selected_host_polar1)
        self.combo_box_polar1['state'] = 'readonly'

        self.combo_box_polar2 = ttk.Combobox(self.frame_right, width=BUTTON_WIDTH, textvariable=self.selected_host_polar2)
        self.combo_box_polar2['state'] = 'readonly'

        self.stop_btn = tk.Button(self.frame_right, text="FINISH CAPTURE", padx=3, width=BUTTON_WIDTH, 
                                        command=self.cleanup)

        self.reset_btn = tk.Button(self.frame_right, text="RESET CAPTURE", padx=3, width=BUTTON_WIDTH, 
                                        command=self.reset_capture)

        self.btn_scan.grid(row=0, column=0, ipady=IPADY, pady=(10,0))

        self.scan_at.grid(row=1, column=0, ipady=IPADY)
        self.scan_entry.grid(row=2, column=0, ipady=IPADY)
        self.btn_scan_at.grid(row=3, column=0, ipady=IPADY)

        self.select_cam1_label.grid(row=4, column=0, ipady=IPADY)
        self.combo_box_cam1.grid(row=5, column=0, ipady=IPADY)
        self.btn_select_cam1.grid(row=6, column=0, ipady=IPADY)

        self.select_cam2_label.grid(row=7, column=0, ipady=IPADY)
        self.combo_box_cam2.grid(row=8, column=0, ipady=IPADY)
        self.btn_select_cam2.grid(row=9, column=0, ipady=IPADY)

        self.select_polar1_label.grid(row=10, column=0, ipady=IPADY)
        self.combo_box_polar1.grid(row=11, column=0, ipady=IPADY)
        self.btn_select_polar1.grid(row=12, column=0, ipady=IPADY)

        self.select_polar2_label.grid(row=13, column=0, ipady=IPADY)
        self.combo_box_polar2.grid(row=14, column=0, ipady=IPADY)
        self.btn_select_polar2.grid(row=15, column=0, ipady=IPADY)

        self.select_routine_label.grid(row=16, column=0, ipady=IPADY)
        self.btn_routine.grid(row=17, column=0, ipady=IPADY)

        self.schedule_time_label.grid(row=18, column=0, ipady=IPADY)
        self.schedule_time.grid(row=19, column=0, ipady=IPADY)
        self.btn_schedule.grid(row=20, column=0, ipady=IPADY, pady=(10,0))
        self.reset_btn.grid(row=21, column=0, ipady=IPADY, pady=IPADY)
        self.stop_btn.grid(row=22, column=0, ipady=IPADY, pady=(0,10))

    ## \brief Scan the network or one specific host looking for open WinSub servers.
    #  @param self The object pointer.
    #  @param scope The scope of the scan, it is either done for the whole network (256 hosts) or 1 specific host.
    def start_scan(self, scope):

        if scope not in ['network', 'specific']:
            return

        if scope == 'network':
            thread = threading.Thread(target=self.scan_network)

        else:
            thread = threading.Thread(target=self.scan_host_at)

        thread.start()

    ## \brief Scan the network looking for open WinSub servers. Will be called by self.start_scan.
    #  @param self The object pointer.
    def scan_network(self):

        # hosts = self.scanner.list_servers([9000,9001,9002])
        hosts = self.scanner.list_servers([9000])

        if not hosts:
            tk.messagebox.showwarning(title="Scanning complete", message="No devices found")  
            return

        print(hosts)
        cameras = []
        polars = []
        devices = {}

        for ip, ports in hosts.items():

            # if ports == [9000, 9001, 9002]:
            if ports == [9000]:

                cameras = self.scanner.list_cams_at(ip)
                polars = self.scanner.list_polars_at(ip)

                devices[ip] = (cameras, polars)

        if devices == {}:

            return
        camera_values = []
        polar_values = []

        for host, devs in devices.items():
            cams = devs[0]
            sensors = devs[1]
            print(cams, sensors)
            for dev in cams:
                camera_values.append(f'{host}; #{dev}')

            for dev in sensors:
                polar_values.append(f'{host}; #{dev}')

        self.combo_box_cam1['values'] = camera_values
        self.combo_box_cam2['values'] = camera_values

        self.combo_box_polar1['values'] = polar_values
        self.combo_box_polar2['values'] = polar_values

        tk.messagebox.showinfo(title="Scanning complete", message="HOSTS updated")  

    ## \brief Scan a specific host looking for open WinSub servers. Will be called by self.start_scan.
    #  @param self The object pointer.
    def scan_host_at(self):

        try:
            ip = self.scan_entry.get()
            if ip == '':
                ip = self.scanner.get_local_machine_ip()
                print(ip)
        except:
            tk.messagebox.showerror(title="Error Obtaining IP to scan", message="Please specify the host IP correctly")
            return

        try:
            cameras = self.scanner.list_cams_at(ip)
        except TimeoutError:
            tk.messagebox.showerror(title="Error Scanning HOST", message="Scan timed out, HOST doesn't exist")
            return
        except ConnectionRefusedError:
            tk.messagebox.showerror(title="Error Scanning HOST", message="This HOST is not running a Server")
            return

        try:
            polars = self.scanner.list_polars_at(ip)
        except:            
            tk.messagebox.showerror(title="Error Scanning for polar devices", message="Please check your server and devices")
            return

        found = 2
        if not cameras:
            tk.messagebox.showwarning(title="Scanning complete", message="No cameras found")
            found -= 1
        if not polars:
            tk.messagebox.showwarning(title="Scanning complete", message="No Polar Sensors found")  
            found -= 1

        if found == 0:
            return

        tk.messagebox.showinfo(title="Scanning complete", message="HOSTS updated")  

        cam_values = []
        for dev in cameras: 
                cam_values.append(f'{ip}; #{dev}')

        for v in cam_values:
            if v in self.combo_box_cam1['values'] or v in self.combo_box_cam2['values']:
                cam_values = cam_values.remove(v)

        if cam_values:
            cam_values = [*self.combo_box_cam1['values'], *cam_values]
        else:
            cam_values = self.combo_box_cam1['values']

        self.combo_box_cam1['values'] = cam_values
        self.combo_box_cam2['values'] = cam_values

        polar_values = []
        for dev in polars:
            polar_values.append(f'{ip}; {dev}')

        for v in polar_values:
            if v in self.combo_box_polar1['values'] or v in self.combo_box_polar2['values']:
                polar_values = polar_values.remove(v)

        if polar_values:
            polar_values = [*self.combo_box_polar1['values'], *polar_values]
        else:
            polar_values = self.combo_box_polar1['values']   

        self.combo_box_polar1['values'] = polar_values
        self.combo_box_polar2['values'] = polar_values
         
    ## \brief Selects the camera of a host in the networks and starts a streaming connection to it's server.
    #  @param self The object pointer.
    #  @param slot A flag to specify which client to use in the connection and which CamScreen to display the streaming on.
    def select_host_cam(self, slot):

        if slot == 1:
            client = self.client1
            screen = self.screen1
            host = self.selected_host_cam1.get()

        else:
            client = self.client2
            screen = self.screen2
            host = self.selected_host_cam2.get()

        self.log(f"HOST {host} selected at CAM {slot}")
        if screen.is_receiving_video:
            return

        if not host:
            tk.messagebox.showerror(title="Error Connecting to HOST 1", message="Select HOST 1 first")  
            return    

        values = list(self.combo_box_cam1['values']).remove(host)
        self.combo_box_cam1['values'] = values
        self.combo_box_cam2['values'] = values

        host = host.split('#')
        device = host[1]
        split_host = host[0].split(';')
        host = split_host[0]

        client.set_host(host)

        try :
            client.start_commands_connection()
            client.send_command(f'SELECT CAM {device}')
            client.start_stream_connection()

        except:
            tk.messagebox.showinfo(title="Problems with HOST", message="Could not make the connection")
            return

        client_thread = threading.Thread(target=screen.display_frames)

        client_thread.start()

    ## \brief Selects the Polar Sensor of a host in the network and starts a streaming connection to it's server.
    #  @param self The object pointer.
    #  @param slot A flag to specify which client to use in the connection and which HrvScreen to display the streaming on.
    def select_host_polar(self, slot):

        if slot == 1:
            client = self.client1
            hrv_plot = self.hrv_plot1
            host = self.selected_host_polar1.get()

        else:
            client = self.client2
            hrv_plot = self.hrv_plot2
            host = self.selected_host_polar2.get()

        self.log(f"HOST {host} selected for Polar {slot}")
        ip, polar_tuple = host.split(';')
        polar_tuple = polar_tuple.replace(')','')
        polar_tuple = polar_tuple.replace('(','')
        name, addr = polar_tuple.split(',')
        addr = addr.replace(' ', '')

        client.set_host(ip)

        try:
            client.start_commands_connection()
            client.send_command(f'SELECT POLAR {addr}')
            client.start_polar_connection()

        except:
            tk.messagebox.showinfo(title="Problems with HOST", message="Could not make the connection")
            return

        print('checkpoint')
        client_thread = threading.Thread(target=lambda : hrv_plot.display_hrv_plot())
        client_thread.start()

    ## \brief Selects the routine file that will be used in the capture. 
    #  @param self The object pointer.
    def select_routine_file(self):
        self.routine_filename = tk.filedialog.askopenfilename()

        if not self.routine_filename:
            return

        self.log(f"selected {self.routine_filename}")
        self.select_routine_label.config(text=f"\nRoutine\n{self.routine_filename.split('/')[-1]}")

    ## \brief Gets the time at which the routine will start and call a thread to send the routine to all hosts. 
    #  @param self The object pointer.
    def schedule_routine(self):

        try:
            time_to_start = self.schedule_time.get()
        except:
            tk.messagebox.showerror(title="Error Scheduling Routine", message="The specified time is not a number")
            return

        if time_to_start == '':
            return

        if time_to_start == '0':
            tk.messagebox.showerror(title="Error Scheduling Routine", message="Please choose a number greater than 0")
            return

        thread = threading.Thread(target=self.send_routine, args=(time_to_start, ))
        thread.start()
 

    ## \brief Reads the routine file, calculate the time to start the routine and sends
    #  Reads the routine file, uses time_to_start to calculate at which clock time the routine should start and
    #  sends everything to all the hosts that are connected. Saves a copy of the routine file that was used 
    #  inside the directory that the data will be saved at. Starts recording streaming and Polar data.
    #
    #  @param self The object pointer.  
    #  @param time_to_start The time in seconds which should pass before the routine procedure starts.     
    def send_routine(self, time_to_start):

        try:
            with open(self.routine_filename) as f:
                routine_lines = f.readlines()
        except:            
            tk.messagebox.showerror(title="Error Scheduling Routine", message="No file was specified")
            return

        routine = ''
        for line in routine_lines:
            if line.strip()[0] != '#':
                routine += line
        i = -1
        while '#' in routine_lines[i]:
            i -= 1

        now = dt.datetime.now()
        time_to_start = int(now.timestamp()) + int(time_to_start)

        self.log(f"routine is schedule to start at {now + dt.timedelta(seconds=int(time_to_start))}")

        routine = str(time_to_start) + '\n' + routine

        if self.screen1.is_receiving_video:
            print(self.client2.get_streaming_dst())
            self.client1.send_command(f"ROUTINE;s1;{self.client2.get_streaming_dst()}")

        if self.screen2.is_receiving_video:
            print(self.client1.get_streaming_dst())
            self.client2.send_command(f"ROUTINE;s2;{self.client1.get_streaming_dst()}")

        if self.screen1.is_receiving_video:
            self.client1.send_command(routine)

        if self.screen2.is_receiving_video:
            self.client2.send_command(routine)

        with open(self.path + 'routine.txt', 'w') as f:
            f.write(routine)
            
        now = datetime.datetime.now().timestamp()
        delay = int(time_to_start) - now
        time.sleep(delay)

        self.screen1.start_recording()
        self.hrv_plot1.start_recording()
        self.screen2.start_recording()
        self.hrv_plot2.start_recording()

        time_to_end = routine_lines[i].split(';')[0]
        time.sleep(float(time_to_end))

        self.screen1.stop_recording()
        self.hrv_plot1.stop_recording()
        self.screen2.stop_recording()
        self.hrv_plot2.stop_recording()
        
    ## \brief Stop all threads and clients in order to exit the program cleanly.
    #  @param self The object pointer.
    def cleanup(self):

        self.screen1.cleanup()
        self.screen2.cleanup()

        self.hrv_plot1.cleanup()
        self.hrv_plot2.cleanup()

        self.client1.stop_commands_client()
        self.client1.stop_stream_client()
        self.client1.stop_polar_client()

        self.client2.stop_commands_client()
        self.client2.stop_stream_client()
        self.client2.stop_polar_client()

        self.stop = True

    def reset_capture(self):
        self.cleanup()
        self.stop = False
        host1 = self.client1.get_streaming_dst()
        host2 = self.client1.get_streaming_dst()
        self.client1.__init__(HOST=host1)
        self.client2.__init__(HOST=host2)


    def check_stop(self):

        if self.stop or DEBUG:
            self.root.destroy()

        else:
            tk.messagebox.showwarning(title="Unable to Quit the APP", message="Click on FINISH CAPTURE first")

"""#########################################################
############################################################
### Main function                                        ###
############################################################
#########################################################"""


if __name__ == "__main__":

    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.title(WIN_TITLE)
    root.minsize(300,300)
    app = WinMainTk(root)
    root.protocol("WM_DELETE_WINDOW", app.check_stop)
    app.mainloop()
