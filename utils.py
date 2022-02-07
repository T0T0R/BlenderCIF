from crystal import Atom
from crystal import Cell


import math as m
import numpy as np

class Tools:
    @classmethod
    def distance_sq(cls, posA, posB):   # Calculates the distance squared between two positions.
        return m.pow(posA[0]-posB[0], 2.0) + m.pow(posA[1]-posB[1], 2.0) + m.pow(posA[2]-posB[2], 2.0)
    

    @classmethod
    def calculate_neighbors_cells(cls, My_Cell, Central_atom): # Calculates the equivalent atoms of Atom in the 8 cells around the central one.
        atoms_list = [Central_atom]

        fractional_moves = [[1,0,0], [-1,0,0], [0,1,0], [0,-1,0], [0,0,1], [0,0,-1],
                            
                            [1,1,0], [1,-1,0], [-1,1,0], [-1,-1,0], 
                            
                            [1,1,1], [0,1,1], [-1,1,1],
                            [1,0,1], [0,0,1], [-1,0,1],
                            [1,-1,1], [0,-1,1], [-1,-1,1],
                            
                            [1,1,-1], [0,1,-1], [-1,1,-1],
                            [1,0,-1], [0,0,-1], [-1,0,-1],
                            [1,-1,-1], [0,-1,-1], [-1,-1,-1]]

        for move in fractional_moves:
            Temp_atom = Atom(label=Central_atom.get_label(), atom_type=Central_atom.get_atom_type())
            Temp_atom.set_cartesian_position(Central_atom.get_cartesian_position())
            Temp_atom.move_cart_pos_by_one_cell(My_Cell, move)
            atoms_list.append(Temp_atom)
        
        return atoms_list

    
    
    @classmethod
    def neighbors(cls, My_Cell, Central_atom, atoms_list, nearest_atom=False):  # Gives a list of the nearest atoms based on a maximum distance.
        maximum_dist = 3.0  # in Angstrom.
        max_dist_sq = m.pow(maximum_dist, 2.0)
        neighbors_list = []
        
        central_position = Central_atom.get_cartesian_position()
        print("Center: ")
        print(central_position)
        
        for Other_atom in atoms_list:
            if Other_atom.get_id() == Central_atom.get_id():    # Avoiding the atom to evaluate itself.
                continue

            repeated_other_atom_list = cls.calculate_neighbors_cells(My_Cell, Other_atom)

            for repeated_other in repeated_other_atom_list:
                if cls.distance_sq(central_position, repeated_other.get_cartesian_position()) <= max_dist_sq:
                    neighbors_list.append(repeated_other)
        
        if nearest_atom:    # Sort the list by distance with central atom
            def d_sq(Other_atom):
                posB = Other_atom.get_cartesian_position()
                return cls.distance_sq(central_position, posB)
            
            neighbors_list.sort(key=d_sq)
        
        print("others:")
        for atom in neighbors_list:
            print(atom.get_cartesian_position())
            print(cls.distance_sq(atom.get_cartesian_position(), central_position)**0.5)
        return neighbors_list
        