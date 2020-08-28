from cv2 import cv2
import tkinter as tk
from PIL import Image, ImageTk
from backend import Database
import ntpath

class Application():
    def __init__(self, root) -> None:
        self.root = root
        self.root.state('zoomed')
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
        
        self.addPicBut = tk.Button(self.frame, text="Add Image", command=self.askopenfile)
        self.addPicBut.grid(row=0, column=0)
        
        self.fileLocStrVar = tk.StringVar()
        self.fileLocEntry = tk.Entry(self.frame, textvariable=self.fileLocStrVar, width=35)
        self.fileLocEntry.grid(row=0, column=1, padx=10)
        
        self.viewBut = tk.Button(self.frame, text="View", command=self.view)
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
        from tkinter.filedialog import askopenfilename
        filename_path = askopenfilename(title="Select Image", filetype=(("png files", "*.png"), ("jpg files", "*.jpg"), ("jpeg files", "*.jpeg")))
        self.fileLocStrVar.set(filename_path)
        self.insert(filename_path)
        
    def insert(self, filename_path):
        im = cv2.imread(filename_path)
        filename = ntpath.basename(filename_path)
        #print(filename)
        #print(im)
        backend.insert(filename, im)
        
    def view(self):
        for row in backend.view():
            print(row[0], row[1], row[2])
        
    


if __name__ == "__main__":
    root = tk.Tk()
    
    app = Application(root)
    root.mainloop()