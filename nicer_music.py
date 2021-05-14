from tkinter import (
    Tk,HORIZONTAL,Label,Button,
    END,PhotoImage,Scrollbar,Listbox,
    LEFT,StringVar,Menu,Toplevel,
    ACTIVE,BOTH,TOP
    )
from tkinter.filedialog import askdirectory
import pygame
import os
from mutagen.mp3 import MP3
import threading
from tkinter.messagebox import  showerror,askquestion,showinfo
from tkinter import ttk
import time
import random

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

        # =====add a music list to the listbox======"
    
        def append_listbox():
            global song_list
            directory = askdirectory()
            try:
                os.chdir(directory)# it permits to change the current dir
                song_list = os.listdir()
                song_list.reverse()
                for item in song_list:# it returns the list of files song
                    pos = 0
                    self.play_list.insert(pos, item)
                    pos += 1
            except:
                showerror("File selected error", "Please choose a file correctly") 
        # =====run the append_listbox function on separate thread======"

        def add_songs_playlist():
            mythreads = threading.Thread(target=append_listbox)
            self.threads.append(mythreads)
            mythreads.start()

        #=====show music time=========#

        def get_time():
            current_time = pygame.mixer.music.get_pos() / 1000
            formated_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
            next_one = self.play_list.curselection()
            song = self.play_list.get(next_one)
            song_timer = MP3(song)
            song_length = int(song_timer.info.length)
            format_for_length = time.strftime("%H:%M:%S", time.gmtime(song_length))
            self.label_time.config(text=f"{ format_for_length} / {formated_time}")
            self.progress["maximum"] = song_length
            self.progress["value"] = int(current_time)
            master.after(100, get_time)

        #=====play the music==#

        def Play_music():
            try:
                track = self.play_list.get(ACTIVE)
                pygame.mixer.music.load(self.play_list.get(ACTIVE))
                self.var.set(track)
                pygame.mixer.music.play()
                get_time()                
            except:
                showerror("No Music", "Please load the music you want to play")

        # ===pause and unpause==

        def pause_unpause():
            if self.button_pause['text'] == PAUSE:
                pygame.mixer.music.pause()
                self.button_pause['text'] = UNPAUSE

            elif self.button_pause['text'] == UNPAUSE:
                pygame.mixer.music.unpause()
                self.button_pause['text'] = PAUSE

        # ==play the music on a diffent thread from the gui==

        def play_thread():
            mythreads = threading.Thread(target=Play_music)
            self.threads.append(mythreads)
            mythreads.start()

        # ===stop===

        def stop():
            pygame.mixer.music.stop()

        #====increase and decrease volume when slider is moved()==#

        def volume(x):
            pygame.mixer.music.set_volume(self.volume_slider.get())

        # ====mute and unmute the song while the song plays

        def muted():
            if self.button_mute['text'] == unmute:
                pygame.mixer.music.set_volume(vol_mute)
                self.volume_slider.set(vol_mute)
                self.button_mute['fg'] = "red"
                self.button_mute['text'] = mute
            elif self.button_mute['text'] == mute:
                pygame.mixer.music.set_volume(vol_unmute)
                self.volume_slider.set(vol_unmute)
                self.button_mute['fg'] = "white"
                self.button_mute['text'] = unmute

        #===move to the next song===#

        def nextsong():
            try:
                next_one = self.play_list.curselection()
                next_one = next_one[0]+1
                song = self.play_list.get(next_one)
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                self.play_list.select_clear(0, END)
                self.play_list.activate(next_one)
                self.play_list.selection_set(next_one, last=None)
                self.var.set(song)
            except:
                showerror("No Next Song", "Please press the previous button")

        #===move to the previous song===#


        def prev_song():
            try:
                next_one = self.play_list.curselection()
                next_one = next_one[0]-1
                song = self.play_list.get(next_one)
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                self.play_list.select_clear(0, END)
                self.play_list.activate(next_one)
                self.play_list.selection_set(next_one, last=None)
                self.var.set(song)
            except:
                showerror("No previous Song", "Please press the Next button")

        #=====exit the application=====#

        def exit():
            MsgBox = askquestion(
                'Exit Application', 'Are you sure you want to exit the music player.', icon='warning')
            if MsgBox == 'yes':
                master.destroy()
            else:
                showinfo(
                    'Return', 'Continue playing your awesome music')
            return

        #=====Help window=====#

        def help():
            top = Toplevel()
            top.title("Help")
            top.geometry("350x554+500+80")
            top.resizable(width=0, height=0)
            user_manual = [
                " MUSIC PLAYER USER MANUAL: \n",
                "1. play button =  ( ► )",
                "2. pause button = ║║ ",
                "3. unpause symbol = ||",
                "4. next button = ⏭ ",
                "5. previous button = ⏮",
                "6. mute button = '\U0001F50A' ",
                "7. unmute symbol = 🔇",
                "8. stop button = ■ ",
                "\n\n| Made by manucho | Copyright @ 2021 |\n"
            ]
            for i in user_manual:
                manual = Label(top, text=i, width=50, height=3,
                            font="Helvetica, 11", bg="black", fg="white")
                manual.pack(side=TOP, fill=BOTH)

        #==============================================================================================#
        #   THis part contains the menu, volume slider , music playlist label and the volume slider  #
        #===============================================================================================#

        self.menu = Menu(self.lab, font="helvetica, 3",)
        master.config(menu=self.menu)
        self.menu.add_command(label="HELP", command=help)
        self.menu.add_command(label="EXIT", command=exit)

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

        self.style = ttk.Style()

        self.style.configure("myStyle.Horizontal.TScale", background="#505050")

        self.volume_slider = ttk.Scale(self.lab, from_=0, to=1, orient=HORIZONTAL,
                        value=1, length=80, command=volume, style="myStyle.Horizontal.TScale")
        self.volume_slider.place(x=415, y=415)

        self.progress = ttk.Progressbar(self.lab, orient=HORIZONTAL, value=0, length = 350, mode = 'determinate')
        self.progress.place(x=0, y=368)

        self.label_time = Label(master, text="00:00:00 / 00:00:00",
                            width=17, font="Helvetica, 10", bg="black", fg="white")
        self.label_time.place(x=355, y=369)

#=================================Tk window function==========================================#

def main():
    root = Tk()
    playerapp = Player(root)
    root.geometry("865x470+250+100")
    root.title("Mp3 Music Player")
    root.configure(bg="black")
    root.resizable(width=0, height=0)
    root.mainloop()

if __name__ == "__main__":
    main()