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
        neighbors_list = t.neighbors(self.__My_cell.get_equiv_atom_list()[0], self.__My_cell.get_equiv_atom_list(), True)
        Vis3D(neighbors_list, is_cartesian_coord)


MyObject = MainClass(path)
MyObject.initialize_cell()
MyObject.debug()

print("done.")