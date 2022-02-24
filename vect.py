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

class vect3D:
    @classmethod
    def distance_sq(cls, posA, posB):   # Calculates the distance squared between two positions.
        return m.pow(posA[0]-posB[0], 2.0) + m.pow(posA[1]-posB[1], 2.0) + m.pow(posA[2]-posB[2], 2.0)