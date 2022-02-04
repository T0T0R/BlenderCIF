class Atom:
    no = 0
    
    def __init__(self, location=[0.0, 0.0, 0.0], label="X", atom_type="Dummy"):
        self.__location = location
        
        if label == "X":
            self.__label = "X" + str(Atom.no)
        else:
            self.__label = label
            
        self.__atom_type = atom_type
        
        Atom.no += 1

    def get_location(self):
        return self.__location
    def get_label(self):
        return self.__label
    def get_atom_type(self):
        return self.__atom_type



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

    def fill_cell(self):
        if len(self.__atom_list) == 0:
            print("No atoms in the cell")
            return
            

