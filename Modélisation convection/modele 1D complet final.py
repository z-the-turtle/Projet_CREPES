import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np

# Paramètres de l'animation
sol_width = 100         # largeur totale du sol en pixels
sol_height = 2          # hauteur du sol (zone fixe)
air_height = 5          # hauteur des blocs d'air
bloc_width = 5          # largeur de chaque bloc d'air
vitesse = 1             # vitesse de déplacement des blocs (pixels par frame)
nb_blocs = sol_width // bloc_width  # nombre total de blocs pour couvrir toute la largeur du sol

# Paramètres physiques pour la loi de Newton du refroidissement/chauffage
m = 1.0                 # masse du bloc d'air (kg)
c = 1000.0              # capacité calorifique massique (J/kg·K)
A = 1.0                 # surface d'échange thermique (m²)
h = 15.0                # coefficient d'échange thermique (W/m²·K)
dt = 1.0                # pas de temps (s)
k = (h * A) / (m * c)   # coefficient thermique combiné (en 1/s) pour la loi de Newton

# Fonction définissant la température fixe du sol selon la position horizontale x
def sol_temperature(x):
    # Sol divisé en deux zones : à gauche 10°C (nuit), à droite 20°C (jour)
    return 10 if x < sol_width / 2 else 20

# Initialisation des positions horizontales des blocs d'air
bloc_positions = np.arange(0, sol_width, bloc_width)

# Initialisation des températures des blocs d'air selon leur position initiale (température du sol en dessous)
bloc_temps = np.array([sol_temperature(x + bloc_width / 2) for x in bloc_positions], dtype=float)

# Création de la figure et de l'axe pour le tracé
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(0, sol_width)                                # limites horizontales
ax.set_ylim(0, sol_height + air_height + 2)              # limites verticales (sol + air + marge)
ax.axis('off')                                           # on supprime les axes pour un affichage propre
plt.title("Masse d'air fragmentée : échanges thermiques avec loi de Newton", fontsize=14, pad=20)

# Représentation visuelle du sol (rectangle divisé en deux zones)
sol_gauche = patches.Rectangle((0, 0), sol_width / 2, sol_height, facecolor='midnightblue', edgecolor='black')
sol_droite = patches.Rectangle((sol_width / 2, 0), sol_width / 2, sol_height, facecolor='lightcoral', edgecolor='black')
ax.add_patch(sol_gauche)                                 # ajouter la zone nuit (10°C)
ax.add_patch(sol_droite)                                 # ajouter la zone jour (20°C)

# Textes explicatifs pour les zones du sol
ax.text(25, 0.5, "Sol nuit 10°C", ha='center', fontsize=10, color='white')
ax.text(75, 0.5, "Sol jour 20°C", ha='center', fontsize=10, color='black')

# Hauteur verticale où sont placés les blocs d'air (au-dessus du sol)
y_air = sol_height + 0.5

# Création graphique des blocs d'air et des étiquettes de température
blocs = []   # liste pour stocker les objets Rectangle des blocs
labels = []  # liste pour stocker les objets Text des températures

for i, x in enumerate(bloc_positions):
    temp = bloc_temps[i]                              # température initiale du bloc
    color_ratio = (temp - 10) / 10                    # normalisation entre 0 et 1 (pour couleur)
    # couleur dégradée entre bleu (froid) et rouge (chaud)
    rect = patches.Rectangle((x, y_air), bloc_width, air_height,
                             facecolor=(color_ratio, 0.2, 1 - color_ratio), edgecolor='black')
    ax.add_patch(rect)                                # ajouter le bloc au graphique
    # ajouter le texte affichant la température au centre du bloc
    label = ax.text(x + bloc_width / 2, y_air + air_height / 2, f"{temp:.1f}°C",
                    ha='center', va='center', fontsize=9, color='white', weight='bold')
    blocs.append(rect)                                # stocker le bloc graphique
    labels.append(label)                              # stocker le texte

# Fonction d'animation appelée à chaque frame
def update(frame):
    global bloc_positions, bloc_temps

    # Mise à jour des positions : décalage horizontal des blocs, avec retour à 0 après la largeur totale
    bloc_positions = (bloc_positions + vitesse) % sol_width

    # Mise à jour des températures des blocs selon la loi de Newton (refroidissement/chauffage)
    for i in range(nb_blocs):
        # position horizontale actuelle du centre du bloc (modulo largeur sol)
        x_center = (bloc_positions[i] + bloc_width / 2) % sol_width

        # température fixe du sol sous le bloc (selon la position)
        T_sol = sol_temperature(x_center)

        # température actuelle du bloc
        T_air = bloc_temps[i]

        # calcul de la température au pas de temps suivant selon la loi de Newton
        T_air_next = T_air + k * (T_sol - T_air) * dt

        # mise à jour de la température dans le tableau
        bloc_temps[i] = T_air_next

        # recalcul de la couleur basée sur la température (0 pour 10°C, 1 pour 20°C)
        color_ratio = (bloc_temps[i] - 10) / 10
        color = (color_ratio, 0.2, 1 - color_ratio)

        # mise à jour graphique : position et couleur du bloc
        blocs[i].set_x(bloc_positions[i])
        blocs[i].set_facecolor(color)

        # mise à jour du texte de température et de sa position
        labels[i].set_position((bloc_positions[i] + bloc_width / 2, y_air + air_height / 2))
        labels[i].set_text(f"{bloc_temps[i]:.1f}°C")

    # on retourne tous les objets modifiés pour animation (blit=True)
    return blocs + labels

# Lancement de l'animation (300 frames, 100 ms entre chaque)
ani = animation.FuncAnimation(fig, update, frames=300, interval=100, blit=True)

# Ajustement de la mise en page et affichage
plt.tight_layout()
plt.show()
