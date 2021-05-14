from tkinter import *
from tkinter.filedialog import askdirectory
import pygame
import glob,os
from mutagen.mp3 import MP3
import threading
from tkinter.messagebox import *
from tkinter import ttk
import time

class Player:
    def __init__(self, master):
        self.master = master
        pygame.init()
        pygame.mixer.init()

        #===Empty thread list=====#
        self.threads = []

        #=====show an icon for the player===#
        def get_icon():
            self.winicon = PhotoImage(file="best (2).png")
            master.iconphoto(False, self.winicon)

        #=====run the get_icon on a different thread from the gui=====#

        def icon():
            mythreads = threading.Thread(target=get_icon)
            self.threads.append(mythreads)
            mythreads.start()
        icon()

        #=======all Button symbols and variables======#
        PLAY = "►"
        PAUSE = "║║"
        RWD = "⏮"
        FWD = "⏭"
        STOP = "■"
        UNPAUSE = "||"
        mute = "🔇"
        unmute = u"\U0001F50A"
        vol_mute = 0.0
        vol_unmute = 1

        #==========music playlist listbox=========#
        self.scroll = Scrollbar(master)
        self.play_list = Listbox(master, font="Sansarif 12 bold", bd=5,
                            bg="white", width=37, height=19, selectbackground="black")
        self.scroll.place(x=850, y=80, height=380, width=15)
        self.play_list.place(x=505, y=77)
        self.scroll.config(command=self.play_list.yview)
        self.play_list.config(yscrollcommand=self.scroll.set)

        self.img = PhotoImage(file="best (2).png", width=500, height=460)
        self.lab = Label(master)
        self.lab.grid()
        self.lab["compound"] = LEFT
        self.lab["image"] = self.img

        #=====show the song playing==========#
        self.var = StringVar()
        self.var.set("..............................................................................")
        self.song_title = Label(master, font="Helvetica 12 bold", bg="black",
                        fg="white", width=48, textvariable=self.var)
        self.song_title.place(x=10, y=5)

       
        #==============================================================================================#
        #   THis part contains the menu, volume slider , music playlist label and the volume slider  #
        #===============================================================================================#

        self.menu = Menu(self.lab, font="helvetica, 3",)
        master.config(menu=self.menu)
        self.menu.add_command(label="Help", command=help)
        self.menu.add_command(label="Exit", command=exit)

        self.separator = ttk.Separator(self.lab, orient='horizontal')
        self.separator.place(relx=0, rely=0.85, relwidth=1, relheight=1)
        self.button_play = Button(master, text=PLAY, width=5, bd=5, bg="black",
                            fg="white", font="Helvetica, 15", command=play_thread)
        self.button_play.place(x=150, y=407)
        self.button_stop = Button(master, text=STOP, width=5, bd=5,
                            font="Helvetica, 15", bg="black", fg="white", command=stop)
        self.button_stop.place(x=225, y=407)
        self.button_prev = Button(master, text=FWD, width=5, bd=5,
                            font="Helvetica, 15", bg="black", fg="white", command=nextsong)
        self.button_prev.place(x=300, y=407)
        self.button_next = Button(master, text=RWD, width=5, bd=5, bg="black",
                            fg="white", font="Helvetica, 15", command=prev_song)
        self.button_next.place(x=10, y=407)
        self.button_pause = Button(master, text=PAUSE, width=4, bd=5,
                            font="Helvetica, 15", bg="black", fg="white", command=pause_unpause)
        self.button_pause.place(x=85, y=407)
        self.button_mute = Button(master, text=unmute, width=2, bd=5,
                            font="Helvetica, 15", bg="black", fg="white", command=muted)
        self.button_mute.place(x=375, y=407)

        self.label_playlist = Label(master, text=u"♫ Music Playlist ♫ ",
                            width=25, font="Helvetica, 15")
        self.label_playlist.place(x=540, y=10)

        self.button_load_music = Button(master, text="♫ Click Here To Load The Music ♫", width=43,
                                bd=5, font="Helvetica, 10", bg="black", fg="white", command=add_songs_playlist)
        self.button_load_music.place(x=505, y=45)

        self.volume_slider = ttk.Scale(self.lab, from_=0, to=1, orient=HORIZONTAL,
                        value=1, length=80, command=volume)
        self.volume_slider.place(x=415, y=415)

        self.progress = ttk.Progressbar(self.lab, orient=HORIZONTAL, value=0, length = 350, mode = 'determinate')
        self.progress.place(x=0, y=368)

        self.label_time = Label(master, text="00:00:00 / 00:00:00",
                            width=17, font="Helvetica, 10", bg="black", fg="white")
        self.label_time.place(x=355, y=369)

#=================================tk window==========================================#

def main():
    root = Tk()
    playerapp = Player(root)
    root.geometry("865x460+250+100")
    root.title("Mp3 Music Player")
    root.configure(bg="black")
    root.resizable(width=0, height=0)
    root.mainloop()

if __name__ == "__main__":
    main()