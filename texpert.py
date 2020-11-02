#!/usr/bin/python
# Texpert Text Editor 
# Written by David Lawson
# using Python/Tkinter (2.7)

import os
import sys
import time
import datetime

try:
    import Tkinter as tk
    import ScrolledText as tkst
    import tkFileDialog
except:
    import tkinter as tk
    import tkinter.scrolledtext as tkst
    import tkinter.filedialog as tkFileDialog


root = tk.Tk()
root.title("Texpert")
root.geometry("700x480")
root.option_add("*Font", "TkDefaultFont 9")

# Main Frame
mainframe = tk.Frame(root, bd=0, relief='flat')
mainframe.pack(fill='both', expand=True, padx=0, pady=0)

# Text Area
texpert = tkst.ScrolledText(mainframe, undo=True, font=('Arial 11'))
texpert.pack(side='bottom', fill='both', expand=True)
texpert.config(padx=2, pady=0, wrap="word")
texpert.focus_set()

# StatusBar
statusbar = tk.Frame(root, bd=1, relief='sunken')
statusbar.pack(side='bottom', fill='x')
mode = tk.Label(statusbar, text=" Mode: Light")
mode.pack(side='left')
line_lbl = tk.Label(statusbar, text="Line 1, Col 1")
line_lbl.pack(side='right', padx=10)


# Menu Functions
# file menu
def new_com(event=None): 
    root.title("New Document ") 
    file = None
    texpert.delete('1.0', 'end-1c') 
    
def open_com(event=None):
    file = tkFileDialog.askopenfile(parent=root, mode='rb', title='Select File')
    if file is not None:
  	contents = file.read()
	name = root.title(file.name) #adds path/filename to title
        texpert.delete('1.0', 'end-1c')
	texpert.insert('1.0', contents)
	file.close()

def save_com(event=None):
    print ("Silent Save")

def saveas_com(event=None):
    file = tkFileDialog.asksaveasfile(mode='w')
    if file is not None:
	data = texpert.get('1.0', 'end-1c')
	file.write(data)
 	file.close()

#print/print preview not done
def print_com():
    print ("Printer not found")

def preview_com():
    root.geometry("740x800+440+175") #experimental
    root.option_add("*Font", "TkDefaultFont 9")
    texpert.config(padx=10, pady=4, wrap="word")
    texpert.focus_set()
    statusbar.pack_forget()
    
def close_com(event=None):
    root.title('Untitled') 
    file = None
    texpert.delete('1.0', 'end-1c') 
    
def exit_com():
    win = tk.Toplevel()
    win.title("Exit")                                     
    tk.Label(win, text="\nUnsaved work will be lost.\n\nAre you sure you want to exit?\n").pack()   
    ex = tk.Button(win, text="Exit", width=4, command=root.destroy)
    ex.pack(side='left', padx=24, pady=4)
    can = tk.Button(win, text="Cancel", width=4, command=win.destroy)
    can.pack(side='right', padx=24, pady=4)
    win.transient(root)
    win.geometry('224x120')
    win.wait_window()


# edit menu
def undo_com():
    texpert.edit_undo()

def redo_com():
    texpert.edit_redo()

def cut_com(): 
    texpert.event_generate("<<Cut>>")

def copy_com(): 
    texpert.event_generate("<<Copy>>") 

def paste_com(): 
    texpert.event_generate("<<Paste>>")  

def select_all(event=None):
    texpert.tag_add('sel', '1.0', 'end-1c')
    texpert.mark_set('insert', '1.0')
    texpert.see('insert')
    return 'break'

# view menu
def tool_bar():
    if is_toolbar.get():
        toolbar.pack_forget()
    else:
	toolbar.pack(side='top', anchor='n', fill='x')

def status_bar():
    if is_statusbar.get():
        statusbar.pack_forget()
    else:
	statusbar.pack(side='bottom', fill='x')

# modes for: [view > mode]
# also statusbar text
def dark_mode():
    mode["text"] = " Mode: Dark"
    texpert.config(background="#181818", fg="#F5F5F5", insertbackground="#F5F5F5")

def light_mode():
    mode["text"] = " Mode: Light"
    texpert.config(background="#F5F5F5", fg="#181818", insertbackground="#181818")

def legal_mode():
    mode["text"] = " Mode: Legal"
    texpert.config(background="#FFFFCC", fg="#181818", insertbackground="#181818")

def night_mode():
    mode["text"] = " Mode: Night"
    texpert.config(background="#181818", fg="#00FF33", insertbackground="#00FF33")


def transparent():
    if is_transparent.get():
	root.wm_attributes('-alpha',0.9)
    else:
	root.wm_attributes('-alpha',1.0)

def tray_com():
    root.iconify()

def vertical_view():
    root.attributes('-zoomed', False)
    root.geometry("540x600+440+175")
    root.option_add("*Font", "TkDefaultFont 9")
    texpert = tkst.ScrolledText(root, undo=True, font=('Arial 11'))
    texpert.config(padx=2, pady=2, wrap="word")
    texpert.focus_set()

def default_view():
    root.attributes('-zoomed', False)
    root.geometry("700x480+440+175") #size+position
    root.option_add("*Font", "TkDefaultFont 9")
    texpert = tkst.ScrolledText(root, undo=True, font=('Arial 11'))
    texpert.config(padx=2, pady=2, wrap="word")
    texpert.focus_set()
    statusbar.pack(side='bottom', fill='x')

def full_screen():
    root.attributes('-zoomed', True)
    root.option_add("*Font", "TkDefaultFont 9")
    texpert = tkst.ScrolledText(root, undo=True, font=('Arial 11'))
    texpert.config(padx=2, pady=2, wrap="word")
    texpert.focus_set()
    

# tools menu
def time_com():
    ctime = time.strftime('%I:%M %p')
    texpert.insert('insert', ctime, "a", ' ')

def date_com():
    full_date = time.localtime()
    day = str(full_date.tm_mday)
    month = str(full_date.tm_mon)
    year = str(full_date.tm_year)
    date = ""+month+'/'+day+'/'+year
    texpert.insert('insert', date, "a", ' ')

def note_area():
    if is_notearea.get():
        note.pack(side='right', anchor='e', fill='y')
        btn_frame.pack(side='right', anchor='e', fill='y')
    else:
        note.pack_forget()
        btn_frame.pack_forget()

def line_numb():
    if is_linenumb.get():
        outer_frame.pack(side='left', anchor='w', fill='y')
    else:
        outer_frame.pack_forget()


# help menu
def about_com(event=None):
    win = tk.Toplevel()
    win.title("About")                                     
    tk.Label(win, text="\n\n\nTexpert\n\nA small text editor designed for Linux\n\nMade in Python with Tkinter\n\n\n").pack()   
    
    cre = tk.Button(win, text="Credits", width=4, command=credits_com)
    cre.pack(side='left', padx=8, pady=4)
    ver = tk.Label(win, text="v 1.0", width=4, bd=0, state='disabled')
    ver.pack(side='left', padx=8, pady=4, expand='yes')
    clo = tk.Button(win, text="Close", width=4, command=win.destroy)
    clo.pack(side='right', padx=8, pady=4)
     
    win.transient(root)
    win.geometry('300x200')
    win.wait_window()

def credits_com(): 
    win = tk.Toplevel()
    win.wm_attributes("-topmost", 0)
    win.title("Credits")                                     
    tk.Label(win, foreground="#404040", text="\n\n\nCreated by David Lawson\n\n\nme = Person()\nwhile (me.awake()):\nme.code()\n\n").pack()   
    
    lic = tk.Button(win, text="License", width=4, command=license_info)
    lic.pack(side='left', padx=8, pady=4)
    cls = tk.Button(win, text="Close", width=4, command=win.destroy)
    cls.pack(side='right', padx=8, pady=4) 
    
    win.transient(root)
    win.geometry('300x200')
    win.wait_window()

def license_info():
    win = tk.Toplevel()
    win.wm_attributes("-topmost", 1)
    win.title("License")                                     
    tk.Label(win, justify='left', text="""\n\nMIT License

Copyright (c) 2019 David Lawson

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, 
publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF 
ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT 
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.\n\n""").pack()   
    
    tk.Button(win, text='Close', command=win.destroy).pack()   
    win.transient(root)
    win.geometry('480x450')
    win.wait_window()


def trouble_com(event=None):
    win = tk.Toplevel()
    win.title("Troubleshooting")                                     
    tk.Label(win, justify='left', text="""\n
This program was designed for Linux and
may not work on other operating systems.\n
Texpert text editor is a work in progress
and may or may not ever be completed.\n\n\n
Known Issues:\n 
Line/Col numbers are not fully functional.
Problem remains: unfixed.\n
Save/Save as both work as 'Save as'\n
Print preview is not entirely accurate.\n
Also, (pay attention because this is important)
anything typed in note area will not be saved
as it was not designed/programmed to do so.
\n\nAnyway..\n""").pack()   
    
    tk.Button(win, text='Close', command=win.destroy).pack()   
    win.transient(root)
    win.geometry('360x424')
    win.wait_window()


#context menu (right-click)
def r_click(event):
    editmenu.tk_popup(event.x_root, event.y_root)
texpert.bind("<Button-3>", r_click)

#line count (statusbar)
def linecount(event):
    (line, char) = map(int, event.widget.index("end-1c").split("."))
    line_lbl['text'] = 'Line {line}, Col {col}'.format(line=line, col=char+1)
texpert.bind("<KeyRelease>", linecount)


# Main Menu 
menu = tk.Menu(root, bd=1, relief='flat')
root.config(menu=menu, bd=2)

#file menu
filemenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File ", menu=filemenu)
filemenu.add_command(label="New", command=new_com, accelerator="Ctrl+N") 
filemenu.add_command(label="Open", command=open_com, accelerator="Ctrl+O")
filemenu.add_separator()
filemenu.add_command(label="Save", command=saveas_com, accelerator="Ctrl+S")
filemenu.add_command(label="Save As", command=saveas_com)
filemenu.add_separator()
filemenu.add_command(label="Print", command=print_com, state="disabled")
filemenu.add_command(label="Print Preview", command=preview_com)
filemenu.add_separator()
filemenu.add_command(label="Close", command=close_com, accelerator="Ctrl+W")
filemenu.add_command(label="Exit", command=exit_com, underline=1, accelerator="Alt+F4")


#edit menu
editmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit ", menu=editmenu)
editmenu.add_command(label="Undo", command=undo_com, accelerator="Ctrl+Z")
editmenu.add_command(label="Redo", command=redo_com, accelerator="Shift+Ctrl+Z")
editmenu.add_separator()
editmenu.add_command(label="Cut", command=cut_com, accelerator="Ctrl+X")
editmenu.add_command(label="Copy", command=copy_com, accelerator="Ctrl+C")  
editmenu.add_command(label="Paste", command=paste_com, accelerator="Ctrl+V") 
editmenu.add_separator()
editmenu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A") 


#view menu
viewmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="View ", menu=viewmenu)

is_toolbar = tk.BooleanVar()
is_toolbar.trace('w', lambda *args: tool_bar())
viewmenu.add_checkbutton(label="Toolbar", variable=is_toolbar, onvalue=0, offvalue=1)

is_statusbar = tk.BooleanVar()
is_statusbar.trace('w', lambda *args: status_bar())
viewmenu.add_checkbutton(label="Statusbar", variable=is_statusbar, onvalue=0, offvalue=1)
viewmenu.add_separator()

#sub-menu for: [view > mode]
submenu = tk.Menu(menu, tearoff=0)
viewmenu.add_cascade(label="Mode ", menu=submenu)
submenu.add_command(label=" Dark ", command=dark_mode, activebackground="#181818", activeforeground="#F5F5F5")
submenu.add_command(label=" Light ", command=light_mode, activebackground="#F5F5F5", activeforeground="#181818")
submenu.add_command(label=" Legal ", command=legal_mode, activebackground="#FFFFCC", activeforeground="#181818")
submenu.add_command(label=" Night ", command=night_mode, activebackground="#181818", activeforeground="#00FF33")

is_transparent = tk.BooleanVar()
is_transparent.trace('w', lambda *args: transparent())
viewmenu.add_checkbutton(label="Transparency", variable=is_transparent, onvalue=1, offvalue=0)

viewmenu.add_separator()
viewmenu.add_command(label="Hide in Tray", command=tray_com)
viewmenu.add_separator()
viewmenu.add_command(label="Vertical", command=vertical_view)
viewmenu.add_command(label="Default", command=default_view)
viewmenu.add_command(label="Fullscreen", command=full_screen)


#tool menu
toolmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Tools ", menu=toolmenu)
toolmenu.add_command(label="Insert Time", command=time_com)
toolmenu.add_command(label="Insert Date", command=date_com)
is_notearea = tk.BooleanVar()
is_notearea.trace('w', lambda *args: note_area())
toolmenu.add_checkbutton(label="Note Area", variable=is_notearea)


#help menu
helpmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Help ", menu=helpmenu)
helpmenu.add_command(label="About", command=about_com)
helpmenu.add_command(label="Troubleshooting", command=trouble_com)


# ToolBar
toolbar = tk.Frame(mainframe, bd=2, relief='groove')
toolbar.pack(side='top', anchor='n', fill='x')
b1 = tk.Button(toolbar, text="Open", width=4, command=open_com)
b1.pack(side='left', padx=4, pady=2)
b2 = tk.Button(toolbar, text="Save", width=4, command=saveas_com)
b2.pack(side='right', padx=4, pady=2)
b4 = tk.Button(toolbar, text="Notes", width=4, 
               command=lambda: is_notearea.set(not is_notearea.get()))
b4.pack(side='right', padx=4, pady=2)

# ToolBar 'Mode' button
var = tk.StringVar(toolbar)
var.set("Mode")
w = tk.OptionMenu(toolbar, variable = var, value='')
w.config(indicatoron=0, bd=1, width=6, padx=4, pady=5)
w.pack(side='left', padx=4, pady=2)
first = tk.BooleanVar()
second = tk.BooleanVar()
third = tk.BooleanVar()
forth = tk.BooleanVar()
fifth = tk.BooleanVar()
sixth = tk.BooleanVar()
w['menu'].delete('0', 'end')
w['menu'].add_checkbutton(label="Dark  ", onvalue=1, offvalue=0, 
                         activebackground="#181818", activeforeground="#F5F5F5", 
                         variable=first, command=dark_mode, indicatoron=0)

w['menu'].add_checkbutton(label="Light  ", onvalue=1, offvalue=0,
                         activebackground="#F5F5F5", activeforeground="#181818", 
                         variable=second, command=light_mode, indicatoron=0)

w['menu'].add_checkbutton(label="Legal  ", onvalue=1, offvalue=0,
                         activebackground="#FFFFCC", activeforeground="#181818", 
                         variable=third, command=legal_mode, indicatoron=0)

w['menu'].add_checkbutton(label="Night  ", onvalue=1, offvalue=0,
                         activebackground="#181818", activeforeground="#00FF33", 
                         variable=forth, command=night_mode, indicatoron=0)


# Init Note Area
btn_frame = tk.Frame(texpert, bd=0, relief='sunken')
note = tk.LabelFrame(btn_frame, bd=0, relief='flat')
tx = tk.Text(note, width=18)
tx.insert('1.0', "Notes are not saved..")
tx.config(padx=2, pady=2, wrap="word")
tx.pack(side='top', fill='both', expand=True)
clear = tk.Button(note, text="Clear", width=4, command=lambda: tx.delete('1.0', 'end-1c'))
clear.pack(side='left', padx=2, pady=2)
close = tk.Button(note, text="Close", width=4, command=lambda: is_notearea.set(not is_notearea.get()))
close.pack(side='right', padx=2, pady=2)

texpert.bind("<Control-a>", select_all)
root.bind_all('<Control-n>', new_com)
root.bind_all('<Control-o>', open_com)
root.bind_all('<Control-s>', save_com)
root.bind_all('<Control-s>', saveas_com)
root.bind_all('<Control-w>', close_com)

root.protocol("WM_DELETE_WINDOW", exit_com)
root.mainloop()
