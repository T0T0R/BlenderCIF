# ##### BEGIN GPL LICENCE BLOCK #####
#  Copyright (C) 2022  Arthur Langlard
#
#  This file is part of Atomic Blender (CIF).
#
#  Atomic Blender (CIF) is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation, either version 3
#  of the License, or (at your option) any later version.
#
#  Atomic Blender (CIF) is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with Atomic Blender (CIF). If not, see <https://www.gnu.org/licenses/>
#
# ##### END GPL LICENCE BLOCK #####

import math as m
import numpy as np

from crystal import Atom
from crystal import Cell
from vect import vect3D as v

class Bond:
    no = 0

    def __init__(self, Atom_a, Atom_b):
        self.__connected_atoms = [Atom_a, Atom_b]
        self.__connected_positions = [Atom_a.get_cartesian_position(), Atom_b.get_cartesian_position()]
        self.__connected_id = [Atom_a.get_id(), Atom_b.get_id()]
        self.__length = np.sqrt( v.distance_sq(*self.__connected_positions) )
        self.__no = Bond.no

        Bond.no += 1
    

    def get_atoms(self):
        return self.__connected_atoms
    def get_positions(self):
        return self.__connected_positions
    def get_id(self):
        return self.__connected_id
    def get_length(self):
        return self.__length
    

    @staticmethod
    def is_same_bond(bond1, bond2):
        position_error = 0.1
        atom_1A, atom_1B = bond1.get_atoms()
        atom_2A, atom_2B = bond2.get_atoms()

        # With a precision of 0.1 Angstrom
        same_atoms_config_1 = Atom.is_same_position(atom_1A.get_cartesian_position(), atom_2A.get_cartesian_position(), position_error) and Atom.is_same_position(atom_1B.get_cartesian_position(), atom_2B.get_cartesian_position(), position_error)
        same_atoms_config_2 = Atom.is_same_position(atom_1A.get_cartesian_position(), atom_2B.get_cartesian_position(), position_error) and Atom.is_same_position(atom_1B.get_cartesian_position(), atom_2A.get_cartesian_position(), position_error)

        return same_atoms_config_1 or same_atoms_config_2
    


    @staticmethod
    def remove_duplicates(bonds_list):

        def contains(bonds_table, bond, bond_index):        # Gives the index of the 
            output = False
            for i in range(bond_index): # Evaluate bonds before the index of the reference
                if Bond.is_same_bond(bond, bonds_table[i]):
                    return True

            return output

        # The bond_list object is modified while searching through it, so it is better to build a new list
        output_list = []
        for i in range(len(bonds_list)):
            bond = bonds_list[i]
            if not contains(bonds_list, bond, i):
                output_list.append(bond)
        #return [bond for bond in bonds_list if not contains(bonds_list, bond)]
        return output_list




class Polyhedron:
    no = 0

    def calculate_vertices(self):
        return [atom.get_cartesian_position() for atom in self.__list_of_atoms]

    def __init__(self, Central_atom, list_of_atoms):
        self.__Central_atom = Central_atom
        self.__list_of_atoms = list_of_atoms
        self.__vertices = self.calculate_vertices()
        self.__no = Polyhedron.no

        Polyhedron.no += 1

    def get_central_atom(self):
        return self.__Central_atom
    def get_vertices(self):
        return self.__vertices
    def get_list_of_atoms(self):
        return self.__list_of_atoms