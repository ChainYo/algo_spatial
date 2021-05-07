import numpy as np
import pandas as pd 
from tkinter import * 
import random
import time


class Root:
    def __init__(self):
        self.root=Tk()
        self.root.title =("titre")
        self.root.geometry("1130x1130")
        self.root.minsize(720, 720)
        self.root.config(background="white")


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
        print(way)


    @classmethod
    def creation_points(cls, NB_LIEUX, LARGEUR, HAUTEUR):
        cls.liste_lieux = {}

        for i in range(NB_LIEUX):
            cls.x = random.randint(1, LARGEUR)
            cls.y = random.randint(1, HAUTEUR)
            cls.liste_lieux[i]=[cls.x, cls.y]

        # print(cls.liste_lieux)
        return cls.liste_lieux

    @classmethod
    def batiste(cls, s):
        return random.randint(0,10)


    @classmethod
    def charger_graph(cls):
        df  = pd.read_csv("out.csv")
        d = dict([(i,[a,b]) for i, a,b in zip(df["index"],df.X,df.Y)])
        print(d)

    @classmethod
    def save_graph(cls, value):
        df = pd.DataFrame.from_dict(data=value, orient='index', columns=['X', 'Y'])
        df.reset_index(inplace=True)
        df.to_csv('out.csv', index=False)

d = {100: [30, 5], 200: [20, 26], 2: [37, 37], 3: [31, 34], 4: [23, 40], 5: [48, 49], 6: [23, 24], 7: [22, 37], 8: [26, 47], 9: [3, 5]}
Route.save_graph(d)
Route.charger_graph()


