#!/usr/bin/python3
# -*- coding: utf-8 -*-

# python 3
import tkinter as tk
from tkinter import ttk
import cv2
import tkinter.messagebox
import tkinter.filedialog

import math as m
import os
import threading
import time
import sys

from PIL import Image
from PIL import ImageTk

from lancamera import *

WIN_TITLE = "Server Window"

class WinSub(tk.Frame):

    ## Object constructor.
    #  @param self The object pointer.
    #  @param root The object root, usualy created by calling tkinter.Tk().
    def __init__(self, root, host, port):

        self.frame = tk.Frame.__init__(self, root)

        self.root = root
        self.host = host
        self.port = port
        self.videoCap = None
        self.__streaming = False
        self.__playing_video = False
        # self.root.attributes('-fullscreen', 1)

        self.server = Server()
        self.client = Client(HOST=self.host, PORT=self.port)

        self.init_server()

        self.create_frame_main()
        
    ## Create main frame, composed by an ImgCanvas object.
    #  @param self The object pointer.
    def create_frame_main(self):

        self.frame_main = tk.Frame(self.root)
        self.frame_main.grid(row=0, column=0, sticky='')

        self.screen_frame = tk.Frame(self.frame_main, width=600, height=480, bg='black')
        self.screen_frame.pack_propagate(False)
        self.screen = tk.Label(self.screen_frame, bg='black')
        self.screen.pack()
        self.message_frame = tk.Frame(self.frame_main)

        self.msg = tk.StringVar()
        self.msg.set("")

        self.message = tk.Label(self.message_frame, textvariable=self.msg, font=50, relief=tk.RIDGE,
                        bg='white', padx=10, pady=10, width=50, height=5, wraplength=500)

        self.screen_frame.grid(row=0, column=0, padx=50, pady=(50,0))
        self.message_frame.grid(row=1, column=0, padx=50, pady=(50,0))
        self.message.pack()

        self.width, self.height = self.root.winfo_screenwidth()/2, self.root.winfo_screenheight()/2

    def init_server(self):

        self.server.start_stream_server()
        self.server.start_commands_server(routine_handler=self.execute_command)

    def execute_command(self, cmd, instruction):

        if cmd == 'message':
            # display message; instruction: string
            self.msg.set(instruction)

        elif cmd == 'clear':
            # clear the canvas; instruction: camera (int)
            if self.__streaming:
                
                self.__streaming = False

            if self.__playing_video:
                self.__playing_video = False

            self.screen.config(bg=instruction)
            self.screen_frame.config(bg=instruction)

        elif cmd == 'play': 
            # show video stream; instruction: color (string)
            if self.__streaming:
                self.__streaming = False

            self.__playing_video = True
            
            if self.videoCap:
                self.videoCap.release()

            self.videoCap = cv2.VideoCapture(instruction)
            video_thread = threading.Thread(target=self.show_video)
            video_thread.start()

        elif cmd == 'show':
            # play the video; instruction: video (string)
            if self.__playing_video:
                self.__playing_video = False

            self.__streaming = True

            self.client.start_connection()
            stream_thread = threading.Thread(target=self.display_frames)
            stream_thread.start()

        elif cmd == 'stop':

            if self.__streaming:
                self.__streaming = False
                self.client.stop_streaming_client()

            elif self.__playing_video:
                self.__playing_video = False
                self.videoCap.release()

            self.screen.config(image='', bg='black')
            self.screen_frame.config(bg='black')

    def show_video(self):

        if not self.__playing_video:
            return

        _, frame = self.videoCap.read()
        # frame = cv2.resize(frame, (self.width, self.height))
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.screen.configure(image=imgtk)
        self.screen.imgtk = imgtk
        self.screen.after(20, self.show_video)

    def display_frames(self):

        if not self.__streaming:
            return

        img_data_size = struct.calcsize('>L')
        frame = self.client.recv_frame(img_data_size)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.screen.configure(image=imgtk)
        self.screen.imgtk = imgtk
        self.screen.after(1, self.display_frames)


    def cleanup(self):

        self.__streaming = False
        self.__playing_video = False
        
        self.server.stop_commands_server()
        self.server.stop_stream()

        self.client.stop_streaming_client()

"""#########################################################
############################################################
### Main function                                        ###
############################################################
#########################################################"""


if __name__ == "__main__":

    # if len(sys.argv) < 3:
    #     print("Please specify HOST and PORT for connection.")
    #     "Usage: python WinSub.py <HOST> <PORT>")
    #     exit(1)

    # host = sys.argv[1]
    # port = int(sys.argv[2])
    host=''
    port=9000
    
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.title(WIN_TITLE)
    root.minsize(300,300)

    app = WinSub(root, host, port)
    app.mainloop()
    app.cleanup()

