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

# Fenêtre de l'app
root = tk.Tk()
root.title("Challenge Spatial - Groupe 2")
root.geometry("1000x1000")
root.bind("<Escape>", lambda x: root.destroy())

# Ajout du canvas
c = tk.Canvas(root, scrollregion=(0,0,500,500), height=os.getenv('HAUTEUR'), width=os.getenv('LARGEUR'))  
c.pack()

# Lancement de la page
root.mainloop()