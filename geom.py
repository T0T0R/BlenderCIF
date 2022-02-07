import math as m
import numpy as np

from crystal import Atom
from crystal import Cell
from vect import vect3D as v

class Bond:
    def __init__(self, Atom_a, Atom_b):
        self.__connected_atoms = [Atom_a, Atom_b]
        self.__connected_positions = [Atom_a.get_cartesian_position(), Atom_b.get_cartesian_position()]
        self.__connected_id = [Atom_a.get_id(), Atom_b.get_id()]
        self.__length = np.sqrt( v.distance_sq(*self.__connected_positions) )
    

    def get_atoms(self):
        return self.__connected_atoms
    def get_positions(self):
        return self.__connected_positions
    def get_id(self):
        return self.__connected_id
    def get_length(self):
        return self.__length