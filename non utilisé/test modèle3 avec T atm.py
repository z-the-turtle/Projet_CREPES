import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Constantes
S = 1361  # Constante solaire en W/m^2
S4 = S / 4
sigma = 5.67e-8  # Constante de Stefan-Boltzmann en W/m^2/K^4
w = 2 * math.pi / 24  # En h^-1
effet_de_serre = 33  # Effet de serre moyen en degrés Celsius

def calculate_temperature(S, A, sigma, lat, lon, t):
    """
    Calcule la température d'équilibre radiatif de la Terre.

    :param S: Constante solaire en W/m^2
    :param A: Albédo terrestre
    :param sigma: Constante de Stefan-Boltzmann en W/m^2/K^4
    :param lat: Latitude en degrés
    :param lon: Longitude en degrés
    :param t: Temps en heures décimales
    :return: Température d'équilibre en Kelvin
    """
    # Calcul de l'énergie reçue en fonction de la latitude
    Salbedo = S4 * (1 - A)
    Salbedo_effet_de_serre = Salbedo + 244  # obtenue par calcul avec rayon incident et réfléchi
    Slatlon = (Salbedo_effet_de_serre * np.cos(w * t) *
               np.sin((90 - lat) * 2 * math.pi / 360) *
               np.sin(lon * 2 * math.pi / 360) +
               Salbedo_effet_de_serre * np.sin(w * t) *
               np.sin((90 - lat) * 2 * math.pi / 360) *
               np.cos(lon * 2 * math.pi / 360))

    # Vérifier que la latitude et la longitude sont dans la plage valide
    if lat < -90 or lat > 90:
        raise ValueError("La latitude doit être comprise entre -90 et 90 degrés.")
    elif lon < -180 or lon > 180:
        raise ValueError("La longitude doit être comprise entre -180 et 180 degrés.")
    elif Slatlon < 0:
        raise ValueError("Nous sommes la nuit.")

    # Énergie moyenne reçue par unité de surface
    energy_received = Slatlon

    # Température d'équilibre
    T = (energy_received / sigma) ** 0.25
    return T

def calculate_average_atmospheric_temperature(T_surface, effet_de_serre):
    """
    Calcule la température moyenne de l'atmosphère en ajoutant l'effet de serre.

    :param T_surface: Température de surface en Kelvin
    :param effet_de_serre: Effet de serre en degrés Celsius
    :return: Température moyenne de l'atmosphère en Kelvin
    """
    T_atmosphere = T_surface - effet_de_serre
    return T_atmosphere

# Dictionnaire des valeurs d'albédo pour chaque partie de la Terre
data_albedo = {
    "Amérique du Nord": 0.25,
    "Amérique du Sud": 0.18,
    "Europe de l'Ouest": 0.25,
    "Europe de l'Est": 0.3,
    "Asie du Sud": 0.15,
    "Asie de l'Est": 0.2,
    "Asie du Sud-Est": 0.2,
    "Afrique du Nord": 0.25,
    "Afrique Sub-saharienne": 0.18,
    "Afrique_Désertique": 0.45,
    "Océans": 0.12,
    "Pole Nord": 0.75,
    "Pole Sud": 0.8
}

def determiner_partie_terre(latitude, longitude):
    """
    Détermine la partie de la Terre en fonction des coordonnées de latitude et de longitude.

    :param latitude: Latitude en degrés
    :param longitude: Longitude en degrés
    :return: Nom de la partie de la Terre
    """
    if latitude >= 60:  # Pole Nord
        return "Pole Nord"
    elif latitude <= -60:  # Pole Sud
        return "Pole Sud"
    elif 30 <= latitude <= 60 and -130 <= longitude <= -60:  # Amérique du Nord
        return "Amérique du Nord"
    elif -60 <= latitude <= 15 and -90 <= longitude <= -30:  # Amérique du Sud
        return "Amérique du Sud"
    elif 45 <= latitude <= 70 and -10 <= longitude <= 40:  # Europe
        if -10 <= longitude <= 20:  # Europe de l'Ouest
            return "Europe de l'Ouest"
        else:  # Europe de l'Est
            return "Europe de l'Est"
    elif -10 <= latitude <= 40 and 60 <= longitude <= 160:  # Asie
        if 5 <= latitude <= 30 and 60 <= longitude <= 120:  # Asie du Sud
            return "Asie du Sud"
        elif 30 <= latitude <= 50 and 100 <= longitude <= 140:  # Asie de l'Est
            return "Asie de l'Est"
        else:  # Asie du Sud-Est
            return "Asie du Sud-Est"
    elif 15 <= latitude <= 30 and -20 <= longitude <= 40:  # Afrique_Désertique
        return "Afrique_Désertique"
    elif -35 <= latitude <= 15 and -20 <= longitude <= 50:  # Afrique
        if latitude > 0:  # Afrique du Nord
            return "Afrique du Nord"
        else:  # Afrique Sub-saharienne
            return "Afrique Sub-saharienne"
    else:
        return "Océans"

def obtenir_albedo(lat, lon):
    """
    Obtient l'albédo en fonction des coordonnées de latitude et de longitude.

    :param lat: Latitude en degrés
    :param lon: Longitude en degrés
    :return: Albédo
    """
    partie_terre = determiner_partie_terre(lat, lon)
    return data_albedo[partie_terre]

try:
    # Entrer la latitude et la longitude
    lat = float(input("Entrer la latitude (entre -90 et 90 degrés) : "))
    lon = float(input("Entrer la longitude (entre -180 et 180 degrés) : "))
    time_input = input("Entrer le temps UTC-0 à Greenwich (format HH:MM) : ")

    # Diviser l'entrée du temps en heures et minutes
    hours, minutes = map(int, time_input.split(':'))
    t = hours + minutes / 60.0  # Convertir en heures décimales

    # Obtention de l'albédo pour les coordonnées spécifiées
    A = obtenir_albedo(lat, lon)

    # Calcul de la température moyenne de la Terre
    T_surface = calculate_temperature(S, A, sigma, lat, lon, t - 6)  # t-6 pour avoir la température maximale à Greenwich à 12h
    print(f"La température moyenne de la surface de la Terre à la latitude {lat}° et la longitude {lon}° est de {T_surface:.2f} K")
    print(f"Ce qui correspond à {T_surface - 273.15:.2f} °C")

    # Calcul de la température moyenne de l'atmosphère
    T_atmosphere = calculate_average_atmospheric_temperature(T_surface, effet_de_serre)
    print(f"La température moyenne de l'atmosphère à la latitude {lat}° et la longitude {lon}° est de {T_atmosphere:.2f} K")
    print(f"Ce qui correspond à {T_atmosphere - 273.15:.2f} °C")

    # Affichage du globe avec le point
    fig, ax = plt.subplots(figsize=(10, 7))

    # Création de la carte
    m = Basemap(projection='ortho', lat_0=lat, lon_0=lon, resolution='l', ax=ax)
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='coral', lake_color='aqua')
    m.drawmapboundary(fill_color='aqua')

    # Ajouter le point spécifié
    x, y = m(lon, lat)
    m.plot(x, y, 'ro', markersize=10, label=f'Latitude: {lat}°, Longitude: {lon}°')
    plt.title(f"Position à la latitude {lat}° et la longitude {lon}°")
    plt.legend()

    plt.show()

except ValueError as e:
    print(f"Erreur: {e}")
