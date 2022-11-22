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

from io_mesh_atomic_cif.crystal import Atom
from io_mesh_atomic_cif.crystal import Cell
from io_mesh_atomic_cif.vect import vect3D as v
from io_mesh_atomic_cif.geom import Bond
from io_mesh_atomic_cif.geom import Polyhedron


import math as m
import numpy as np


class Tools:
    @classmethod
    def calculate_neighbors_cells(cls, My_Cell, Central_atom): # Calculates the equivalent atoms of Atom in the 8 cells around the central one.
        atoms_list = [Central_atom]

        fractional_moves = [[1,0,0], [0,1,0], [0,0,1], [0,0,-1], [0,-1,0], [-1,0,0],
                            
                            [1,1,0], [1,-1,0], [-1,1,0], [-1,-1,0], 
                            
                            [1,1,1], [0,1,1], [-1,1,1],
                            [1,0,1], [-1,0,1],
                            [1,-1,1], [0,-1,1], [-1,-1,1],
                            
                            [1,1,-1], [0,1,-1], [-1,1,-1],
                            [1,0,-1], [-1,0,-1],
                            [1,-1,-1], [0,-1,-1], [-1,-1,-1]
                            ]

        for move in fractional_moves:
            Temp_atom = Atom(label=Central_atom.get_label(), atom_type=Central_atom.get_atom_type())
            Temp_atom.fake()
            Temp_atom.set_cartesian_position(Central_atom.get_cartesian_position())
            Temp_atom.move_cart_pos_by_one_cell(My_Cell, move)
            atoms_list.append(Temp_atom)
        
        return atoms_list

    
    
    @classmethod
    def neighbors(cls, My_Cell, Central_atom, atoms_list, allowed_atom_types="all", max_dist = 2.0, nearest_atom=False):  # Gives a list of the nearest atoms based on a maximum distance.
        maximum_dist = max_dist  # in Angstrom.
        max_dist_sq = m.pow(maximum_dist, 2.0)
        neighbors_list = []
     
        central_position = Central_atom.get_cartesian_position()
        
        for Other_atom in atoms_list:
            if Other_atom.get_id() == Central_atom.get_id():    # Avoiding the atom to evaluate itself.
                continue
            if not (allowed_atom_types=="all"):
                if not Other_atom.get_atom_type() in allowed_atom_types:
                    continue

            repeated_other_atom_list = cls.calculate_neighbors_cells(My_Cell, Other_atom)

            for repeated_other in repeated_other_atom_list:
                if v.distance_sq(central_position, repeated_other.get_cartesian_position()) <= max_dist_sq:
                    neighbors_list.append(repeated_other)
        
        if nearest_atom:    # Sort the list by distance with central atom
            def d_sq(Other_atom):
                posB = Other_atom.get_cartesian_position()
                return v.distance_sq(central_position, posB)
            
            neighbors_list.sort(key=d_sq)
        
        return neighbors_list



    @classmethod
    def calculate_bonds_for_one_atom(cls, My_Cell, Central_atom, allowed_atom_types="all", max_dist = 1.8):
        max_distance = max_dist
        neighbors = cls.neighbors(My_Cell, Central_atom, My_Cell.get_equiv_atom_list(), allowed_atom_types, max_dist=max_distance)
        bonds = []

        
        for other_atom in neighbors:
            conn_a = Central_atom.connect(other_atom)
            conn_b = other_atom.connect(Central_atom)
            if conn_a and conn_b: # If both atoms are not already connected
                    bonds.append(Bond(Central_atom, other_atom))

        return bonds
    

    @classmethod
    def calculate_bonds(cls, My_Cell, central_atom_types="all", allowed_atom_types="all", max_distance=1.8):
        if central_atom_types == "all":
            central_atoms_list = My_Cell.get_equiv_atom_list()
        else:
            central_atoms_list = [atom for atom in My_Cell.get_equiv_atom_list() if atom.get_atom_type() in central_atom_types]
        
        bonds = []
        for central_atom in central_atoms_list:
            temp_bonds = cls.calculate_bonds_for_one_atom(My_Cell, central_atom, allowed_atom_types, max_dist=max_distance)
            bonds = [*bonds, *temp_bonds]

        return bonds

    

    @classmethod
    def calculate_polyhedron_for_one_atom(cls, My_Cell, Central_atom, allowed_atom_types="all", max_dist = 2.5):
        neighbors = cls.neighbors(My_Cell, Central_atom, My_Cell.get_equiv_atom_list(), allowed_atom_types, max_dist)
        if not len(neighbors)==0:
            return Polyhedron(Central_atom, neighbors)
        else:
            return None
    
    @classmethod
    def calculate_polyhedra(cls, My_Cell, central_atom_types="all", allowed_atom_types="all", max_distance=2.5):
        if central_atom_types == "all":
            central_atoms_list = My_Cell.get_equiv_atom_list()
        else:
            central_atoms_list = [atom for atom in My_Cell.get_equiv_atom_list() if atom.get_atom_type() in central_atom_types]
        
        polyhedra = []
        for central_atom in central_atoms_list:
            polyhedron = cls.calculate_polyhedron_for_one_atom(My_Cell, central_atom, allowed_atom_types, max_distance)
            if not polyhedron == None:
                polyhedra.append(polyhedron)

        return polyhedra