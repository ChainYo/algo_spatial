import numpy as np
import pandas as pd 
import tkinter as tk
import random
import time
import os

from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

class CSV():

    @classmethod
    def charger_graph(cls):
        cls.df  = pd.read_csv("coord.csv")
        cls.df_to_dict = dict([(i,[a,b]) for i, a,b in zip(cls.df.index, cls.df.X, cls.df.Y)])
        return cls.df_to_dict

    @classmethod
    def save_graph(cls, value):
        cls.df = pd.DataFrame.from_dict(data=value, orient='index', columns=['X', 'Y'])
        cls.df.to_csv('coord.csv', index=False)

class Lieu():
    
    @classmethod
    def init_lieu(cls, x, y):
        return np.array([x, y])
    
    @classmethod
    def calc_distance(cls, vector1, vector2):
        return np.linalg.norm(vector1 - vector2)

class Route:
    
    @classmethod
    def calcul_distance_route(cls, fifo=[0]):
        marque = list()
        #file_.append(s)
        while len(marque) < 10:
            while fifo:
                noeud = fifo[0]
                del fifo[0]
                marque.append(noeud)
                if noeud not in marque:
                    fifo.append(points)
            fifo = Graph.plus_proche_voisin(noeud)
                

        way = marque.copy()
        way.append(0)
        print(way)
        return way

class Graph():

    @classmethod
    def creation_points(cls, NB_LIEUX, LARGEUR, HAUTEUR):
        cls.liste_lieux = {}

        for i in range(NB_LIEUX):
            cls.x = random.randint(20, LARGEUR-20)
            cls.y = random.randint(20, HAUTEUR-20)
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
        new_list = list(np.argsort(cls.matrix[chiffre]))
        new_list.remove(chiffre)
        return new_list

        return cls.passage

# Fenêtre de l'app
root = tk.Tk()
root.title("Challenge Spatial - Groupe 2")
root.geometry("1000x1000")
root.bind("<Escape>", lambda x: root.destroy())

# Ajout du canvas
c = tk.Canvas(root, scrollregion=(0,0,500,500), height=os.getenv('HAUTEUR'), width=os.getenv('LARGEUR'))  
c.pack()

# Génération des lieux et enregistrement en csv
CSV.save_graph(Graph.creation_points(int(os.getenv("NB_LIEUX")), int(os.getenv("LARGEUR")), int(os.getenv("HAUTEUR"))))
# Affichage des points
all_points = CSV.charger_graph()
for k, v in all_points.items():
    if k == 0:
        c.create_oval(v[0]-12, v[1]-12 ,v[0]+12, v[1]+12, fill="red")
    else:
        c.create_oval(v[0]-12, v[1]-12 ,v[0]+12, v[1]+12)
    c.create_text(v[0], v[1], text=str(k))

# Génération des chemins
Graph.calcul_matrice_cout_od(int(os.getenv("NB_LIEUX")), int(os.getenv("LARGEUR")), int(os.getenv("HAUTEUR")))
order = Route.calcul_distance_route()
for i in order:
    if i == 0:
        start = all_points[i]
    else:
        c.create_line(start[0], start[1], all_points[i][0], all_points[i][1], dash = (5, 2))
        start = all_points[i]

# Lancement de la page
root.mainloop()