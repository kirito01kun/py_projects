import tkinter as tk
from tkinter import filedialog, Text
import os

root = tk.Tk()
apps = []

if os.path.isfile('save.txt'):
    with open('save.txt', 'r') as f:
        temp_apps = f.read()
        temp_apps = temp_apps.split(',')
        apps = [x for x in temp_apps if x .strip()]

def add_app():

    for widget in frame.winfo_children():
        widget.destroy()

    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                        filetypes=(("executables","*.exe"),("allfiles","*./*")))
    apps.append(filename)
    print(filename)
    for app in apps:
        label = tk.Label(frame,text=app, bg="gray")
        label.pack()


def run_apps():

    for app in apps:
        os.startfile(app)


canvas = tk.Canvas(root, height=500, width=500, bg="#b401c7")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relheight=0.72, relwidth=0.8207, relx=0.08, rely=0.08)

Open_file = tk.Button(root, text="open file!", padx=10, pady=5, fg="white", bg="#9501b4", command=add_app)
Open_file.pack()

Run_apps = tk.Button(root, text="Run Apps!", padx=10, pady=5, fg="white", bg="#9501b4", command=run_apps)
Run_apps.pack()

for app in apps:
    label = tk.Label(frame, text=app)
    label.pack()

root.mainloop()

with open('save.txt', 'w') as f:
    for app in apps:
        f.write(app + ',')