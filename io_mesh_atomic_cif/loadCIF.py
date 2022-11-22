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

import sys
from gemmi import cif # MPL-2.0 License




class CIF:
    def __init__(self, path):
        self.__path = path
        self.__greeted = set()
        self.__atoms = set()
        self.__equiv_pos = set()
    
    
        self.__atomic_table = []
        
        self.__atoms_labels = []
        self.__atoms_site_fract_x = []
        self.__atoms_site_fract_y = []
        self.__atoms_site_fract_z = []
        self.__atoms_type_symbols = []
    
        try:
            doc = cif.read_file(self.__path)
            block = doc.sole_block()
            
            self.__equiv_pos = [cif.as_string(string) for string in block.find_values("_symmetry_equiv_pos_as_xyz")]
            self.__atoms_labels = [cif.as_string(string) for string in block.find_values("_atom_site_label")]
            self.__atoms_site_fract_x = [cif.as_number(value) for value in block.find_values("_atom_site_fract_x")]    
            self.__atoms_site_fract_y = [cif.as_number(value) for value in block.find_values("_atom_site_fract_y")]        
            self.__atoms_site_fract_z = [cif.as_number(value) for value in block.find_values("_atom_site_fract_z")]       
            self.__atoms_type_symbols = [cif.as_string(string) for string in block.find_values("_atom_site_type_symbol")]
        
                      
        except Exception as e:
            print("Oops. %s" % e)
            sys.exit(1)
        
        
        self.__cell_length_a = cif.as_number(block.find_value("_cell_length_a"))
        self.__cell_length_b = cif.as_number(block.find_value("_cell_length_b"))
        self.__cell_length_c = cif.as_number(block.find_value("_cell_length_c"))
        self.__cell_angle_alpha = cif.as_number(block.find_value("_cell_angle_alpha"))
        self.__cell_angle_beta = cif.as_number(block.find_value("_cell_angle_beta"))
        self.__cell_angle_gamma = cif.as_number(block.find_value("_cell_angle_gamma"))
        self.__cell_space_group = block.find_value("_symmetry_space_group_name_H-M")
        
    
    def get_lengths(self):
        return [self.__cell_length_a, self.__cell_length_b, self.__cell_length_c]
    def get_angles(self):
        return [self.__cell_angle_alpha, self.__cell_angle_beta, self.__cell_angle_gamma] 
    def get_equiv_positions(self):
        return self.__equiv_pos
    def get_space_group(self):
        return self.__cell_space_group
    def get_atomic_table(self):
        return self.__atomic_table
    def get_atom_labels(self):
        return self.__atoms_labels
    def get_atom_type_symbols(self):
        return self.__atoms_type_symbols
    def get_atoms_site_fract_x(self):
        return self.__atoms_site_fract_x
    def get_atoms_site_fract_y(self):
        return self.__atoms_site_fract_y
    def get_atoms_site_fract_z(self):
        return self.__atoms_site_fract_z