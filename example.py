import tkinter as tk

root = tk.Tk()
label = tk.Label(root, width=20)
label.pack(side="top", fill="both", expand=True, padx=20, pady=20)

def handle_configure(event):
    text="window geometry:\n" + root.geometry()
    label.configure(text=text)

root.bind("<Configure>", handle_configure)

root.mainloop()