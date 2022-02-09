import math as m
import numpy as np
from scipy.spatial import ConvexHull
#from scipy.spatial import HalfspaceIntersection

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

from crystal import Cell
from crystal import Atom

class Vis3D:
    def __init__(self, atom_list, bonds_list=[], polyhedra_list=[], corners_list=[], is_cartesian_coord=True):
        fig = plt.figure()
        ax = plt.axes(projection='3d')  
        
        COLORS = {'Ti':'blue', 'C':'black', 'O':'red', 'H':'white'}
        SIZES = {'Ti':30, 'C':6, 'O':6, 'H':2}
        X=[]
        Y=[]
        Z=[]
        C=[]
        S=[]
        
        for atom in atom_list:
            if atom.get_label()=="Ow1" or atom.get_label()=="Ow2" or atom.get_label()=="Ow3" or atom.get_label()=="Ow4":
                continue
            
            if is_cartesian_coord:
                equiv_pos = atom.get_cartesian_position()
            else:
                equiv_pos = atom.get_location()

            #for i in range(len(equiv_pos)):
                #X.append(equiv_pos[i][0])
                #Y.append(equiv_pos[i][1])
                #Z.append(equiv_pos[i][2])
                #C.append(COLORS[atom.get_atom_type()])
                #S.append(SIZES[atom.get_atom_type()])
                
            X.append(equiv_pos[0])
            Y.append(equiv_pos[1])
            Z.append(equiv_pos[2])
            C.append(COLORS[atom.get_atom_type()])
            S.append(SIZES[atom.get_atom_type()])    
        
        ax.scatter3D(X, Y, Z, c=C, s=S)

        for bond in bonds_list:
            posA, posB = bond.get_positions()
            ax.plot3D([posA[0],posB[0]], [posA[1],posB[1]], [posA[2],posB[2]], 'black')
        
        for poly in polyhedra_list:
            vertices = np.array(poly.get_vertices())
            hull = ConvexHull(vertices)
            triangles = []
            for simplex in hull.simplices:
                sq = [
                    (vertices[simplex[0], 0], vertices[simplex[0], 1], vertices[simplex[0], 2]),
                    (vertices[simplex[1], 0], vertices[simplex[1], 1], vertices[simplex[1], 2]),
                    (vertices[simplex[2], 0], vertices[simplex[2], 1], vertices[simplex[2], 2])
                    ]
                triangles.append(sq)
            for sq in triangles:
                f = mplot3d.art3d.Poly3DCollection([sq])
                f.set_edgecolor('0.8')
                f.set_alpha(0.1)
                ax.add_collection3d(f)
                #ax.plot3D(vertices[simplex,0], vertices[simplex,1], vertices[simplex,2])

        vertices = np.array(corners_list)
        hull = ConvexHull(vertices)
        triangles = []
        for simplex in hull.simplices:
            sq = [
                (vertices[simplex[0], 0], vertices[simplex[0], 1], vertices[simplex[0], 2]),
                (vertices[simplex[1], 0], vertices[simplex[1], 1], vertices[simplex[1], 2]),
                (vertices[simplex[2], 0], vertices[simplex[2], 1], vertices[simplex[2], 2])
                ]
            triangles.append(sq)
        for sq in triangles:
            f = mplot3d.art3d.Poly3DCollection([sq])
            f.set_edgecolor('1')
            f.set_alpha(0.0)
            ax.add_collection3d(f)

        
        ax.set_xlabel("Axis X")
        ax.set_ylabel("Axis Y")
        ax.set_zlabel("Axis Z")
        ax.set_xlim(-10.0, 20.0) 
        ax.set_ylim(0.00, 30.00)
        ax.set_zlim(0.00, 30.00)

        #ax.set_xlim(-40.0, 50.0) 
        #ax.set_ylim(-30.00, 60.00)
        #ax.set_zlim(-15.0, 15.00)
        
        plt.show()