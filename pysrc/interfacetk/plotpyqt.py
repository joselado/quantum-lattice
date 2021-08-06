#!/usr/bin/python

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import sys

from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QSlider
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random

def get_interface(plot_figure,i=0):
    """Return an object that plots stuff"""
    class Window(QDialog):
        def __init__(self, parent=None):
            super(Window, self).__init__(parent)
            self.figure = plt.figure(i)
            # this is the Canvas Widget that displays the `figure`
            # it takes the `figure` instance as a parameter to __init__
            self.canvas = FigureCanvas(self.figure)
#            self.button = QPushButton('Plot')
#            self.button.clicked.connect(self.plot)
            # set the layout
            layout = QGridLayout()
            self.row = 1
            self.column = 0
            self.layout = layout
            self._dynamic_ax = self.canvas.figure.subplots()
            self.layout.addWidget(self.canvas, 1,0,1,0)
            self.setLayout(layout)
        def plot(self):
            '''Plot the figure'''
            # instead of ax.hold(False)
            self._dynamic_ax.clear()
            self.figure.clear()
#            self.layout.removeWidget(self.canvas)
            fig = plot_figure(self) # get that figure
            plt.tight_layout(h_pad=0.1,w_pad=0.1) # adjust axis
            if fig.number!=self.figure.number: 
                print("You must plot in the same figure as the one initialized for the interface, use fig = plt.figure(obj.figure.number) in your function, where obj is the input of your function")
                exit()
            self._dynamic_ax.figure.canvas.draw()
#            self.canvas = FigureCanvas(self.figure)
#            self.toolbar = NavigationToolbar(self.canvas, self)
            # refresh canvas
#            self.canvas = FigureCanvas(self.figure)
            # add the new canvas at the position of the old one
#            self.layout.addWidget(self.toolbar,0,0,1,0)
#            self.layout.addWidget(self.canvas, 1,0,1,0)
#            self.setLayout(self.layout)
#            self.canvas.draw()
        def add_combobox(self,cs,label=None,key=None):
            """Add a combo box"""
            if key is None: 
                if label is None: raise
                key=label
            combo = QtWidgets.QComboBox(objectName=key)
            combo.addItems(cs)
            combo.currentTextChanged.connect(self.plot)
            self.row += 1 # increase
            if label is not None: # empty string
              lb = QtWidgets.QLabel(label)
              self.layout.addWidget(lb,self.row,0)
              self.layout.addWidget(combo,self.row,1)
              self.column += 2 # increase counter
            else:
              self.layout.addWidget(combo,self.row,1,1,0)
              self.column += 1 # increase counter
        def get_combobox(self,name):
            """Get the value of a combobox"""
            obj = self.findChild(QtWidgets.QComboBox,name)
            return obj.currentText()
        def add_slider(self,key=None,
                label=None,vs=range(100),v0=None,
                next_row=True):
            """Add a slider"""
            vs = np.array(vs) # set as array
            if key is None: 
                if label is None: raise
                key = label
            slider = QSlider(Qt.Horizontal,objectName=key)
            slider.vs = vs # store
            slider.setMinimum(0) # minimum value
            slider.setMaximum(len(vs)) # maximum value
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setTickInterval(1)
            if v0 is None: v0 = min(vs) # not provided
            dd = np.abs(vs-v0) # difference
            ii = [y for (x,y) in sorted(zip(dd,range(len(dd))))][0]
            slider.setValue(ii) # initial value
            slider.valueChanged.connect(self.plot)
            if next_row: 
                self.column = 0 # start a new column
                self.row += 1 # increase counter
            if label is not None:
              lb = QtWidgets.QLabel(label) # label object
              self.layout.addWidget(lb,self.row,self.column)
              self.layout.addWidget(slider,self.row,self.column+1,1,1)
              self.column += 2 # increase counter
            else:
              self.layout.addWidget(slider,self.row,0,1,0)
              self.column += 1 # increase counter
            self.setLayout(self.layout)
        def get_slider(self,name):
            """Get the value of a slider"""
            slider = self.findChild(QSlider,name)
            out = int(slider.value())
            if out>=len(slider.vs): out = len(slider.vs) -1
            return slider.vs[int(out)]
        def add_text(self,key=None,label=None,text=""):
            """Add a text label"""
            le = QtWidgets.QLineEdit(objectName=key)
            le.editingFinished.connect(self.plot) # plot the new figure
            le.setText(str(text))
            self.row += 1 # increase counter
            if label is not None:
              lb = QtWidgets.QLabel(label)
              self.layout.addWidget(lb,self.row,0)
              self.layout.addWidget(le,self.row,1)
              self.column += 2 # increase counter
            else:
              self.layout.addWidget(le,self.row,-1)
              self.column += 1 # increase counter
            self.setLayout(self.layout)
        def get_text(self,name):
            le = self.findChild(QtWidgets.QLineEdit,name)
            return le.text() # return text


    app = QApplication(sys.argv)
    main = Window()
    return app,main








if __name__ == '__main__':
    def funfig(obj): # dummy function
        xs = np.linspace(0.,10.,300) # xgrid
        # get the value of the slider
        ys = np.cos(xs*obj.get_slider("k") + obj.get_slider("phi")) 
        ys = ys + float(obj.get_text("dy")) # shift the values
        fig = plt.figure(obj.figure.number) # initialize figure
        fig.clear()
        plt.plot(xs,ys,c=obj.get_combobox("c")) # plot data
        plt.ylim([-2,2])
        return fig # return figure
    app,main = get_interface(funfig) # get the interface
    ks = np.linspace(1.0,3.0,50) # wavevectors
    ps = np.linspace(0.0,2.0,50)*np.pi # phases
    main.add_slider(label="Wavevector",key="k",vs=ks) # initialize the slider
    main.add_slider(label="Phi",key="phi",vs=ps) # initialize the slider
    main.add_text(label="Shift",key="dy",text="0.0") # initialize the slider
    # initialize the combobox
    main.add_combobox(["red","blue","black"],label="Color",key="c") 
    main.plot()
    main.show()
    sys.exit(app.exec_())
