from loadCIF import CIF
from crystal import Cell

#import bpy
import json

path = "./MIL-177-LT.cif"

MyCIF = CIF(path)
My_cell = Cell(MyCIF)
My_cell.fill_cell()
My_cell.fract_coords_to_cartesian_coords()


print("done.")