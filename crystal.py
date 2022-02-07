import math as m
import numpy as np


class Atom:
    no = 0
    position_error = 0.01 # Two positions with less than 1% difference are the same.
    
    
    def __init__(self, location=[0.0, 0.0, 0.0], label="X", atom_type="Dummy"):
        self.__location = [a % 1.0 for a in location]   # Fractional coordinates
        self.__cartesian_position = [0.0, 0.0, 0.0]
        
        if label == "X":
            self.__label = "X" + str(Atom.no)
        else:
            self.__label = label
        
        self.__id = Atom.no
        self.__atom_type = atom_type
        self.__equiv_positions = []         # in fractional coordinates
        self.__equiv_positions_cart = []    # in cartesian coordinates
        self.__connected_to = []            # List of cartesians positions to which it is connected
        self.__fake_atom = False            # The atom is fake if it is a repetition outside of the cell of an existing atom
        
        Atom.no += 1

    def get_location(self):
        return self.__location
    def get_cartesian_position(self):
        return self.__cartesian_position    
    def get_label(self):
        return self.__label
    def get_atom_type(self):
        return self.__atom_type
    def get_equiv_positions(self):
        return self.__equiv_positions
    def get_equiv_positions_cart(self):
        return self.__equiv_positions_cart
    def get_id(self):
        return self.__id
    def get_connections(self):
        return self.__connected_to
    def is_fake(self):
        return self.__fake_atom
    
    def set_equiv_positions_cart(self, equiv_positions_cart):
        self.__equiv_positions_cart = equiv_positions_cart[:]
    def set_cartesian_position(self, cartesian_position):
        self.__cartesian_position = cartesian_position[:]
    def fake(self):
        self.__fake_atom = True

    def connect(self, other_atom):
        other_cart_pos = other_atom.get_cartesian_position()
        if all(not Atom.is_same_position(other_cart_pos, connection_pos) for connection_pos in self.__connected_to): # If the connection has never been made with this other position:
            self.__connected_to.append(other_cart_pos)
            return True
        else:   # If it has already been made:
            return False
        
    
    @staticmethod
    def is_same_position(posA, posB, error_sq=position_error**2):
        return (posA[0]-posB[0])**2 + (posA[1]-posB[1])**2 + (posA[2]-posB[2])**2 < error_sq
    

    def add_equiv_position(self, position):
        corrected_position = [a % 1.0 for a in position]
        if all(not self.is_same_position(corrected_position, existing_position) for existing_position in self.__equiv_positions):
            self.__equiv_positions.append(corrected_position)
    

    def move_cart_pos_by_one_cell(self, My_cell, cell_units):
        cart_units = Cell.fract_coord_to_cartesian_coord(My_cell.get_length_a(), My_cell.get_length_b(), My_cell.get_length_c(), My_cell.get_angle_alpha(), My_cell.get_angle_beta(), My_cell.get_angle_gamma(), cell_units)
        self.__cartesian_position[0] = self.__cartesian_position[0] + cart_units[0]
        self.__cartesian_position[1] = self.__cartesian_position[1] + cart_units[1]
        self.__cartesian_position[2] = self.__cartesian_position[2] + cart_units[2]

            



class Cell:    
    def __init__(self, My_CIF):
        self.__length_a, self.__length_b, self.__length_c = My_CIF.get_lengths()
        self.__angle_alpha, self.__angle_beta, self.__angle_gamma = My_CIF.get_angles()
        self.__equiv_pos = My_CIF.get_equiv_positions()
        self.__space_group = My_CIF.get_space_group()
        
        self.__atom_list = []
        for i in range(len(My_CIF.get_atom_labels())):
            self.__atom_list.append( Atom([My_CIF.get_atoms_site_fract_x()[i], My_CIF.get_atoms_site_fract_y()[i], My_CIF.get_atoms_site_fract_z()[i]], My_CIF.get_atom_labels()[i], My_CIF.get_atom_type_symbols()[i] ) )
        
        self.__equiv_atoms_list = []    # The list that will store every real atom in the cell (including equivalent ones).
        
        
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
    def get_equiv_atom_list(self):
        return self.__equiv_atoms_list



    def fill_cell(self):
        if len(self.__atom_list) == 0:
            print("No atoms in the cell")
            return
        else:
            for atom in self.__atom_list:
                self.calculate_equiv_cart_coord(atom)

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
        if i == -1: # No z component
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
    
    
    
    
    def calculate_equiv_cart_coord(self, atom):
        for equiv_position_string in self.__equiv_pos:
            S, T = Cell.equiv_pos_matrices(equiv_position_string)
            npS = np.array(S)
            npT = np.array(T)
            npA = np.array(atom.get_location())   # Original position.
            npB = np.matmul(npS,npA) + npT    # Applying symmetry and translation.
            
            atom.add_equiv_position(list(npB)) # Stores the fractional coordinates of equivalent positions in the orginial atoms list

            
    
    def fract_coords_to_cartesian_coords(self):
        alphaR = np.deg2rad(self.__angle_alpha)
        betaR = np.deg2rad(self.__angle_beta)
        gammaR = np.deg2rad(self.__angle_gamma)
        a,b,c = self.__length_a,self.__length_b,self.__length_c
        V = a*b*c*m.pow(1 - m.pow(m.cos(alphaR),2) - m.pow(m.cos(betaR),2) - m.pow(m.cos(gammaR),2) + 2*b*c*m.cos(alphaR)*m.cos(betaR)*m.cos(gammaR), 0.5)

        M = np.array([[a , b*np.cos(gammaR), c*np.cos(betaR)],
                      [0.0 , b*np.sin(gammaR) , c*(np.cos(alphaR)-np.cos(betaR)*np.cos(gammaR))/np.sin(gammaR)],
                    [0.0 , 0.0 , V/(a*b*np.sin(gammaR))]])

        def convert_to_cartesian_coord(f_coord):
            return list( np.matmul(M , np.array(f_coord)) )
        
        for atom in self.__atom_list: # Building a list of equivalent cartesian coordinates for each original atom.
            c_coords_list = []
            for f_coord in atom.get_equiv_positions():
                c_coords_list.append(convert_to_cartesian_coord(f_coord))
            atom.set_equiv_positions_cart(c_coords_list)
        

     
    @staticmethod  
    def fract_coord_to_cartesian_coord(a, b, c, alpha, beta, gamma, f_coord):
        alphaR = np.deg2rad(alpha)
        betaR = np.deg2rad(beta)
        gammaR = np.deg2rad(gamma)

        V = a*b*c*m.pow(1 - m.pow(m.cos(alphaR),2) - m.pow(m.cos(betaR),2) - m.pow(m.cos(gammaR),2) + 2*b*c*m.cos(alphaR)*m.cos(betaR)*m.cos(gammaR), 0.5)

        M = np.array([[a , b*np.cos(gammaR), c*np.cos(betaR)],
                      [0.0 , b*np.sin(gammaR) , c*(np.cos(alphaR)-np.cos(betaR)*np.cos(gammaR))/np.sin(gammaR)],
                      [0.0 , 0.0 , V/(a*b*np.sin(gammaR))]])

        return list( np.matmul(M , np.array(f_coord)) )
    
    
    def fill_equiv_atoms(self):
        for atom in self.__atom_list:
            for equiv_position_cart in atom.get_equiv_positions_cart():
                temp_atom = Atom(equiv_position_cart, atom.get_label(), atom.get_atom_type())
                temp_atom.set_cartesian_position(equiv_position_cart)
                self.__equiv_atoms_list.append(temp_atom)