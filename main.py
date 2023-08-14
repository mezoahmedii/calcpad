import tkinter as tk, pyglet, threading, math, decimal
from simpleeval import SimpleEval, MAX_STRING_LENGTH, IterableTooLong
from time import sleep
from tkinter import ttk

pyglet.font.add_file("LigalexMono.ttf")

class AssignEx(Exception): pass

class DecimalEval(SimpleEval):
  @staticmethod
  def _eval_constant(node):
    if hasattr(node.value, "__len__") and len(node.value) > MAX_STRING_LENGTH:
      raise IterableTooLong(
        "Literal in statement is too long!"
        " ({0}, when {1} is max)".format(len(node.value), MAX_STRING_LENGTH)
      )
    
    if type(node.n) == float: return decimal.Decimal(str(node.n))
    else: return node.n

  @staticmethod
  def _eval_assign(node):
    raise AssignEx()

s = DecimalEval()
for o in [25, 24, 23, 22, 15, 14, 13, 12, 11, 10, 9, 6, 5]: del s.operators[list(s.operators.keys())[o]]

s.functions = {"sqrt": math.sqrt, "cbrt": math.cbrt, "round": round,
              "floor": math.floor, "ceil": math.ceil, "abs": abs,
              "fact": math.factorial, "log": math.log, "sin": math.sin,
              "cos": math.cos, "tan": math.tan}

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
    self.root.title("Calcpad")
    self.root.iconbitmap("icon.ico")
    self.root["bg"] = "#1e1e1e"
    self.root.minsize(250, 250)

    self.fs = ttk.Style()
    self.fs.configure(".", font=("Ligalex Mono", 12), background="#1e1e1e")

    self.mainframe = tk.Frame(self.root, bg="#1e1e1e")
    self.mainframe.place(x=250, y=187.5, anchor="center")

    self.text = tk.Text(self.mainframe, width=math.floor((math.floor(500/11.002)-2)), height=math.floor(375/24.002)-1, font=("Ligalex Mono", 14), bg="#1e1e1e", fg="white", borderwidth=0, wrap="none")
    self.text.grid(row=0, column=0)
    self.text.tag_config("res", foreground="#48c2ad", font=("Ligalex Mono", 14, "italic"))

    self.scrollv = ttk.Scrollbar(self.mainframe, command=self.text.yview)
    self.scrollv.grid(row=0, column=2, sticky="NSEW")
    self.text["yscrollcommand"] = self.scrollv.set

    self.scrollh = ttk.Scrollbar(self.mainframe, orient="horizontal", command=self.text.xview)
    self.scrollh.grid(row=1, column=0, sticky="NESW")
    self.text["xscrollcommand"] = self.scrollh.set

    self.lineEnds, self.variables = {}, {"pi": math.pi, "e": math.e, "phi": (1 + 5 ** 0.5) / 2}

    self.thread = threading.Thread(target=checkEdited, args=(self,), daemon=True)
    self.thread.start()

    self.root.bind("<Configure>", self.resize)
    self.root.mainloop()

  def checkLines(self, lines):
    # initialize variables
    text = ""
    self.variables = {"pi": math.pi, "e": math.e, "phi": (1 + 5 ** 0.5) / 2}

    for i, line in enumerate(lines.splitlines()):
      lineend = math.inf

      # remove invisible character
      if "‎" in line: line = line[:line.index("‎")-3]

      exline = "**".join(part.replace("**", "^") for part in line.split("^"))

      try: s.eval(exline)
      except AssignEx: # if the line is a variable assignment
        newvarval, vars = line.split("=")[1], {}
        for j in sorted(self.variables, key=len, reverse=True): vars[j] = self.variables[j]
        for varname, varval in vars.items(): newvarval = newvarval.replace(varname, str(varval))
        try: self.variables.update({line.split("=")[0].strip(): s.eval(newvarval)})
        except: pass
        text += f"{line}\n"
      except: # if it's not a variable assignment but it contains variables
        try:
          vars = {}
          for j in sorted(self.variables, key=len, reverse=True): vars[j] = self.variables[j]
          for varname, varval in vars.items(): exline = exline.replace(varname, str(varval))
          if type(r := s.eval(exline)) in [decimal.Decimal, int, float]: text += f"{line} = ‎{str(r)}\n"
          else: text += f"{line}\n"
          lineend = len(line) + 1
        except: text += f"{line}\n" # if it's not an equasion
      else: # if the equasion doesn't contain any variables
        if type(r := s.eval(exline)) in [decimal.Decimal, int, float]: text += f"{line} = ‎{str(r)}\n"
        else: text += f"{line}\n"
        lineend = len(line) + 1
      self.lineEnds.update({i+1: lineend})

    curpos = self.text.index("insert")
    self.text.delete(1.0, "end")
    self.text.insert("end", text)
    for i, line in enumerate(self.text.get(1.0, "end-1c").splitlines()):
      if "‎" in line: self.text.tag_add("res", f"{i+1}.{line.index('‎')-2}", f"{i+1}.{len(line)}")
    self.text.mark_set("insert", curpos)

  def resize(self, event):
    self.text.config(width=math.floor((math.floor(int(self.root.geometry().split("x")[0])/11.002)-2)), height=math.floor(int(self.root.geometry().split("x")[1].split("+")[0])/24.002)-1)
    self.mainframe.place(x=int(self.root.geometry().split("x")[0]) / 2, y=int(self.root.geometry().split("x")[1].split("+")[0]) / 2, anchor="center")

if __name__ == "__main__":
  app = App()