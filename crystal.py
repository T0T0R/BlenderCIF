import numpy as np

class Atom:
    no = 0
    position_error = 0.01 # Two positions with less than 1% difference are the same.
    
    
    def __init__(self, location=[0.0, 0.0, 0.0], label="X", atom_type="Dummy"):
        self.__location = location
        
        if label == "X":
            self.__label = "X" + str(Atom.no)
        else:
            self.__label = label
            
        self.__atom_type = atom_type
        self.__equiv_positions = []
        
        Atom.no += 1

    def get_location(self):
        return self.__location
    def get_label(self):
        return self.__label
    def get_atom_type(self):
        return self.__atom_type
    def get_equiv_positions(self):
        return self.__equiv_positions
    
    @classmethod
    def is_same_position(cls, posA, posB):
        return (posA[0]-posB[0])**2 + (posA[1]-posB[1])**2 + (posA[2]-posB[2])**2 < cls.position_error**2
    

    def add_equiv_position(self, position):
        corrected_position = [a % 1.0 for a in position]
        if all(not self.is_same_position(corrected_position, existing_position) for existing_position in self.__equiv_positions):
            self.__equiv_positions.append(corrected_position)



class Cell:    
    def __init__(self, lengths=[0.0, 0.0, 0.0], angles=[90.0, 90.0, 90.0], equiv_pos=['x, y, z'], space_group="", atom_list=[]):
        self.__lenght_a = lengths[0]
        self.__lenght_b = lengths[1]
        self.__lenght_c = lengths[2]
        self.__angle_alpha = angles[0]
        self.__angle_beta = angles[1]
        self.__angle_gamma = angles[2]
        self.__equiv_pos = equiv_pos
        self.__space_group = space_group
        self.__atom_list = atom_list
        
        
    def get_length_a(self):
        return self.__length_a
    def get_length_b(self):
        return self.__length_b
    def get_length_c(self):
        return self.__length_c    
    def get_angle_alpha(self):
        return self.__angle_alpha
    def get_angle_beta(self):
        return self.__angle_beta
    def get_angle_gamma(self):
        return self.__angle_gamma
    def get_atom_list(self):
        return self.__atom_list



    def fill_cell(self):
        if len(self.__atom_list) == 0:
            print("No atoms in the cell")
            return
        else:
            for atom in self.__atom_list:
                self.calculate_equiv_atoms(atom)

    @classmethod    
    def equiv_pos_matrices(cls, string):    # eg. string = "-x+y, 1/2+y, -z-1/2"
        x_string, y_string, z_string = string.split(", ")
        X_transform, X_translation = Cell.convert_equiv_pos_str_to_vec(x_string)
        Y_transform, Y_translation = Cell.convert_equiv_pos_str_to_vec(y_string)
        Z_transform, Z_translation = Cell.convert_equiv_pos_str_to_vec(z_string)
        return ([X_transform, Y_transform, Z_transform], [X_translation, Y_translation, Z_translation])
        
    
    @classmethod
    def convert_equiv_pos_str_to_vec(cls, string):  # eg. string = "-x+y-1/2"
        i = string.find("x")
        if i == -1: # No x component
            x_value = 0.0
        else:
            if (i-1 >= 0 and string[i-1]=="-"):
                x_value = -1.0
            else:
                x_value = 1.0
        
        i = string.find("y")
        if i == -1: # No y component
            y_value = 0.0
        else:
            if (i-1 >= 0 and string[i-1]=="-"):
                y_value = -1.0
            else:
                y_value = 1.0
        
        i = string.find("z")
        if i == -1: # No y component
            z_value = 0.0
        else:
            if (i-1 >= 0 and string[i-1]=="-"):
                z_value = -1.0
            else:
                z_value = 1.0    
                
        i = string.find("/")
        if i == -1: # No translation component
            transl_value = 0.0
        else:
            if (i-2 >= 0 and string[i-2]=="-"):
                transl_value = -1.0/int(string[i+1])
            else:
                transl_value = 1.0/int(string[i+1])         
      
        return([x_value, y_value, z_value], transl_value)
    
    
    def calculate_equiv_atoms(self, atom):
        for equiv_position_string in self.__equiv_pos:
            S, T = Cell.equiv_pos_matrices(equiv_position_string)
            npS = np.array(S)
            npT = np.array(T)
            npA = np.array(atom.get_location())   # Original position.
            npB = np.matmul(npS,npA) + npT    # Applying symmetry and translation.
            atom.add_equiv_position(list(npB))