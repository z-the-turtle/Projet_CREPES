from math import cos, sin, pi
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from fonction_découpage_capacité import colours, capacite
import matplotlib.patches as mpatches



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

# Define colors for each zone


def color_zones(ax):
    # choisir la resolution
    res = 100
    for lon in np.arange(-180, 180, 10):
        for lat in np.arange(-90, 90, res):
            cap = capacite(lat + res/2, lon + res/2)  # Center of the cell
            color = colours.get(cap, '#FF00FF')  # Default to magenta if not found
            print(f"lat={lat+res/2}, lon={lon+res/2}, cap={cap}, color={color}")
            rect = mpatches.Rectangle(
                (lon, lat), res, res,
                facecolor=color, alpha=0.6,  # More visible
                transform=ccrs.PlateCarree(),
                linewidth=0
            )
            ax.add_patch(rect)

# Créer la carte du monde
fig, ax = plot_world_map()
color_zones(ax)  # Color the zones

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

