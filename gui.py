#from python.HackAlliance.tts import gender_control
from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
import pathlib
from scan_demo import Scanner
from tts import Speaker
from ttkbootstrap import Style
from threading import *
import time
import cv2 as cv

style = Style(theme = 'cyborg')

root = style.master
root.state('zoomed')
root.title("Project Sullivan")
root.geometry("1200x800")
root.resizable(False,False)
root.option_add('*font', "Raleway 20")
root.grid_columnconfigure(0, weight=1)

speaker = Speaker()
logo_file = pathlib.Path.cwd()/'src'/'logo.png'
logo = ImageTk.PhotoImage(Image.open(logo_file).resize((450,120),Image.ANTIALIAS))
#root.iconbitmap(logo)


img_no=0
pg_no=0 

#def
def speak(text):
    speaker.say(text)
    speaker.run()
def search():
    x="search"

def prevpage():
    global img_no

    img_no-=1

    # scanned_Label['text'] = text_list[img_no]
    status_Label['text']=f"{img_no+1} of {pg_no+1}"
    mylist.delete('0','end')
    for line in text_list[img_no].split('\n'):
        mylist.insert(END,line)
    nextpage_Button['state']=NORMAL

    if img_no == 0:
        prevpage_Button['state']=DISABLED
    speak("Previous Page")

def prevsent():
    speak("Previous Sentence")

def nextsent():
    speak("Next Sentence")

def nextpage():
    global img_no

    img_no+=1

    # scanned_Label['text'] = text_list[img_no]
    status_Label['text']=f"{img_no+1} of {pg_no+1}"
    mylist.delete('0','end')
    for line in text_list[img_no].split('\n'):
        mylist.insert(END,line)
    prevpage_Button['state']=NORMAL

    if img_no >= len(text_list)-1:
        nextpage_Button['state']=DISABLED
    speak("Next Page")

def pause():
    if pause_Button['text']=='Pause':
        pause_Button['text']='Play'
    else:
        pause_Button['text']='Pause'

def scan():
    speaker.say("Please tell me the name of the document you are trying to scan.")
    speaker.run()
    time.sleep(3)
    threading(speak(f"Ok. Let's scan the document: covid"))
    
    scan = Scanner("sample")
    scan.open_camera(speaker)


def save():
    x="save"

def bookmark():
    if(len(text_list)==0):
        speak("Loading bookmark")
        speak("Which bookmark do you wish to retrieve?")
        speak("1. Covid, page 2")
        speak("2. test, page 5")
        cv.namedWindow('Key')
        while True:
            key = cv.waitKey(0)
            if (key):
                break
        cv.destroyAllWindows()
        speak("Opening bookmarked page")
        global pg_no
        del text_list[0:-1]
        while(True):
            file = pathlib.Path.cwd()/'text'/f'covid{pg_no+1}.txt'
            if(file.exists()):
                text_list.append(file.read_text())
                pg_no += 1
            else:
                pg_no -= 1
                break
        status_Label['text']=f"2 of {pg_no+1}"
        # scanned_Label['text'] = text_list[0]
        mylist.delete('0','END')
        for line in text_list[1].split('\n'):
            mylist.insert(END,line)
        prevpage_Button['state']=NORMAL
        # nextpage_Button['state']=NORMAL
        #prevsent_Button['state']=NORMAL
        # nextsent_Button['state']=NORMAL

        speaker.say("Document loaded. Please press r to read")
        speaker.run()

def say():
    speaker.say(text_list[img_no].replace("\n\n",". ").replace("\n"," "))
    speaker.run()
    
    
def check_voice():
    speaker.say("This is your voice and this is your speed.")
    speaker.run()

def open_file(text_list,mylist):
    speak("Please enter the number of the document to open")
    speak("1: covid")
    speak("2: test")
    cv.namedWindow('Key')
    while True:
        key = cv.waitKey(0)
        if (key):
            break
    cv.destroyAllWindows()
    speak("Loading document covid")
    global pg_no
    del text_list[0:-1]
    while(True):
        file = pathlib.Path.cwd()/'text'/f'covid{pg_no+1}.txt'
        if(file.exists()):
            text_list.append(file.read_text())
            pg_no += 1
        else:
            pg_no -= 1
            break
    status_Label['text']=f"{img_no+1} of {pg_no+1}"
    # scanned_Label['text'] = text_list[0]
    mylist.delete('0','END')
    for line in text_list[0].split('\n'):
        mylist.insert(END,line)
    #prevpage_Button['state']=NORMAL
    nextpage_Button['state']=NORMAL
    #prevsent_Button['state']=NORMAL
    # nextsent_Button['state']=NORMAL

    speaker.say("Document loaded. Please press r to read")
    speaker.run()

def gender():
    if gender_Button['text']=='Male':
        gender_Button['text']='Female'
        speaker.set_gender(False)
    else: 
        gender_Button['text']='Male'
        speaker.set_gender(True)

def speed_changed(val):
    speaker.engine.setProperty('rate', 75+(int(val)-1)*(300-75)/10)

def threading(fun):
    # Call work function
    t1=Thread(target=fun)
    t1.start()

def search(word):
    sentence_list = text_list[img_no].lower().replace("\n\n",".").replace("\n",'').split('.')
    for i in range(len(sentence_list)):
        if(word.lower() in sentence_list[i]):
            speak(sentence_list[i])
            speak("If you want to listen to next result, press N. If you want to listen further, press R. Press q to return to main menu")
            cv.namedWindow('Key')
            while True:
                key = cv.waitKey(0)
                if key == ord('n'):
                    break
                elif(key == ord('r')):
                    speak("".join(sentence_list[i+1:]))
                    break
                elif(key == ord('q')):
                    cv.destroyAllWindows()
                    speak("Returning to main menu.")
                    return
            
    cv.destroyAllWindows()
    speak("End of search. Returning to main menu.")
    return 

one_frame = Frame(root)
two_frame = Frame(root)
three_frame = Frame(root)

#first page - do it later
#open_Button = Button(root, text="Open document", command = open)


#project_Label = Label(root, text="Welcome to Project Sullivan")
project_Label = Label(one_frame, image=logo) #change size 

#search_Label = Label(root, text="Search:")
search_Label = Label(one_frame, text = "Search: ")
search_word = StringVar(value="Search word")
search_Entry = Entry(one_frame, borderwidth = 3, textvariable=search_word)
search_Button = Button(one_frame, text="Search",command=lambda : search(search_Entry.get()))

search_Frame = LabelFrame(one_frame, padx=50, pady=20)
first_Label = Label(search_Frame, text="", anchor=W)
firstresult_Label = Label(search_Frame, text="",anchor=W)
second_Label = Label(search_Frame, text="", anchor=W)
secondresult_Label = Label(search_Frame, text="",anchor=W)


scroll_bar = Scrollbar(two_frame)
mylist = Listbox(two_frame, yscrollcommand = scroll_bar.set )
#PNG Image Display
text_list = list()

current_pg = None
scanned_Label = Label(two_frame, text=current_pg)
pg_frame = Frame(two_frame)

pg_frame.pack(side=BOTTOM)
Label(two_frame, text = "TEXT AREA", bg='grey').pack(side=TOP,fill="x")
scanned_Label.pack(side=TOP)
mylist.pack(side = TOP, fill = BOTH, expand=True)
scroll_bar.pack(side = TOP,fill = BOTH)
scroll_bar.config( command = mylist.yview )

PAGE_WIDTH = 15
prevpage_Button = Button(pg_frame,width=PAGE_WIDTH,text="Previous Page", command=prevpage, state=DISABLED)
prevsent_Button = Button(pg_frame,width=PAGE_WIDTH, text="Previous Sentence", command=prevsent, state=DISABLED)
nextsent_Button = Button(pg_frame,width=PAGE_WIDTH, text="Next Sentence", command=nextsent, state=DISABLED)
nextpage_Button = Button(pg_frame,width=PAGE_WIDTH, text="Next Page", command=lambda: nextpage(), state=DISABLED)
status_Label = Label(pg_frame,width=PAGE_WIDTH, text= f"{img_no} of {pg_no}", bd=1, relief=SUNKEN) # text= currentstatus +" of " + str(len(image_list))

BTN_H = 3
BTN_W = 15
pause_Button = Button(three_frame,text="Pause", height =BTN_H, command=pause)
scan_Button = Button(three_frame,text="Scan", height=BTN_H,command=scan)
save_Button = Button (three_frame,text="Read",height=BTN_H,command=lambda x: threading(say))
bookmark_Button = Button (three_frame, text="Bookmark",height=BTN_H, command=bookmark)
say_Button = Button(three_frame, text="Check Voice",height=BTN_H, command=lambda x: threading(check_voice))

open_Button = Button (three_frame, text="Open File", height=BTN_H,  command=lambda x : open_file(text_list,mylist))
gender_Button = Button(three_frame,text="Male", height =BTN_H, command=gender)







speed_currentvalue = DoubleVar()
speed_Label = Label(three_frame,text="Speed")
speed_Scale = Scale(three_frame,from_=1,to=10, orient=HORIZONTAL, command=speed_changed)
#genderstatus_Label = Label (root, text = gender_Scale.get())
#genderstatus_Label.grid(row=5,column=8)


#grid inside search frame
first_Label.pack(side=BOTTOM)
firstresult_Label.pack(side=BOTTOM)
second_Label.pack(side=BOTTOM)
secondresult_Label.pack(side=BOTTOM)

#grid
verticalgrid=20

project_Label.pack(side=TOP, fill="x")
search_Entry.pack(side=TOP, anchor=W, fill="x")
search_Button.pack(side=TOP, anchor=E, fill="x")
search_Frame.pack(side=BOTTOM, anchor =S,fill="both")



prevpage_Button.pack(side=LEFT)
prevsent_Button.pack(side=LEFT)
status_Label.pack(side=LEFT)
nextpage_Button.pack(side=RIGHT)
nextsent_Button.pack(side=RIGHT)


pause_Button.pack(side=TOP, fill="x")
scan_Button.pack(side=TOP, fill="x")
save_Button.pack(side=TOP, fill="x")
bookmark_Button.pack(side=TOP, fill="x")
say_Button.pack(side=TOP, fill="x")

open_Button.pack(side=TOP, fill="x")
gender_Button.pack(side=TOP, fill="x")
#gender_Label.grid(row=3,column=8)
#gender_Scale.grid(row=3,column=9)
speed_Label.pack(side=TOP, fill="x")
speed_Scale.pack(side=TOP, fill="x")
speed_Scale.set(6)


one_frame.pack(side=LEFT, anchor=NW, fill="both", expand=True)
two_frame.pack(side=LEFT, anchor=S, fill="both", expand=True)
three_frame.pack(side=RIGHT, anchor=NE, fill="both", expand=True)



def speed_scale_up():
    speed_Scale.set(speed_Scale.get()+1)
    speak(f"Speed set to {speed_Scale.get()}")
def speed_scale_down():
    speed_Scale.set(speed_Scale.get()-1)
    speak(f"Speed set to {speed_Scale.get()}")

def search_demo():
    threading(speak("Please tell me what you want to search."))
    time.sleep(2)
    search_Entry['text'] = "pandemic"
    search_Entry.delete(0,END)
    search_Entry.insert(0,"pandemic") 
    search_word.set("")
    root.update()
    
    threading(speak("Searching pandemic. . . "))
    search("pandemic")

root.bind('<Up>',lambda x: speed_scale_up())
root.bind('<Down>',lambda x: speed_scale_down())    
root.bind('o',lambda x: open_file(text_list,mylist))
root.bind('<space>',lambda x: pause())
root.bind('s',lambda x: scan())
root.bind('v',lambda x: threading(check_voice))
root.bind('<Right>',lambda x: nextpage())
root.bind('<Left>',lambda x: prevpage())
root.bind('.',lambda x: nextsent())
root.bind(',',lambda x: prevsent())
root.bind('r',lambda x: threading(say))
root.bind('g',lambda x: gender())
root.bind('q', lambda x: search_demo())
root.bind('b',lambda x: bookmark())
root.mainloop()