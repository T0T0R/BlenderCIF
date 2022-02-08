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