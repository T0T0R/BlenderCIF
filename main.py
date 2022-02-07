from loadCIF import CIF
from crystal import Cell
from test3D import Vis3D
from utils import Tools as t

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
        neighbors_cells = t.calculate_neighbors_cells(self.__My_cell, self.__My_cell.get_equiv_atom_list()[0])
        Vis3D(neighbors_cells, is_cartesian_coord)

        #neighbors_list = t.neighbors(self.__My_cell.get_equiv_atom_list()[0], self.__My_cell.get_equiv_atom_list(), True)
        #Vis3D(neighbors_list, is_cartesian_coord)

        atom_list = self.__My_cell.get_equiv_atom_list()[:]
        atom_list[1].move_cart_pos_by_one_cell(self.__My_cell, [0,0,1])
        Vis3D(atom_list, is_cartesian_coord)


MyObject = MainClass(path)
MyObject.initialize_cell()
MyObject.debug()

print("done.")