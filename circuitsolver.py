from __future__ import print_function
from __future__ import division
import SchemDraw as schem
import SchemDraw.elements as e
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
import sympy
import numpy as np
from IPython.display import display, Math

class element:
    def __init__(self, kind, position, value = 0, dposition = "", dtype = "", a = 0, b = 0):
        self.kind = kind
        self.position = position
        self.value = value
        self.dposition = dposition
        self.dtype = dtype
        self.a = a
        self.b = b

class MyWindow:
    def __init__(self, win):
        self.lbl1=Label(win, text='Start Point')
        self.lbl2=Label(win, text='End Point')
        self.lbl4=Label(win, text='Value')
        self.lbl5=Label(win, text='Type')
        self.lbl6=Label(win, text='Start Point')
        self.lbl7=Label(win, text='End Point')
        self.lbl8=Label(win, text='Depends on:')
        self.lbl9=Label(win, text='Relation: ')
        self.lbl10=Label(win, text='  x  +\t')
        self.Start_Point=Entry()
        self.End_Point=Entry()
        self.Value=Entry()
        self.Start_Point2=Entry()
        self.End_Point2=Entry()
        self.a=Entry()
        self.b=Entry()
        self.b1=Button(win, text='Set Value', command=self.set)
        self.b2=Button(win, text='Add Element', command=self.add)
        self.b3=Button(win, text='Draw Circuit', command=self.drawCircuit)
        self.b3.place(x=300, y=500)
        self.b4=Button(win, text='Analyze', command=self.analyze)
        self.b4.place(x=150, y=550, width=200)
        self.menubar = Menu(win)
        self.menubar.add_command(label="New", command=self.newCircuit)
        win.config(menu=self.menubar)
        self.b1.place(x=100, y=500)
        self.lbl5.place(x=100, y=50)
        data=("Resistor","Capacitor", "Inductor", "Voltage Independent Source", "Current Independent Source", "Voltage Dependent Source", "Current Dependent Source", "Wire")
        self.cb=Combobox(win, values=data)
        self.cb.place(x=200, y=50)
        self.dtype=IntVar()
        self.dtype.set(1)
        self.r1=Radiobutton(win, text="Voltage of", variable=self.dtype, value=1)
        self.r2=Radiobutton(win, text="Current of", variable=self.dtype, value=2)
        self.txt = scrolledtext.ScrolledText(win)
        self.elements = []
        self.results = []
