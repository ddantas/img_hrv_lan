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
import struct

from PIL import Image
from PIL import ImageTk

import LanDevice as dev
import const as k

WIN_TITLE = "Server Window"

class WinSub(tk.Frame):

    ## \brief Object constructor.
    #  @param self The object pointer.
    #  @param root The object root, usualy created by calling tkinter.Tk().
    def __init__(self, root, host):

        self.frame = tk.Frame.__init__(self, root)

        self.root = root
        self.host = host
        self.videoCap = None
        self.videoFps = 0
        self.connected = False
        self.__clear = False
        self.is_receiving_video = False
        self.is_playing_video = False
        self.threads = []
        # self.root.attributes('-fullscreen', 1)

        self.server = dev.Server()
        self.client = dev.Client(HOST=self.host)

        self.img_dict = {}

        self.init_server()

        self.create_frame_main()
        
    ## \brief Create main frame, composed by a Label object (where the video will be displayed) and a Message box.
    #  @param self The object pointer.
    def create_frame_main(self):

        self.frame_main = tk.Frame(self.root)
        self.frame_main.grid(row=0, column=0, sticky='')

        self.screen_frame = tk.Frame(self.frame_main, width=k.SUBJ_W, height=k.SUBJ_H, bg='black')
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

    ## \brief Initialize all the servers that will be used during the connection.
    #  @param self The object pointer.
    def init_server(self):

        self.server.start_stream_server()
        self.server.start_commands_server(routine_handler=self.execute_command)
        self.server.start_polar_server()

    ## \brief Intepret the instructions received during a ROUTINE command.
    #  @param cmd The command that is supposed to be executed.
    #  @param instruction Indicates the flavor of the command (i.e. color of the screen).
    def execute_command(self, cmd, instruction):

        if cmd == 'message':
            
            self.msg.set(instruction)

        elif cmd == 'clear':

            self.__clear = True
            self.is_playing_video = False

            self.screen.config(image='', bg=instruction)
            self.screen_frame.config(bg=instruction)

        elif cmd == 'play': 

            if not os.path.exists(instruction):
                return

            self.is_playing_video = True
            
            if self.videoCap:
                self.videoCap.release()

            self.videoCap = cv2.VideoCapture(instruction)
            self.videoFps = self.videoCap.get(cv2.CAP_PROP_FPS)
            video_thread = threading.Thread(target=self.show_video)
            video_thread.start()
            self.threads.append(video_thread)

        elif cmd == 'show':

            self.is_playing_video = False 
            self.__clear = False
            self.is_receiving_video = True

            if self.connected:
                return 

            self.client.start_stream_connection()
            stream_thread = threading.Thread(target=self.display_frames)
            stream_thread.start()
            self.threads.append(stream_thread)
            self.connected = True

        elif cmd == 'connect':
            self.client.set_host(instruction)

        elif cmd == 'stop':
            pass

            #if self.is_receiving_video:
            #    self.is_receiving_video = False
            #    self.client.stop_stream_client()

            #if self.is_playing_video:
            #    self.is_playing_video = False
            #    self.videoCap.release()

            #self.screen.config(image='', bg='black')
            #self.screen_frame.config(bg='black')
            #self.cleanup()

        elif cmd == 'image':
            print(cmd)
            print(instruction)

            filename = instruction
            if (filename in self.img_dict.keys()):
                img = self.img_dict[filename]
            else:
                img = cv2.imread(filename)
                self.img_dict[filename] = img
            if (img is None):
                print("Error opening file: " + filename)
            else:
                self.show_image_cv(img)
            #self.show_image_cv(self.img_dict[filename])


        elif cmd == 'path':
            print(cmd)
            print(instruction)

    ## \brief Convert image from opencv format to ImageTk
    #  @param self The object pointer.
    #  @param frame Image as read by opencv
    def convert_image_cv2tk(self, frame):
            # frame = cv2.resize(frame, (self.width, self.height))
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            return imgtk

    ## \brief Show an image on the App's screen.
    #  @param self The object pointer.
    #  @param frame Image as read by opencv
    def show_image_tk(self, imgtk):
            self.screen.configure(image=imgtk)
            self.screen.imgtk = imgtk

    ## \brief Show an image on the App's screen.
    #  @param self The object pointer.
    #  @param frame Image as read by opencv
    def show_image_cv(self, frame):
            imgtk = self.convert_image_cv2tk(frame)
            self.show_image_tk(imgtk)

    ## \brief Show a locally available video on the App's screen.
    #  @param self The object pointer.
    def show_video(self):

        while self.is_playing_video:

            start = time.time()
            ret, frame = self.videoCap.read()

            if not ret:
                break

            self.show_image_cv(frame)

            # calculate screen refresh rate
            delay = max(0, time.time() - start)
            delta = max(0 , 1/self.videoFps - delay)

            time.sleep(delta)

        self.screen.config(image='')
    ## \brief Show the video received on the App's screen.
    #  Show the video received from the other subject on the App's screen
    #
    #  @param self The object pointer.
    """
    the flag 'screen_cleared' is used to cover the race condition between the 'clear' command
    and the thread that is executing this function when the command is executed.
    The thread might be inside of 'if self.__clear == False': and change the screen back to the
    last frame captured after we already cleared it.
    """
    def display_frames(self):

        screen_cleared = False

        while self.is_receiving_video:

            img_data_size = struct.calcsize('>L')
            frame = self.client.recv_frame(img_data_size)

            if len(frame) == 0:
                self.is_receiving_video = False
                self.screen.config(image='')
                break                    

            if self.__clear == False and self.is_playing_video == False:

                self.show_image_cv(frame)
                #cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                #img = Image.fromarray(cv2image)
                #imgtk = ImageTk.PhotoImage(image=img)
                #self.screen.configure(image=imgtk)
                #self.screen.imgtk = imgtk
                screen_cleared = False

            else:

                if screen_cleared == False:
                    self.screen.config(image='')
                    screen_cleared = True

                time.sleep(0.010)

        self.screen.config(image='')

    ## \brief Stop all threads and servers in order to exit the program cleanly.
    #  @param self The object pointer.
    def cleanup(self):
        self.is_receiving_video = False
        self.is_playing_video = False
        
        for t in self.threads:
            t.join()

        self.server.stop_stream_server()
        self.server.stop_commands_server()
        self.server.stop_polar_server()

        self.client.stop_stream_client()


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

    app = WinSub(root, '')
    app.mainloop()
    app.cleanup()

