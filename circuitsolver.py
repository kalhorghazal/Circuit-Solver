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
