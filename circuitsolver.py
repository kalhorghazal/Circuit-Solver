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

    def solvecircuit(self):
        mycircuit = circuit()
        mycircuit.addR('R0', 0, 6, 0)
        for elem in self.elements:
            if elem.kind == "Wire":
                mycircuit.addR('R'+ elem.position, int(elem.position[0]), int(elem.position[1]), 0)

            elif elem.kind == "Resistor":
                mycircuit.addR('R'+ elem.position, int(elem.position[0]), int(elem.position[1]), elem.value)

            elif elem.kind == "Voltage Independent Source":
                mycircuit.addV('V'+ elem.position, int(elem.position[0]), int(elem.position[1]), elem.value)

            elif elem.kind == "Current Independent Source":
                mycircuit.addI('I'+ elem.position, int(elem.position[0]), int(elem.position[1]), elem.value)

            elif elem.kind == "Voltage Dependent Source":
                if elem.dtype == "V":
                    mycircuit.addVM('VM'+ elem.dposition, int(elem.dposition[0]), int(elem.dposition[1]))
                    mycircuit.addCVS('VD'+ elem.position, int(elem.position[0]), int(elem.position[1]), 'VM'+ elem.dposition, elem.a)
                else:
                    mycircuit.addIM('IM'+ elem.dposition, int(elem.dposition[0]), int(elem.dposition[1]))
                    mycircuit.addCVS('VD'+ elem.position, int(elem.position[0]), int(elem.position[1]), 'IM'+ elem.dposition, elem.a)

                if  elem.b != 0:
                    mycircuit.addV('V'+ elem.position, int(elem.position[0]), int(elem.position[1]), elem.b)

            elif elem.kind == "Current Dependent Source":
                if elem.dtype == "V":
                    mycircuit.addVM('VM'+ elem.dposition, int(elem.dposition[0]), int(elem.dposition[1]))
                    mycircuit.addCIS('VD'+ elem.position, int(elem.position[0]), int(elem.position[1]), 'VM'+ elem.dposition, elem.a)
                else:
                    mycircuit.addIM('IM'+ elem.dposition, int(elem.dposition[0]), int(elem.dposition[1]))
                    mycircuit.addCIS('VD'+ elem.position, int(elem.position[0]), int(elem.position[1]), 'IM'+ elem.dposition, elem.a)

                if  elem.b != 0:
                    mycircuit.addI('I'+ elem.position, int(elem.position[0]), int(elem.position[1]), elem.b)

            # Bonus part
            elif elem.kind == "Capacitor":
                mycircuit.addC('C'+ elem.position, int(elem.position[0]), int(elem.position[1]), elem.value)

            elif elem.kind == "Inductor":
                mycircuit.addL('L'+ elem.position, int(elem.position[0]), int(elem.position[1]), elem.value)

            self.results = mycircuit.solve()

    def circuit_is_lc(self):
        for elem in self.elements:
            if elem.kind == "Capacitor" or elem.kind == "Inductor":
                return True
        return False

    def analyze(self):
        self.b2.place(x=-100, y=-500)
        self.lbl6.place(x=-100, y=-350)
        self.lbl7.place(x=-100, y=-400)
        self.lbl1.place(x=-100, y=-350)
        self.lbl2.place(x=-100, y=-400)
        self.lbl8.place(x=-100, y=-300)
        self.r1.place(x=-100, y=-300)
        self.r2.place(x=-200, y=-300)
        self.Start_Point2.place(x=-200, y=-350)
        self.End_Point2.place(x=-200, y=-400)
        self.Start_Point.place(x=-200, y=-350)
        self.End_Point.place(x=-200, y=-400)
        self.lbl9.place(x=-100, y=-450)
        self.lbl10.place(x=230, y=-450)
        self.a.place(x=-200, y=-450, width=30)
        self.b.place(x=-300, y=-450, width=30)
        self.Value.place(x=-200, y=-200)
        self.lbl4.place(x=-100, y=-200)
        self.lbl5.place(x=-100, y=-200)
        self.cb.place(x=-100, y=-200)
        self.b1.place(x=-300, y=-500)
        self.b2.place(x=-300, y=-500)
        self.b3.place(x=-300, y=-500)
        self.b4.place(x=-300, y=-500)
        self.solvecircuit()
        for result in self.results:
            self.txt.insert(INSERT,result)
            self.txt.insert(INSERT, " = ")
            self.txt.insert(INSERT,self.results[result])
            self.txt.insert(INSERT,'\n')
            if self.circuit_is_lc():
                numer, denom = self.results[result].as_numer_denom()
                zeros = sympy.roots(numer)
                poles = sympy.roots(denom)
                self.txt.insert(INSERT, "zeros = ")
                self.txt.insert(INSERT,zeros)
                self.txt.insert(INSERT,'\n')
                self.txt.insert(INSERT, "poles = ")
                self.txt.insert(INSERT,poles)
                self.txt.insert(INSERT,'\n')
        self.txt.place(x=20, y=20)

    def newCircuit(self):
        self.cb.place(x=200, y=50)
        self.lbl5.place(x=100, y=50)
        self.b3.place(x=300, y=500)
        self.b4.place(x=150, y=550, width=200)
        self.b1.place(x=100, y=500)
        self.txt.place(x=-1000, y=-1000)
        for elem in self.elements:
            self.elements.remove(elem)
        self.b2.place(x=-100, y=-500)
        self.lbl6.place(x=-100, y=-350)
        self.lbl7.place(x=-100, y=-400)
        self.lbl1.place(x=-100, y=-350)
        self.lbl2.place(x=-100, y=-400)
        self.lbl8.place(x=-100, y=-300)
        self.r1.place(x=-100, y=-300)
        self.r2.place(x=-200, y=-300)
        self.Start_Point2.place(x=-200, y=-350)
        self.End_Point2.place(x=-200, y=-400)
        self.Start_Point.place(x=-200, y=-350)
        self.End_Point.place(x=-200, y=-400)
        self.lbl9.place(x=-100, y=-450)
        self.lbl10.place(x=230, y=-450)
        self.a.place(x=-200, y=-450, width=30)
        self.b.place(x=-300, y=-450, width=30)
        self.Value.place(x=-200, y=-200)
        self.lbl4.place(x=-100, y=-200)

    def set(self):
        self.cb.place(x=200, y=50)
        self.lbl5.place(x=100, y=50)
        self.b3.place(x=300, y=500)
        self.b4.place(x=150, y=550, width=200)
        self.b1.place(x=100, y=500)
        self.txt.place(x=-1000, y=-1000)
        self.b2.place(x=-100, y=-500)
        self.lbl6.place(x=-100, y=-350)
        self.lbl7.place(x=-100, y=-400)
        self.lbl1.place(x=-100, y=-350)
        self.lbl2.place(x=-100, y=-400)
        self.lbl8.place(x=-100, y=-300)
        self.r1.place(x=-100, y=-300)
        self.r2.place(x=-200, y=-300)
        self.Start_Point2.place(x=-200, y=-350)
        self.End_Point2.place(x=-200, y=-400)
        self.Start_Point.place(x=-200, y=-350)
        self.End_Point.place(x=-200, y=-400)
        self.lbl9.place(x=-100, y=-450)
        self.lbl10.place(x=230, y=-450)
        self.a.place(x=-200, y=-450, width=30)
        self.b.place(x=-300, y=-450, width=30)
        self.Value.place(x=-200, y=-200)
        self.lbl4.place(x=-100, y=-200)

        self.Start_Point.delete(0, 'end')
        self.End_Point.delete(0, 'end')
        self.Start_Point2.delete(0, 'end')
        self.End_Point2.delete(0, 'end')
        self.Value.delete(0, 'end')
        self.a.delete(0, 'end')
        self.b.delete(0, 'end')

        kind = self.cb.get()
        self.lbl1.place(x=100, y=100)
        self.Start_Point.place(x=200, y=100)
        self.lbl2.place(x=100, y=150)
        self.End_Point.place(x=200, y=150)
        self.b2.place(x=200, y=500)


        if (kind == 'Voltage Dependent Source' or kind == 'Current Dependent Source'):
            self.lbl6.place(x=100, y=350)
            self.lbl7.place(x=100, y=400)
            self.lbl8.place(x=100, y=250)
            self.r1.place(x=100, y=300)
            self.r2.place(x=200, y=300)
            self.Start_Point2.place(x=200, y=350)
            self.End_Point2.place(x=200, y=400)
            self.lbl9.place(x=100, y=450)
            self.lbl10.place(x=230, y=450)
            self.a.place(x=200, y=450, width=30)
            self.b.place(x=270, y=450, width=30)

        elif (kind == "Resistor" or kind == "Voltage Independent Source" or kind == "Current Independent Source" or kind == "Capacitor" or kind == "Inductor"):
            self.Value.place(x=200, y=200)
            self.lbl4.place(x=100, y=200)

    def add(self):
        self.b2.place(x=-100, y=-500)
        self.lbl6.place(x=-100, y=-350)
        self.lbl7.place(x=-100, y=-400)
        self.lbl1.place(x=-100, y=-350)
        self.lbl2.place(x=-100, y=-400)
        self.lbl8.place(x=-100, y=-300)
        self.r1.place(x=-100, y=-300)
        self.r2.place(x=-200, y=-300)
        self.Start_Point2.place(x=-200, y=-350)
        self.End_Point2.place(x=-200, y=-400)
        self.Start_Point.place(x=-200, y=-350)
        self.End_Point.place(x=-200, y=-400)
        self.lbl9.place(x=-100, y=-450)
        self.lbl10.place(x=230, y=-450)
        self.a.place(x=-200, y=-450, width=30)
        self.b.place(x=-300, y=-450, width=30)
        self.Value.place(x=-200, y=-200)
        self.lbl4.place(x=-100, y=-200)

        sp = self.Start_Point.get()
        ep = self.End_Point.get()
        position = sp + ep
        kind = self.cb.get()
        if (kind == 'Voltage Dependent Source' or kind == 'Current Dependent Source'):
            sp2 = self.Start_Point2.get()
            ep2 = self.End_Point2.get()
            position2 = sp2+ep2
            dtype = self.dtype.get()
            if dtype == 1:
                dtype = 'V'
            else:
                dtype = 'I'
            a = int(self.a.get())
            b = int(self.b.get())
            elem = element(kind, position, 0, position2, dtype, a, b)
        elif (kind == "Resistor" or kind == "Voltage Independent Source" or kind == "Current Independent Source" or kind == "Capacitor" or kind == "Inductor"):
            value = int(self.Value.get())
            elem = element(kind, position, value)
        else:
            elem = element(kind, position)
        self.elements.append(elem)
