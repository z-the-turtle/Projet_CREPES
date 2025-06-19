import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np

sol_l = 36e6
sol_h = 250e3
air_h = 10e3

nb_blocs = 18
bloc_l = sol_l / nb_blocs
vitesse = 10

# Physique
m = 4e11
c = 1000.0
A = 2000e3
h = 15.0
dt = 24*3600/100
k = (h * A) / (m * c)

# Température du sol
def sol_temperature(x):
    return -10 if x < sol_l / 2 else 20 # Nuit à -10°C, Jour à 20°C (sans dégradé)
