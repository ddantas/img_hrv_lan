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

# python 2
# import Tkinter as tk

# import my
import math as m
import os
import threading
import time

from PIL import Image
from PIL import ImageTk

from lancamera import *
# import ImgCanvas as ic
# import WinThresh
# import WinContrast

WIN_TITLE = "GUIIMP"
IMG_DATA_SIZE = struct.calcsize('>L')

class CamScreen(tk.Frame):

    def __init__(self, window, client, vid='john-mayer.mp4'):
        super().__init__(window)
        self.client = client
        self.window = window
        self.width = 600
        self.height = 480
        self.screen = tk.Label(window, width=self.width, height=self.height, bg='black')
        self.screen.pack()
        self.delay = 15

    def display_frames(self):

        try:
            frame = self.client.recv_frame(IMG_DATA_SIZE)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        except:
            self.client.stop_streaming_client()
            self.client.stop_commands_client()
            self.screen.config(image='', bg='black')
            return

        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.screen.imgtk = imgtk
        self.screen.config(image=imgtk)

        self.window.after(self.delay, self.display_frames)      

class WinMainTk(tk.Frame):

    ## Object constructor.
    #  @param self The object pointer.
    #  @param root The object root, usualy created by calling tkinter.Tk().
    def __init__(self, root):

        self.frame = tk.Frame.__init__(self, root)

        self.root = root
        self.client1 = Client()
        self.client2 = Client()

        self.create_frame_main()

        self.create_frame_toolbox()
        
    ## Create main frame, composed by an ImgCanvas object.
    #  @param self The object pointer.
    def create_frame_main(self):
        self.frame_main = tk.Frame(self.root)
        self.frame_main.grid(row=0, column=0, stick='nsew')

        self.frame1 = tk.Frame(self.frame_main, bg='black', height=480, width=600)
        self.frame2 = tk.Frame(self.frame_main, bg='black', height=480, width=600)

        self.frame1.pack_propagate(False)
        self.frame2.pack_propagate(False)
        self.frame1.grid_propagate(False)
        self.frame2.grid_propagate(False)

        self.frame1.grid(row=0, column=0, padx=50, pady=100)
        self.frame2.grid(row=0, column=1, padx=50, pady=100)

        self.screen1 = CamScreen(self.frame1, self.client1)
        self.screen1.pack()
        self.screen2 = CamScreen(self.frame2, self.client2)
        self.screen2.pack()

    ## Create toolbox frame, with buttons to access tools.
    #  @param self The object pointer.
    def create_frame_toolbox(self):
        self.frame_right = tk.Frame(self.root)
        self.frame_right.grid(row=0, column=1, stick='nswe', ipadx=5)

        self.root.columnconfigure(1, weight=0, minsize=200)

        BUTTON_WIDTH = 20

        self.selected_host_cam1 = tk.StringVar()
        self.selected_host_cam2 = tk.StringVar()

        self.btn_scan = tk.Button(self.frame_right, text="Scan the network", padx=3, width=BUTTON_WIDTH,
                                    command=self.scan_network)

        self.select_cam1_label = tk.Label(self.frame_right,text="\nCAM 1", padx=3)
        self.select_cam2_label = tk.Label(self.frame_right,text="\nCAM 2", padx=3)

        self.btn_select_cam1 = tk.Button(self.frame_right, text="Select host", padx=3, width=BUTTON_WIDTH, 
                                            command=self.select_host_cam1)
        self.btn_select_cam2 = tk.Button(self.frame_right, text="Select host", padx=3, width=BUTTON_WIDTH, 
                                            command=self.select_host_cam2)

        self.select_routine_label = tk.Label(self.frame_right,text="\nRoutine\nNo file selected", padx=3)
        self.btn_routine = tk.Button(self.frame_right, text="Select routine file", padx=3, width=BUTTON_WIDTH, 
                                        command=self.select_routine_file)

        self.schedule_time_label = tk.Label(self.frame_right, text="\nSelect routine start in seconds", padx=3)

        self.schedule_time = tk.Entry(self.frame_right, width=BUTTON_WIDTH)
        self.schedule_time.insert(0, '0')

        self.btn_schedule = tk.Button(self.frame_right, text="Schedule routine start", padx=3, width=BUTTON_WIDTH, 
                                        command=self.schedule_routine)

        self.combo_box_cam1 = ttk.Combobox(self.frame_right, width=BUTTON_WIDTH, textvariable=self.selected_host_cam1)
        self.combo_box_cam1['state'] = 'readonly'

        self.combo_box_cam2 = ttk.Combobox(self.frame_right, width=BUTTON_WIDTH, textvariable=self.selected_host_cam2)
        self.combo_box_cam2['state'] = 'readonly'

        self.btn_scan.grid(row=0, column=0, ipady=10, pady=(100,0))

        self.select_cam1_label.grid(row=1, column=0, ipady=10)
        self.combo_box_cam1.grid(row=2, column=0, ipady=10)
        self.btn_select_cam1.grid(row=3, column=0, ipady=10)

        self.select_cam2_label.grid(row=4, column=0, ipady=10)
        self.combo_box_cam2.grid(row=5, column=0, ipady=10)
        self.btn_select_cam2.grid(row=6, column=0, ipady=10)

        self.select_routine_label.grid(row=7, column=0, ipady=10)
        self.btn_routine.grid(row=8, column=0, ipady=10)

        self.schedule_time_label.grid(row=9, column=0, ipady=10)
        self.schedule_time.grid(row=10, column=0, ipady=10)
        self.btn_schedule.grid(row=11, column=0, ipady=10, pady=(0,100))

    def scan_network(self):

        hosts = self.client1.list_cams_lan()  

        if not hosts:
            tk.messagebox.showwarning(title="Scanning complete", message="No devices found")  
            return

        tk.messagebox.showinfo(title="Scanning complete", message="HOSTS updated")  

        values = []
        for host, devices in hosts.items():
            for dev in devices: 
                values.append(f'{host}; #{dev}')

        self.combo_box_cam1['values'] = values
        self.combo_box_cam2['values'] = values


    def select_host_cam1(self):

        host = self.selected_host_cam1.get()
        if not host:
            tk.messagebox.showerror(title="Error Connecting to HOST 1", message="Select HOST 1 first")  
            return    

        self.combo_box_cam1['values'] = list(self.combo_box_cam1['values']).remove(host) 
        self.combo_box_cam2['values'] = list(self.combo_box_cam2['values']).remove(host) 
        host = host.split('#')
        device = host[1]
        split_host = host[0].split(';')
        host = split_host[0]
        port = 9000

        # should send message to server to record its screen, because the server won't be able to capture the
        # device that is being used to record the subjects camera

        self.client1.set_host(host, port)
        self.client1.start_commands_connection()

        self.client1.send_command(f'SELECT {device}')

        self.client1.start_connection()
        client1_thread = threading.Thread(target=lambda : self.screen1.display_frames())
        client1_thread.start()
        
    def select_host_cam2(self):

        host = self.selected_host_cam2.get()
        if not host:
            tk.messagebox.showerror(title="Error Connecting to HOST 2", message="Select HOST 2 first")  
            return    

        self.combo_box_cam1['values'] = list(self.combo_box_cam1['values']).remove(host) 
        self.combo_box_cam2['values'] = list(self.combo_box_cam2['values']).remove(host) 

        host = host.split('#')
        device = host[1]
        split_host = host[0].split(';')
        host = split_host[0]
        port = 9000

        # should send message to server to record its screen, because the server won't be able to capture the
        # device that is being used to record the subjects camera

        self.client2.set_host(host, port)
        self.client2.start_commands_connection()

        self.client2.send_command(f'SELECT {device}')

        self.client2.start_connection()
        client2_thread = threading.Thread(target=lambda : self.screen2.display_frames())
        client2_thread.start()

    def select_routine_file(self):
        self.routine_filename = tk.filedialog.askopenfilename()

        if not self.routine_filename:
            return

        print(f"Log: selected {self.routine_filename}")
        self.select_routine_label.config(text=f"\nRoutine\n{self.routine_filename.split('/')[-1]}")

    def schedule_routine(self):

        try:
            delay = int(self.schedule_time.get())
        except:
            tk.messagebox.showerror(title="Error Scheduling Routine", message="The specified time is not a number")
            return

        thread = threading.Thread(target=self.send_routine, args=(delay, ))
        thread.start()
        
    def send_routine(self, delay):
        try:
            with open(self.routine_filename) as f:
                routine = f.read()
        except:            
            tk.messagebox.showerror(title="Error Scheduling Routine", message="No file was specified")
            return

        time.sleep(delay)
        cur_time = 0.0
        self.client1.send_command("ROUTINE")
        self.client2.send_command("ROUTINE")
        lines = routine.split('\n')
        
        for line in lines:

            if line:
                cmds = line.split(';')
                instant, cmd, hosts, instruction = cmds
                instant = instant.strip()
                cmd = cmd.strip()
                hosts = hosts.strip()
                instruction = instruction.lstrip()
                instruction = instruction.rstrip()
                instant = float(instant)
                print(cur_time, instant, cmd, hosts, instruction)

                if instant - cur_time > 0:
                    time.sleep(instant - cur_time)
                    cur_time += instant - cur_time

                if hosts == 'all':
                    hosts = ['s1', 's2']

                if 's1' in hosts:
                    self.client1.send_command(cmd + ';' + instruction)

                if 's2' in hosts:
                    self.client2.send_command(cmd + ';' + instruction)

        self.client1.send_command("ROUTINEEND")
        self.client2.send_command("ROUTINEEND")

    def cleanup(self):

        self.client1.stop_commands_client()
        self.client1.stop_streaming_client()
        self.client2.stop_commands_client()
        self.client2.stop_streaming_client()

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
  app.mainloop()
  app.cleanup()

