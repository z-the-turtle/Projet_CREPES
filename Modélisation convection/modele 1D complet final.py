import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np

# Paramètres généraux
sol_width = 100  #largeur du sol
sol_height = 2   #hauteur du sol
air_height = 10  #hauteur des blocs d'air

nb_blocs = 18  # ici 18 blocs
bloc_width = sol_width / nb_blocs  # ≈ 5.5555

vitesse = 1

# Grandeurs physiques
m = 1.0      #masse du bloc d'air (kg)
c = 1000.0   #capacité thermique massique (J/Kg/K)
A = 1.0      #surface d'échange thermique (m²)
h = 15.0     #coefficient d'échange thermique (W/m²·K)
dt = 1.0     #pas de temps (s)
k = (h * A) / (m * c)     # coefficient thermique combiné (en 1/s) pour la loi de Newton

# Température du sol
def sol_temperature(x):
    return 10 if x < sol_width / 2 else 20

# Initialisation
bloc_positions = np.arange(0, sol_width, bloc_width)
bloc_temps = np.array([sol_temperature(x + bloc_width / 2) for x in bloc_positions], dtype=float)

sol_y = 4
y_air = sol_y + sol_height + 0.5

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, sol_width)
ax.set_ylim(0, y_air + air_height + 3)
ax.axis('off')
plt.title("Échange thermique (loi de Newton) — flèches directionnelles", fontsize=18)

# Sol visuel
ax.add_patch(patches.Rectangle((0, sol_y), sol_width / 2, sol_height, facecolor='midnightblue'))
ax.add_patch(patches.Rectangle((sol_width / 2, sol_y), sol_width / 2, sol_height, facecolor='lightcoral'))
ax.text(25, sol_y + 0.5, "Sol nuit 10°C", ha='center', fontsize=14, color='white')
ax.text(75, sol_y + 0.5, "Sol jour 20°C", ha='center', fontsize=14, color='black')

blocs = []
labels = []
arrows = []
power_labels = []

max_arrow_length = 4.0
scaling_factor = 0.08

for i, x in enumerate(bloc_positions):
    temp = bloc_temps[i]
    color_ratio = (temp - 10) / 10
    rect = patches.Rectangle((x, y_air), bloc_width, air_height,
                             facecolor=(color_ratio, 0.2, 1 - color_ratio), edgecolor='black')
    ax.add_patch(rect)

    label = ax.text(x + bloc_width / 2, y_air + air_height / 2, f"{temp:.1f}°C",
                    ha='center', va='center', fontsize=12, color='white', weight='bold')

    arrow = ax.arrow(0, 0, 0, 0, head_width=3, head_length=0.6, fc='orange', ec='orange')
    power_label = ax.text(x + bloc_width / 2, sol_y - 1, "",
                          ha='center', va='top', fontsize=12, color='orange')

    blocs.append(rect)
    labels.append(label)
    arrows.append(arrow)
    power_labels.append(power_label)

def update(frame):
    global bloc_positions, bloc_temps

    bloc_positions[:] = (bloc_positions + vitesse) % sol_width

    for i in range(nb_blocs):
        x_center = (bloc_positions[i] + bloc_width / 2) % sol_width
        T_sol = sol_temperature(x_center)
        T_air = bloc_temps[i]
        T_air_next = T_air + k * (T_sol - T_air) * dt
        bloc_temps[i] = T_air_next

        color_ratio = (T_air_next - 10) / 10
        color = (color_ratio, 0.2, 1 - color_ratio)
        blocs[i].set_x(bloc_positions[i])
        blocs[i].set_facecolor(color)

        labels[i].set_position((bloc_positions[i] + bloc_width / 2, y_air + air_height / 2))
        labels[i].set_text(f"{T_air_next:.1f}°C")

        P = h * A * (T_sol - T_air)
        arrow_length = np.clip(abs(P) * scaling_factor, 0.3, max_arrow_length)

        arrows[i].remove()

        x_arrow = bloc_positions[i] + bloc_width / 2
        if P > 0:
            y_arrow = sol_y + sol_height
            dy = arrow_length
        else:
            y_arrow = y_air
            dy = -arrow_length

        arrows[i] = ax.arrow(x_arrow, y_arrow, 0, dy,
                             head_width=3, head_length=0.6, fc='orange', ec='orange')

        power_labels[i].set_position((x_arrow, sol_y - 0.5))
        power_labels[i].set_text(f"{P:+.1f} W")

    return blocs + labels + arrows + power_labels

ani = animation.FuncAnimation(fig, update, frames=300, interval=100, blit=True)

def puissance_echange(t_heure):
    """
    Calcule la puissance totale échangée entre sol et air
    à un temps t donné en heures réelles.

    t_heure : float, temps en heures

    Retourne : puissance totale en Watts (float)
    """

    # Conversion temps réel en pas de temps (dt simulé)
    # dt simulé correspond à 20 heures réelles
    dt_sim = t_heure / 20.0

    # On calcule la nouvelle position des blocs (en simulé)
    new_positions = (bloc_positions + vitesse * dt_sim) % sol_width

    # On copie les températures actuelles pour simuler l'évolution sur dt_sim
    temps_air_sim = bloc_temps.copy()

    # On applique l'évolution de la température sur dt_sim (approximation)
    # Ici on fait juste une étape discrète avec k*dt_sim
    for i in range(nb_blocs):
        x_center = (new_positions[i] + bloc_width / 2) % sol_width
        T_sol = sol_temperature(x_center)
        T_air = temps_air_sim[i]
        T_air_next = T_air + k * (T_sol - T_air) * dt_sim
        temps_air_sim[i] = T_air_next

    # Calcul de la puissance totale échangée (somme sur tous les blocs)
    puissances = []
    for i in range(nb_blocs):
        x_center = (new_positions[i] + bloc_width / 2) % sol_width
        T_sol = sol_temperature(x_center)
        T_air = temps_air_sim[i]
        P = h * A * (T_sol - T_air)
        puissances.append(P)

    P_totale = sum(puissances)
    return P_totale


temps = np.linspace(0, 24, 100)  # 100 points entre 0 et 24h
puissances = [puissance_echange(t) for t in temps]

plt.figure(figsize=(10,5))
plt.plot(temps, puissances, color='orange', lw=2)
plt.xlabel("Temps (heures)")
plt.ylabel("Puissance totale échangée (W)")
plt.title("Puissance échangée sol-air sur 24 heures")
plt.grid(True)
plt.show()


plt.tight_layout()
plt.show()

