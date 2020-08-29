from tkinter import PhotoImage
from tkinter.constants import *
from cv2 import cv2
import tkinter as tk
from PIL import Image, ImageTk
from backend import Database
import ntpath
from io import BytesIO

class Application():
    def __init__(self, root) -> None:
        self.root = root
        #self.root.state('zoomed')
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky=(N,W,E,S))
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.top_frame = tk.Frame(self.main_frame, bg='red')
        self.top_frame.pack(side=TOP, fill=X)
        self.bottom_frame = tk.Frame(self.main_frame, bg='black')
        self.bottom_frame.pack(side=BOTTOM, fill=X)
        
        self.canvas = tk.Canvas(self.bottom_frame)
        self.vsb = tk.Scrollbar(self.bottom_frame, orient="vertical", command=self.canvas.yview)
        self.scrollFrame = tk.Frame(self.canvas)
        
        self.scrollFrame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0,0), window=self.scrollFrame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.vsb.set)
        
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")
        
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
        
        self.addPicBut = tk.Button(self.top_frame, text="Add Image", command=self.askopenfile)
        self.addPicBut.grid(row=0, column=0)
        
        self.fileLocStrVar = tk.StringVar()
        self.fileLocEntry = tk.Entry(self.top_frame, textvariable=self.fileLocStrVar, width=35)
        self.fileLocEntry.grid(row=0, column=1, padx=10)
        
        self.viewBut = tk.Button(self.top_frame, text="View", command=self.view)
        self.viewBut.grid(row=1, column=0)
        
    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.root.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)
        return "break"
    
    def askopenfile(self):
        self.fileLocStrVar.set("")
        from tkinter.filedialog import askopenfilename
        filename_path = askopenfilename(title="Select Image", filetype=(("png files", "*.png"), ("jpg files", "*.jpg"), ("jpeg files", "*.jpeg")))
        self.fileLocStrVar.set(filename_path)
        self.insert(filename_path)
        
    def insert(self, filename_path):
        im = open(filename_path, "rb").read()
        filename = ntpath.basename(filename_path)
        database.insert(filename, im)
        
    def view(self):
        for row in database.view():
            img = Image.open(BytesIO(row[2]))
            img = img.resize((450, 500), Image.ANTIALIAS)
            phimg = ImageTk.PhotoImage(img)
            
            self.pic = tk.Label(self.scrollFrame, image=phimg)
            self.pic.image = phimg
            self.pic.pack()

        


if __name__ == "__main__":
    root = tk.Tk()
    database = Database()
    app = Application(root)
    root.mainloop()