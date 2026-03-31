import tkinter as tk
from piecetable import Piecetable, Piece, Buffer

def onKeyPress(event):
    if (event.keysym == "BackSpace"):
        notepad.delete(len(text.get("1.0", tk.INSERT)) - 1, 1)
        text.delete("insert-1c", tk.INSERT)
    elif (event.keysym == "Return"):
        notepad.insert(len(text.get("1.0", tk.INSERT)),"\n")
        text.insert(tk.INSERT, "\n")
    else:
        if event.char and event.char.isprintable():
            notepad.insert(len(text.get("1.0", tk.INSERT)),event.char)
            text.insert(tk.INSERT, event.char)
    return "break"

def onUndo(event):
    notepad.undo()
    text.delete("1.0", tk.END)
    text.insert("1.0", notepad.getText())
    return "break"

def onRedo(event):
    notepad.redo()
    text.delete("1.0", tk.END)
    text.insert("1.0", notepad.getText())
    return "break"

root = tk.Tk()
notepad = Piecetable()
root.title("Notepad")
text = tk.Text(root)
text.pack()
text.bind("<Control-z>", onUndo)
text.bind("<Control-y>", onRedo)
text.bind("<Key>", onKeyPress)
root.mainloop()