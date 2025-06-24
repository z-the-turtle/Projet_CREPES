import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np


# PARAMÈTRES DE SIMULATION


# Dimensions du sol et de l'air
sol_width = 36e6         # Largeur du sol (36 000 km)
sol_height = 250e3       # Hauteur du sol dans le schéma (250 km)
air_height = 10e3        # Hauteur de l'air (10 km)

nb_blocs = 18                        # Nombre de blocs d'air
bloc_width = sol_width / nb_blocs   # Largeur d’un bloc
vitesse = 10                        # Vitesse horizontale de déplacement (m/s)

# Paramètres physiques pour le calcul de température
m = 4e11       # Masse d’un bloc d’air
c = 1000.0     # Capacité thermique massique
A = 2000e3     # Surface de contact sol-air (2 000 000 m²)
h = 15.0       # Coefficient d’échange thermique (loi de Newton)
dt = 24*3600/100   # Pas de temps (fraction de 24 h en secondes)
k = (h * A) / (m * c)  # Coefficient pour le calcul de température de l’air


# FONCTION TEMPÉRATURE DU SOL


def sol_temperature(x):
    # Le sol est à -10°C à gauche (nuit), +20°C à droite (jour)
    return -10 if x < sol_width / 2 else 20


# INITIALISATION DES BLOCS D'AIR ET TEMPERATURE


bloc_positions = np.arange(0, sol_width, bloc_width)
bloc_temps = np.array([sol_temperature(x + bloc_width / 2) for x in bloc_positions], dtype=float)

# Coordonnées verticales pour le schéma
sol_y = 4
y_air = sol_y + sol_height + 100000

# Préparation de la figure matplotlib
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, sol_width)
ax.set_ylim(0, y_air + air_height + 3)
ax.axis('off')
plt.title("Échange thermique (loi de Newton)", fontsize=18)


# DESSIN DU SOL (nuit/jour)


ax.add_patch(patches.Rectangle((0, sol_y), sol_width / 2, sol_height, facecolor='midnightblue'))  # Zone nuit
ax.add_patch(patches.Rectangle((sol_width / 2, sol_y), sol_width / 2, sol_height, facecolor='lightcoral'))  # Zone jour
ax.text(9000000, sol_y + 100000, "Sol nuit -10°C", ha='center', fontsize=14, color='white')
ax.text(26000000, sol_y + 100000, "Sol jour 20°C", ha='center', fontsize=14, color='black')


# BLOCS D'AIR INITIAUX


blocs = []          # Rectangles représentant les blocs d’air
labels = []         # Labels de température des blocs
arrows = []         # Flèches de transfert de chaleur
power_labels = []   # Labels indiquant la puissance échangée

max_arrow_length = 100000  # Longueur maximale des flèches
scaling_factor = 0.08      # Facteur d’échelle pour la flèche

# Création des objets graphiques
for i, x in enumerate(bloc_positions):
    temp = bloc_temps[i]
    color_ratio = (temp + 10) / 30  # Mise à l’échelle couleur entre -10°C et 20°C
    rect = patches.Rectangle((x, y_air), bloc_width, air_height,
                             facecolor=(color_ratio, 0.2, 1 - color_ratio), edgecolor='black')
    ax.add_patch(rect)

    label = ax.text(x + bloc_width / 2, y_air + air_height / 2, f"{temp:.1f}°C",
                    ha='center', va='center', fontsize=12, color='white', weight='bold')

    # Création de flèches et labels (initialement vides)
    arrow = ax.arrow(0, 0, 0, 0, head_width=3, head_length=0.6, fc='orange', ec='orange')
    power_label = ax.text(x + bloc_width / 2, sol_y - 1, "", ha='center', va='top', fontsize=12, color='orange')

    blocs.append(rect)
    labels.append(label)
    arrows.append(arrow)
    power_labels.append(power_label)


# FONCTION D’ANIMATION


def update(frame):
    global bloc_positions, bloc_temps

    # Mise à jour de la position des blocs (ils se déplacent sur le sol)
    bloc_positions[:] = (bloc_positions + vitesse * dt) % sol_width

    # Calcul physique et mise à jour graphique
    for i in range(nb_blocs):
        x_center = (bloc_positions[i] + vitesse * dt) % sol_width
        T_sol = sol_temperature(x_center)
        T_air = bloc_temps[i]
        T_air_next = T_air + k * (T_sol - T_air) * dt
        bloc_temps[i] = T_air_next

        # Couleur du bloc d’air selon température
        color_ratio = (T_air_next + 10) / 30
        color = (color_ratio, 0.2, 1 - color_ratio)
        blocs[i].set_x(bloc_positions[i])
        blocs[i].set_facecolor(color)

        # Mise à jour des labels de température
        labels[i].set_position((bloc_positions[i] + bloc_width / 2, y_air + air_height / 2))
        labels[i].set_text(f"{T_air_next:.1f}°C")

        # Calcul de la puissance échangée (loi de Newton)
        P = h * A * (T_sol - T_air)
        arrow_length = np.clip(abs(P) * scaling_factor, 0.3, max_arrow_length)

        arrows[i].remove()  # Supprimer ancienne flèche

        # Nouvelle flèche selon sens du transfert de chaleur
        x_arrow = bloc_positions[i] + bloc_width / 2
        if P > 0:
            y_arrow = sol_y + sol_height  # Chaleur vers le haut
            dy = arrow_length
        else:
            y_arrow = y_air               # Chaleur vers le sol
            dy = -arrow_length

        arrows[i] = ax.arrow(x_arrow, y_arrow, 0, dy, head_width=3, head_length=0.6, fc='orange', ec='orange')

        # Mise à jour du label de puissance
        power_labels[i].set_position((x_arrow, sol_y - 0.5))
        power_labels[i].set_text(f"{P:+.1f} W")

    return blocs + labels + arrows + power_labels

# Lancer l'animation
ani = animation.FuncAnimation(fig, update, frames=300, interval=20, blit=True)


# CALCUL DE LA PUISSANCE TOTALE ÉCHANGÉE (POUR UN GRAPHIQUE)

n_steps = 100

def puissance_echange(t_heure):
    """Calcule la puissance totale échangée à un temps donné (en secondes)"""
    dt_sim = t_heure / n_steps
    positions_sim = bloc_positions.copy()
    temps_air_sim = bloc_temps.copy()

    # Simulation sur n_steps petits pas de temps
    for step in range(n_steps):
        positions_sim = (positions_sim + vitesse * dt_sim) % sol_width
        for i in range(nb_blocs):
            x_center = (positions_sim[i] + bloc_width / 2) % sol_width
            T_sol = sol_temperature(x_center)
            T_air = temps_air_sim[i]
            T_air_next = T_air + k * (T_sol - T_air) * dt_sim
            temps_air_sim[i] = T_air_next

    # Calcul final de la puissance échangée par chaque bloc
    puissances = []
    for i in range(nb_blocs):
        x_center = (positions_sim[i] + bloc_width / 2) % sol_width
        T_sol = sol_temperature(x_center)
        T_air = temps_air_sim[i]
        puissances.append(h * A * (T_sol - T_air))

    return sum(puissances)  # Puissance totale


# AFFICHAGE DU GRAPHE FINAL

temps = np.linspace(0, dt * n_steps, 100)            # Échelle de temps (en secondes)
puissances = [puissance_echange(t) for t in temps]   # Calcul de puissance totale à chaque instant

plt.figure(figsize=(10, 5))
plt.plot(temps, puissances, color='orange', lw=2)
plt.xlabel("Temps (s)")
plt.ylabel("Puissance totale échangée (W)")
plt.title("Puissance échangée sol-air sur 24 heures")
plt.grid(True)
plt.tight_layout()
plt.show()
