# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import messagebox
import tkinter

window = tkinter.Tk()
window.geometry('400x300')
def clicked():
    messagebox.showinfo("Title-ha",  "Test is successful")

bt = tkinter.Button(window,text="Take",bg="orange",fg="black",command=clicked)
bt.grid(column=1,row=1)
window.mainloop()



