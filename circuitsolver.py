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

    def drawCircuit(self):
        d = schem.Drawing(unit=2, fontsize=12, font='monospace')
        d1 = d.add(e.DOT)
        l12 = d.add(e.LINE, d='down', xy = d1.end, color='white')
        d2 = d.add(e.DOT, xy = l12.end)
        l23 = d.add(e.LINE, d='down', xy = d2.end, color='white')
        d3 = d.add(e.DOT, xy = l23.end)
        l14 = d.add(e.LINE, d='right', xy = d1.end, color='white')
        d4 = d.add(e.DOT, xy = l14.end)
        l45 = d.add(e.LINE, d='down', xy = d4.end, color='white')
        d5 = d.add(e.DOT, xy = l45.end)
        l56 = d.add(e.LINE, d='down', xy = d5.end, color='white')
        d6 = d.add(e.DOT, xy = l56.end)
        l47 = d.add(e.LINE, d='right', xy = d4.end, color='white')
        d7 = d.add(e.DOT, xy = l47.end)
        l78 = d.add(e.LINE, d='down', xy = d7.end, color='white')
        d8 = d.add(e.DOT, xy = l78.end)
        l89 = d.add(e.LINE, d='down', xy = d8.end, color='white')
        d9 = d.add(e.DOT, xy = l89.end)
        l25 = d.add(e.LINE, d='right', xy = d2.end, color='white')
        l58 = d.add(e.LINE, d='right', xy = d5.end, color='white')
        l36 = d.add(e.LINE, d='right', xy = d3.end, color='white')
        l69 = d.add(e.LINE, d='right', xy = d6.end, color='white')
        gnd = d.add(e.GND, d='right', xy = l56.end, color='black')

        for elem in self.elements:
            if elem.position == '12':
                if (elem.kind == 'Resistor'):
                    R1 = d.add(e.RES, d='down', label=str(elem.value)+'$\Omega$', xy = l12.start)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='down', label=str(elem.value)+'F', xy = l12.start)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='down', label=str(elem.value)+'H', xy = l12.start)
                elif (elem.kind == 'Voltage Independent Source'):
                    S1 = d.add(e.SOURCE_V, d='down', label=str(elem.value)+'V', xy = l12.start)
                elif (elem.kind == 'Current Independent Source'):
                    S1 = d.add(e.SOURCE_I, d='down', label=str(elem.value)+'A', xy = l12.start)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S1 = d.add(e.SOURCE_CONT_V, d='down', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l12.start)
                elif (elem.kind == 'Current Dependent Source'):
                    S1 = d.add(e.SOURCE_CONT_I, d='down', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l12.start)
                l12.color = 'none'
                if (elem.kind == 'Wire'):
                    l12.color = 'black'
            if elem.position == '21':
                if (elem.kind == 'Resistor'):
                    R1 = d.add(e.RES, d='up', label=str(elem.value)+'$\Omega$', xy = l12.end)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='up', label=str(elem.value)+'F', xy = l12.end)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='up', label=str(elem.value)+'H', xy = l12.end)
                elif (elem.kind == 'Voltage Independent Source'):
                    S1 = d.add(e.SOURCE_V, d='up', label=str(elem.value)+'V', xy = l12.end)
                elif (elem.kind == 'Current Independent Source'):
                    S1 = d.add(e.SOURCE_I, d='up', label=str(elem.value)+'A', xy = l12.end)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S1 = d.add(e.SOURCE_CONT_V, d='up', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l12.end)
                elif (elem.kind == 'Current Dependent Source'):
                    S1 = d.add(e.SOURCE_CONT_I, d='up', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l12.end)
                l12.color = 'none'
                if (elem.kind == 'Wire'):
                    l12.color = 'black'
            elif elem.position == '23':
                if (elem.kind == 'Resistor'):
                    R2 = d.add(e.RES, d='down', label=str(elem.value)+'$\Omega$', xy = l23.start)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='down', label=str(elem.value)+'F', xy = l23.start)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='down', label=str(elem.value)+'H', xy = l23.start)
                elif (elem.kind == 'Voltage Independent Source'):
                    S2 = d.add(e.SOURCE_V, d='down', label=str(elem.value)+'V', xy = l23.start)
                elif (elem.kind == 'Current Independent Source'):
                    S2 = d.add(e.SOURCE_I, d='down', label=str(elem.value)+'A', xy = l23.start)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S2 = d.add(e.SOURCE_CONT_V, d='down', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l23.start)
                elif (elem.kind == 'Current Dependent Source'):
                    S2 = d.add(e.SOURCE_CONT_I, d='down', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l23.start)
                l23.color = 'none'
                if (elem.kind == 'Wire'):
                    l23.color = 'black'
            elif elem.position == '32':
                if (elem.kind == 'Resistor'):
                    R2 = d.add(e.RES, d='up', label=str(elem.value)+'$\Omega$', xy = l23.end)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='up', label=str(elem.value)+'F', xy = l23.end)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='up', label=str(elem.value)+'H', xy = l23.end)
                elif (elem.kind == 'Voltage Independent Source'):
                    S2 = d.add(e.SOURCE_V, d='up', label=str(elem.value)+'V', xy = l23.end)
                elif (elem.kind == 'Current Independent Source'):
                    S2 = d.add(e.SOURCE_I, d='up', label=str(elem.value)+'A', xy = l23.end)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S2 = d.add(e.SOURCE_CONT_V, d='up', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l23.end)
                elif (elem.kind == 'Current Dependent Source'):
                    S2 = d.add(e.SOURCE_CONT_I, d='up', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l23.end)
                l23.color = 'none'
                if (elem.kind == 'Wire'):
                    l23.color = 'black'
            elif elem.position == '58':
                if (elem.kind == 'Resistor'):
                    R3 = d.add(e.RES, d='right', label=str(elem.value)+'$\Omega$', xy = l58.start)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='right', label=str(elem.value)+'F', xy = l58.start)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='right', label=str(elem.value)+'H', xy = l58.start)
                elif (elem.kind == 'Voltage Independent Source'):
                    S3 = d.add(e.SOURCE_V, d='right', label=str(elem.value)+'V', xy = l58.start)
                elif (elem.kind == 'Current Independent Source'):
                    S3 = d.add(e.SOURCE_I, d='right', label=str(elem.value)+'A', xy = l58.start)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S3 = d.add(e.SOURCE_CONT_V, d='right', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l58.start)
                elif (elem.kind == 'Current Dependent Source'):
                    S3 = d.add(e.SOURCE_CONT_I, d='right', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l58.start)
                l58.color = 'none'
                if (elem.kind == 'Wire'):
                    l58.color = 'black'
            elif elem.position == '85':
                if (elem.kind == 'Resistor'):
                    R3 = d.add(e.RES, d='left', label=str(elem.value)+'$\Omega$', xy = l58.end)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='left', label=str(elem.value)+'F', xy = l58.end)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='left', label=str(elem.value)+'H', xy = l58.end)
                elif (elem.kind == 'Voltage Independent Source'):
                    S3 = d.add(e.SOURCE_V, d='left', label=str(elem.value)+'V', xy = l58.end)
                elif (elem.kind == 'Current Independent Source'):
                    S3 = d.add(e.SOURCE_I, d='left', label=str(elem.value)+'A', xy = l58.end)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S3 = d.add(e.SOURCE_CONT_V, d='left', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l58.end)
                elif (elem.kind == 'Current Dependent Source'):
                    S3 = d.add(e.SOURCE_CONT_I, d='left', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l58.end)
                l58.color = 'none'
                if (elem.kind == 'Wire'):
                    l58.color = 'black'
            elif elem.position == '14':
                if (elem.kind == 'Resistor'):
                    R4 = d.add(e.RES, d='right', label=str(elem.value)+'$\Omega$', xy = l14.start)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='right', label=str(elem.value)+'F', xy = l14.start)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='right', label=str(elem.value)+'H', xy = l14.start)
                elif (elem.kind == 'Voltage Independent Source'):
                    S4 = d.add(e.SOURCE_V, d='right', label=str(elem.value)+'V', xy = l14.start)
                elif (elem.kind == 'Current Independent Source'):
                    S4 = d.add(e.SOURCE_I, d='right', label=str(elem.value)+'A', xy = l14.start)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S4 = d.add(e.SOURCE_CONT_V, d='right', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l14.start)
                elif (elem.kind == 'Current Dependent Source'):
                    S4 = d.add(e.SOURCE_CONT_I, d='right', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l14.start)
                l14.color = 'none'
                if (elem.kind == 'Wire'):
                    l14.color = 'black'
            elif elem.position == '41':
                if (elem.kind == 'Resistor'):
                    R4 = d.add(e.RES, d='left', label=str(elem.value)+'$\Omega$', xy = l14.end)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='left', label=str(elem.value)+'F', xy = l14.end)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='left', label=str(elem.value)+'H', xy = l14.end)
                elif (elem.kind == 'Voltage Independent Source'):
                    S4 = d.add(e.SOURCE_V, d='left', label=str(elem.value)+'V', xy = l14.end)
                elif (elem.kind == 'Current Independent Source'):
                    S4 = d.add(e.SOURCE_I, d='left', label=str(elem.value)+'A', xy = l14.end)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S4 = d.add(e.SOURCE_CONT_V, d='left', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l14.end)
                elif (elem.kind == 'Current Dependent Source'):
                    S4 = d.add(e.SOURCE_CONT_I, d='left', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l14.end)
                l14.color = 'none'
                if (elem.kind == 'Wire'):
                    l14.color = 'black'
            elif elem.position == '47':
                if (elem.kind == 'Resistor'):
                    R5 = d.add(e.RES, d='right', label=str(elem.value)+'$\Omega$', xy = l47.start)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='right', label=str(elem.value)+'F', xy = l47.start)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='right', label=str(elem.value)+'H', xy = l47.start)
                elif (elem.kind == 'Voltage Independent Source'):
                    S5 = d.add(e.SOURCE_V, d='right', label=str(elem.value)+'V', xy = l47.start)
                elif (elem.kind == 'Current Independent Source'):
                    S5 = d.add(e.SOURCE_I, d='right', label=str(elem.value)+'A', xy = l47.start)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S5 = d.add(e.SOURCE_CONT_V, d='right', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l47.start)
                elif (elem.kind == 'Current Dependent Source'):
                    S5 = d.add(e.SOURCE_CONT_I, d='right', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l47.start)
                l47.color = 'none'
                if (elem.kind == 'Wire'):
                    l47.color = 'black'
            elif elem.position == '74':
                if (elem.kind == 'Resistor'):
                    R5 = d.add(e.RES, d='left', label=str(elem.value)+'$\Omega$', xy = l47.end)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='left', label=str(elem.value)+'F', xy = l47.end)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='left', label=str(elem.value)+'H', xy = l47.end)
                elif (elem.kind == 'Voltage Independent Source'):
                    S5 = d.add(e.SOURCE_V, d='left', label=str(elem.value)+'V', xy = l47.end)
                elif (elem.kind == 'Current Independent Source'):
                    S5 = d.add(e.SOURCE_I, d='left', label=str(elem.value)+'A', xy = l47.end)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S5 = d.add(e.SOURCE_CONT_V, d='left', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l47.end)
                elif (elem.kind == 'Current Dependent Source'):
                    S5 = d.add(e.SOURCE_CONT_I, d='left', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l47.end)
                l47.color = 'none'
                if (elem.kind == 'Wire'):
                    l47.color = 'black'
            elif elem.position == '45':
                if (elem.kind == 'Resistor'):
                    R6 = d.add(e.RES, d='down', label=str(elem.value)+'$\Omega$', xy = l45.start)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='down', label=str(elem.value)+'F', xy = l45.start)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='down', label=str(elem.value)+'H', xy = l45.start)
                elif (elem.kind == 'Voltage Independent Source'):
                    S6 = d.add(e.SOURCE_V, d='down', label=str(elem.value)+'V', xy = l45.start)
                elif (elem.kind == 'Current Independent Source'):
                    S6 = d.add(e.SOURCE_I, d='down', label=str(elem.value)+'A', xy = l45.start)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S6 = d.add(e.SOURCE_CONT_V, d='down', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l45.start)
                elif (elem.kind == 'Current Dependent Source'):
                    S6 = d.add(e.SOURCE_CONT_I, d='down', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l45.start)
                l45.color = 'none'
                if (elem.kind == 'Wire'):
                    l45.color = 'black'
            elif elem.position == '54':
                if (elem.kind == 'Resistor'):
                    R6 = d.add(e.RES, d='up', label=str(elem.value)+'$\Omega$', xy = l45.end)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='up', label=str(elem.value)+'F', xy = l45.end)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='up', label=str(elem.value)+'H', xy = l45.end)
                elif (elem.kind == 'Voltage Independent Source'):
                    S6 = d.add(e.SOURCE_V, d='up', label=str(elem.value)+'V', xy = l45.end)
                elif (elem.kind == 'Current Independent Source'):
                    S6 = d.add(e.SOURCE_I, d='up', label=str(elem.value)+'A', xy = l45.end)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S6 = d.add(e.SOURCE_CONT_V, d='up', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l45.end)
                elif (elem.kind == 'Current Dependent Source'):
                    S6 = d.add(e.SOURCE_CONT_I, d='up', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l45.end)
                l45.color = 'none'
                if (elem.kind == 'Wire'):
                    l45.color = 'black'
            elif elem.position == '56':
                if (elem.kind == 'Resistor'):
                    R7 = d.add(e.RES, d='down', label=str(elem.value)+'$\Omega$', xy = l56.start)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='down', label=str(elem.value)+'F', xy = l56.start)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='down', label=str(elem.value)+'H', xy = l56.start)
                elif (elem.kind == 'Voltage Independent Source'):
                    S7 = d.add(e.SOURCE_V, d='down', label=str(elem.value)+'V', xy = l56.start)
                elif (elem.kind == 'Current Independent Source'):
                    S7 = d.add(e.SOURCE_I, d='down', label=str(elem.value)+'A', xy = l56.start)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S7 = d.add(e.SOURCE_CONT_V, d='down', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l56.start)
                elif (elem.kind == 'Current Dependent Source'):
                    S7 = d.add(e.SOURCE_CONT_I, d='down', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l56.start)
                l56.color = 'none'
                if (elem.kind == 'Wire'):
                    l56.color = 'black'
            elif elem.position == '65':
                if (elem.kind == 'Resistor'):
                    R7 = d.add(e.RES, d='up', label=str(elem.value)+'$\Omega$', xy = l56.end)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='up', label=str(elem.value)+'F', xy = l56.end)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='up', label=str(elem.value)+'H', xy = l56.end)
                elif (elem.kind == 'Voltage Independent Source'):
                    S7 = d.add(e.SOURCE_V, d='up', label=str(elem.value)+'V', xy = l56.end)
                elif (elem.kind == 'Current Independent Source'):
                    S7 = d.add(e.SOURCE_I, d='up', label=str(elem.value)+'A', xy = l56.end)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S7 = d.add(e.SOURCE_CONT_V, d='up', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l56.end)
                elif (elem.kind == 'Current Dependent Source'):
                    S7 = d.add(e.SOURCE_CONT_I, d='up', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l56.end)
                l56.color = 'none'
                if (elem.kind == 'Wire'):
                    l56.color = 'black'
            elif elem.position == '78':
                if (elem.kind == 'Resistor'):
                    R8 = d.add(e.RES, d='down', label=str(elem.value)+'$\Omega$', xy = l78.start)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='down', label=str(elem.value)+'F', xy = l78.start)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='down', label=str(elem.value)+'H', xy = l78.start)
                elif (elem.kind == 'Voltage Independent Source'):
                    S8 = d.add(e.SOURCE_V, d='down', label=str(elem.value)+'V', xy = l78.start)
                elif (elem.kind == 'Current Independent Source'):
                    S8 = d.add(e.SOURCE_I, d='down', label=str(elem.value)+'A', xy = l78.start)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S8 = d.add(e.SOURCE_CONT_V, d='down', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l78.start)
                elif (elem.kind == 'Current Dependent Source'):
                    S8 = d.add(e.SOURCE_CONT_I, d='down', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l78.start)
                l78.color = 'none'
                if (elem.kind == 'Wire'):
                    l78.color = 'black'
            elif elem.position == '87':
                if (elem.kind == 'Resistor'):
                    R8 = d.add(e.RES, d='up', label=str(elem.value)+'$\Omega$', xy = l78.end)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='up', label=str(elem.value)+'F', xy = l78.end)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='up', label=str(elem.value)+'H', xy = l78.end)
                elif (elem.kind == 'Voltage Independent Source'):
                    S8 = d.add(e.SOURCE_V, d='up', label=str(elem.value)+'V', xy = l78.end)
                elif (elem.kind == 'Current Independent Source'):
                    S8 = d.add(e.SOURCE_I, d='up', label=str(elem.value)+'A', xy = l78.end)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S8 = d.add(e.SOURCE_CONT_V, d='up', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l78.end)
                elif (elem.kind == 'Current Dependent Source'):
                    S8 = d.add(e.SOURCE_CONT_I, d='up', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l78.end)
                l78.color = 'none'
                if (elem.kind == 'Wire'):
                    l78.color = 'black'
            elif elem.position == '36':
                if (elem.kind == 'Resistor'):
                    R9 = d.add(e.RES, d='right', label=str(elem.value)+'$\Omega$', xy = l36.start)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='right', label=str(elem.value)+'F', xy = l36.start)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='right', label=str(elem.value)+'H', xy = l36.start)
                elif (elem.kind == 'Voltage Independent Source'):
                    S9 = d.add(e.SOURCE_V, d='right', label=str(elem.value)+'V', xy = l36.start)
                elif (elem.kind == 'Current Independent Source'):
                    S9 = d.add(e.SOURCE_I, d='right', label=str(elem.value)+'A', xy = l36.start)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S9 = d.add(e.SOURCE_CONT_V, d='right', label=str(elem.value)+'V', xy = l36.start)
                elif (elem.kind == 'Current Dependent Source'):
                    S9 = d.add(e.SOURCE_CONT_I, d='right', label=str(elem.value)+'A', xy = l36.start)
                l36.color = 'none'
                if (elem.kind == 'Wire'):
                    l36.color = 'black'
            elif elem.position == '63':
                if (elem.kind == 'Resistor'):
                    R9 = d.add(e.RES, d='left', label=str(elem.value)+'$\Omega$', xy = l36.end)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='left', label=str(elem.value)+'F', xy = l36.end)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='left', label=str(elem.value)+'H', xy = l36.end)
                elif (elem.kind == 'Voltage Independent Source'):
                    S9 = d.add(e.SOURCE_V, d='left', label=str(elem.value)+'V', xy = l36.end)
                elif (elem.kind == 'Current Independent Source'):
                    S9 = d.add(e.SOURCE_I, d='left', label=str(elem.value)+'A', xy = l36.end)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S9 = d.add(e.SOURCE_CONT_V, d='left', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l36.end)
                elif (elem.kind == 'Current Dependent Source'):
                    S9 = d.add(e.SOURCE_CONT_I, d='left', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l36.end)
                l36.color = 'none'
                if (elem.kind == 'Wire'):
                    l36.color = 'black'
            elif elem.position == '69':
                if (elem.kind == 'Resistor'):
                    R10 = d.add(e.RES, d='right', label=str(elem.value)+'$\Omega$', xy = l69.start)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='right', label=str(elem.value)+'F', xy = l69.start)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='right', label=str(elem.value)+'H', xy = l69.start)
                elif (elem.kind == 'Voltage Independent Source'):
                    S10 = d.add(e.SOURCE_V, d='right', label=str(elem.value)+'V', xy = l69.start)
                elif (elem.kind == 'Current Independent Source'):
                    S10 = d.add(e.SOURCE_I, d='right', label=str(elem.value)+'A', xy = l69.start)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S10 = d.add(e.SOURCE_CONT_V, d='right', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l69.start)
                elif (elem.kind == 'Current Dependent Source'):
                    S10 = d.add(e.SOURCE_CONT_I, d='right', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l69.start)
                l69.color = 'none'
                if (elem.kind == 'Wire'):
                    l69.color = 'black'
            elif elem.position == '96':
                if (elem.kind == 'Resistor'):
                    R10 = d.add(e.RES, d='left', label=str(elem.value)+'$\Omega$', xy = l69.end)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='left', label=str(elem.value)+'F', xy = l69.end)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='left', label=str(elem.value)+'H', xy = l69.end)
                elif (elem.kind == 'Voltage Independent Source'):
                    S10 = d.add(e.SOURCE_V, d='left', label=str(elem.value)+'V', xy = l69.end)
                elif (elem.kind == 'Current Independent Source'):
                    S10 = d.add(e.SOURCE_I, d='left', label=str(elem.value)+'A', xy = l69.end)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S10 = d.add(e.SOURCE_CONT_V, d='left', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l69.end)
                elif (elem.kind == 'Current Dependent Source'):
                    S10 = d.add(e.SOURCE_CONT_I, d='left', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l69.end)
                l69.color = 'none'
                if (elem.kind == 'Wire'):
                    l69.color = 'black'
            elif elem.position == '89':
                if (elem.kind == 'Resistor'):
                    R11 = d.add(e.RES, d='down', label=str(elem.value)+'$\Omega$', xy = l89.start)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='down', label=str(elem.value)+'F', xy = l89.start)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='down', label=str(elem.value)+'H', xy = l89.start)
                elif (elem.kind == 'Voltage Independent Source'):
                    S11 = d.add(e.SOURCE_V, d='down', label=str(elem.value)+'V', xy = l89.start)
                elif (elem.kind == 'Current Independent Source'):
                    S11 = d.add(e.SOURCE_I, d='down', label=str(elem.value)+'A', xy = l89.start)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S11 = d.add(e.SOURCE_CONT_V, d='down', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l89.start)
                elif (elem.kind == 'Current Dependent Source'):
                    S11 = d.add(e.SOURCE_CONT_I, d='down', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l89.start)
                l89.color = 'none'
                if (elem.kind == 'Wire'):
                    l89.color = 'black'
            elif elem.position == '98':
                if (elem.kind == 'Resistor'):
                    R11 = d.add(e.RES, d='up', label=str(elem.value)+'$\Omega$', xy = l89.end)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='up', label=str(elem.value)+'F', xy = l89.end)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='up', label=str(elem.value)+'H', xy = l89.end)
                elif (elem.kind == 'Voltage Independent Source'):
                    S11 = d.add(e.SOURCE_V, d='up', label=str(elem.value)+'V', xy = l89.end)
                elif (elem.kind == 'Current Independent Source'):
                    S11 = d.add(e.SOURCE_I, d='up', label=str(elem.value)+'A', xy = l89.end)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S11 = d.add(e.SOURCE_CONT_V, d='up', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l89.end)
                elif (elem.kind == 'Current Dependent Source'):
                    S11 = d.add(e.SOURCE_CONT_I, d='up', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l89.end)
                l89.color = 'none'
                if (elem.kind == 'Wire'):
                    l89.color = 'black'
            elif elem.position == '25':
                if (elem.kind == 'Resistor'):
                    R12 = d.add(e.RES, d='right', label=str(elem.value)+'$\Omega$', xy = l25.start)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='right', label=str(elem.value)+'F', xy = l25.start)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='right', label=str(elem.value)+'H', xy = l25.start)
                elif (elem.kind == 'Voltage Independent Source'):
                    S12 = d.add(e.SOURCE_V, d='right', label=str(elem.value)+'V', xy = l25.start)
                elif (elem.kind == 'Current Independent Source'):
                    S12 = d.add(e.SOURCE_I, d='right', label=str(elem.value)+'A', xy = l25.start)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S12 = d.add(e.SOURCE_CONT_V, d='right', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l25.start)
                elif (elem.kind == 'Current Dependent Source'):
                    S12 = d.add(e.SOURCE_CONT_I, d='right', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l25.start)
                l25.color = 'none'
                if (elem.kind == 'Wire'):
                    l25.color = 'black'
            elif elem.position == '52':
                if (elem.kind == 'Resistor'):
                    R12 = d.add(e.RES, d='left', label=str(elem.value)+'$\Omega$', xy = l25.end)
                elif (elem.kind == 'Capacitor'):
                    R1 = d.add(e.CAP, d='left', label=str(elem.value)+'F', xy = l25.end)
                elif (elem.kind == 'Inductor'):
                    R1 = d.add(e.INDUCTOR, d='left', label=str(elem.value)+'H', xy = l25.end)
                elif (elem.kind == 'Voltage Independent Source'):
                    S12 = d.add(e.SOURCE_V, d='left', label=str(elem.value)+'V', xy = l25.end)
                elif (elem.kind == 'Current Independent Source'):
                    S12 = d.add(e.SOURCE_I, d='left', label=str(elem.value)+'A', xy = l25.end)
                elif (elem.kind == 'Voltage Dependent Source'):
                    S12 = d.add(e.SOURCE_CONT_V, d='left', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l25.end)
                elif (elem.kind == 'Current Dependent Source'):
                    S12 = d.add(e.SOURCE_CONT_I, d='left', label=str(elem.a)+elem.dtype+elem.dposition+' + '+str(elem.b), xy = l25.end)
                l25.color = 'none'
                if (elem.kind == 'Wire'):
                    l25.color = 'black'
        d.draw()


verbose = False

class circuitEx(Exception):
    def __init__(self, msg=""):
        print('**')
        print('** Circuit exception')
        print('**')
        print('** ' + msg)
        print('**')
        print("\n")

s = sympy.Symbol('s')

# TODO: circuit class implementation

if __name__ == "__main__":
    window = Tk()
    mywin = MyWindow(window)
    window.title('Circuit Solver')
    window.geometry("400x600+10+10")
    window.mainloop()
    elements = mywin.elements
