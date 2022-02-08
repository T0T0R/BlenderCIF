from loadCIF import CIF
from crystal import Cell
from test3D import Vis3D
from vect import vect3D as v
from utils import Tools as t
from geom import Bond

#import bpy
import json

path = "./MIL-177-HT.cif"


class MainClass:
    def __init__(self, path):
        MyCIF = CIF(path)
        self.__My_cell = Cell(MyCIF)

    def initialize_cell(self):
        self.__My_cell.fill_cell()
        self.__My_cell.fract_coords_to_cartesian_coords()
        self.__My_cell.fill_equiv_atoms()
        
    
    def debug(self, is_cartesian_coord=True):
        
        #neighbors_list = t.neighbors(self.__My_cell, self.__My_cell.get_equiv_atom_list()[0], self.__My_cell.get_equiv_atom_list(), max_dist = 2.3, nearest_atom=True)
        #bonds_list = t.calculate_bonds(self.__My_cell, central_atom_types=["Ti"], allowed_atom_types=["O"], max_distance=2.3)
        bonds_list = t.calculate_bonds(self.__My_cell, central_atom_types=["C"], allowed_atom_types=["O"])
        bonds_list = [*bonds_list, *t.calculate_bonds(self.__My_cell, central_atom_types=["C"], allowed_atom_types=["C"])]

        #Vis3D(neighbors_list, bonds_list, is_cartesian_coord)
        Vis3D(self.__My_cell.get_equiv_atom_list(), bonds_list, is_cartesian_coord)


MyObject = MainClass(path)
MyObject.initialize_cell()
MyObject.debug()

print("done.")