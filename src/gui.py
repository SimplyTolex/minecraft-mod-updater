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

# from tabnanny import verbose
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import os.path
import pickledb
import webbrowser
import github_api as gh_api
import curseforge_api as cf_api
import modrinth_api as mr_api
import internal_vars as internal
from PIL import ImageTk, Image
import tldextract
import shutil

next_free_row = 1
modlist = []
db = ""
config = ""
verbose = True
modqueue = []

# TODO: add ability to 'freeze' or 'ignore' new versions of a mod
# TODO: add ability to choose whether you want to update to a stable or to a beta or to an alpha version of the mod

verboseprint = print if verbose else lambda *a, **k: None

def get_file_from_parent_dir(filename: str):
    """
    Helps me to get files in parent directory.
    Will be mainly used for development, since regular files should be stored in APPDATA anyway.
    """
    CURRENT_DIR = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(CURRENT_DIR, os.pardir)) + "\\" + filename


# # Load config
# # TODO: Not sure if I will even use YAML in the future, maybe I will just move everything, including configs to PickleDB
# with open(get_file_from_parent_dir("config.yaml"), "r") as config:
#     cfg = yaml.safe_load(config)

def load_config():
    global config
    if os.path.exists(get_file_from_parent_dir("settings.jsonc")):
        config = pickledb.load(get_file_from_parent_dir("settings.jsonc"), True)
        verboseprint("Loaded settings.jsonc")
    else:
        shutil.copyfile(get_file_from_parent_dir("default_settings.jsonc"), get_file_from_parent_dir("settings.jsonc"))
        verboseprint("Copied default_settings.jsonc to settings.jsonc to use as config file")
        load_config()


def load_modDB():
    """
    modDB is a database that stores everything about imported mods (their id, names, versions, etc.)
    """
    global db
    db = pickledb.load(get_file_from_parent_dir("modDB.json"), False)
    
    match db.get("version"):    # later, this will check the version of the modDB and call a function to convert the old versions of the modDB to a new ones. Right now this isn't necessary, since there are no other versions
        case 1:
            verboseprint("Loaded modDB version 1")
        case _:
            print(db.get("version"))
            raise Exception("Undefined database version")


def read_modDB():
    pass


def write_modDB(queue: list):   # TODO: fix ids maybe being the same from different sites, which will overwrite the other entry
    """
    Gets a queue, then sets all the keys from the queue, then dumps it into modDB file.
    Currently, you need to provide *all* of the keys or else they will be lost.
    
    Avaliable keys: "id": str, "name": str, "current": str, "last_latest": str, "url": str.
    
    Queue should look like this: [{"id": "AABBCCDD", "name": "foo mod", etc...}, {"id2": "EEFFGGHH", "name2": "chocolate bar", etc...}, etc...]
    """
    global db
    
    db.set("version", 1)
    for entry in queue:
        db.set(entry["id"], {"name": entry["name"],  "current": entry["current"], "last_latest": entry["last_latest"], "url": entry["url"]})
    db.dump()


def fill_treeview_from_db():
    """
    Reads the database version and depending on it, does different things.
    Currently, it will fill out the rows in the GUI with every entry, other then the first one (so, everything but version).
    """
    global next_free_row

    for entry in range(1, db.totalkeys()):
        key = (list(db.getall())[entry])
        value = db.get(key)

        ext = tldextract.extract(str(value['url']))
        tld_url = '.'.join(part for part in ext if part)

        tree.insert('', 'end', text=next_free_row, values=(str(key), str(value['name']), str(value['current']), str(value['last_latest']), tld_url))

        next_free_row += 1


def import_from_modlist():
    """
    Modlist is just a long txt file how batch-importing mods, this is not a database, that the app uses.
    """
    global modlist

    with open(get_file_from_parent_dir("modlist.txt"), "r") as list:
        for line in list:
            modlist.append(line)


def scan_mods_dir():
    """
    This will scan %APPDATA%/Minecraft/mods directory for changes, they will be used for stuff like automatically removing mods, that don't exist in the folder anymore, from modDB
    """
    pass
    

def open_link(url: str):
    webbrowser.open(url)    # Make sure that the link starts with `https://`


def ui_add_url():
    pass


def ui_add_modlist():
    pass


def ui_add_manually():
    pass


def ui_autoadd():
    pass


def ui_remove_manually():
    pass


def ui_remove_modlist():
    pass


def ui_autoremove():
    pass


def ui_rescan_mods_dir():
    pass


def ui_settings():
    # TODO: add a button to purge tldextract cache (reference: <https://github.com/john-kurkowski/tldextract#note-about-caching>)
    settings_root = Toplevel(root)
    settings_root.title("Preferences")
    # settings_root.resizable(FALSE, FALSE)

    settings_mainframe = ttk.Frame(settings_root, padding=(10, 10))
    settings_mainframe.grid()

    notebook = ttk.Notebook(settings_mainframe)
    notebook.grid()

    # create frames
    f_general = ttk.Frame(notebook, width=400, height=280, padding=10)
    f_visual = ttk.Frame(notebook, width=400, height=280, padding=10)
    f_misc = ttk.Frame(notebook, width=400, height=280, padding=10)

    f_general.grid()
    f_visual.grid()
    f_misc.grid()

    # add frames to notebook
    notebook.add(f_general, text='General')
    notebook.add(f_visual, text='Visual')
    notebook.add(f_misc, text='Misc')
    
    apply_button = ttk.Button(settings_mainframe, text="Apply")
    apply_button.grid(column=0, row=1)
    
    nothing_label = ttk.Label(f_general, text="There is nothing so far")
    opt_in_prereleases = ttk.Checkbutton(f_general, text="Also update to pre-release versions")
    nothing2_label = ttk.Label(f_visual, text="There is should be font size settings, but I didn't made them yet")
    
    nothing_label.grid()
    opt_in_prereleases.grid(row=1, column=0)
    nothing2_label.grid()
    
    purge_tld_cache = ttk.Button(f_misc, text="Purge tldextract cache")
    purge_tld_cache_explain = ttk.Label(f_misc, text="See this link: hpspaihpeoahnopwhnxfoai")
    purge_tld_cache.grid(column=1, row=1)
    purge_tld_cache_explain.grid(column=1, row=2)
    
    github_login_frame = ttk.Labelframe(f_misc, padding=10, borderwidth=2, relief='solid', text="Signin to Github")
    github_login_username_label = ttk.Label(github_login_frame, text="Username or email address", justify='left')
    github_login_username = ttk.Entry(github_login_frame)
    github_login_password_label = ttk.Label(github_login_frame, text="Password", justify='left')
    github_login_password = ttk.Entry(github_login_frame, show='*')
    
    github_login_frame.grid(column=2, row=1)
    github_login_username_label.grid(column=1, row=1)
    github_login_username.grid(column=1, row=2)
    github_login_password_label.grid(column=1, row=3)
    github_login_password.grid(column=1, row=4)


def ui_refresh_list():
    pass


def ui_choose_columns():
    pass


def check_mods_for_updates():
    pass


def open_help():
    pass


def open_github():
    open_link(internal.github_link)


def open_discussions():
    open_link(f"{internal.github_link}/discussions")


def open_docs():
    open_link(f"{internal.github_link}/wiki")


def check_updates():
    # TODO: maybe add a popup, telling the user that you *are* actually checking updates
    update_name = gh_api.check_releases(internal.author, internal.app_name)
    verboseprint("r: " + update_name)
    verboseprint("internal: " + internal.version)

    # TODO: maybe rewrite it to use tag_names instead(?)
    if update_name != internal.version:
        outcome = messagebox.askyesno(message="A new version of the program had been found.\nDo you want to open the release page in the browser?",
                                      title="Update is avaliable!")   # TODO: add link to the "yes" button
        if outcome == "yes":
            open_link("")
    else:
        messagebox.showinfo(
            message="You are running the latest version.\nNo update necessary.", title="No updates avaliable")


def open_about():
    # TODO: make the about_root grab focus when opened
    about_root = Toplevel(root)
    about_root.title(f"About {internal.app_name}")
    # about_window.geometry("450x350")
    about_root.resizable(FALSE, FALSE)

    # Frames
    about_mainframe = ttk.Frame(about_root, padding=(10, 10))
    branding_frame = ttk.Frame(about_mainframe, borderwidth=2)
    thanks_frame = ttk.Frame(about_mainframe, borderwidth=2)

    # Branding
    image_path = get_file_from_parent_dir("images\\icon.gif")

    banner = ImageTk.PhotoImage(Image.open(image_path))
    banner_label = ttk.Label(branding_frame, image=banner, anchor='center')
    banner_label.image = banner

    about_name = ttk.Label(branding_frame, text=internal.app_name, font="TkHeaderFont", anchor='center')
    about_version = ttk.Label(branding_frame, text=f"v{internal.version}", justify='center', anchor='center', font="TkFixedFont")
    about_label = ttk.Label(branding_frame, text=internal.about_text, justify='center', anchor='center')

    # Thanks
    about_special_thanks = ttk.Label(thanks_frame, text="Special Thanks to...", font="TkHeaderFont", anchor="center")
    people_list = ttk.Label(thanks_frame, text=internal.special_thanks, anchor="center", relief="solid", borderwidth=2, justify='center')       # TODO: implement list with canvas instead (or just make it scrollable somehow)

    # Grids
    about_mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
    branding_frame.grid(column=0, row=0, sticky=(N, S, E, W))
    thanks_frame.grid(column=0, row=1, sticky=(N, S, E, W))

    banner_label.grid(column=0, row=0, sticky=(E, W))
    about_name.grid(column=0, row=1, sticky=(E, W))
    about_version.grid(column=0, row=2, sticky=(E, W))
    about_label.grid(column=0, row=3, sticky=(E, W))

    about_special_thanks.grid(column=0, row=0, sticky=(E, W))
    people_list.grid(column=0, row=1, sticky=(N, S, E, W))

    # Grid configuration
    about_root.columnconfigure(0, weight=1)
    about_root.rowconfigure(0, weight=1)

    about_mainframe.columnconfigure(0, weight=1)
    about_mainframe.rowconfigure(0, weight=1)
    about_mainframe.rowconfigure(1, weight=1)

    branding_frame.columnconfigure(0, weight=1)
    branding_frame.rowconfigure(0, weight=1)
    branding_frame.rowconfigure(1, weight=10)
    branding_frame.rowconfigure(2, weight=10)
    branding_frame.rowconfigure(3, weight=10)

    thanks_frame.columnconfigure(0, weight=1)
    thanks_frame.rowconfigure(0, weight=1)
    thanks_frame.rowconfigure(1, weight=10)


def tree_event_handler(event):
    x = event.x
    y = event.y
    verboseprint(f"{x}, {y}")
    clicked_column = tree.identify_column(x)
    clicked_row = tree.identify_row(y)

    # We do nothing if x = 0 or y = 0 because it leads to errors and also nothing highlights when you click on stuff this way, so technically you aren't clicking anything.
    if (x != 0) and (y != 0):
        if clicked_column != "#0":  # prevents overflow to the last column; prevents ValueError invalid literal for int() with base 10: ''
            clicked_column = (tree['columns'][int(clicked_column[1:])-1])   # accouting for the `#0`, which is missing from 'columns'
        verboseprint(f"Clicked column name: {clicked_column}")

        if clicked_row == "" or y <= 24:    # POV: you are working around tk's bugs
            verboseprint("Clicked on header")    # TODO: make a sorting when clicking on headers
        else:
            clicked_row = int(clicked_row[1:], base=16)
            verboseprint(f"Clicked row (base10): {clicked_row}")

            match clicked_column:
                case "link":
                    key_lookup = (list(db.getall())[clicked_row])
                    verboseprint(f"Opening URL: {db.get(key_lookup)['url']}")
                    open_link(db.get(key_lookup)['url'])
                case "latest":
                    print('hi dad')     # TODO: check for updates for a clicked mod when user clicks on latest version


root = Tk()
root.title(internal.app_name)

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

# def size=9; TODO: make settings
header_font = font.Font(name="header_font", size=11, weight='bold')

mainframe.columnconfigure(0, weight=1)
# mainframe.columnconfigure(1, weight=20)
# mainframe.columnconfigure(2, weight=50)
# mainframe.columnconfigure(3, weight=10)
# mainframe.columnconfigure(4, weight=10)
# mainframe.columnconfigure(5, weight=30)
mainframe.rowconfigure(0, weight=1)

# TODO: add theming for headers and links
tree = ttk.Treeview(mainframe, columns=('id', 'name', 'current', 'latest', 'link'))
tree.heading('#0', text='№')
tree.column('#0', width=50, anchor='w')
tree.heading('id', text='ID')
tree.column('id', width=150, anchor='center')
tree.heading('name', text='Name')
tree.column('name', anchor='center')
tree.heading('current', text='Current')
tree.column('current', width=50, anchor='center')
tree.heading('latest', text='Latest')
tree.column('latest', width=50, anchor='center')
tree.heading('link', text='URL')
tree.column('link', width=100, anchor='center')
tree.grid(column=0, row=0, sticky=(N, S, E, W))

scrollbar = ttk.Scrollbar(root, orient=['vertical'], command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

tree.bind('<Button-1>', tree_event_handler)

root.option_add('*tearOff', FALSE)
menubar = Menu(root)
root["menu"] = menubar

menu_file = Menu(menubar)
menu_add = Menu(menu_file)
menu_remove = Menu(menu_file)
menu_edit = Menu(menubar)
menu_view = Menu(menubar)
menu_mods = Menu(menubar)
menu_about = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='File')
menubar.add_cascade(menu=menu_edit, label='Edit')
menubar.add_cascade(menu=menu_view, label='View')
menubar.add_cascade(menu=menu_mods, label='Mods')
menubar.add_cascade(menu=menu_about, label='About')

menu_file.add_cascade(menu=menu_add, label='Add entries...')
menu_file.add_cascade(menu=menu_remove, label='Remove entries...')
menu_file.add_command(label='Rescan `mods` directory', command=ui_rescan_mods_dir)

menu_add.add_command(label="Add URL", command=ui_add_url)
menu_add.add_command(label="Bulk-add with modlist file",
                     command=ui_add_modlist)
menu_add.add_command(label="Add manually", command=ui_add_manually)
menu_add.add_separator()
menu_add.add_command(label="Add automatically by mod's filename",
                     command=ui_autoadd, state=DISABLED)

menu_remove.add_command(
    label="Choose which mods to remove", command=ui_remove_manually)
menu_remove.add_command(
    label="Bulk-remove with modlist file", command=ui_remove_modlist)
menu_remove.add_separator()
menu_remove.add_command(label="Remove entries not present in `mods` directory",
                        command=ui_autoremove, state=DISABLED)

menu_edit.add_command(label="Preferences", command=ui_settings)

menu_view.add_command(label="Refresh list", command=ui_refresh_list)
menu_view.add_command(label="Choose visible columns",
                      command=ui_choose_columns)

menu_mods.add_command(label="Check all mods for updates",
                      command=check_mods_for_updates)

menu_about.add_command(label="Get help", command=open_help)
menu_about.add_command(label="Open GitHub page", command=open_github)
menu_about.add_command(label="Open GitHub Discussions",
                       command=open_discussions)
menu_about.add_command(label="Open online documentation", command=open_docs)
menu_about.add_separator()
menu_about.add_command(label="Check program for updates",
                       command=check_updates)
menu_about.add_separator()
menu_about.add_command(label="About program", command=open_about)

if __name__ == '__main__':
    load_config()
    load_modDB()
    # write_modDB([{"id": "3", "name": "modDB write test", "current": "1.4.4", "last_latest": "1.4.5", "url": "https://example.com"}, {"id": "4", "name": "modDB write test 2", "current": "1.4", "last_latest": "1.4.4", "url": "https://example.com"}])
    fill_treeview_from_db()

    root.mainloop()
