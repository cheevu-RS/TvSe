from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import vlc
import os
import time
import json
class App:
    instance = vlc.Instance(['--no-video-on-top','--no-xlib'])
    player = instance.media_player_new()
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack()
        f = os.path.isfile("isPresent.json")
        if not f:
            self.w1 = Label(self.frame,text="You are not binging\n yet,add a season",fg="green",bg="black",width="25",height="5")
            self.w1.pack()
            self.button = Button(self.frame, text="QUIT", fg="red", command=lambda:self.on_close(master))
            self.button.pack(side=LEFT)
            self.button1 = Button(self.frame,text="browse",command=lambda:self.browse(master))
            self.button1.pack(side=LEFT)
        else:
            master.bind("<space>",lambda event, arg=master: self.space_bar(event, arg))
            with open("PreSeas.json", "r") as read_file:
                w = json.load(read_file)
            self.w = Label(self.frame,text="Binge away to glory\n by pressing the spacebar\n/clicking the play button \n %s"%w,fg="green",bg="black",width="25",height="5")
            self.w.pack()
            self.button = Button(self.frame, text="QUIT", fg="red", command=lambda:self.on_close(master))
            self.button.pack(side=LEFT)
            self.button1 = Button(self.frame,text="browse",command=lambda:self.browse(master))
            self.button1.pack(side=LEFT)
            self.playid = Image.open("play.png")
            self.playif = self.playid.resize((25,25),Image.ANTIALIAS)
            self.playi = ImageTk.PhotoImage(self.playif)
            self.hi_there = Button(self.frame,image=self.playi,command=lambda:self.play_vid(master))
            self.hi_there.pack(side=LEFT)

    def browse(self,master):
        dir_loc = filedialog.askdirectory()
        if hasattr(self, 'w'):
            self.w['text'] = "Binge away to glory\n by pressing the spacebar\n/clicking the play button \n %s"%dir_loc
        if hasattr(self, 'w1'):
            self.w1['text'] = "Binge away to glory\n by pressing the spacebar\n/clicking the play button \n %s"%dir_loc
        self.playid = Image.open("play.png")
        self.playif = self.playid.resize((25,25),Image.ANTIALIAS)
        self.playi = ImageTk.PhotoImage(self.playif)
        self.hi_there = Button(self.frame,image=self.playi,command=lambda:self.play_vid(master))
        self.hi_there.pack(side=LEFT)
        #print (dir_loc)
        with open("isPresent.json", "w+") as write_file:
            json.dump(1,write_file)
        with open("PreSeas.json", "w+") as write_file:
            json.dump(dir_loc,write_file)
        with open("time.json","w+") as write_file:
            json.dump(0,write_file)
        master.bind("<space>",lambda event, arg=master: self.space_bar(event, arg))
    def list_ini(self):
        with open("PreSeas.json", "r") as read_file:
            dir = json.load(read_file)
        self.list = []
        for file in os.listdir(dir):
            if file.endswith(".mkv"):
                self.list.append(os.path.join(dir,file))
        self.list.sort()

    def play_vid(self,master):
        self.list_ini()
        if os.path.isfile('index.json'):
            with open("index.json", "r") as read_file:
                data = json.load(read_file)
            i = data
        else:
            with open("index.json", "w+") as write_file:
                data = json.dump(0,write_file)
            i = 0
        #print (i)
        if os.path.isfile('time.json'):
            with open("time.json","r") as read_file:
                t = json.load(read_file)
        else:
            with open("time.json","w+") as write_file:
                json.dump(0,write_file)
                t = 0
        #print (t)

        #lab = Label(self.vid,"dnl")
        self.media = self.instance.media_new(self.list[i])
        self.player.set_media(self.media)
        #master.wm_attributes("-fullscreen", True)
        self.frame.pack_forget()
        self.vid = Frame(master,width=master.winfo_screenwidth(), height=master.winfo_screenheight())
        self.vid.pack()
        self.player.set_xwindow(self.vid.winfo_id())
        self.player.play()
        self.player.set_time(t-10000)
#list_player.play_item_at_index(3);print("yo")
    #for file in [f for f in os.listdir('/mydir') if f.endswith('.txt')]:

    def play_pause(self):
        if self.player.is_playing():
            self.player.pause()
        else:
            self.player.play()

    def space_bar(self,event,master):
        d = self.player.get_state()
        if str(d) == "State.NothingSpecial":
            self.play_vid(master)
        else:
            self.play_pause()
    def play_next(self,event,master):
        with open("index.json", "r") as read_file:
            data = json.load(read_file)
        data +=1
        with open("index.json", "w+") as write_file:
            json.dump(data,write_file)
        #self.frame.destroy()
        self.play_vid(master)
    def play_before(self,event,master):
        with open("index.json", "r") as read_file:
            data = json.load(read_file)
        data -=1
        with open("index.json", "w+") as write_file:
            json.dump(data,write_file)
        #self.frame.destroy()
        self.play_vid(master)
    def on_close(self,master):
        t = self.player.get_time()
        #print (t)
        with open("time.json","w+") as write_file:
            json.dump(t,write_file)
        master.quit()
root = Tk()
app = App(root)
root.bind("<Right>",lambda event, arg=root: app.play_next(event, arg))
root.bind("<Left>",lambda event, arg=root: app.play_before(event, arg))
root.bind("<Alt-F4>",lambda : app.on_close(root))
root.protocol("WM_DELETE_WINDOW", lambda : app.on_close(root))
root.mainloop()

#todo
#pause/play11
#resume11
#subs
#random
#styling
#mouse test in another linux lap
