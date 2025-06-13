import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, pi
import requests
from datetime import datetime, timedelta

# Constantes et paramètres
dt = 600  # Pas de temps
rho_terre = 5500  # Masse volumique de la Terre
rho_atmosphère = 1.2  # Masse volumique de l'atmosphère
capa_atm = 1000
epaisseur_atm = 13000  # Epaisseur de l'atmosphère
Prof = 0.6  # Profondeur typique de variation de température
sigma = 4.67*10**(-8)  # Constante de Stefan-Boltzmann
pi = np.pi
puiss = np.array([1340, 0, 0])
epsilon = 0.71

# Cache pour stocker les albédos calculés par l'API NASA
albedo_cache = {}

def get_albedo_estimation(latitude, longitude, start_date, end_date):
    """Récupère l'estimation d'albédo depuis l'API NASA POWER"""
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point"

    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,ALLSKY_SFC_SW_UP",
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "start": start_date,
        "end": end_date,
        "format": "JSON"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extraire les données de rayonnement solaire
        down_radiation = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
        up_radiation = data['properties']['parameter']['ALLSKY_SFC_SW_UP']

        # Calculer l'albédo pour chaque jour
        albedo_estimation = {}
        for date in down_radiation.keys():
            if down_radiation[date] != 0 and down_radiation[date] is not None:
                albedo_estimation[date] = up_radiation[date] / down_radiation[date]
            else:
                albedo_estimation[date] = None

        return albedo_estimation
    except Exception as e:
        print(f"Erreur lors de la récupération des données NASA: {e}")
        return None

def get_nasa_albedo(lat, lng, date_debut="2022-01-01", duree_simulation_jours=365):
    """
    Récupère l'albédo moyen depuis l'API NASA pour une position donnée

    Args:
        lat: latitude en degrés
        lng: longitude en degrés
        date_debut: date de début au format "YYYY-MM-DD"
        duree_simulation_jours: durée de la simulation en jours

    Returns:
        float: albédo moyen

    Raises:
        Exception: Si l'API NASA ne peut pas fournir de données valides
    """
    # Clé pour le cache
    cache_key = f"{lat},{lng},{date_debut},{duree_simulation_jours}"

    if cache_key in albedo_cache:
        return albedo_cache[cache_key]

    # Convertir les dates au format requis par l'API
    date_debut_obj = datetime.strptime(date_debut, "%Y-%m-%d")
    date_fin_obj = date_debut_obj + timedelta(days=duree_simulation_jours-1)

    start_date_str = date_debut_obj.strftime("%Y%m%d")
    end_date_str = date_fin_obj.strftime("%Y%m%d")

    print(f"Récupération albédo NASA pour lat={lat}, lng={lng} du {start_date_str} au {end_date_str}")

    # Appel à l'API
    albedo_data = get_albedo_estimation(lat, lng, start_date_str, end_date_str)

    if albedo_data is None:
        raise Exception("Échec de récupération des données depuis l'API NASA POWER")

    # Calculer la moyenne des albédos valides
    valeurs_valides = [v for v in albedo_data.values() if v is not None and 0 <= v <= 1]

    if not valeurs_valides:
        raise Exception("Aucune donnée d'albédo valide trouvée dans la réponse de l'API NASA")

    albedo_moyen = sum(valeurs_valides) / len(valeurs_valides)
    # Limiter l'albédo entre 0 et 1
    albedo_moyen = max(0, min(1, albedo_moyen))
    print(f"Albédo NASA calculé: {albedo_moyen:.3f} (basé sur {len(valeurs_valides)} mesures)")

    # Mettre en cache
    albedo_cache[cache_key] = albedo_moyen
    return albedo_moyen

def convertir(degres):
    """Permet de convertir une valeur en degrés en radians"""
    rad = (degres * 2 * pi) / 360
    return rad

alpha = convertir(23.5)  # angle Terre
R = 6371000  # rayon de la Terre

# Albédos par défaut supprimés - utilisation exclusive de l'API NASA

def albedo(lat, lng, date_debut="2022-01-01", duree_simulation=365):
    """
    Fonction d'albédo qui utilise exclusivement l'API NASA

    Args:
        lat: latitude en degrés
        lng: longitude en degrés
        date_debut: date de début de simulation
        duree_simulation: durée en jours

    Returns:
        float: albédo moyen depuis l'API NASA

    Raises:
        Exception: Si l'API NASA ne peut pas fournir de données
    """
    return get_nasa_albedo(lat, lng, date_debut, duree_simulation)

# Capacités thermiques (inchangées)
capa_glace = 2060
capa_eau = 4185
capa_neige = 2092
capa_desert = 835
capa_foret = 2400
capa_terre = 750

def capacite(lat, lng):
    """Capacité thermique massique en fonction de la localisation"""
    if lat >= 65 or lat <= -65:
        return capa_glace
    elif lng >= 160 or lng <= -140:
        return capa_eau
    # [Reste du code de la fonction capacite inchangé]
    elif lng <= -120 and lng >= -140 and lat >= -65 and lat <= 50:
        return capa_eau
    elif lng <= -80 and lng >= -120 and lat >= -65 and lat <= 20:
        return capa_eau
    elif lng <= 140 and lng >= -60 and lat >= -65 and lat <= -30:
        return capa_eau
    elif lng <= -60 and lng >= -80 and lat >= 10 and lat <= 40:
        return capa_eau
    elif lng <= 0 and lng >= -60 and lat >= 30 and lat <= 65:
        return capa_eau
    elif lng <= -20 and lng >= -60 and lat >= 10 and lat <= 30:
        return capa_eau
    elif lng <= 10 and lng >= -60 and lat >= 0 and lat <= 10:
        return capa_eau
    elif lng <= 10 and lng >= -40 and lat >= -30 and lat <= 0:
        return capa_eau
    elif lng <= 120 and lng >= 40 and lat >= 10 and lat <= 20:
        return capa_eau
    elif lng <= 100 and lng >= 40 and lat >= -30 and lat <= 10:
        return capa_eau
    elif lng <= 120 and lng >= 100 and lat >= -30 and lat <= -10:
        return capa_eau
    elif lng <= 140 and lng >= 120 and lat >= 0 and lat <= 30:
        return capa_eau
    elif lng <= 160 and lng >= 140 and lat >= 0 and lat <= 60:
        return capa_eau
    elif lng <= -60 and lng >= -80 and lat <= 10 and lat >= 0:
        return capa_foret
    elif lng <= -40 and lng >= -80 and lat <= 0 and lat >= -30:
        return capa_foret
    elif lng <= -60 and lng >= -80 and lat <= -30 and lat >= -65:
        return capa_foret
    elif lng <= 40 and lng >= -20 and lat <= 20 and lat >= -10:
        return capa_foret
    elif lng <= 140 and lng >= 100 and lat <= 40 and lat >= 30:
        return capa_foret
    elif lng <= 120 and lng >= 100 and lat <= 30 and lat >= 0:
        return capa_foret
    elif lng <= 160 and lng >= 100 and lat <= 0 and lat >= -10:
        return capa_foret
    elif lng <= 40 and lng >= 10 and lat <= -10 and lat >= -30:
        return capa_desert
    elif lng <= 60 and lng >= 0 and lat <= 40 and lat >= 20:
        return capa_desert
    elif lng <= 160 and lng >= 120 and lat <= -10 and lat >= -30:
        return capa_desert
    elif lng <= -80 and lng >= -120 and lat <= 50 and lat >= 20:
        return capa_terre
    elif lng <= 140 and lng >= 0 and lat <= 60 and lat >= 30:
        return capa_terre
    elif lng <= 60 and lng >= 40 and lat <= 40 and lat >= 20:
        return capa_terre
    elif lng <= 100 and lng >= 40 and lat <= 40 and lat >= 20:
        return capa_terre
    else:
        return capa_neige

def B_point(j):
    """Calcule l'angle d'inclinaison de la Terre"""
    return alpha * cos(2 * pi * j / 365)

def dpuiss(lat, lng, h, j, puiss):
    """Puissance reçue par une maille"""
    B = B_point(j)
    er = np.array([
        cos(lng + ((h - 8) * 2 * pi / 24) - pi/2) * sin(B + (pi / 2) - lat),
        sin(B + (pi / 2) - lat) * sin(lng + ((h - 8) * 2 * pi / 24) - pi/2),
        cos((B + (pi / 2) - lat))
    ])

    vec = np.dot(er, puiss)

    if vec <= 0:
        return abs(vec)
    else:
        return 0

def Temp(lat, lng, date_debut="2022-01-01", nb_jours_simulation=365):
    """
    Simulation de température avec albédo NASA exclusivement

    Args:
        lat, lng: coordonnées
        date_debut: date de début au format "YYYY-MM-DD"
        nb_jours_simulation: nombre de jours à simuler

    Raises:
        Exception: Si l'API NASA ne peut pas fournir les données d'albédo
    """
    print(f"Début simulation pour lat={lat}, lng={lng}")
    print(f"Date de début: {date_debut}")
    print("Utilisation exclusive de l'API NASA pour l'albédo")

    # Récupérer l'albédo depuis l'API NASA (obligatoire)
    try:
        albedo_local = albedo(lat, lng, date_debut, nb_jours_simulation)
        print(f"Albédo NASA récupéré: {albedo_local:.3f}")
    except Exception as e:
        print(f"ERREUR: {e}")
        raise Exception(f"Impossible de continuer la simulation sans les données d'albédo NASA: {e}")

    jour = 0
    liste_T_atm = []
    liste_T = []
    liste_t = []
    T_T = 280
    T_atm = 250

    while jour < nb_jours_simulation:
        t = 0
        while t < 84600:  # Une journée
            h = t // 3600
            liste_T.append(T_T)
            liste_T_atm.append(T_atm)
            liste_t.append(t + jour * 84600)

            dT_T = ((1 - albedo_local) * dpuiss(lat, lng, h, jour, puiss) +
                   sigma * (epsilon * T_atm**4 - T_T**4)) * dt / (capacite(lat, lng) * rho_terre * Prof)
            dT_atm = sigma * (epsilon * T_T**4 - 2 * epsilon * T_atm**4) * dt / (capa_atm * rho_atmosphère * epaisseur_atm)

            T_T = T_T + dT_T
            T_atm = T_atm + dT_atm
            t = t + dt
        jour = jour + 1

        if jour % 30 == 0:  # Affichage du progrès
            print(f"Jour {jour}/{nb_jours_simulation} - T_surface: {T_T:.1f}K")

    # Affichage des résultats
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.plot(np.array(liste_t) / 86400, liste_T, label='Température surface')
    ax.set_xlabel('Temps (jours)', fontsize=15)
    ax.set_ylabel('Température à la surface (K)', fontsize=15)
    ax.set_title(f'Simulation température - Lat:{lat}° Lng:{lng}° - Albédo NASA:{albedo_local:.3f}')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

    return liste_T, liste_T_atm, liste_t

# Exemple d'utilisation
if __name__ == "__main__":
    try:
        # Test avec l'API NASA (mode exclusif)
        print("=== Simulation avec API NASA ===")
        Temp(45,4, date_debut="2012-06-01", nb_jours_simulation=3000)  # Paris



    except Exception as e:
        print(f"Erreur lors de la simulation: {e}")
        print("Vérifiez votre connexion internet et que l'API NASA POWER est accessible.")