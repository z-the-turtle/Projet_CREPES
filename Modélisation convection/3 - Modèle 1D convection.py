import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np


# PARAMÈTRES DE BASE


# Dimensions de la scène
sol_width = 100       # largeur totale du sol
sol_height = 2        # hauteur du sol (zone colorée en bas)
air_height = 5        # hauteur des blocs d'air
bloc_width = 5        # largeur d'un bloc d'air
vitesse = 1           # vitesse de déplacement des blocs (en pixels par frame)
nb_blocs = sol_width // bloc_width  # nombre total de blocs

# Paramètres physiques
m = 1.0        # masse de chaque bloc (kg)
c = 1000.0     # capacité thermique (J/kg·K)
A = 1.0        # surface de contact (m²)
h = 15.0       # coefficient d'échange thermique (W/m²·K)
dt = 1.0       # durée d'une étape (s)
k = (h * A) / (m * c)  # coefficient thermique simplifié (1/s)


# TEMPÉRATURE DU SOL


# Fonction de température fixe du sol (bimodale)
def sol_temperature(x):
    return 10 if x < sol_width / 2 else 20

# Température initiale de chaque bloc d'air (en fonction de sa position)
bloc_positions = np.arange(0, sol_width, bloc_width)
bloc_temps = np.array([sol_temperature(x + bloc_width / 2) for x in bloc_positions], dtype=float)


# INITIALISATION DU DESSIN


fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(0, sol_width)
ax.set_ylim(0, sol_height + air_height + 2)
ax.axis('off')  # cacher les axes
plt.title("Masse d'air fragmentée : échanges thermiques avec loi de Newton", fontsize=14, pad=20)

# Dessin du sol (2 zones : nuit et jour)
sol_gauche = patches.Rectangle((0, 0), sol_width / 2, sol_height, facecolor='midnightblue', edgecolor='black')
sol_droite = patches.Rectangle((sol_width / 2, 0), sol_width / 2, sol_height, facecolor='lightcoral', edgecolor='black')
ax.add_patch(sol_gauche)
ax.add_patch(sol_droite)

# Labels sol
ax.text(25, 0.5, "Sol nuit 10°C", ha='center', fontsize=10, color='white')
ax.text(75, 0.5, "Sol jour 20°C", ha='center', fontsize=10, color='black')

# Position verticale des blocs d'air
y_air = sol_height + 0.5


# CRÉATION BLOCS D'AIR


blocs = []
labels = []

for i, x in enumerate(bloc_positions):
    temp = bloc_temps[i]
    color_ratio = (temp - 10) / 10  # Normalise entre 0 (bleu) et 1 (rouge)
    rect = patches.Rectangle((x, y_air), bloc_width, air_height,
                             facecolor=(color_ratio, 0.2, 1 - color_ratio), edgecolor='black')
    ax.add_patch(rect)
    
    label = ax.text(x + bloc_width / 2, y_air + air_height / 2, f"{temp:.1f}°C",
                    ha='center', va='center', fontsize=9, color='white', weight='bold')
    
    blocs.append(rect)
    labels.append(label)


# FONCTION D'ANIMATION


def update(frame):
    global bloc_positions, bloc_temps

    # Déplacement horizontal des blocs
    bloc_positions = (bloc_positions + vitesse) % sol_width

    # Mise à jour de chaque bloc
    for i in range(nb_blocs):
        x_center = (bloc_positions[i] + bloc_width / 2) % sol_width
        T_sol = sol_temperature(x_center)

