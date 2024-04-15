import tkinter as tk 
from tkinter import PhotoImage
import time 


class carregamento:
    def __init__(self):
        None
    def carrega_interface(self):
        self.master=tk.Tk()
        self.master.overrideredirect(True)
        self.master.attributes('-topmost',True)
        width=self.master.winfo_screenmmwidth()
        height=self.master.winfo_screenheight()
        centrox=int(width/2)+100
        centroy=int(height/2)-100
        self.master.geometry(f'800x170+{centrox}+{centroy}')
        self.frames=[]
        self.current=0
        for z in range(0,17):
            img=PhotoImage(file=f'icones\\carregando_frames_ledav\\frame_{z}.png',master=self.master)
            self.frames.append(img)
        
        self.master.wm_attributes("-transparentcolor", 'pink')
        self.master.config(background='pink')
        self.imageledav=PhotoImage(file="icones\\ledav.png",master=self.master)
        
        self.ledavcarre=tk.Label(self.master,image=self.imageledav,border=0,borderwidth=0)
        self.carregandotela=tk.Label(self.master,background="pink",border=0,borderwidth=0)
        self.ledavcarre.pack()
        self.carregandotela.pack()

        self.master.mainloop()

    def limpa_tela(self):
        self.carregandotela.destroy()
        self.ledavcarre.destroy()

    def tela_carregamento(self,n=100,step=0.1):
        if n==100:
            self.limpa_tela()
            return self.master
        
        try:
            print(n)
            n=int(17*(n/100))
            time.sleep(0.2)
            for i in range(self.current,n):
                self.current=n
                self.carregandotela.config(image=self.frames[i])
                time.sleep(step)
            if n>=17:
                self.master.destroy()
        
        except:
            pass

        return

        
