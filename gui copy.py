#from python.HackAlliance.tts import gender_control
from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
import pathlib
from scan import Scanner
from tts import Speaker
from ttkbootstrap import Style

style = Style(theme = 'darkly')

root = style.master
root.state('zoomed')
root.title("Project Sullivan")
root.geometry("1200x800")
root.resizable(False,False)
root.option_add('*font', "Raleway 20")

speaker = Speaker()
logo_file = pathlib.Path.cwd()/'src'/'logo.png'
logo = ImageTk.PhotoImage(Image.open(logo_file).resize((300,90),Image.ANTIALIAS))
#root.iconbitmap(logo)


img_no=0
pg_no=0 

#def
def search():
    x="search"

def prevpage():
    global img_no

    img_no-=1

    scanned_Label['text'] = text_list[img_no]
    status_Label['text']=f"{img_no+1} of {pg_no+1}"

    nextpage_Button['state']=NORMAL

    if img_no == 0:
        prevpage_Button['state']=DISABLED

def prevsent():
    x="prevsent"

def nextsent():
    x="nextsent"

def nextpage(text_list):
    global img_no

    img_no+=1

    scanned_Label['text'] = text_list[img_no]
    status_Label['text']=f"{img_no+1} of {pg_no+1}"

    prevpage_Button['state']=NORMAL

    if img_no >= len(text_list)-1:
        nextpage_Button['state']=DISABLED

def pause():
    if pause_Button['text']=='pause':
        pause_Button['text']='play'
    else:
        pause_Button['text']='pause'

def scan():
    scan = Scanner("sample")
    scan.open_camera(speaker)


def save():
    x="save"

def bookmark():
    x="bookmark"

def goto():
    x="goto"

def open_file(text_list):
    global pg_no
    del text_list[0:-1]
    while(True):
        file = pathlib.Path.cwd()/'text'/f'test{pg_no+1}.txt'
        if(file.exists()):
            text_list.append(file.read_text())
            pg_no += 1
        else:
            pg_no -= 1
            break
    status_Label['text']=f"{img_no+1} of {pg_no+1}"
    scanned_Label['text'] = text_list[0]
    #prevpage_Button['state']=NORMAL
    nextpage_Button['state']=NORMAL
    #prevsent_Button['state']=NORMAL
    # nextsent_Button['state']=NORMAL

def gender():
    if gender_Button['text']=='Male':
        gender_Button['text']='Female'
        speaker.set_gender(False)
    else: 
        gender_Button['text']='Male'
        speaker.set_gender(True)




#first page - do it later
#open_Button = Button(root, text="Open document", command = open)


#project_Label = Label(root, text="Welcome to Project Sullivan")
project_Label = Label(root, image=logo) #change size 

#search_Label = Label(root, text="Search:")
search_Label = Label(root, text = "Search: ")
search_Entry = Entry(root, borderwidth = 3)
search_Button = Button(root, text="click this",command=search)

search_Frame = LabelFrame(root, padx=50, pady=20)
first_Label = Label(search_Frame, text="Pg.1", anchor=W)
firstresult_Label = Label(search_Frame, text="This is the first result.",anchor=W)
second_Label = Label(search_Frame, text="Pg.2", anchor=W)
secondresult_Label = Label(search_Frame, text="This is the second result.",anchor=W)


#PNG Image Display
text_list = list()

current_pg = None
scanned_Label = Label(root, text=current_pg)

prevpage_Button = Button(root,text="Previous Page", command=prevpage, state=DISABLED)

    # prevpage_Button['state']=NORMAL
prevsent_Button = Button(root, text="Previous Sentence", command=prevsent, state=DISABLED)
nextsent_Button = Button(root, text="Next Sentence", command=nextsent, state=DISABLED)
nextpage_Button = Button(root, text="Next Page", command=lambda: nextpage(text_list), state=DISABLED)
status_Label = Label(root, text= f"{img_no} of {pg_no}", bd=1, relief=SUNKEN) # text= currentstatus +" of " + str(len(image_list))

pause_Button = Button(root,text="pause", height =5, width=21,command=pause, fg='red')
scan_Button = Button(root,text="Scan", height=5,width=10,command=scan)
save_Button = Button (root,text="Save",height=5,width=10,command=save)
bookmark_Button = Button (root, text="Bookmark",height=5,width=10, command=bookmark)
goto_Button = Button(root, text="Go to \nBookmark",height=5,width=10, command=goto)

open_Button = Button (root, text="Open File", height=5, width=10, command=lambda : open_file(text_list))
gender_Button = Button(root,text="Male", height =5, width=10,command=gender, fg='red')





def speed_changed(val):
    speaker.engine.setProperty('rate', 75+(int(val)-1)*(300-75)/10)

speed_currentvalue = DoubleVar()
speed_Label = Label(root,text="Speed")
speed_Scale = Scale(root,from_=1,to=10, orient=HORIZONTAL, command=speed_changed)
#genderstatus_Label = Label (root, text = gender_Scale.get())
#genderstatus_Label.grid(row=5,column=8)


#grid inside search frame
first_Label.grid(row=0, column=0, sticky='w')
firstresult_Label.grid(row=0, column=1, sticky='w')
second_Label.grid(row=1, column=0, sticky='e')
secondresult_Label.grid(row=1, column=1, sticky='w')

#grid
verticalgrid=20

project_Label.grid(row=0,column=0, columnspan=3)
search_Label.grid(row=1,column=0)
search_Entry.grid(row=1,column=1)
search_Button.grid(row=1,column=2)
search_Frame.grid(row=2,column=0,rowspan=1,columnspan=3)

scanned_Label.grid(row=0,column=3,rowspan=verticalgrid-1,columnspan=5)

prevpage_Button.grid(row=verticalgrid,column=3)
prevsent_Button.grid(row=verticalgrid,column=4)
status_Label.grid(row=verticalgrid,column=5)
nextsent_Button.grid(row=verticalgrid,column=6)
nextpage_Button.grid(row=verticalgrid,column=7)

pause_Button.grid(row=0,column=8,columnspan=2)
scan_Button.grid(row=1,column=8)
save_Button.grid(row=1,column=9)
bookmark_Button.grid(row=2,column=8)
goto_Button.grid(row=2,column=9)

open_Button.grid(row=3,column=8)
gender_Button.grid(row=3,column=9)
#gender_Label.grid(row=3,column=8)
#gender_Scale.grid(row=3,column=9)
speed_Label.grid(row=4,column=8)
speed_Scale.grid(row=4,column=9)
speed_Scale.set(5)

root.mainloop()