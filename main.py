from loadCIF import CIF
from crystal import Cell
from test3D import Vis3D

#import bpy
import json

path = "./MIL-177-HT.cif"

MyCIF = CIF(path)
My_cell = Cell(MyCIF)
My_cell.fill_cell()
My_cell.fract_coords_to_cartesian_coords()

Vis3D(My_cell)

print("done.")