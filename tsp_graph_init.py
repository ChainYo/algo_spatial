import numpy as np
import pandas as pd 
import tkinter as tk
import random
import time
import os

from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

class Lieu():
    
    @classmethod
    def init_lieu(cls, x, y):
        return np.array([x, y])
    
    @classmethod
    def calc_distance(cls, vector1, vector2):
        return np.linalg.norm(vector1 - vector2)

class Route:
    
    @classmethod
    def calcul_distance_route(cls, file_=[0]):
        marque = list()
        #file_.append(s)
        while file_:
            noeud = file_[0]
            del file_[0]
            marque.append(noeud)
            point = cls.batiste(noeud)
            if point not in marque:
                file_.append(point)

        way = marque.copy()
        way.append(0)
        return way

class Graph():

    @classmethod
    def creation_points(cls, NB_LIEUX, LARGEUR, HAUTEUR):
        cls.liste_lieux = {}

        for i in range(NB_LIEUX):
            cls.x = randint(20, LARGEUR)
            cls.y = randint(20, HAUTEUR)
            cls.liste_lieux[i]=Lieu.init_lieu(cls.x, cls.y)

        return cls.liste_lieux



    @classmethod
    def calcul_matrice_cout_od(cls, NB_LIEUX, LARGEUR, HAUTEUR):
        cls.coord = cls.creation_points(NB_LIEUX, LARGEUR, HAUTEUR)
        cls.matrix = np.zeros((NB_LIEUX, NB_LIEUX))
        for i in range(len(cls.matrix)):
            for j in range(len(cls.matrix[i])):
                if cls.matrix[i,j] == 0:
                    cls.vecteur1 = cls.coord[i]
                    cls.vecteur2 = cls.coord[j]
                    cls.result = Lieu.calc_distance(cls.vecteur1, cls.vecteur2)
                    cls.matrix[i,j] = cls.result
                    cls.matrix[j,i] = cls.result
        print(pd.DataFrame(cls.matrix))
        return cls.matrix

    @classmethod
    def plus_proche_voisin(cls, chiffre):
        cls.passage = np.sort(cls.matrix[chiffre])
        cls.passage = cls.passage[np.nonzero(cls.passage)]

        return cls.passage



# # Fenêtre de l'app
# root = tk.Tk()
# root.title("Challenge Spatial - Groupe 2")
# root.geometry("1000x1000")
# root.bind("<Escape>", lambda x: root.destroy())

# # Ajout du canvas
# c = tk.Canvas(root, scrollregion=(0,0,500,500), height=os.getenv('HAUTEUR'), width=os.getenv('LARGEUR'))  
# c.pack()

# # Lancement de la page
# root.mainloop()