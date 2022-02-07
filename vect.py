import math as m
import numpy as np

class vect3D:
    @classmethod
    def distance_sq(cls, posA, posB):   # Calculates the distance squared between two positions.
        return m.pow(posA[0]-posB[0], 2.0) + m.pow(posA[1]-posB[1], 2.0) + m.pow(posA[2]-posB[2], 2.0)