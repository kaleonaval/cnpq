import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class criagrafico:
        def __init__(self,master):
                self.frame=master
                self.limpar_frame()

        def limpar_frame(self):
            widgets = self.frame.winfo_children()

            for widget in widgets:
                widget.destroy()



        def geragrafico(self):

            fig, ax1 = plt.subplots()
            canvasgraficomotores = FigureCanvasTkAgg(fig, master=self.frame)
            canvasgraficomotores.draw()
            toolbar = NavigationToolbar2Tk(canvasgraficomotores, self.frame,pack_toolbar=True)
            toolbar.update()
            canvasgraficomotores.get_tk_widget().pack(expand=True, fill=tk.BOTH)
            return plt,ax1,fig,canvasgraficomotores,toolbar

