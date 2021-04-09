from __future__ import unicode_literals

import youtube_dl

from tkinter import *


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


class Application(Frame):

    string_eta = ""

    def my_hook(self, d):
        self.eta_label = Label(
            self, text="Download ETA : " + self.string_eta)
        self.eta_label.pack(side=LEFT)
        # while d['status'] != 'finished':

        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    def download_video(self):
        video_options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [self.my_hook],
        }

        if self.video_status.get() == 1 and self.audio_status.get() == 1:

            with youtube_dl.YoutubeDL(video_options) as ydl:
                ydl.download([self.address_contents.get()])

    def createWidgets(self):
        self.winfo_toplevel().title("ydownload")
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit

        self.QUIT.pack({"side": "left"})

        self.download = Button(self)
        self.download["text"] = "Download",
        self.download["command"] = self.download_video
        self.download.pack({"side": "right"})

        self.video_status = IntVar()
        self.audio_status = IntVar()

        self.video = Checkbutton(self)
        self.video["text"] = "Video"
        self.video["onvalue"] = 1
        self.video["offvalue"] = 0
        self.video["height"] = 5
        self.video["width"] = 20
        self.video["variable"] = self.video_status

        self.audio = Checkbutton(self)
        self.audio["text"] = "audio"
        self.audio["onvalue"] = 1
        self.audio["offvalue"] = 0
        self.audio["height"] = 1
        self.audio["width"] = 2
        self.audio["variable"] = self.audio_status

        self.video.pack(side="bottom", fill="x")
        self.audio.pack(side="bottom", fill="x")

        self.eta = StringVar(name='eta')

        self.address_entry = Entry(self)

        self.address_entry.pack(side="top", fill="x")

        # here is the application variable
        self.address_contents = StringVar()

        # set it to some value
        self.address_contents.set("")

        # tell the entry widget to watch this variable
        self.address_entry["textvariable"] = self.address_contents

        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.address_entry.bind('<Key-Return>',
                                self.download_video)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
