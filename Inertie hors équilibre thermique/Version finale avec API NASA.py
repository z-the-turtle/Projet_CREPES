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
sigma = 5.67e-8  # CORRECTION: Constante de Stefan-Boltzmann (était 4.67*10**(-8))
pi = np.pi
puiss = np.array([1340, 0, 0])
epsilon = 0.71
PHI = 0.409  # precession angle rad  (23.45 deg)

# Cache pour stocker les albédos calculés par l'API NASA
albedo_cache = {}

def get_albedo_estimation(latitude, longitude, start_date, end_date):
    """Récupère l'estimation d'albédo depuis l'API NASA POWER"""
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

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
        print(f"Requête API NASA: {url}")
        print(f"Paramètres: {params}")

        response = requests.get(url, params=params, timeout=30)
        print(f"Status code: {response.status_code}")

        if response.status_code != 200:
            print(f"Erreur HTTP: {response.status_code}")
            print(f"Réponse: {response.text[:500]}")
            return None

        data = response.json()
        print("Réponse JSON reçue avec succès")

        # Vérifier la structure de la réponse
        if 'properties' not in data or 'parameter' not in data['properties']:
            print("Structure de réponse inattendue")
            print(f"Clés disponibles: {data.keys()}")
            return None

        # Extraire les données de rayonnement solaire
        parameters = data['properties']['parameter']
        if 'ALLSKY_SFC_SW_DWN' not in parameters or 'ALLSKY_SFC_SW_UP' not in parameters:
            print("Paramètres de rayonnement non trouvés dans la réponse")
            return None

        down_radiation = parameters['ALLSKY_SFC_SW_DWN']
        up_radiation = parameters['ALLSKY_SFC_SW_UP']

        # Calculer l'albédo pour chaque jour
        albedo_estimation = {}
        for date in down_radiation.keys():
            down_val = down_radiation[date]
            up_val = up_radiation[date]

            if down_val and up_val and down_val > 0:
                albedo_val = up_val / down_val
                # Limiter l'albédo entre 0 et 1
                albedo_estimation[date] = max(0, min(1, albedo_val))
            else:
                albedo_estimation[date] = None

        return albedo_estimation

    except requests.RequestException as e:
        print(f"Erreur de requête: {e}")
        return None
    except Exception as e:
        print(f"Erreur lors du traitement: {e}")
        return None

def get_nasa_albedo(lat, lng, date_debut="2022-01-01", duree_simulation_jours=365):
    """Récupère l'albédo moyen depuis l'API NASA pour une position donnée"""
    # Clé pour le cache
    cache_key = f"{lat},{lng},{date_debut},{duree_simulation_jours}"

    if cache_key in albedo_cache:
        print(f"Albédo trouvé dans le cache: {albedo_cache[cache_key]:.3f}")
        return albedo_cache[cache_key]

    # Limiter les requêtes à 1 an maximum pour éviter les timeouts
    duree_limitee = min(duree_simulation_jours, 365)

    # Convertir les dates au format requis par l'API
    date_debut_obj = datetime.strptime(date_debut, "%Y-%m-%d")
    date_fin_obj = date_debut_obj + timedelta(days=duree_limitee-1)

    start_date_str = date_debut_obj.strftime("%Y%m%d")
    end_date_str = date_fin_obj.strftime("%Y%m%d")

    print(f"Récupération albédo NASA pour lat={lat}, lng={lng} du {start_date_str} au {end_date_str}")

    # Appel à l'API
    albedo_data = get_albedo_estimation(lat, lng, start_date_str, end_date_str)

    if albedo_data is None:
        print("Échec de récupération des données NASA, utilisation d'une valeur par défaut")
        # Utiliser une valeur par défaut raisonnable
        albedo_defaut = 0.3  # Valeur moyenne pour terre/végétation
        albedo_cache[cache_key] = albedo_defaut
        return albedo_defaut

    # Calculer la moyenne des albédos valides
    valeurs_valides = [v for v in albedo_data.values() if v is not None and 0 <= v <= 1]

    if not valeurs_valides:
        print("Aucune donnée d'albédo valide, utilisation d'une valeur par défaut")
        albedo_defaut = 0.3
        albedo_cache[cache_key] = albedo_defaut
        return albedo_defaut

    albedo_moyen = sum(valeurs_valides) / len(valeurs_valides)
    # Limiter l'albédo entre 0.05 et 0.95 pour éviter les valeurs extrêmes
    albedo_moyen = max(0.05, min(0.95, albedo_moyen))
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

def capacite(lat, lng, t=0):
    """Capacité thermique massique en fonction de la localisation"""
    # Capacités thermiques (constantes)
    capa_glace = 2060
    capa_eau = 4185
    capa_neige = 2092
    capa_desert = 835
    capa_foret = 2400
    capa_terre = 750

    if lat >= 65 or lat <= -65:
        return capa_glace
    elif lng >= 160 or lng <= -140:
        return capa_eau
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



def dpuiss(lat, lng, t):
    """Puissance reçue par une maille"""
    puiss_local = np.array([1340, 0, 0])

    # Calcul du jour et de l'heure à partir du temps t
    j = t / 86400  # Jour en valeur continue
    h = (t % 86400) / 3600  # Heure dans la journée courante

    B = PHI * cos(2 * pi * j / 365)

    er = np.array([
        cos(lng + ((h - 8) * 2 * pi / 24) - pi/2) * sin(B + (pi / 2) - lat),
        sin(B + (pi / 2) - lat) * sin(lng + ((h - 8) * 2 * pi / 24) - pi/2),
        cos((B + (pi / 2) - lat))
    ])

    vec = np.dot(er, puiss_local)

    # CORRECTION: Retourner 0 si vec <= 0 (pas de soleil), sinon vec
    if vec > 0:
        return vec
    else:
        return 0

def Temp(lat, lng, date_debut="2022-01-01", nb_jours_simulation=30):
    """Simulation de température avec albédo NASA"""
    print(f"Début simulation pour lat={lat}, lng={lng}")
    print(f"Date de début: {date_debut}")
    print(f"Durée: {nb_jours_simulation} jours")

    # Récupérer l'albédo depuis l'API NASA
    try:
        albedo_local = get_nasa_albedo(lat, lng, date_debut, nb_jours_simulation)
        print(f"Albédo utilisé: {albedo_local:.3f}")
    except Exception as e:
        print(f"Erreur albédo NASA: {e}")
        albedo_local = 0.3  # Valeur par défaut
        print(f"Utilisation albédo par défaut: {albedo_local}")

    t = 0
    liste_T_atm = []
    liste_T = []
    liste_t = []
    T_T = 280  # Température initiale surface
    T_atm = 250  # Température initiale atmosphère

    temps_final = nb_jours_simulation * 86400

    while t < temps_final:
        # CORRECTION: Utiliser albedo_local au lieu d'appeler albedo() à chaque itération
        puissance_recue = dpuiss(lat, lng, t)

        dT_T = ((1 - albedo_local) * puissance_recue
                + sigma * (epsilon * T_atm ** 4 - T_T ** 4)) * dt / (
                capacite(lat, lng) * rho_terre * Prof)

        dT_atm = (sigma * (epsilon * T_T ** 4 - 2 * epsilon * T_atm ** 4)) * dt / (
                capa_atm * rho_atmosphère * epaisseur_atm)

        T_T += dT_T
        T_atm += dT_atm

        liste_T.append(T_T - 273)  # Conversion en degrés celsius
        liste_T_atm.append(T_atm - 273)  # Conversion en degrés celsius
        liste_t.append(t)

        t += dt

    # Affichage des résultats
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.plot(np.array(liste_t) / 86400, liste_T, label='Température surface', linewidth=2)
    plt.plot(np.array(liste_t) / 86400, liste_T_atm, label='Température atmosphère', linewidth=2)

    ax.set_xlabel('Temps (jours)', fontsize=15)
    ax.set_ylabel('Température (°C)', fontsize=15)
    ax.set_title(f'Simulation - Lat:{lat}° Lng:{lng}° - Albédo:{albedo_local:.3f}', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    #plt.show()

    print(f"Température finale surface: {liste_T[-1]:.1f}°C")
    print(f"Température finale atmosphère: {liste_T_atm[-1]:.1f}°C")

    #return liste_T

# Exemple d'utilisation
if __name__ == "__main__":
    try:
        print("=== Simulation avec API NASA ===")
        # Test avec une simulation plus courte pour commencer
        Temp(45, 4, date_debut="2022-06-01", nb_jours_simulation=500)  # 500 jours seulement

    except Exception as e:
        print(f"Erreur lors de la simulation: {e}")
        print("Vérifiez votre connexion internet et que l'API NASA POWER est accessible.")