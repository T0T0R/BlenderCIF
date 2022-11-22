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
#  along with Foobar. If not, see <https://www.gnu.org/licenses/>
#
# ##### END GPL LICENCE BLOCK #####

#
#  Author            : Clemens Barth (Blendphys@root-1.de)
#  Homepage(Wiki)    : http://development.root-1.de/Atomic_Blender.php
#
#  Start of project                  : 2011-08-31 by CB
#  First publication in Blender      : 2011-11-11 by CB
#  Fusion of the PDB, XYZ and Panel  : 2019-03-22 by CB
#  Last modified                     : 2019-05-17
#
#  Contributing authors
#  ====================
#
#  So far ... none ... .
#
#
#  Acknowledgements
#  ================
#
#  A big thank you to all those people who I met in particular in the IRC and
#  who helped me a lot.
#
#  Blender developers
#  ------------------
#  Campbell Barton      (ideasman)
#  Brendon Murphy       (meta_androcto)
#  Truman Melton (?)    (truman)
#  Kilon Alios          (kilon)
#  ??                   (CoDEmanX)
#  Dima Glib            (dairin0d)
#  Peter K.H. Gragert   (PKHG)
#  Valter Battioli (?)  (valter)
#  ?                    (atmind)
#  Ray Molenkamp        (bzztploink)
#
#  Other
#  -----
#  Frank Palmino (Femto-St institute, Belfort-Montbéliard, France)
#  ... for testing the addons and for feedback
#

#
#  Author            : Arthur Langlard (arthur.langlard@univ-nantes.fr)
#  Homepage          : http://github.com/T0T0R/BlenderCIF
#
#  Start of project                  : 2021-02-04 by AL
#  Last modified                     : 2022-11-22 by AL
#



bl_info = {
    "name": "Atomic Blender PDB/XYZ/CIF",
    "description": "Importing atoms listed in PDB, XYZ or CIF files as balls into Blender",
    "author": "Arthur Langlard",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "File -> Import -> CIF (.cif)",
    "warning": "",
    #"doc_url": "{BLENDER_MANUAL_URL}/addons/import_export/mesh_atomic.html",
    "category": "Import-Export",
}



import subprocess
import sys
py_exec = sys.executable
# ensure pip is installed & update
subprocess.call([str(py_exec), "-m", "ensurepip", "--user"])
# install dependencies using pip
subprocess.call([str(py_exec),"-m", "pip", "install", "gemmi",  "--target", str(sys.exec_prefix)])


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

from . import (
        pdb_gui,
        xyz_gui,
        cif_gui,
        utility_gui,
        utility_panel
        )

# -----------------------------------------------------------------------------
#                                                                   Preferences

class AddonPreferences(AddonPreferences):
    # This must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    bool_pdb : BoolProperty(
               name="PDB import/export",
               default=True,
               description="Import/export PDB",
               )
    bool_xyz : BoolProperty(
               name="XYZ import/export",
               default=True,
               description="Import/export XYZ",
               )
    bool_cif : BoolProperty(
               name="CIF import",
               default=True,
               description="Import CIF",
               )    
    # This boolean is checked in the poll function in PANEL_PT_prepare
    # (see utility.py).
    bool_utility : BoolProperty(
                   name="Utility panel",
                   default=False,
                   description=("Panel with functionalities for modifying " \
                                "atomic structures"),
                   )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Choose the importer(s) and a 'utility' panel")
        layout.prop(self, "bool_pdb")
        layout.prop(self, "bool_xyz")
        layout.prop(self, "bool_cif")
        layout.prop(self, "bool_utility")


# -----------------------------------------------------------------------------
#                                                                          Menu


# The entry into the menu 'file -> import'
def menu_func_import_pdb(self, context):
    lay = self.layout
    lay.operator(pdb_gui.IMPORT_OT_pdb.bl_idname,text="Protein Data Bank (.pdb)")

def menu_func_import_xyz(self, context):
    lay = self.layout
    lay.operator(xyz_gui.IMPORT_OT_xyz.bl_idname,text="XYZ (.xyz)")

def menu_func_import_cif(self, context):
    lay = self.layout
    lay.operator(cif_gui.IMPORT_OT_cif.bl_idname,text="CIF (.cif)")

# The entry into the menu 'file -> export'
def menu_func_export_pdb(self, context):
    lay = self.layout
    lay.operator(pdb_gui.EXPORT_OT_pdb.bl_idname,text="Protein Data Bank (.pdb)")

def menu_func_export_xyz(self, context):
    lay = self.layout
    lay.operator(xyz_gui.EXPORT_OT_xyz.bl_idname,text="XYZ (.xyz)")


# -----------------------------------------------------------------------------
#                                                                      Register

def register():
    from bpy.utils import register_class

    register_class(AddonPreferences)

    register_class(pdb_gui.IMPORT_OT_pdb)
    register_class(pdb_gui.EXPORT_OT_pdb)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_pdb)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_pdb)

    register_class(xyz_gui.IMPORT_OT_xyz)
    register_class(xyz_gui.EXPORT_OT_xyz)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_xyz)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_xyz)

    register_class(cif_gui.IMPORT_OT_cif)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_cif)

    classes = (utility_gui.PANEL_PT_prepare,
                utility_gui.PanelProperties,
                utility_gui.DatafileApply,
                utility_gui.DefaultAtom,
                utility_gui.ReplaceAtom,
                utility_gui.SeparateAtom,
                utility_gui.DistanceButton,
                utility_gui.RadiusAllBiggerButton,
                utility_gui.RadiusAllSmallerButton,
                utility_gui.SticksAllBiggerButton,
                utility_gui.SticksAllSmallerButton)
    from bpy.utils import register_class
    utility_panel.read_elements()
    for cls in classes:
        register_class(cls)

    scene = bpy.types.Scene
    scene.atom_blend = bpy.props.PointerProperty(type=utility_gui.PanelProperties)


def unregister():
    from bpy.utils import unregister_class

    unregister_class(AddonPreferences)

    unregister_class(pdb_gui.IMPORT_OT_pdb)
    unregister_class(pdb_gui.EXPORT_OT_pdb)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_pdb)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_pdb)

    unregister_class(xyz_gui.IMPORT_OT_xyz)
    unregister_class(xyz_gui.EXPORT_OT_xyz)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_xyz)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_xyz)

    unregister_class(cif_gui.IMPORT_OT_cif)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_cif)

    classes = (utility_gui.PANEL_PT_prepare,
                utility_gui.PanelProperties,
                utility_gui.DatafileApply,
                utility_gui.DefaultAtom,
                utility_gui.ReplaceAtom,
                utility_gui.SeparateAtom,
                utility_gui.DistanceButton,
                utility_gui.RadiusAllBiggerButton,
                utility_gui.RadiusAllSmallerButton,
                utility_gui.SticksAllBiggerButton,
                utility_gui.SticksAllSmallerButton)
    for cls in classes:
        unregister_class(cls)


# -----------------------------------------------------------------------------
#                                                                          Main

if __name__ == "__main__":

    register()
