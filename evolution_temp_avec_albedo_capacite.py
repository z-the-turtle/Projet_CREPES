import matplotlib.pyplot as plt
import numpy as np
import requests

# Constantes
Ps = 800  # Puissance solaire max (W/m²)
profondeur = 0.5  # profondeur en mètre
rho_eau = 1000  # densité eau kg/m3
sigma = 5.67e-8  # constante Stefan-Boltzmann
Beta = 0.5  # proportion rayonnement renvoyé par atmosphère
dt = 3600  # pas de temps en secondes (1h)
pi = np.pi

# Capacités thermiques massiques en J/kg.K
glace = 2060
eau = 4185
neige = 2092
desert = 830
foret = 2400
terre = 750


def capacite(lat, lng):
    # Fonction qui retourne capacité thermique massique (J/kg.K) selon localisation
    if lat >= 65 or lat <= -65 :
        return glace
    elif lng >= 160 or lng <= -140 :
        return eau
    elif lng <= -120 and lng >= -140 and lat >= -65 and lat <= 50 :
        return eau
    elif lng <= -80 and lng >= -120 and lat >= -65 and lat <= 20 :
        return eau
    elif lng <= 140 and lng >= -60 and lat >= -65 and lat <= -30 :
        return eau
    elif lng <= -60 and lng >= -80 and lat >= 10 and lat <= 40 :
        return eau
    elif lng <= 0 and lng >= -60 and lat >= 30 and lat <= 65 :
        return eau
    elif lng <= -20 and lng >= -60 and lat >= 10 and lat <= 30 :
        return eau
    elif lng <= 10 and lng >= -60 and lat >= 0 and lat <= 10 :
        return eau
    elif lng <= 10 and lng >= -40 and lat >= -30 and lat <= 0 :
        return eau
    elif lng <= 120 and lng >= 40 and lat >= 10 and lat <= 20 :
        return eau
    elif lng <= 100 and lng >= 40 and lat >= -30 and lat <= 10 :
        return eau
    elif lng <= 120 and lng >= 100 and lat >= -30 and lat <= -10 :
        return eau
    elif lng <= 140 and lng >= 120 and lat >= 0 and lat <= 30 :
        return eau
    elif lng <= 160 and lng >= 140 and lat >= 0 and lat <= 60 :
        return eau
    elif lng <= -60 and lng >= -80 and lat <= 10 and lat >= 0 :
        return foret
    elif lng <= -40 and lng >= -80 and lat <= 0 and lat >= -30 :
        return foret
    elif lng <= -60 and lng >= -80 and lat <= -30 and lat >= -65 :
        return foret
    elif lng <= 40 and lng >= -20 and lat <= 20 and lat >= -10 :
        return foret
    elif lng <= 140 and lng >= 100 and lat <= 40 and lat >= 30 :
        return foret
    elif lng <= 120 and lng >= 100 and lat <= 30 and lat >= 0 :
        return foret
    elif lng <= 160 and lng >= 100 and lat <= 0 and lat >= -10 :
        return foret
    elif lng <= 40 and lng >= 10 and lat <= -10 and lat >= -30 :
        return desert
    elif lng <= 60 and lng >= 0 and lat <= 40 and lat >= 20 :
        return desert
    elif lng <= 160 and lng >= 120 and lat <= -10 and lat >= -30 :
        return desert
    elif lng <= -80 and lng >= -120 and lat <= 50 and lat >= 20 :
        return terre
    elif lng <= 140 and lng >= 0 and lat <= 60 and lat >= 30 :
        return terre
    elif lng <= 60 and lng >= 40 and lat <= 40 and lat >= 20 :
        return terre
    elif lng <= 100 and lng >= 40 and lat <= 40 and lat >= 20 :
        return terre
    else:
        return neige


def get_albedo_estimation(latitude, longitude, start_date, end_date):
    # Récupérer albédo moyen via NASA POWER API
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
    response = requests.get(url, params=params)
    data = response.json()

    allsky = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
    clearsky = data['properties']['parameter']['ALLSKY_SFC_SW_UP']

    albedo_estimation = {}
    for date in allsky.keys():
        if clearsky[date] != 0:
            albedo_estimation[date] = clearsky[date] / allsky[date]
        else:
            albedo_estimation[date] = None

    valeurs = [v for v in albedo_estimation.values() if v is not None]
    if len(valeurs) > 0:
        return sum(valeurs) / len(valeurs)
    else:
        return 0.3  # valeur par défaut si aucune donnée


def P_rec(t_sec):
    # Rayonnement solaire incident en fonction du temps (s)
    # On considère la journée de 86400s (24h)
    t = t_sec % 86400
    if t < 28800:  # avant 8h du matin, pas de rayonnement
        return 0
    elif 28800 <= t <= 72000:  # de 8h à 20h
        return Ps * np.sin((t - 28800) * pi / 43200)
    else:
        return 0


def calcul_temperature(latitude, longitude, start_date, end_date, duree_jours=10):
    # Récupération des paramètres
    C_massique = capacite(latitude, longitude)
    albedo_moyen = get_albedo_estimation(latitude, longitude, start_date, end_date)

    # Capacité thermique volumique = masse volumique * capacité thermique massique
    C_volumique = rho_eau * C_massique  # approximé avec densité eau

    profondeur_sol = profondeur

    # Initialisation variables
    T = 290  # Température initiale (K)
    t = 0
    dt_sec = dt  # pas de temps en secondes (1h)
    liste_T = []
    liste_t = []

    # Boucle de calcul sur durée en secondes
    duree_sec = duree_jours * 86400

    while t < duree_sec:
        liste_T.append(T)
        liste_t.append(t)
        Pr = P_rec(t)

        # Equation de bilan énergétique simplifiée
        dT = dt_sec * (1 - albedo_moyen) * (1 + albedo_moyen * Beta * (1 - albedo_moyen)) * Pr / (C_volumique * profondeur_sol) \
             - dt_sec * sigma * (T ** 4) * (1 - (1 - albedo_moyen) * Beta) / (C_volumique * profondeur_sol)

        T = T + dT
        t += dt_sec

    return liste_t, liste_T, albedo_moyen, C_massique


if __name__ == "__main__":
    # appel
    latitude = float(input("entrez valeur latitude entre -90° et 90°"))
    longitude = float(input("entrez valeur longitude entre -180° et 180°"))
    start_date = "20220101" #une année
    end_date = "20221231"

    temps, temperatures, albedo_moy, capacite_therm = calcul_temperature(latitude, longitude, start_date, end_date, duree_jours=30)

    print(f"Albédo moyen sur la période: {albedo_moy:.3f}") #albedo oyen sur une année au point donné
    print(f"Capacité thermique massique estimée: {capacite_therm} J/kg.K")

    # Affichage graphique
    plt.plot(np.array(temps) / 3600, temperatures)
    plt.xlabel("Temps (heures)")
    plt.ylabel("Température (K)")
    plt.title(f"Evolution température à lat={latitude}, lon={longitude}")
    plt.grid()
    plt.show()
