# Circuit Solver

A software for visualizing and solving electrical circuits, written in Python

## Getting Started

These instructions help you run this software on your local machine.

### Prerequisites

* pygraphics
* schemDraw
* matplotlib
* numpy

### Installing

Assuming you have pip installed on your computer, run this command in the command line(in the project folder):

```
pip install -r requirements.txt
```

## Using the Software

Double click on the **circuitsolver.py** file, or run this command in the command line:

```
python circuitsolver.py
```
The circuit is a 3x3 board(9 points). The point numbering is column-wise and starting from top-left.
1. In the _Type_ drop-down menu, choose the type of the element you want to add to the circuit.
2. Using the _Set Value_ button, choose the start point, end point, and the value of the element.
3. If the element is a dependent one, set the dependency info in the corresponding fields.
4. You can add the element to the circuit by clicking on the _Add Element_ button.
5. You can view the circuit in any of the steps using _Draw Circuit_ button.
6. To analyze the circuit, simply click on the _Analyze_ button.
7. To make a new circuit, click on the _New_ option in the top toolbar.

## Built With

* [Tkinter](https://github.com/python/cpython/tree/3.8/Lib/tkinter) - The graphical library
* [Sympy](https://www.sympy.org/en/index.html) - The algebra library

## Developers

* [**Mobina Shahbandeh**](https://github.com/mobinashb)
* [**Ghazal Kalhor**](https://github.com/kalhorghazal)

