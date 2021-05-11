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
        return cls.matrix

    @classmethod
    def plus_proche_voisin(cls, chiffre):
        new_list = list(np.argsort(cls.matrix[chiffre]))
        new_list.remove(chiffre)
        return new_list

class AlgoGen():
    
    @classmethod
    def selection(cls, liste):
        return sorted(liste, key=lambda k: k['score'])[:10]

    @classmethod
    def mutation(cls, mutant, n = 3):
        cpt = round(len(mutant) / n)
        if cpt == 1:
            cpt = 2
        index = random.randint(0, len(mutant) - 3)
        mutant[index: index + cpt] = random.sample(mutant[index: index + cpt], k = cpt)
        return mutant

    @classmethod
    def cross_over(cls, p1, p2):
        index = random.randint(1, len(p1)-2)
        cpt =  round((len(p1) - index) / 2)
        p1 = (random.sample(p2[index:index+cpt], k=cpt))
        for i in p2[1 : -1]:
            if i not in p1:
                p1.append(i)
        p1.append(0)
        p1.insert(0, 0)
        return(p1)

    @classmethod
    def init_parents(cls, parent):
        cls.population = [parent]
        for _ in range(9):
            cls.population.append([0] + random.sample(parent[1 : -1], k = len(parent[1 : -1])) + [0])
        return cls.population

    @classmethod
    def calc_score(cls, liste, matrice):
        cls.scores_routes = []
        for i in liste:
            cls.scores_routes.append({"route": i, "score": Route.calcul_distance_route(i, matrice)})
        return cls.scores_routes

    @classmethod
    def crea_couple(cls):
        cls.index_couple = list(range(10))
        random.shuffle(cls.index_couple)
        cls.couples = []
        for i in range(0, len(cls.index_couple), 2):
            cls.couples.append([cls.index_couple[i], cls.index_couple[i+1]])
        return cls.couples

    @classmethod
    def reproduction(cls, population, matrice):
        cls.enfants = []
        for _ in range(int(os.getenv("TAUX_REPRODUCTION"))):
            for i in cls.crea_couple():
                cls.enfants.append(cls.cross_over(population[i[0]]["route"], population[i[1]]["route"]))
        # map(cls.mutation, cls.enfants[random.randint(0, len(cls.enfants)-1)])
        cls.enfants_notes = cls.calc_score(cls.enfants, matrice)
        for enfant in cls.enfants_notes:
            if enfant not in population:
                population.append(enfant)
        return cls.selection(population)

class Interface():

    @classmethod
    def launch_app(cls):
        cls.crea_fenetre()
        cls.gene_route()
        cls.population = AlgoGen.calc_score(AlgoGen.init_parents(cls.route), cls.matrice)
        for i in range(100):
            cls.population = AlgoGen.reproduction(cls.population, cls.matrice)
            print(f"Génération n°{i}")
            print(cls.population[0]["score"], cls.population[0]["route"])
            print(cls.population[1]["score"], cls.population[1]["route"])
            print(cls.population[2]["score"], cls.population[2]["route"])
            print("============================")
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

Interface.launch_app()
