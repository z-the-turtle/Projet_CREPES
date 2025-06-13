import numpy as np
import matplotlib.pyplot as plt

# Données physiques
m = 1.0        # kg
c = 1000.0     # J/kg·K
A = 1.0        # m²
h = 15.0       # W/m²·K
dt = 1.0       # s
steps = 300    # nombre de pas de temps

# Coefficient thermique
k = (h * A) / (m * c)  # en 1/s

# Températures initiales
T_air_1 = [10.0]   # Bloc au-dessus d’un sol à 20°C
T_air_2 = [20.0]   # Bloc au-dessus d’un sol à 30°C


# Températures fixes (sols / thermostat)
T_sol_1 = 20.0
T_sol_2 = 10.0


# Évolution des températures
for t in range(steps):
    T_next_1 = T_air_1[-1] + k * (T_sol_1 - T_air_1[-1]) * dt
    T_next_2 = T_air_2[-1] + k * (T_sol_2 - T_air_2[-1]) * dt
    T_air_1.append(T_next_1)
    T_air_2.append(T_next_2)


# Affichage graphique
plt.plot(T_air_1, label="Sol à 20°C", color='orange')
plt.plot(T_air_2, label="Sol à 10°C", color='red')

plt.hlines([T_sol_1, T_sol_2], 0, steps, linestyles='dashed', colors=['orange', 'red'], alpha=0.3)

plt.xlabel("Temps (s)")
plt.ylabel("Température de l'air (°C)")
plt.title("Évolution thermique de 2 blocs d'air (loi de Newton)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
