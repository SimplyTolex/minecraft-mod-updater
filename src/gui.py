from operator import mod
from tkinter import *
from tkinter import ttk
import yaml
import os.path

root = Tk()
root.title("minecraft-mod-updater")

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

number_column = 0
id_column = 1
name_column = 2
current_column = 3
latest_column = 4
url_column = 5

number_label = ttk.Label(mainframe, text="№")
number_label.grid(column=number_column, row=0, sticky=W)
id_label = ttk.Label(mainframe, text="ID")
id_label.grid(column=id_column, row=0)
name_label = ttk.Label(mainframe, text="Name")
name_label.grid(column=name_column, row=0)
current_label = ttk.Label(mainframe, text="Current")
current_label.grid(column=current_column, row=0)
latest_label = ttk.Label(mainframe, text="Latest")
latest_label.grid(column=latest_column, row=0)
url_label = ttk.Label(mainframe, text="URL")
url_label.grid(column=url_column, row=0)

mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=20)
mainframe.columnconfigure(2, weight=50)
mainframe.columnconfigure(3, weight=10)
mainframe.columnconfigure(4, weight=10)
mainframe.columnconfigure(5, weight=30)
# mainframe.rowconfigure(0, weight=1)

next_free_row = 1
modlist = []


def get_file_from_parent_dir(filename:str):
    """
    Helps me to get files in parent directory.
    Will be mainly used for development, since regular files should be stored in APPDATA anyway.
    """
    CURRENT_DIR = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(CURRENT_DIR, os.pardir)) + "\\" + filename


# Read config
with open(get_file_from_parent_dir("config.yaml"), "r") as config:
    cfg = yaml.safe_load(config)
    print(cfg)


def read_modlist():
    """
    Modlist is just a long txt file how batch-importing mods, this is not a database, that the app uses.
    """
    global modlist
    
    with open(get_file_from_parent_dir("modlist.txt"), "r") as list:
        for line in list:
            modlist.append(line)


def read_modDB():
    """
    modDB is a database that stores everything about imported mods (their id, names, versions, etc.)
    """
    pass


def fill_row(id:str, name:str, current:str, latest:str, url:str):
    global next_free_row
    global number_column
    global id_column
    global name_column
    global current_column
    global latest_column
    global url_column

    mod_number = ttk.Label(mainframe, text=next_free_row)
    mod_id = ttk.Label(mainframe, text=id)
    mod_name = ttk.Label(mainframe, text=name)
    mod_current = ttk.Label(mainframe, text=current)
    mod_latest = ttk.Label(mainframe, text=latest)
    mod_url = ttk.Label(mainframe, text=url)

    mod_number.grid(column=number_column, row=next_free_row, sticky=W)
    mod_id.grid(column=id_column, row=next_free_row)
    mod_name.grid(column=name_column, row=next_free_row)
    mod_current.grid(column=current_column, row=next_free_row)
    mod_latest.grid(column=latest_column, row=next_free_row)
    mod_url.grid(column=url_column, row=next_free_row)

    next_free_row += 1

for i in range(15):
    fill_row("AABBCCDDEE", "test_mod_1", "1.0", "1.2", "example.com")

read_modlist()
print(modlist)

root.mainloop()
