import loadCIF

import bpy
import json

def draw_cell(cell):
    for atom in cell:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location = atom.location)
        bpy.ops.object.shade_smooth()




class Atom:
    def __init__(self):
        self.location = [0.252, -0.116, -0.704]


molecule = [Atom()]
draw_cell(molecule)