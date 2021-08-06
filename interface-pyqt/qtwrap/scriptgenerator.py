
# These are function to generate the required text for a script

def get_header():
    out = ""
    out = "import sys\n"
    out = "import os\n"
    out += 'qhroot = os.environ["QHROOT"]\n'
    out = "import geometry\n"
    out = "import hamiltonians\n"
    return out # return header



def add_term(name,value):
    """Add a term to the Hamiltonian"""
    out = "" # empty line
    if value==0.0: return out # do nothing
    if name in ["m","mAB","mass"]:
        out += "h.add_sublattice_imbalance("+str(value)+")\n"
    if name in ["mAF"]:
        out += "h.add_antiferromagnetism("+str(value)+")\n"
    elif name in ["kanemele"]:
        out += "h.add_kane_mele("+str(value)+")\n"
    elif name in ["rashba"]:
        out += "h.add_rashba("+str(value)+")\n"
    elif name in ["Bx"]:
        out += "h.add_zeeman(["+str(value)+",0.0,0.0])\n"
    elif name in ["By"]:
        out += "h.add_zeeman([0.0,"+str(value)+",0.0])\n"
    elif name in ["Bz"]:
        out += "h.add_zeeman([0.0,0.0,"+str(value)+"])\n"
    elif name in ["swave"]:
        out += "h.add_swave("+str(value)+")\n"
    elif name in ["haldane"]:
        out += "h.add_haldane("+str(value)+")\n"
    elif name in ["antihaldane"]:
        out += "h.add_antihaldane("+str(value)+")\n"
    else: print(name, not recognised)
    return out


