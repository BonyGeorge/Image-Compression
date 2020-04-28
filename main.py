import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

root = Tk()
root.title("Image Compression")
root.geometry("500x500+300+150")
root.resizable(width=True, height=True)


def Open():
    filename = filedialog.askopenfilename(title='Choose image', filetypes=[("Image File", '.jpg')])
    return filename


def Open_img():
    x = Open()
    img = Image.open(x)
    img = img.resize((250, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image=img)
    panel.image = img
    panel.pack()


Add_img = Button(root, text='Choose an image.', fg='white', bg='black', command=Open_img).place(x=130, y=400)
Proceed = Button(root, text='Compress.', fg='white',   bg='black').place(x=250, y=400)

root.mainloop()
