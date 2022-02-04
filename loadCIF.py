from crystal import Atom
from crystal import Cell

import sys
from gemmi import cif # MPL-2.0 License

path = "./MIL-177-LT.cif"

greeted = set()
Atoms = set()
EquivPos = set()


Atomic_table = []

Atoms_label = []
Atoms_site_fract_x = []
Atoms_site_fract_y = []
Atoms_site_fract_z = []
Atoms_type_symbol = []

try:
    doc = cif.read_file(path)
    block = doc.sole_block()
    for element in block.find_loop("_atom_site_type_symbol"):
        if element not in greeted:
            #print("Hello " + element)
            greeted.add(element)
    
    for symmetry in block.find_loop("_symmetry_equiv_pos_as_xyz"):
        if symmetry not in EquivPos:
            #print("Hello " + symmetry)
            EquivPos.add(symmetry)   
            

    Atoms_label = [cif.as_string(string) for string in block.find_values("_atom_site_label")]
    Atoms_site_fract_x = [cif.as_number(value) for value in block.find_values("_atom_site_fract_x")]    
    Atoms_site_fract_y = [cif.as_number(value) for value in block.find_values("_atom_site_fract_y")]        
    Atoms_site_fract_z = [cif.as_number(value) for value in block.find_values("_atom_site_fract_z")]       
    Atoms_type_symbol = [cif.as_string(string) for string in block.find_values("_atom_site_type_symbol")]

              
            

    
except Exception as e:
    print("Oops. %s" % e)
    sys.exit(1)


cell_length_a = cif.as_number(block.find_value("_cell_length_a"))
cell_length_b = cif.as_number(block.find_value("_cell_length_b"))
cell_length_c = cif.as_number(block.find_value("_cell_length_c"))
cell_angle_alpha = cif.as_number(block.find_value("_cell_angle_alpha"))
cell_angle_beta = cif.as_number(block.find_value("_cell_angle_beta"))
cell_angle_gamma = cif.as_number(block.find_value("_cell_angle_gamma"))
cell_space_group = block.find_value("_symmetry_space_group_name_H-M")

for i in range(len(Atoms_label)):
    Atomic_table.append( Atom([Atoms_site_fract_x[i], Atoms_site_fract_y[i], Atoms_site_fract_z[i]], Atoms_label[i], Atoms_type_symbol[i] ) )

My_cell = Cell([cell_length_a,cell_length_b,cell_length_c], [cell_angle_alpha,cell_angle_beta,cell_angle_gamma], EquivPos, cell_space_group, Atomic_table)

print("test")