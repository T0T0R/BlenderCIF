from loadCIF import CIF
from crystal import Atom
from crystal import Cell
from test3D import Vis3D
from vect import vect3D as v
from utils import Tools as t
from geom import Bond
from geom import Polyhedron

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

        #MyPolyhedron = t.calculate_polyhedron_for_one_atom(self.__My_cell, self.__My_cell.get_equiv_atom_list()[0], ["O"])
        polyhedra_list = t.calculate_polyhedra(self.__My_cell, central_atom_types=["Ti"], allowed_atom_types=["O"], max_distance=2.3)
        
        #bonds_list = t.calculate_bonds(self.__My_cell, central_atom_types=["C"], allowed_atom_types=["O"])
        #bonds_list = [*bonds_list, *t.calculate_bonds(self.__My_cell, central_atom_types=["C"], allowed_atom_types=["C"])]

        atomA = Atom()
        atomB = Atom()
        atomC = Atom()
        atomB.set_cartesian_position([1.0, 0.0, 0.0])
        atomC.set_cartesian_position([1.0, 1.0, 0.0])
        bond1 = Bond(atomA, atomB)
        bond2 = Bond(atomA, atomB)
        bonds_list = [bond1, bond2]
        stripped_bonds_list = Bond.remove_duplicates(bonds_list)

        #Vis3D(neighbors_list, [], polyhedra_list, is_cartesian_coord)
        Vis3D(self.__My_cell.get_equiv_atom_list(), stripped_bonds_list, polyhedra_list, is_cartesian_coord)


MyObject = MainClass(path)
MyObject.initialize_cell()
MyObject.debug()

print("done.")