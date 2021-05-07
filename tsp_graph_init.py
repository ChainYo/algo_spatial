import numpy as np
import pandas as pd 
import tkinter as tk
import random
import time

class Lieu():
    
    @classmethod
    def init_lieu(cls, x, y):
        return np.array([x, y])
    
    @classmethod
    def calc_distance(cls, vector1, vector2):
        return np.linalg.norm(vector1 - vector2)

# Fenêtre de l'app
root = tk.Tk()
root.title("Challenge Spatial")
root.geometry("1000x1000")

# Ajout du canvas
c = tk.Canvas(root, scrollregion=(0,0,500,500), height=hauteur, width=largeur)  
c.pack()

# Lancement de la page
root.mainloop()