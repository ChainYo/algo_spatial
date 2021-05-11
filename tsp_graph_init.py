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
    def generation_route(cls, fifo=[0]):
        marquer = []
        while fifo:
            noeud = fifo[0]
            #print(noeud)
            del fifo[0]
            marquer.append(noeud)
            voisin = Graph().plus_proche_voisin(noeud)
            #print(marquer)
            for i in voisin:
                if i not in marquer:
                    fifo.append(i)
                    break
        marquer.append(0)
        way = marquer
        return way

    @classmethod
    def calcul_distance_route(cls, route, matrice):
        cls.score = 0
        for i in range(len(route) - 1):
            cls.pt_start = route[i]
            cls.pt_goal = route[i + 1]
            cls.score += matrice[cls.pt_start, cls.pt_goal]
        return cls.score

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
    def calcul_matrice_cout_od(cls, NB_LIEUX, CSV):
        cls.coord = np.array([v for v in CSV.values()])
        cls.matrix = np.zeros((NB_LIEUX, NB_LIEUX))
        for i in range(len(cls.matrix)):
            for j in range(len(cls.matrix[i])):
                if cls.matrix[i, j] == 0:
                    cls.vecteur1 = cls.coord[i]
                    cls.vecteur2 = cls.coord[j]
                    cls.result = Lieu.calc_distance(cls.vecteur1, cls.vecteur2)
                    cls.matrix[i, j] = cls.result
                    cls.matrix[j, i] = cls.result
        print(pd.DataFrame(cls.matrix))
        return cls.matrix

    @classmethod
    def plus_proche_voisin(cls, chiffre):
        new_list = list(np.argsort(cls.matrix[chiffre]))
        new_list.remove(chiffre)
        return new_list

class AlgoGen():
    
    @classmethod
    def selection(cls, liste):
        return sorted(liste, key=lambda k: k['score']) 

    @classmethod
    def cross_over(n, p1, p2):
        enfant = p2[1:3]
        for i in p1[1:-1]:
            if i not in enfant:
                enfant.append(i)
        enfant.append(0)
        enfant.insert(0,0)
        return enfant

    @classmethod
    def init_parents(cls, parent):
        cls.first_parent = parent[1 : -1]
        cls.population = [cls.first_parent]
        for _ in range(9):
            cls.population.append(random.sample(cls.first_parent, k = len(cls.first_parent)))
        return cls.population


class Interface():

    @classmethod
    def launch_app(cls):
        cls.crea_fenetre()
        cls.gene_route()
        cls.root.mainloop()

    @classmethod
    def crea_fenetre(cls):
        cls.root = tk.Tk()
        cls.root.title("Challenge Spatial - Groupe 2")
        cls.root.geometry("1000x1000")
        cls.root.bind("<Escape>", lambda x: cls.root.destroy())
        cls.crea_canva()

    @classmethod
    def crea_canva(cls):
        cls.canva = tk.Canvas(cls.root, scrollregion=(0,0,500,500), height=os.getenv('HAUTEUR'), width=os.getenv('LARGEUR'))  
        cls.canva.pack()
        cls.aff_points()

    @classmethod
    def aff_points(cls):
        # Génération des lieux et enregistrement en csv
        CSV.save_graph(Graph.creation_points(int(os.getenv("NB_LIEUX")), int(os.getenv("LARGEUR")), int(os.getenv("HAUTEUR"))))
        # Affichage des points
        cls.all_points = CSV.charger_graph()
        for k, v in cls.all_points.items():
            if k == 0:
                cls.canva.create_oval(v[0]-12, v[1]-12 , v[0]+12, v[1]+12, fill="red")
            else:
                cls.canva.create_oval(v[0]-12, v[1]-12 , v[0]+12, v[1]+12)
            cls.canva.create_text(v[0], v[1], text=str(k))
        cls.gene_matrice_cout()
    
    @classmethod
    def gene_matrice_cout(cls):
        cls.matrice = Graph.calcul_matrice_cout_od(int(os.getenv("NB_LIEUX")), cls.all_points)

    @classmethod
    def gene_route(cls):    
        cls.route = Route.generation_route()
        cls.gene_score_route()
        cls.create_line()

    @classmethod
    def gene_score_route(cls):
        cls.score = Route.calcul_distance_route(cls.route, cls.matrice)

    @classmethod
    def create_line(cls):
        cls.canva.create_line([cls.all_points[i] for i in cls.route], dash = (5, 2))

# Interface.launch_app()

AlgoGen.init_parents([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])