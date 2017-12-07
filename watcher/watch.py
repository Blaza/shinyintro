from PIL import Image, ImageTk
from difflib import SequenceMatcher
import tkinter as tk
import os, sys, time
import pyinotify

window = tk.Tk()

#This creates the main window of an application
window.title("UI mock")
window.geometry("772x594")
window.configure(background='grey')

print("Showing empty image")
#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img = ImageTk.PhotoImage(Image.open("images/empty.png"))

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
panel = tk.Label(window, image = img)

#The Pack geometry manager packs widgets in rows or columns.
panel.pack(side = "bottom", fill = "both", expand = "yes")

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def minify(f):
    with open(f, 'r') as myfile:
        mini = "".join(myfile.read().split())
    return mini

def noext(f):
    return os.path.splitext(f)[0]

template_codes = {}

for f in os.listdir("templates"):
    template_codes[noext(f)] = minify("templates/" + f)

watch_file = sys.argv[1]

def display_mock():
    ui_code = minify(watch_file)
    for template in os.listdir("templates"):
        if similarity(ui_code, template_codes[noext(template)]) > 0.95:
            im = Image.open("images/" + noext(template) + ".png")
            print("Showing image " + noext(template))
            img = ImageTk.PhotoImage(im)
            panel.configure(image=img)
            panel.image = img
            return


class ModHandler(pyinotify.ProcessEvent):
    # evt has useful properties, including pathname
    def process_IN_MODIFY(self, evt):
        display_mock()


def start_watching():
    handler = ModHandler()
    wm = pyinotify.WatchManager()
    notifier = pyinotify.ThreadedNotifier(wm, handler)
    print("Started watcher")
    notifier.start()
    while not os.path.exists(watch_file):
        time.sleep(1)
    print("Found file, watching")
    wdd = wm.add_watch(watch_file, pyinotify.IN_MODIFY)


window.after(0, start_watching)

#Start the GUI
window.mainloop()

