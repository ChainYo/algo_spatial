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
