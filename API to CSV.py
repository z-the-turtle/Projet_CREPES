import numpy as np
from datetime import datetime, timedelta
import requests
import csv

# Cache local
albedo_cache = {}

def get_albedo_estimation(latitude, longitude, start_date, end_date):
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

        down_radiation = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
        up_radiation = data['properties']['parameter']['ALLSKY_SFC_SW_UP']

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
    cache_key = f"{lat},{lng},{date_debut},{duree_simulation_jours}"
    if cache_key in albedo_cache:
        return albedo_cache[cache_key]

    date_debut_obj = datetime.strptime(date_debut, "%Y-%m-%d")
    date_fin_obj = date_debut_obj + timedelta(days=duree_simulation_jours-1)

    start_date_str = date_debut_obj.strftime("%Y%m%d")
    end_date_str = date_fin_obj.strftime("%Y%m%d")

    albedo_data = get_albedo_estimation(lat, lng, start_date_str, end_date_str)

    if albedo_data is None:
        raise Exception("Échec de récupération des données depuis l'API NASA POWER")

    valeurs_valides = [v for v in albedo_data.values() if v is not None and 0 <= v <= 1]

    if not valeurs_valides:
        raise Exception("Aucune donnée d'albédo valide trouvée")

    albedo_moyen = sum(valeurs_valides) / len(valeurs_valides)
    albedo_moyen = max(0, min(1, albedo_moyen))

    albedo_cache[cache_key] = albedo_moyen
    return albedo_moyen

# Paramètres de grille
step_rad = 0.5
latitudes = np.arange(-np.pi/2, np.pi/2, step_rad)
longitudes = np.arange(-np.pi, np.pi, step_rad)

# Période
date_debut = "2022-01-01"
duree_simulation_jours = 365

# Stockage des résultats
grid_cells = []

for lat in latitudes:
    for lon in longitudes:
        lat_centre_rad = lat + step_rad / 2
        lon_centre_rad = lon + step_rad / 2

        lat_deg = np.degrees(lat_centre_rad)
        lon_deg = np.degrees(lon_centre_rad)

        try:
            albedo = get_nasa_albedo(lat_deg, lon_deg, date_debut, duree_simulation_jours)
            grid_cells.append({
                "latitude": round(lat_deg, 4),
                "longitude": round(lon_deg, 4),
                "albedo": round(albedo, 4)
            })
        except Exception as e:
            print(f"[!] Erreur pour lat={lat_deg:.2f}, lon={lon_deg:.2f} : {e}")

# Sauvegarde dans un fichier CSV
csv_filename = "albedo_lat_lon.csv"
with open(csv_filename, mode='w', newline='') as csv_file:
    fieldnames = ["latitude", "longitude", "albedo"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for cell in grid_cells:
        writer.writerow(cell)

print(f"\n✅ Fichier CSV généré avec {len(grid_cells)} points : {csv_filename}")
