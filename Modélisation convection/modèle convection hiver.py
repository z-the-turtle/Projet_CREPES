import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np

# Paramètres généraux
sol_width = 36e6
sol_height = 250e3
air_height = 10e3

nb_blocs = 18
bloc_width = sol_width / nb_blocs
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
    return -10 if x < sol_width / 2 else 20  # Nuit à -10°C, Jour à 20°C

# Initialisation
bloc_positions = np.arange(0, sol_width, bloc_width)
bloc_temps = np.array([sol_temperature(x + bloc_width / 2) for x in bloc_positions], dtype=float)

sol_y = 4
y_air = sol_y + sol_height + 100000

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, sol_width)
ax.set_ylim(0, y_air + air_height + 3)
ax.axis('off')
plt.title("Échange thermique (loi de Newton)", fontsize=18)

# Sol visuel
ax.add_patch(patches.Rectangle((0, sol_y), sol_width / 2, sol_height, facecolor='midnightblue'))
ax.add_patch(patches.Rectangle((sol_width / 2, sol_y), sol_width / 2, sol_height, facecolor='lightcoral'))
ax.text(9000000, sol_y + 100000, "Sol nuit -10°C", ha='center', fontsize=14, color='white')
ax.text(26000000, sol_y + 100000, "Sol jour 20°C", ha='center', fontsize=14, color='black')

blocs = []
labels = []
arrows = []
power_labels = []

max_arrow_length = 100000
scaling_factor = 0.08 #on sait pas trop

for i, x in enumerate(bloc_positions):
    temp = bloc_temps[i]
    color_ratio = (temp + 10) / 30  # Échelle adaptée [-10 ; 20] → [0 ; 1]
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

    bloc_positions[:] = (bloc_positions + vitesse*dt) % sol_width

    for i in range(nb_blocs):
        x_center = (bloc_positions[i] + vitesse*dt) % sol_width
        T_sol = sol_temperature(x_center)
        T_air = bloc_temps[i]
        T_air_next = T_air + k * (T_sol - T_air) * dt
        bloc_temps[i] = T_air_next

        color_ratio = (T_air_next + 10) / 30
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

ani = animation.FuncAnimation(fig, update, frames=300, interval=20, blit=True)
n_steps = 100
def puissance_echange(t_heure):

    dt_sim = t_heure / n_steps
    positions_sim = bloc_positions.copy()
    temps_air_sim = bloc_temps.copy()

    for step in range(n_steps):
        positions_sim = (positions_sim + vitesse * dt_sim) % sol_width
        for i in range(nb_blocs):
            x_center = (positions_sim[i] + bloc_width / 2) % sol_width
            T_sol = sol_temperature(x_center)
            T_air = temps_air_sim[i]
            T_air_next = T_air + k * (T_sol - T_air) * dt_sim
            temps_air_sim[i] = T_air_next

    # DEBUG ICI, après 100 étapes
    for i in range(nb_blocs):
        x_center = (positions_sim[i] + bloc_width / 2) % sol_width
        T_sol = sol_temperature(x_center)
        T_air = temps_air_sim[i]
        # print(f"Bloc {i} : T_air = {T_air:.2f}°C, T_sol = {T_sol:.2f}°C")

        puissances = [h * A * (T_sol - T_air) for i in range(nb_blocs)]
        print(puissances)

    return sum(puissances)


temps = np.linspace(0, dt*n_steps, 100)
puissances = [puissance_echange(t) for t in temps]



plt.figure(figsize=(10, 5))
plt.plot(temps, puissances, color='orange', lw=2)
plt.xlabel("Temps (s)")
plt.ylabel("Puissance totale échangée (W)")
plt.title("Puissance échangée sol-air sur 24 heures")
plt.grid(True)
plt.tight_layout()
plt.show()

