import ephem
from datetime import datetime

def calculate_sunrise_sunset(latitude, longitude, date):
    # Convertir les coordonnées en radians
    lat = ephem.degrees(str(latitude))
    lon = ephem.degrees(str(longitude))

    # Initialiser l'observateur
    observer = ephem.Observer()
    observer.lat = lat
    observer.lon = lon
    observer.date = date

    # Calculer le lever et le coucher du soleil
    sunrise = observer.previous_rising(ephem.Sun(), use_center=True)
    sunset = observer.next_setting(ephem.Sun(), use_center=True)

    # Convertir les résultats en format lisible
    sunrise_str = ephem.localtime(sunrise).strftime('%H:%M:%S')
    sunset_str = ephem.localtime(sunset).strftime('%H:%M:%S')

    return sunrise_str, sunset_str

# Entrer les coordonnées GPS
latitude = float(input("Entrez la latitude en degrés décimaux (positif pour Nord, négatif pour Sud) : "))
longitude = float(input("Entrez la longitude en degrés décimaux (positif pour Est, négatif pour Ouest) : "))

# Entrer la date pour le calcul
date_str = input("Entrez la date au format YYYY-MM-DD (laissez vide pour utiliser la date actuelle) : ")
if date_str:
    date = datetime.strptime(date_str, '%Y-%m-%d')
else:
    date = datetime.now()

# Calculer le lever et le coucher du soleil
sunrise, sunset = calculate_sunrise_sunset(latitude, longitude, date)

print("Lever du soleil:", sunrise)
print("Coucher du soleil:", sunset)
