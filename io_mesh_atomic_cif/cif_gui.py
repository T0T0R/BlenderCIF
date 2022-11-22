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

import bpy
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import (
        StringProperty,
        BoolProperty,
        EnumProperty,
        IntProperty,
        FloatProperty,
        )

from io_mesh_atomic_cif.cif_import import import_cif

# -----------------------------------------------------------------------------
#                                                                     Operators

# This is the class for the file dialog of the importer.
class IMPORT_OT_cif(Operator, ImportHelper):
    bl_idname = "import_mesh.cif"
    bl_label  = "Import Crystallographic Information File (*.cif)"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".cif"
    filter_glob: StringProperty(default="*.cif", options={'HIDDEN'},)

    use_center: BoolProperty(
        name = "Object to origin", default=False,
        description = "Put the object into the global origin")
    use_camera: BoolProperty(
        name="Camera", default=False,
        description="Do you need a camera?")
    use_light: BoolProperty(
        name="Lamp", default=False,
        description = "Do you need a lamp?")
    ball: EnumProperty(
        name="Type of ball",
        description="Choose ball",
        items=(('0', "NURBS", "NURBS balls"),
               ('1', "Mesh" , "Mesh balls"),
               ('2', "Meta" , "Metaballs")),
               default='0',)
    mesh_azimuth: IntProperty(
        name = "Azimuth", default=32, min=1,
        description = "Number of sectors (azimuth)")
    mesh_zenith: IntProperty(
        name = "Zenith", default=32, min=1,
        description = "Number of sectors (zenith)")
    scale_ballradius: FloatProperty(
        name = "Balls", default=1.0, min=0.0001,
        description = "Scale factor for all atom radii")
    scale_distances: FloatProperty (
        name = "Distances", default=1.0, min=0.0001,
        description = "Scale factor for all distances")
    atomradius: EnumProperty(
        name="Type",
        description="Choose type of atom radius",
        items=(('0', "Pre-defined", "Use pre-defined radius"),
               ('1', "Atomic", "Use atomic radius"),
               ('2', "van der Waals", "Use van der Waals radius")),
               default='0',)
    use_sticks: BoolProperty(
        name="Use sticks", default=True,
        description="Do you want to display the sticks?")
    bond_connections: StringProperty(
        name = "Connections", description="Which bonds should be calculated. For instance: C,O;C,H;O,H will compute bonds between C and O then C and H then O and H",
        default = "C,C; C,O")
    use_sticks_type: EnumProperty(
        name="Type",
        description="Choose type of stick",
        items=(('0', "Dupliverts", "Use dupliverts structures"),
               #('1', "Skin", "Use skin and subdivision modifier"),
               ('2', "Normal", "Use simple cylinders")),
               default='0',)
    sticks_subdiv_view: IntProperty(
        name = "SubDivV", default=2, min=1,
        description="Number of subdivisions (view)")
    sticks_subdiv_render: IntProperty(
        name = "SubDivR", default=2, min=1,
        description="Number of subdivisions (render)")
    sticks_sectors: IntProperty(
        name = "Sector", default=20, min=1,
        description="Number of sectors of a stick")
    sticks_radius: FloatProperty(
        name = "Radius", default=0.2, min=0.0001,
        description ="Radius of a stick")
    sticks_unit_length: FloatProperty(
        name = "Unit", default=0.05, min=0.0001,
        description = "Length of the unit of a stick in Angstrom")
    use_sticks_color: BoolProperty(
        name="Color", default=True,
        description="The sticks appear in the color of the atoms")
    use_sticks_smooth: BoolProperty(
        name="Smooth", default=True,
        description="The sticks are round (sectors are not visible)")
    #use_sticks_bonds: BoolProperty(
        #name="Bonds", default=False,
        #description="Show double and triple bonds")
    include_hydrogen: BoolProperty(
        name="Load H", default=True,
        description="Load hydrogen atoms")
    remove_oxygenw: StringProperty(
        name="Remove Ow", default="Ow1",
        description="Label of oxygen atoms in water molecules to remove. E.g. O1,O2,O3,G1")
    sticks_dist: FloatProperty(
        name="", default = 1.1, min=1.0, max=3.0,
        description="Distance between sticks measured in stick diameter")
    use_sticks_one_object: BoolProperty(
        name="One object", default=False,
        description="All sticks are one object")
    use_sticks_one_object_nr: IntProperty(
        name = "No.", default=200, min=10,
        description="Number of sticks to be grouped at once")
    datafile: StringProperty(
        name = "", description="Path to your custom data file",
        maxlen = 256, default = "", subtype='FILE_PATH')
    polyhedra_connections: StringProperty(
        name = "Coordination polyhedra", description="For which atoms coordination polyhedra must be calculated. For instance: Ti,O;Ti,N will compute the coordination of Ti by O then of Ti by N",
        default = "Ti,O")

    # This thing here just guarantees that the menu entry is not active when the
    # check box in the addon preferences is not activated! See __init__.py
    @classmethod
    def poll(cls, context):
        pref = context.preferences
        return pref.addons[__package__].preferences.bool_cif

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "use_camera")
        row.prop(self, "use_light")
        row = layout.row()
        row.prop(self, "use_center")
        box = layout.box()
        row = box.row()
        row.label(text="Water")
        row = box.row()
        row.prop(self, "include_hydrogen")
        row = box.row()
        row.prop(self, "remove_oxygenw")
        # Balls
        box = layout.box()
        row = box.row()
        row.label(text="Balls / atoms")
        row = box.row()
        col = row.column()
        col.prop(self, "ball")
        row = box.row()
        row.active = (self.ball == "1")
        col = row.column(align=True)
        col.prop(self, "mesh_azimuth")
        col.prop(self, "mesh_zenith")
        row = box.row()
        col = row.column()
        col.label(text="Scaling factors")
        col = row.column(align=True)
        col.prop(self, "scale_ballradius")
        col.prop(self, "scale_distances")
        row = box.row()
        row.prop(self, "atomradius")
        # Sticks
        box = layout.box()
        row = box.row()
        row.label(text="Sticks / bonds")
        row = box.row()
        row.prop(self, "use_sticks")
        row = box.row()
        row.active = self.use_sticks
        row.prop(self, "bond_connections")
        row = box.row()
        row.active = self.use_sticks
        row.prop(self, "use_sticks_type")
        row = box.row()
        row.active = self.use_sticks
        col = row.column()
        if self.use_sticks_type == '0' or self.use_sticks_type == '2':
            col.prop(self, "sticks_sectors")
        col.prop(self, "sticks_radius")
        if self.use_sticks_type == '1':
            row = box.row()
            row.active = self.use_sticks
            row.prop(self, "sticks_subdiv_view")
            row.prop(self, "sticks_subdiv_render")
            row = box.row()
            row.active = self.use_sticks
        if self.use_sticks_type == '0':
            col.prop(self, "sticks_unit_length")
        col = row.column(align=True)
        if self.use_sticks_type == '0':
            col.prop(self, "use_sticks_color")
        col.prop(self, "use_sticks_smooth")
        #if self.use_sticks_type == '0' or self.use_sticks_type == '2':
            #col.prop(self, "use_sticks_bonds")
        row = box.row()
        if self.use_sticks_type == '0':
            #row.active = self.use_sticks and self.use_sticks_bonds
            row.label(text="Distance")
            row.prop(self, "sticks_dist")
        if self.use_sticks_type == '2':
            row.active = self.use_sticks
            col = row.column()
            col.prop(self, "use_sticks_one_object")
            col = row.column()
            col.active = self.use_sticks_one_object
            col.prop(self, "use_sticks_one_object_nr")
        
        box = layout.box()
        row = box.row()
        row.label(text="Coordination polyhedra")
        row = box.row()
        row.prop(self, "polyhedra_connections")


    def execute(self, context):
        # This is in order to solve this strange 'relative path' thing.
        filepath_cif = bpy.path.abspath(self.filepath)

        # Execute main routine
        import_cif(self.ball,
                   self.mesh_azimuth,
                   self.mesh_zenith,
                   self.scale_ballradius,
                   self.atomradius,
                   self.scale_distances,
                   self.use_sticks,
                   self.use_sticks_type,
                   self.sticks_subdiv_view,
                   self.sticks_subdiv_render,
                   self.use_sticks_color,
                   self.use_sticks_smooth,
                   self.include_hydrogen,
                   self.remove_oxygenw,
                   self.use_sticks_one_object,
                   self.use_sticks_one_object_nr,
                   self.sticks_unit_length,
                   self.sticks_dist,
                   self.sticks_sectors,
                   self.sticks_radius,
                   self.use_center,
                   self.use_camera,
                   self.use_light,
                   self.polyhedra_connections,
                   self.bond_connections,
                   filepath_cif)

        return {'FINISHED'}
