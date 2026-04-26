from PyQt5 import QtWidgets
import PyQt5 


def set_labels(self):
    """Add all the labels"""
#    label2formula(self,"Hoppings","hopping")
#    label2formula(self,"Fermi energy","fermi")
#    replace(self,"Hoppings","Hoppings t_{ij}")
#    replace(self,"Fermi energy","Fermi energy \epsilon_{i}")
#    replace(self,"Exchange field","Exchange field (J_x,J_y,J_z)")
    # this should be finished




def replace(self,a,b):
    """Given a certain label a, replace it be the label b"""
    obs = dir(self)
    name = None
    for obj in obs: # loop over objects
        o = getattr(self,obj) # get this object
        if type(o)==QtWidgets.QLabel: # line object
            name = o.text() # save this info
            if name==a: # if this is the string
              o.setText(b) # set the new text
              return

def get_label_from_text(self,text):
    """Return a certain label object form its text"""
    obs = dir(self)
    name = None
    for obj in obs: # loop over objects
        o = getattr(self,obj) # get this object
        if type(o)==QtWidgets.QLabel: # line object
            name = o.text() # save this info
            if name==text: # if this is the string
                return o
    return None




