from PyQt5 import QtWidgets

# use more sophisticated labels

def set_labels(self):
    """Add all the labels"""
    replace(self,"Hoppings","Hoppings t_{ij}")
    replace(self,"Fermi energy","Fermi energy \epsilon_{i}")
    replace(self,"Exchange field","Exchange field (J_x,J_y,J_z)")
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


