""" Contains the core logic of model.
This file  include functions or classes that define your model's behavior, calculations, data processing, etc. """
# model.py
import networkx as nx
import math

def eucl_dist(x1, y1, x2, y2):
    return round(math.sqrt((x1-x2)**2 + (y1-y2)**2))
