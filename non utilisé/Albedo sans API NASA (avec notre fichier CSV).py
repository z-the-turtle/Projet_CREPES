import pandas as pd
import numpy as np
from math import sqrt

def charger_donnees_albedo(fichier_csv):
    """
    Charge les données d'albédo depuis le fichier CSV.

    Args:
        fichier_csv (str): Chemin vers le fichier CSV contenant les données d'albédo

    Returns:
        pandas.DataFrame: DataFrame contenant les données d'albédo
    """
    try:
        df = pd.read_csv(fichier_csv)
        # Nettoyer les en-têtes (supprimer les espaces)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        print(f"Erreur lors du chargement du fichier: {e}")
        return None

def distance_euclidienne(lat1, lon1, lat2, lon2):
    """
    Calcule la distance euclidienne entre deux points (approximation simple).
    Pour une précision géographique plus élevée, utilisez la formule de Haversine.

    Args:
        lat1, lon1: Coordonnées du premier point
        lat2, lon2: Coordonnées du second point

    Returns:
        float: Distance euclidienne
    """
    return sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def obtenir_albedo(latitude, longitude, df_albedo, methode='plus_proche'):
    """
    Trouve l'albédo pour des coordonnées données.

    Args:
        latitude (float): Latitude recherchée
        longitude (float): Longitude recherchée
        df_albedo (pandas.DataFrame): DataFrame contenant les données d'albédo
        methode (str): Méthode de recherche ('plus_proche' ou 'interpolation')

    Returns:
        dict: Dictionnaire contenant l'albédo et les métadonnées
              {'albedo': float, 'albedo_std': float, 'distance': float,
               'lat_trouve': float, 'lon_trouve': float, 'points_reussis': int}
        None si aucune donnée n'est trouvée
    """
    if df_albedo is None or df_albedo.empty:
        print("Aucune donnée disponible")
        return None

    # Calculer les distances pour tous les points
    df_albedo = df_albedo.copy()
    df_albedo['distance'] = df_albedo.apply(
        lambda row: distance_euclidienne(latitude, longitude, row['latitude'], row['longitude']),
        axis=1
    )

    if methode == 'plus_proche':
        # Trouver le point le plus proche
        point_proche = df_albedo.loc[df_albedo['distance'].idxmin()]

        return {
            'albedo': point_proche['albedo'],
            'albedo_std': point_proche['albedo_std'],
            'distance': point_proche['distance'],
            'lat_trouve': point_proche['latitude'],
            'lon_trouve': point_proche['longitude'],
            'points_reussis': point_proche['points_reussis'],
            'points_total': point_proche['points_total']
        }

    elif methode == 'interpolation':
        # Interpolation par moyenne pondérée des 4 points les plus proches
        n_points = min(4, len(df_albedo))
        points_proches = df_albedo.nsmallest(n_points, 'distance')

        # Éviter la division par zéro pour les distances très petites
        points_proches = points_proches.copy()
        points_proches['distance'] = points_proches['distance'].apply(lambda x: max(x, 1e-10))

        # Poids inversement proportionnels à la distance
        points_proches['poids'] = 1 / points_proches['distance']
        poids_total = points_proches['poids'].sum()

        # Moyenne pondérée
        albedo_interpole = (points_proches['albedo'] * points_proches['poids']).sum() / poids_total
        albedo_std_interpole = (points_proches['albedo_std'] * points_proches['poids']).sum() / poids_total

        return {
            'albedo': albedo_interpole,
            'albedo_std': albedo_std_interpole,
            'distance_moyenne': points_proches['distance'].mean(),
            'nombre_points_utilises': n_points,
            'methode': 'interpolation'
        }

def rechercher_albedo_simple(latitude, longitude, fichier_csv='albedo_lat_lon_multisampled_3pts.csv'):
    """
    Fonction simplifiée pour rechercher l'albédo.

    Args:
        latitude (float): Latitude recherchée
        longitude (float): Longitude recherchée
        fichier_csv (str): Chemin vers le fichier CSV

    Returns:
        float: Valeur d'albédo du point le plus proche
    """
    df = charger_donnees_albedo(fichier_csv)
    if df is None:
        return None

    resultat = obtenir_albedo(latitude, longitude, df)
    return resultat['albedo'] if resultat else None

#Exemple d'utilisation :
# albedo_simple = rechercher_albedo_simple(0,0)
# print(albedo_simple)