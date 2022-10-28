import os
import tkinter as tk
import tkinter.ttk as ttk

class whoAmIApp:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Who am I?")
        self.master.geometry('250x150')
        self.master.resizable(False, False)
        self.myname = ''
        
        self.label1 = tk.Label(self.master, text='학번:')
        self.label1.place(x=10, y=10)

        self.entry1 = tk.Entry(self.master, width=10)
        self.entry1.place(x=50, y=10)
        self.entry1.focus_set()

        self.label2 = tk.Label(self.master, text='이름:')
        self.label2.place(x=10, y=50)

        self.entry2 = tk.Entry(self.master, width=10)
        self.entry2.place(x=50, y=50)
        
        self.btnRun = tk.Button(self.master, text='저장/수정', command=self.saveName)
        self.btnRun.place(x=150, y=10)

        self.label3 = tk.Label(self.master, text='저장된 이름:')
        self.label3.place(x=10, y=100)
        
        self.label4 = tk.Label(self.master, text='')
        self.label4.place(x=100, y=100)

    def saveName(self):
        self.myname = self.entry1.get()+'_'+self.entry2.get()
        f=open('/home/ubuntu/.stuenv/myname.txt','w')
        f.write(self.myname)
        f.close()
        self.label4.config(text=self.myname)
        
    def run(self):
        self.master.mainloop()
        

if __name__ == "__main__":
    root = tk.Tk()
    app = whoAmIApp(root)
    app.run()
