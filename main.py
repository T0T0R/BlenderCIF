from loadCIF import CIF
from crystal import Cell
from test3D import Vis3D

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
    
    def debug(self, is_cartesian_coord=True):
        Vis3D(self.__My_cell, is_cartesian_coord)


MyObject = MainClass(path)
MyObject.initialize_cell()
MyObject.debug()

print("done.")