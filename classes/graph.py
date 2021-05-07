import numpy as np
import pandas as pd 
import tkinter as tk
from random import *
import time
import os
from dotenv import load_dotenv
# from ..tsp_graph_init import Lieu

# Chargement des variables d'environnement
load_dotenv()

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
        cls.voisin_proche = np.where(cls.matrix[chiffre] == np.amin(cls.matrix[chiffre][np.nonzero(cls.matrix[chiffre])]))
        print(cls.voisin_proche[0][0])
        return cls.voisin_proche[0][0]



# Graph.calcul_matrice_cout_od(10, 1000, 1000)
# Graph.plus_proche_voisin(1)