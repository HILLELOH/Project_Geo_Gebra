import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

class Shape:
    def __init__(self,coords):
        self.coords= np.array(coords)

    def __repr__(self):
        return str(self.__class__).split(".")[1][:]

