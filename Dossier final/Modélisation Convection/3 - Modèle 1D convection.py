import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np

# Paramètres animation
sol_width = 100
sol_height = 2
air_height = 5
bloc_width = 5
vitesse = 1  # pixels/frame
nb_blocs = sol_width // bloc_width

# Paramètres physiques
m = 1.0        # kg
c = 1000.0     # J/kg·K
A = 1.0        # m²
h = 15.0       # W/m²·K
dt = 1.0       # s
k = (h * A) / (m * c)  # coefficient thermique (1/s)

# Température du sol (fixe dans l'espace)
def sol_temperature(x):
    return 10 if x < sol_width / 2 else 20

# Températures initiales par bloc (en fonction de leur position)
bloc_positions = np.arange(0, sol_width, bloc_width)
bloc_temps = np.array([sol_temperature(x + bloc_width / 2) for x in bloc_positions], dtype=float)

# Initialisation figure
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(0, sol_width)
ax.set_ylim(0, sol_height + air_height + 2)
ax.axis('off')
plt.title("Masse d'air fragmentée : échanges thermiques avec loi de Newton", fontsize=14, pad=20)

# Sol visuel
sol_gauche = patches.Rectangle((0, 0), sol_width / 2, sol_height, facecolor='midnightblue', edgecolor='black')
sol_droite = patches.Rectangle((sol_width / 2, 0), sol_width / 2, sol_height, facecolor='lightcoral', edgecolor='black')
ax.add_patch(sol_gauche)
ax.add_patch(sol_droite)
ax.text(25, 0.5, "Sol nuit 10°C", ha='center', fontsize=10, color='white')
ax.text(75, 0.5, "Sol jour 20°C", ha='center', fontsize=10, color='black')

# Position verticale des blocs
y_air = sol_height + 0.5

# Création des blocs graphiques
blocs = []
labels = []

for i, x in enumerate(bloc_positions):
    temp = bloc_temps[i]
    color_ratio = (temp - 10) / 10
    rect = patches.Rectangle((x, y_air), bloc_width, air_height,
                             facecolor=(color_ratio, 0.2, 1 - color_ratio), edgecolor='black')
    ax.add_patch(rect)
    label = ax.text(x + bloc_width / 2, y_air + air_height / 2, f"{temp:.1f}°C",
                    ha='center', va='center', fontsize=9, color='white', weight='bold')
    blocs.append(rect)
    labels.append(label)

# Animation
def update(frame):
    global bloc_positions, bloc_temps

    # Avancer tous les blocs
    bloc_positions = (bloc_positions + vitesse) % sol_width

    for i in range(nb_blocs):
        x_center = (bloc_positions[i] + bloc_width / 2) % sol_width
        T_sol = sol_temperature(x_center)

        # Application de la loi de Newton pour mise à jour thermique
        T_air = bloc_temps[i]
        T_air_next = T_air + k * (T_sol - T_air) * dt
        bloc_temps[i] = T_air_next

        color_ratio = (bloc_temps[i] - 10) / 10
        color = (color_ratio, 0.2, 1 - color_ratio)

        blocs[i].set_x(bloc_positions[i])
        blocs[i].set_facecolor(color)

        labels[i].set_position((bloc_positions[i] + bloc_width / 2, y_air + air_height / 2))
        labels[i].set_text(f"{bloc_temps[i]:.1f}°C")

    return blocs + labels

ani = animation.FuncAnimation(fig, update, frames=300, interval=100, blit=True)
plt.tight_layout()
plt.show()

