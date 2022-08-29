# minecraft-mod-updater -- Check updates for Minecraft mods and optionally update them.
# Copyright (C) 2022  SimplyTolex
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from tkinter import *
from tkinter import ttk
from tkinter import font
import yaml
import os.path
import pickledb
import webbrowser

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

header_font = font.Font(name= "header_font", size=11, weight='bold')    # def size=9; TODO: make settings

number_label = ttk.Label(mainframe, text="№", font=header_font)
number_label.grid(column=number_column, row=0, sticky=W)
id_label = ttk.Label(mainframe, text="ID", font=header_font)
id_label.grid(column=id_column, row=0)
name_label = ttk.Label(mainframe, text="Name", font=header_font)
name_label.grid(column=name_column, row=0)
current_label = ttk.Label(mainframe, text="Current", font=header_font)
current_label.grid(column=current_column, row=0)
latest_label = ttk.Label(mainframe, text="Latest", font=header_font)
latest_label.grid(column=latest_column, row=0)
url_label = ttk.Label(mainframe, text="URL", font=header_font)
url_label.grid(column=url_column, row=0)

mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=20)
mainframe.columnconfigure(2, weight=50)
mainframe.columnconfigure(3, weight=10)
mainframe.columnconfigure(4, weight=10)
mainframe.columnconfigure(5, weight=30)
# mainframe.rowconfigure(0, weight=1)

root.option_add('*tearOff', FALSE)
menubar = Menu(root)
root["menu"] = menubar

menu_file = Menu(menubar)
menu_add = Menu(menu_file)
menu_edit = Menu(menubar)
menu_view = Menu(menubar)
menu_mods = Menu(menubar)
menu_about = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='File')
menubar.add_cascade(menu=menu_edit, label='Edit')
menubar.add_cascade(menu=menu_view, label='View')
menubar.add_cascade(menu=menu_mods, label='Mods')
menubar.add_cascade(menu=menu_about, label='About')

menu_file.add_cascade(menu=menu_add, label='Add entry...')
menu_file.add_command(label='Remove entries')
menu_file.add_command(label='Rescan `mods` directory')

menu_add.add_command(label="Add URL")
menu_add.add_command(label="Bulk-add with modlist file")
menu_add.add_command(label="Add manually")
menu_add.add_command(label="Add automatically by mod's filename")

menu_edit.add_command(label="Preferences")

menu_view.add_command(label="Choose visible columns")

menu_mods.add_command(label="Check all mods for updates")

menu_about.add_command(label="Get help")
menu_about.add_command(label="Open GitHub page")
menu_about.add_command(label="Open online documentation")
menu_about.add_command(label="Check program for updates")
menu_about.add_command(label="About program")


next_free_row = 1
modlist = []
db = ""


def get_file_from_parent_dir(filename:str):
    """
    Helps me to get files in parent directory.
    Will be mainly used for development, since regular files should be stored in APPDATA anyway.
    """
    CURRENT_DIR = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(CURRENT_DIR, os.pardir)) + "\\" + filename


# Load config
# TODO: Not sure if I will even use YAML in the future, maybe I will just move everything, including configs to PickleDB
with open(get_file_from_parent_dir("config.yaml"), "r") as config:
    cfg = yaml.safe_load(config)


def init_modDB():
    """
    modDB is a database that stores everything about imported mods (their id, names, versions, etc.)
    """
    global db
    db = pickledb.load(get_file_from_parent_dir("modDB.db"), False)


def write_modDB(id:str, name:str, current:str, last_latest:str, url:str):
    global db
    db.set("version", 1)
    db.set(id, {"name": name, "current": current, "last_latest": last_latest, "url": url})
    # Examples:
    # write_modDB("AABBCCDDEE", "Sodium", "1.2", "1.2", "example.com")
    # write_modDB("BBCCDDEEFF", "test_mod_1", "1.0", "1.2", "example.com")
    db.dump()


def get_info_from_db():
    """
    Reads the database version and depending on it, does different things.
    Currently, it will fill out the rows in the GUI with every entry, other then the first one (so, everything but version).
    """
    match db.get("version"):
        case 1:
            for entry in range(1, db.totalkeys()):
                print(list(db.getall())[entry])
                key = (list(db.getall())[entry])
                print(db.get(key))
                value = db.get(key)

                fill_row(str(key), str(value["name"]), str(value["current"]), str(value["last_latest"]), str(value["url"]))
        case _:
            raise Exception("Undefined database version")


def fill_row(id:str, name:str, current:str, latest:str, url:str):
    global next_free_row
    global number_column
    global id_column
    global name_column
    global current_column
    global latest_column
    global url_column

    mod_number = ttk.Label(mainframe, text=next_free_row, font="TkFixedFont")
    mod_id = ttk.Label(mainframe, text=id, font="TkFixedFont")
    mod_name = ttk.Label(mainframe, text=name)
    mod_current = ttk.Label(mainframe, text=current)
    mod_latest = ttk.Label(mainframe, text=latest)
    mod_url = ttk.Label(mainframe, text=url, cursor="hand2", foreground="blue")

    mod_number.grid(column=number_column, row=next_free_row, sticky=W)
    mod_id.grid(column=id_column, row=next_free_row)
    mod_name.grid(column=name_column, row=next_free_row)
    mod_current.grid(column=current_column, row=next_free_row)
    mod_latest.grid(column=latest_column, row=next_free_row)
    mod_url.grid(column=url_column, row=next_free_row)

    mod_url.bind("<Button-1>", lambda e: open_link(url))

    next_free_row += 1


def import_from_modlist():
    """
    Modlist is just a long txt file how batch-importing mods, this is not a database, that the app uses.
    """
    global modlist

    with open(get_file_from_parent_dir("modlist.txt"), "r") as list:
        for line in list:
            modlist.append(line)


def open_link(url):
    webbrowser.open(url)    # Make sure that the link starts with `https://`


if __name__ == '__main__':
    init_modDB()
    get_info_from_db()

    root.mainloop()
