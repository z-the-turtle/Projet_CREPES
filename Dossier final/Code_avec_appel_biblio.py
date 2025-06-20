import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, pi
import requests
from datetime import datetime, timedelta
from librairie_puissances import *


# Constantes et paramètres
dt = 600  # Pas de temps
rho_terre = 5500  # Masse volumique de la Terre
rho_atmosphère = 1.2  # Masse volumique de l'atmosphère
capa_atm = 1000
epaisseur_atm = 13000  # Epaisseur de l'atmosphère
Prof = 0.6  # Profondeur typique de variation de température
sigma = 5.67e-8  # CORRECTION: Constante de Stefan-Boltzmann (était 4.67*10**(-8))
pi = np.pi
epsilon = 0.71
PHI = 0.409  # precession angle rad  (23.45 deg)

# Cache pour stocker les albédos calculés par l'API NASA

def Temp(lat, lng, nb_jours_simulation=30):
    """Simulation de température avec albédo NASA, sans appel API"""
    print(f"Début simulation pour lat={lat}, lng={lng}")
    print(f"Durée: {nb_jours_simulation} jours")

    albedo_local = rechercher_albedo_simple(lat,lng)
    print(f"Albédo utilisé: {albedo_local:.3f}")

    T_T = 280
    T_atm = 220
    liste_T = []
    liste_T_atm = []
    liste_t = []

    t = 0  # Temps en secondes depuis le 1er janvier minuit
    temps_final = nb_jours_simulation * 86400  # Temps final en secondes

    while t < temps_final:
        dT_T = ((1 - albedo_local) * P_inc_solar(lat, lng, t)
                + sigma * (epsilon * T_atm ** 4 - T_T ** 4)) * dt / (
                capacite(lat, lng) * rho_terre * Prof)
        dT_atm = (sigma * (epsilon * T_T ** 4 - 2 * epsilon * T_atm ** 4)) * dt / (
                capa_atm * rho_atmosphère * epaisseur_atm)
        T_T += dT_T
        T_atm += dT_atm
        liste_T.append(T_T-273) #Conversion en degrés celsius
        liste_T_atm.append(T_atm-273) #Conversion en degrés celsius
        liste_t.append(t)
        t += dt

    fig, ax = plt.subplots()

    plt.plot(liste_t, liste_T)
    ax.set_xlabel('temps (s)', fontsize=15)
    ax.set_ylabel('Température à la surface (°C)', fontsize=15)
    plt.show()
    return 0

# Exemple d'utilisation
if __name__ == "__main__":
    try:
        print("=== Simulation avec API NASA ===")
        Temp(48,7, nb_jours_simulation=500)  # 500 jours seulement

    except Exception as e:
        print(f"Erreur lors de la simulation: {e}")
        print("Vérifiez votre connexion internet et que l'API NASA POWER est accessible.")