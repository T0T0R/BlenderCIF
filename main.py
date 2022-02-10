from loadCIF import CIF
from crystal import Atom
from crystal import Cell
from test3D import Vis3D
from vect import vect3D as v
from utils import Tools as t

#import bpy
import json

path = "./MIL-177-HT.cif"


class MainClass:
    def __init__(self, path, include_hydrogen=True):
        MyCIF = CIF(path)
        self.__My_cell = Cell(MyCIF, include_hydrogen)
        self.__bonds_list = []
        self.__polhedra_list = []
        self.__coordination_distance = 2.3


    def initialize_cell(self):
        self.__My_cell.fill_cell()
        self.__My_cell.fract_coords_to_cartesian_coords()
        self.__My_cell.fill_equiv_atoms()
    

    def update_bonds(self, central_atom_types="all", allowed_atom_types="all"):
        new_bonds = [*t.calculate_bonds(self.__My_cell, central_atom_types, allowed_atom_types)]
        self.__bonds_list = [*self.__bonds_list, *new_bonds]


    def update_polyhedra(self, central_atom_types="all", allowed_atom_types="all"):
        new_polyhedra = [*t.calculate_polyhedra(self.__My_cell, central_atom_types, allowed_atom_types, max_distance=self.__coordination_distance)]
        self.__polhedra_list = [*self.__polhedra_list, *new_polyhedra]
        
    
    def debug(self, is_cartesian_coord=True):
        
        #neighbors_list = t.neighbors(self.__My_cell, self.__My_cell.get_equiv_atom_list()[0], self.__My_cell.get_equiv_atom_list(), max_dist = 2.3, nearest_atom=True)
        #bonds_list = t.calculate_bonds(self.__My_cell, central_atom_types=["Ti"], allowed_atom_types=["O"], max_distance=2.3)

        #MyPolyhedron = t.calculate_polyhedron_for_one_atom(self.__My_cell, self.__My_cell.get_equiv_atom_list()[0], ["O"])
        #polyhedra_list = t.calculate_polyhedra(self.__My_cell, central_atom_types=["Ti"], allowed_atom_types=["O"], max_distance=self.__coordination_distance)
        
        #bonds_list = t.calculate_bonds(self.__My_cell, central_atom_types=["C"], allowed_atom_types=["O"])
        #bonds_list = [*bonds_list, *t.calculate_bonds(self.__My_cell, central_atom_types=["C"], allowed_atom_types=["C"])]

        #stripped_bonds_list = Bond.remove_duplicates(bonds_list)

        #Vis3D(neighbors_list, [], polyhedra_list, is_cartesian_coord)
        print(self.__My_cell.get_cell_offsets())
        Vis3D(self.__My_cell.get_equiv_atom_list(), self.__bonds_list, self.__polhedra_list, self.__My_cell.get_borders(), self.__My_cell.get_cell_offsets(), is_cartesian_coord)


MyObject = MainClass(path, include_hydrogen=True)
MyObject.initialize_cell()
MyObject.update_bonds(["C"],["O"])
MyObject.update_bonds(["C"],["C"])
MyObject.update_polyhedra(["Ti"],["O"])

MyObject.debug()

print("done.")