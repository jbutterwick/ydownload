from __future__ import unicode_literals

import youtube_dl

from tkinter import *


def progress_hook(status_object):
    if status_object['status'] == 'finished':
        print('Done downloading, now converting ...')


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


class Application(Frame):

    string_output_directory = "%USERPROFILE%\Videos\%(extractor_key)s\%(extractor)s-%(id)s-%(title)s.%(ext)s'"

    video_options = {
        'format': 'best',
        'outtmpl': string_output_directory,
        'logger': MyLogger(),
        'progress_hooks': [progress_hook],
    }

    audio_options = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': string_output_directory,
        'logger': MyLogger(),
        'progress_hooks': [progress_hook],
    }

    def download_video(self):

        self.download_status_label_text.set("Download In Progress")
        self.download_status_label.config(fg="black")
        self.download_status_label.config(bg="yellow")

        Frame.update(self)

        if self.video_status.get() == 1:

            with youtube_dl.YoutubeDL(self.video_options) as ydl:
                ydl.download([self.address_contents.get()])

            self.download_status_label.config(fg="white")
            self.download_status_label.config(bg="green")
            self.download_status_label_text.set("Download Complete")
            Frame.update(self)

        if self.video_status.get() != 1:

            with youtube_dl.YoutubeDL(self.audio_options) as ydl:
                ydl.download([self.address_contents.get()])

            self.download_status_label.config(fg="white")
            self.download_status_label.config(bg="green")
            self.download_status_label_text.set("Download Complete")
            Frame.update(self)

    def createWidgets(self):

        self.winfo_toplevel().title("ydownload")

        self.download_status_label_text = StringVar()
        self.download_status_label_text.set("No download in progress")

        self.download_status_label = Label(self, fg="white", bg="gray")
        self.download_status_label["textvariable"] = self.download_status_label_text
        self.download_status_label.pack(
            {"side": "bottom", "padx": (10, 1), "pady": (10, 1)})

        # download button - initiates download process
        self.download = Button(self)
        self.download["text"] = "Download",
        self.download["command"] = self.download_video
        self.download["width"] = 9
        self.download.pack({"side": "right", "padx": (10, 1), "pady": (1, 5)})

        self.video_status = IntVar()

        # video checkbutton for selecting video download
        self.video = Checkbutton(self)
        self.video["text"] = "Download Video (Leave unchecked to only download Audio)"
        self.video["onvalue"] = 1
        self.video["offvalue"] = 0
        self.video["width"] = 20
        self.video["variable"] = self.video_status

        self.video.pack({"side": "bottom", "fill": "x",
                         "padx": (10, 1), "pady": (1, 1)})

        # stores contents of the address entry
        self.address_contents = StringVar()
        self.address_contents.set("")

        # address entry label
        self.address_label_contents = StringVar()
        self.address_label_contents.set("Youtube Video URL")

        self.address_label = Label(self)
        self.address_label['textvariable'] = self.address_label_contents
        self.address_label["width"] = 20
        self.address_label.pack({"side": "left", "pady": (30, 10)})

        # address entry box itself
        self.address_entry = Entry(self)
        self.address_entry["textvariable"] = self.address_contents
        self.address_entry["width"] = 50
        self.address_entry.pack(
            {"side": "left", "padx": (1, 10), "pady": (30, 10)})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
root.geometry("500x150")
app = Application(master=root)
app.mainloop()
root.destroy()
