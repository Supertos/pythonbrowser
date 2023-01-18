import sys
sys.path.append("../pygui")

import json

from tkinterx.meta import WindowMeta, ask_window, askokcancel, showwarning
from tkinter import Tk, StringVar, ttk



class Root(Tk):
    def __init__(self):
        super().__init__()
        self.printX = 0
        self.printY = 0
    def getText(self, tbl):
        out = ""
        if 'inner' not in tbl or tbl['name']=="script" or tbl['name']=="title": return ""
        for element in tbl['inner']:
            if isinstance( element, str ):
                out += element
            else:
                out += self.getText( element )
        return out
    def renderTag(self, tbl):
        name = tbl['name']
        #print( name )
        #if name == "p" or name == "div":
        txt = self.getText( tbl )
        div = ttk.Label( self, text = txt).grid(row=0, column=0)
