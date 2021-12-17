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
from lancamera import *
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

WIN_TITLE = "GUIIMP"

class WinMainTk(tk.Frame):

    ## Object constructor.
    #  @param self The object pointer.
    #  @param root The object root, usualy created by calling tkinter.Tk().
    def __init__(self, root):

        self.frame = tk.Frame.__init__(self, root)

        self.root = root

        self.create_frame_main()

        self.create_frame_toolbox()

        self.cap_cam1 = cv2.VideoCapture('john-mayer.mp4')
        self.cap_cam2 = cv2.VideoCapture('john-mayer.mp4')
        
    ## Create main frame, composed by an ImgCanvas object.
    #  @param self The object pointer.
    def create_frame_main(self):
        self.frame_main = tk.Frame(self.root)
        self.frame_main.grid(row=0, column=0, stick='nsew')

        self.frame1 = tk.Frame(self.frame_main, bg='black', height=400, width=600)
        self.frame2 = tk.Frame(self.frame_main, bg='black', height=400, width=600)
        self.frame1.grid(row=0, column=0, padx=50, pady=100)
        self.frame2.grid(row=0, column=1, padx=50, pady=100)

    ## Create toolbox frame, with buttons to access tools.
    #  @param self The object pointer.
    def create_frame_toolbox(self):
        self.frame_right = tk.Frame(self.root)
        self.frame_right.grid(row=0, column=1, stick='nswe', ipadx=5)

        self.root.columnconfigure(1, weight=0, minsize=200)

        BUTTON_WIDTH = 20

        self.selected_host_cam1 = tk.StringVar()
        self.selected_host_cam2 = tk.StringVar()

        self.btn_search =      tk.Button(self.frame_right, text="Scan the network", padx=3, width=BUTTON_WIDTH, command=self.search_network)

        self.select_cam1_label = tk.Label(self.frame_right,text="\nCAM 1", padx=3)
        self.select_cam2_label = tk.Label(self.frame_right,text="\nCAM 2", padx=3)
        self.btn_select_cam1 = tk.Button(self.frame_right, text="Select host", padx=3, width=BUTTON_WIDTH, command=self.select_host_cam1)
        self.btn_select_cam2 = tk.Button(self.frame_right, text="Select host", padx=3, width=BUTTON_WIDTH, command=self.select_host_cam2)

        self.select_routine_label = tk.Label(self.frame_right,text="\nRoutine\nNo file selected", padx=3)
        self.btn_routine =     tk.Button(self.frame_right, text="Select routine file", padx=3, width=BUTTON_WIDTH, command=self.select_routine_file)

        self.schedule_time_label = tk.Label(self.frame_right, text="\nSelect routine start in seconds", padx=3)
        self.schedule_time = tk.Entry(self.frame_right, width=BUTTON_WIDTH)
        self.btn_schedule =    tk.Button(self.frame_right, text="Schedule routine start", padx=3, width=BUTTON_WIDTH, command=self.schedule_routine)

        self.combo_box_cam1 = ttk.Combobox(self.frame_right, width=BUTTON_WIDTH, textvariable=self.selected_host_cam2)
        self.combo_box_cam1['state'] = 'readonly'

        self.combo_box_cam2 = ttk.Combobox(self.frame_right, width=BUTTON_WIDTH, textvariable=self.selected_host_cam1)
        self.combo_box_cam2['state'] = 'readonly'


        self.btn_search.grid(row=0, column=0, ipady=10, pady=(100,0))

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

    def get_frame_cam1(self):
        _, frame = self.cap_cam1.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        return imgtk

    def get_frame_cam2(self):
        _, frame = self.cap_cam2.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        return imgtk

    def show_video_cam1(self, frame=None):
        imgtk = self.get_frame_cam1()
        self.image_frame1.imgtk = imgtk
        self.image_frame1.configure(image=imgtk)
        self.image_frame1.after(10, self.show_video_cam1) 

    def show_video_cam2(self, frame=None):
        imgtk = self.get_frame_cam2()
        self.image_frame2.imgtk = imgtk
        self.image_frame2.configure(image=imgtk)
        self.image_frame2.after(10, self.show_video_cam2) 

    def select_host_cam1(self):
        """first establish connection with host1"""
        print("Select host cam1")
        self.image_frame1 = tk.Label(self.frame1)
        self.image_frame1.pack()

        self.show_video_cam1()

    def select_host_cam2(self):
        """first establish connection with host2"""
        print("Select host cam2")
        self.image_frame2 = tk.Label(self.frame2)
        self.image_frame2.pack()

        self.show_video_cam2()

    def search_network(self):
        """ replace with call to list_cams_local"""
        self.combo_box_cam1['values'] = ['mock' for m in range(5)]
        self.combo_box_cam2['values'] = ['mock' for m in range(5)]
        print("Search network")

    def select_routine_file(self):
        self.routine_filename = tk.filedialog.askopenfilename()
        if not self.routine_filename:
            return
        print(f"Log: selected {self.routine_filename}")
        self.select_routine_label.config(text=f"\nRoutine\n{self.routine_filename.split('/')[-1]}")
        """ do stuff with the file
            ..."""

    def schedule_routine(self):
        try:
            delay = int(self.schedule_time.get())
        except:
            tk.messagebox.showerror(title="Error Scheduling Routine", message="The specificied time is not a number")
            return
            
        time.sleep(delay)
        """ implement function to execute routine..."""

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

