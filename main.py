import tkinter as tk, pyglet, os, threading, math, decimal
from simpleeval import SimpleEval, MAX_STRING_LENGTH, IterableTooLong
from time import sleep
from tkinter import ttk

class DecimalEval(SimpleEval):
  @staticmethod
  def _eval_constant(node):
    if hasattr(node.value, "__len__") and len(node.value) > MAX_STRING_LENGTH:
      raise IterableTooLong(
        "Literal in statement is too long!"
        " ({0}, when {1} is max)".format(len(node.value), MAX_STRING_LENGTH)
      )
    return decimal.Decimal(str(node.n))

s = DecimalEval()

s.functions = {"sqrt": math.sqrt, "cbrt": math.cbrt, "round": round,
              "floor": math.floor, "ceil": math.ceil, "abs": abs,
              "fact": math.factorial, "log": math.log, "sin": math.sin,
              "cos": math.cos, "tan": math.tan}

s.names = {"pi": math.pi, "e": math.e, "phi": (1 + 5 ** 0.5) / 2}

def checkEdited(app):
  while not app.text.edit_modified():
    sleep(0.1)
    curpos = app.text.index("insert")
    try:
      if int(curpos.split(".")[1]) > app.lineEnds[int(curpos.split(".")[0])]:
        app.text.mark_set("insert", f"{curpos.split('.')[0]}.{app.lineEnds[int(curpos.split('.')[0])]}")
    except:
      app.lineEnds.update({int(curpos.split(".")[0]): math.inf})
      if int(curpos.split(".")[1]) > app.lineEnds[int(curpos.split(".")[0])]:
        app.text.mark_set("insert", f"{curpos.split('.')[0]}.{app.lineEnds[int(curpos.split('.')[0])]}")

  app.checkLines(app.text.get(1.0, "end-1c"))

  app.text.edit_modified(False)
  return checkEdited(app)

class App:
  def __init__(self):
    self.root = tk.Tk()
    self.root.geometry("500x375+250+150")
    self.root.title("Sticky Calculator 2")
    self.root["bg"] = "#1e1e1e"
    self.root.minsize(250, 250)

    pyglet.font.add_file(os.path.join("fonts", "LigalexMono.ttf"))

    self.mainframe = tk.Frame(self.root, bg="#1e1e1e")
    self.mainframe.place(x=250, y=187.5, anchor="center")

    self.text = tk.Text(self.mainframe, width=math.floor((math.floor(500/11.002)-2)), height=math.floor(375/24.002)-2, font=("Ligalex Mono", 14), bg="#1e1e1e", fg="white", borderwidth=0, wrap="none")
    self.text.grid(row=0, column=0)

    self.scrollv = ttk.Scrollbar(self.mainframe, command=self.text.yview)
    self.scrollv.grid(row=0, column=2, sticky="NSEW")

    self.text["yscrollcommand"] = self.scrollv.set

    self.scrollh = ttk.Scrollbar(self.mainframe, orient="horizontal", command=self.text.xview)
    self.scrollh.grid(row=1, column=0, sticky="NESW")
    self.text["xscrollcommand"] = self.scrollh.set

    self.settingsb = ttk.Button(self.mainframe, text=u"\uE713 Settings")
    self.settingsb.grid(row=2, column=0, columnspan=3)

    self.lineEnds = {}

    self.thread = threading.Thread(target=checkEdited, args=(self,), daemon=True)
    self.thread.start()

    self.root.bind("<Configure>", self.resize)
    self.root.mainloop()

  def checkLines(self, lines):
    text = """"""
    for i, line in enumerate(lines.splitlines()):
      lineend = math.inf
      line = "^".join(part.replace("^", "**") for part in line.split("**"))
      if "‎" in line:
        line = line[:line.index("‎")-3]
      try:
        text += f"""{line} = ‎{str(s.eval(line))}
"""
        lineend = len(line) + 1
      except: text += f"""{line}
"""
      self.lineEnds.update({i+1: lineend})
    curpos = self.text.index("insert")
    self.text.delete(1.0, "end")
    self.text.insert("end", text)
    self.text.mark_set("insert", curpos)

  def resize(self, event):
    self.text.config(width=math.floor((math.floor(int(self.root.geometry().split("x")[0])/11.002)-2)), height=math.floor(int(self.root.geometry().split("x")[1].split("+")[0])/24.002)-2)
    self.mainframe.place(x=int(self.root.geometry().split("x")[0]) / 2, y=int(self.root.geometry().split("x")[1].split("+")[0]) / 2, anchor="center")

if __name__ == "__main__":
  app = App()