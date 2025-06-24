import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np

sol_l = 36e6          #largeur du sol
sol_h = 250e3         #hauteur du sol
air_h = 10e3          #hauteur des blocs d'air


# Grandeurs physiques
m = 1.0      #masse du bloc d'air (kg)
c = 1000.0   #capacité thermique massique (J/Kg/K)
A = 1.0      #surface d'échange thermique (m²)
h = 15.0     #coefficient d'échange thermique (W/(m²·K))
dt = 1.0     #pas de temps (s)
k = (h * A) / (m * c)     # coefficient thermique combiné (en 1/s) pour la loi de Newton

# Température du sol
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
