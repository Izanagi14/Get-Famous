from PIL import Image, ImageTk
from Tkinter import Tk, Label, BOTH
from ttk import Frame, Style


class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Absolute positioning")
        self.pack(fill=BOTH, expand=1)

        Style().configure("TFrame", background="#333")

        bard = Image.open("FB_IMG_1480585320571.jpg")
        bard = bard.resize((250,250),Image.ANTIALIAS)
        bardejov = ImageTk.PhotoImage(bard)
        label1 = Label(self, image=bardejov)
        label1.image = bardejov
        label1.place(x=20, y=20)


        rot = Image.open("IMG_20141026_164122275_4.jpg")
        rot = rot.resize((250,250),Image.ANTIALIAS)
        rotunda = ImageTk.PhotoImage(rot)
        label2 = Label(self, image=rotunda)
        label2.image = rotunda
        label2.place(x=20, y=290)



root3 = Tk()
root3.geometry("920x1080")
app3 = Example(root3)
root3.mainloop()




