#import the necessary libraries
import tkinter as tk
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import os

#create the main window
root = tk.Tk()
root.title("Notepad")
root.geometry("500x400")

#create the menu bar
menu_bar = Menu(root)

#create the file menu
file_menu = Menu(menu_bar, tearoff=0)

#add commands to the file menu
file_menu.add_command(label="New", command=lambda: new_file())
file_menu.add_command(label="Open", command=lambda: open_file())
file_menu.add_command(label="Save", command=lambda: save_file())
file_menu.add_command(label="Save As", command=lambda: save_as_file())
file_menu.add_separator()
file_menu.add_command(label="Exit", command=lambda: exit_app())

#add the file menu to the menu bar
menu_bar.add_cascade(label="File", menu=file_menu)

#create the edit menu
edit_menu = Menu(menu_bar, tearoff=0)

#add commands to the edit menu
edit_menu.add_command(label="Undo", command=lambda: undo())
edit_menu.add_command(label="Cut", command=lambda: cut())
edit_menu.add_command(label="Copy", command=lambda: copy())
edit_menu.add_command(label="Paste", command=lambda: paste())

#add the edit menu to the menu bar
menu_bar.add_cascade(label="Edit", menu=edit_menu)

#create the help menu
help_menu = Menu(menu_bar, tearoff=0)

#add commands to the help menu
help_menu.add_command(label="About", command=lambda: about_app())

#add the help menu to the menu bar
menu_bar.add_cascade(label="Help", menu=help_menu)

#add the menu bar to the main window
root.config(menu=menu_bar)

#create the text widget
text_widget = Text(root, bg="white", fg="black")
text_widget.pack(fill=BOTH, expand=1)

#create a scrollbar
scrollbar = Scrollbar(text_widget)
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar.config(command=text_widget.yview)
text_widget.config(yscrollcommand=scrollbar.set)

#global variables
file_name = None

#functions
def new_file():
    global file_name
    file_name = "Untitled"
    text_widget.delete(1.0, END)

def open_file():
    global file_name
    file_name = tk.filedialog.askopenfilename(defaultextension=".txt", 
                                            filetypes=[("All Files","*.*"),
                                            ("Text Documents","*.txt")])
    if file_name == "":
        file_name = None
    else:
        root.title(os.path.basename(file_name) + " - Notepad")
        text_widget.delete(1.0, END)
        f = open(file_name, "r")
        text_widget.insert(1.0, f.read())
        f.close()

def save_file():
    global file_name
    if file_name == None:
        save_as_file()
    else:
        f = open(file_name, "w")
        f.write(text_widget.get(1.0, END))
        f.close()

def save_as_file():
    f = tk.filedialog.asksaveasfile(mode="w", defaultextension=".txt", 
                                    filetypes=[("All Files","*.*"),
                                    ("Text Documents","*.txt")])
    global file_name
    if f is None:
        file_name = None
    else:
        file_name = f.name
        f = open(file_name, "w")
        f.write(text_widget.get(1.0, END))
        f.close()
        root.title(os.path.basename(file_name) + " - Notepad")

def exit_app():
    if tk.messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

def undo():
    text_widget.event_generate("<<Undo>>")

def cut():
    text_widget.event_generate("<<Cut>>")

def copy():
    text_widget.event_generate("<<Copy>>")

def paste():
    text_widget.event_generate("<<Paste>>")

def about_app():
    tk.messagebox.showinfo("About Notepad", "Notepad is a simple text editor.")

#run the main loop
root.mainloop()