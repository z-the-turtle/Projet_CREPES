from math import cos, sin, pi
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


# Fonction pour créer une carte du monde avec Cartopy
def plot_world_map():
    """créer une carte du monde où l'on peut cliquer sur un point pour afficher la température"""
    fig = plt.figure(figsize=(10, 6))

    # Création de la carte du monde en utilisant la fonction Plate Carrée (planisphère)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Ajout des éléments de la carte
    ax.coastlines()
    ax.gridlines(draw_labels=True)

    return fig, ax

# Créer la carte du monde
fig, ax = plot_world_map()

# Fonction pour obtenir les coordonnées des clics
def onclick(event):
    if event.inaxes == ax:

        lon, lat = ax.projection.transform_point(event.xdata, event.ydata, ccrs.PlateCarree())
        print(f'coordonnée: Longitude = {lon:.2f}, Latitude = {lat:.2f}')
        
        return lon, lat 


# Lier l'événement de clic à la fonction onclick
cid = fig.canvas.mpl_connect('button_press_event', onclick)
#afficher carte
plt.title('World Map')
plt.show()

