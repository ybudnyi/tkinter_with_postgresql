"""App which stores information in PostgresDb.
User can view, search, update, delete information.
And DB is connected via google api to search info about product."""

from tkinter import *
from oop_db import DataBase
from webbrowser_search import open_search

db = DataBase()


def view_comm():
    win_list.delete(0, END)
    for item in db.view_all():
        win_list.insert(END, item)


def search_comm():
    win_list.delete(0, END)
    for item in db.search_data(name_text.get(), color_text.get(), producer_text.get()):
        win_list.insert(END, item)


def add_data_to_db():
    db.insert_data(name_text.get(), color_text.get(), producer_text.get(), group_text.get())
    win_list.delete(0, END)
    win_list.insert(END, (name_text.get(), color_text.get(), producer_text.get(), group_text.get()))


def get_selected_row(event):
    global selected_tuple
    index = win_list.curselection()[0]
    selected_tuple = win_list.get(index)
    t1.delete(0, END)
    t1.insert(END, selected_tuple[1])
    t2.delete(0, END)
    t2.insert(END, selected_tuple[3])
    t3.delete(0, END)
    t3.insert(END, selected_tuple[2])
    t4.delete(0, END)
    t4.insert(END, selected_tuple[4])


def del_comm():
    db.delete_data(selected_tuple[0])
    win_list.delete(0, END)


def update_comm():
    db.update_data(selected_tuple[0], name_text.get(), color_text.get(), producer_text.get(), group_text.get())


def web_search_comm():
    open_site = selected_tuple[4]
    open_search(open_site)


def exit_from_app():
    db.close()


window = Tk()
window.wm_title('Nail Polish DataBase')

# Create labels for entry windows
l1 = Label(window, text='Name')
l1.grid(row=0, column=0)
l2 = Label(window, text='Producer')
l2.grid(row=1, column=0)
l3 = Label(window, text='Color')
l3.grid(row=0, column=2)
l4 = Label(window, text='Google')
l4.grid(row=1, column=2)

# Create entry windows
name_text = StringVar()
t1 = Entry(window, textvariable=name_text)
t1.grid(row=0, column=1)
producer_text = StringVar()
t2 = Entry(window, textvariable=producer_text)
t2.grid(row=1, column=1)
color_text = StringVar()
t3 = Entry(window, textvariable=color_text)
t3.grid(row=0, column=3)
group_text = StringVar()
t4 = Entry(window, textvariable=group_text)
t4.grid(row=1, column=3)

# Create buttons
b1 = Button(window, text='ViewAll', width=10, command=view_comm)
b1.grid(row=2, column=3)
b2 = Button(window, text='Add', width=10, command=add_data_to_db)
b2.grid(row=3, column=3)
b3 = Button(window, text='Update', width=10, command=update_comm)
b3.grid(row=4, column=3)
b4 = Button(window, text='Search', width=10, command=search_comm)
b4.grid(row=5, column=3)
b5 = Button(window, text='Delete', width=10, command=del_comm)
b5.grid(row=6, column=3)
b6 = Button(window, text='Close', width=10, command=exit_from_app)
b6.grid(row=7, column=3)
b7 = Button(window, text='WebSearch', width=10, command=web_search_comm)
b7.grid(row=8, column=3)

# Create window which views a list of DB data
win_list = Listbox(window, height=10, width=40)
win_list.grid(row=2, column=0, rowspan=6, columnspan=2)
win_list.bind('<<ListboxSelect>>', get_selected_row)

# Create horizontal scrollbar
sb_vert = Scrollbar(window)
sb_vert.grid(row=2, column=2, rowspan=6)

# Create vertical scrollbar
sb_horz = Scrollbar(window, orient='horizontal')
sb_horz.grid(row=9, column=0, columnspan=2)

# Binding scrollbars with window
win_list.configure(yscrollcommand=sb_vert.set)
sb_vert.configure(command=win_list.yview)
win_list.configure(xscrollcommand=sb_horz.set)
sb_horz.configure(command=win_list.xview)

window.mainloop()
