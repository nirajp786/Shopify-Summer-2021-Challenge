from tkinter import Canvas, PhotoImage
from tkinter.constants import *
from tkinter.filedialog import askopenfilename
import tkinter as tk
from PIL import Image, ImageTk
from backend import Database
import ntpath
from io import BytesIO

class ToolTip(object):
    
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text, event):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        #x, y, cx, cy = self.widget.bbox("insert")
        #x = x + self.widget.winfo_rootx() + 57
        #y = y + cy + self.widget.winfo_rooty() +27
        x = event.x_root
        y = event.y_root
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text,
                      background="gray46", foreground="white", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class Application():
    def __init__(self, root) -> None:
        self.pictures = set()
        
        self.root = root
        self.root.state('zoomed')
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=BOTH)
        
        self.top_frame = tk.Frame(self.main_frame, bg='gray46')
        self.top_frame.pack(side=TOP, fill=BOTH)
        self.bottom_frame = tk.Frame(self.main_frame, bg='black')
        self.bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=True)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(0, weight=1)
        
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
        
        self.canvas.grid(row=0,column=0,sticky='nsew')
        self.vsb.grid(row=0,column=1, sticky='nswe')
        
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
        self.root.bind(sequence='<Button-3>', func=self.onObjectClick) 
        
        self.addPicBut = tk.Button(self.top_frame, text="Add Image", command=self.askopenfile)
        self.addPicBut.grid(row=0, column=0)
        
        self.fileLocStrVar = tk.StringVar()
        self.fileLocEntry = tk.Entry(self.top_frame, textvariable=self.fileLocStrVar, width=35)
        self.fileLocEntry.grid(row=0, column=1, padx=10)
        
        self.viewBut = tk.Button(self.top_frame, text="View", command=self.view)
        self.viewBut.grid(row=1, column=0, sticky='nw')
        
        self.menuPic = tk.Menu(self.scrollFrame, tearoff=0)
        self.menuPic.add_command(label="Delete Picture", command=self.deletePic)
        self.menuPic.add_command(label="Update Picture", command=self.updatePic)
        self.menuPic.add_separator()
        self.menuPic.add_command(label="Exit Menu")
        
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
        filename_path = askopenfilename(title="Select Image", filetype=[("Image files", ".png .jpg .jpeg")])
        self.fileLocStrVar.set(filename_path)
        self.insert(filename_path)
        
    def insert(self, filename_path):
        im = open(filename_path, "rb").read()
        filename = ntpath.basename(filename_path)
        database.insert(filename, im)
        self.view()
        
    def view(self):
        #self.canvas.delete('all')
        for widget in self.scrollFrame.winfo_children():
            widget.pack_forget()
        
        for row in database.view():
            picID = row[0]
            picName = row[1][:row[1].find(".")]
            picExtension = row[1][row[1].find(".")+1:]
            picDetails = "({}, {}, {}, {})".format(str(picID), picName, picExtension, row[3])
            print(picID, picName, type(str(picID)), type(picName))
            img = Image.open(BytesIO(row[2]))
            img = img.resize((self.main_frame.winfo_width(), self.main_frame.winfo_height()-20), Image.ANTIALIAS)
            phimg = ImageTk.PhotoImage(img)
            
            self.pic = tk.Label(self.scrollFrame, image=phimg)
            self.pic.image = phimg
            self.pic.text = picDetails
            self.pictures.add(self.pic)
            self.pic.pack(fill=BOTH, expand=True, anchor=E)
            
            self.createtooltip(widget=self.pic, text=f'ID: {picID}\n'
                                                        f'Picture Name: {picName}'+f'.{picExtension}\n'
                                                        f'Date Added: {row[3]}')
            
    def onObjectClick(self, event):
        print("Clicked", event.x, event.y, event.y, event.widget)
        self.caller = event
        if isinstance(event.widget, tk.Label):
            try:
                self.menuPic.tk_popup(event.x_root, event.y_root)
            finally:
                self.menuPic.grab_release()
    
    def deletePic(self):
        #print(self.caller.widget.text)
        #print(type(self.caller.widget.text))
        tup = tuple(str(word) for word in self.caller.widget.text.replace('(', '').replace(')', '').replace('...', '').split(', '))
        database.delete(int(tup[0]))
        self.view()
        
    def updatePic(self):
        tup = tuple(str(word) for word in self.caller.widget.text.replace('(', '').replace(')', '').replace('...', '').split(', '))
        filename_path = askopenfilename(title="Select Image", filetype=[("Image files", ".png .jpg .jpeg")])
        im = open(filename_path, "rb").read()
        database.update(int(tup[0]), im)
        self.view()
        
    def createtooltip(self, widget, text):
        tooltip = ToolTip(widget)
        def enter(event):
            tooltip.showtip(text, event)
        def leave(event):
            tooltip.hidetip()
        widget.bind('<Enter>', enter)
        widget.bind("<Leave>", leave)
        
    
if __name__ == "__main__":
    root = tk.Tk()
    database = Database()
    app = Application(root)
    root.mainloop()