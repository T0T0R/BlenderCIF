import math as m
import numpy as np

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

from crystal import Cell
from crystal import Atom

class Vis3D:
    def __init__(self, MyCell, is_cartesian_coord=True):
        fig = plt.figure()
        ax = plt.axes(projection='3d')  
        
        COLORS = {'Ti':'blue', 'C':'black', 'O':'red', 'H':'white'}
        SIZES = {'Ti':15, 'C':6, 'O':6, 'H':2}
        X=[]
        Y=[]
        Z=[]
        C=[]
        S=[]
        
        for atom in MyCell.get_atom_list():
            if atom.get_label()=="Ow1" or atom.get_label()=="Ow2" or atom.get_label()=="Ow3" or atom.get_label()=="Ow4":
                continue
            
            if is_cartesian_coord:
                equiv_pos = atom.get_equiv_positions_cart()
            else:
                equiv_pos = atom.get_equiv_positions()

            for i in range(len(equiv_pos)):
                X.append(equiv_pos[i][0])
                Y.append(equiv_pos[i][1])
                Z.append(equiv_pos[i][2])
                C.append(COLORS[atom.get_atom_type()])
                S.append(SIZES[atom.get_atom_type()])
                
        
        ax.scatter3D(X, Y, Z, c=C, s=S)
        ax.set_xlabel("Axis X")
        ax.set_ylabel("Axis Y")
        ax.set_zlabel("Axis Z")
        ax.set_xlim(-10.0, 20.0) 
        ax.set_ylim(0.00, 30.00)
        ax.set_zlim(0.00, 30.00)
        #plt.xlim(-10.0, 20.0)
        #plt.ylim(0.00, 30.00)        
        #plt.zlim(0.00, 30.00)        
        
        plt.show()