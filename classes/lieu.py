import numpy as np
import pandas as pd 
import tkinter as tk
from random import *
import time


class Graph():


    @classmethod
    def creation_points(cls, NB_LIEUX, LARGEUR, HAUTEUR):
        cls.liste_lieux = {}

        for i in range(NB_LIEUX):
            cls.x = randint(1, LARGEUR)
            cls.y = randint(1, HAUTEUR)
            cls.liste_lieux[i]=[cls.x, cls.y]

        # print(cls.liste_lieux)
        return cls.liste_lieux



    # calculer une matrice de distances entre chaque lieu du graphe
    @classmethod
    def calcul_matrice_cout_od(cls):
        matrice_od = []
        pass

    @classmethod
    def plus_proche_voisin(cls):
        voisin_proche = ""
        pass 

    @classmethod
    def charger_graph(cls):
        pass

    @classmethod
    def sauvegarder_graph(cls):
        pass 

# on défini une largeur et une longueur max pour le graph
# on renseigne un nombre
# on créée un nombre de point avec des latitudes et longitudes aléatoires
# on stock les points créés dans une liste 


Graph.creation_points(3, 1000, 1000)