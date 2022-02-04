import loadCIF
import crystal

import bpy
import json

def draw_molecule(molecule):
    for atom in molecule:
        bpy.ops.mesh.primitive_uv_sphere_add(location = atom.location)
        bpy.ops.object.shade_smooth()




molecule = [Atom()]