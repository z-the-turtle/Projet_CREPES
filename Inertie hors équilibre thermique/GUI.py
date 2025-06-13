from math import cos, sin, pi
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from fonction_découpage_capacité import colours, capacite
import matplotlib.patches as mpatches
from Temp_Terre_et_atm_dynamiques_avec_infrarouge import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    # Use a finer grid to cover the whole map
    res = 10
    for lon in np.arange(-180, 180, res):
        for lat in np.arange(-90, 90, res):
            cap = capacite(lat + res/2, lon + res/2)  # Center of the cell
            color = colours.get(cap, '#FF00FF')  # Default to magenta if not found
            # Debug print can be commented out if not needed
            # print(f"lat={lat+res/2}, lon={lon+res/2}, cap={cap}, color={color}")
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
ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())

# --- Tkinter GUI Setup ---
root = tk.Tk()
root.title("Carte du monde et Température")
root.geometry("1200x600")

# --- Frames for layout ---
left_frame = ttk.Frame(root, width=600, height=600)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
right_frame = ttk.Frame(root, width=600, height=600)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# --- Matplotlib Figure for World Map ---
fig_map = plt.Figure(figsize=(6, 6))
ax_map = fig_map.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax_map.coastlines()
ax_map.gridlines(draw_labels=True)
ax_map.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())

# Color zones
res = 10
for lon in np.arange(-180, 180, res):
    for lat in np.arange(-90, 90, res):
        cap = capacite(lat + res/2, lon + res/2)
        color = colours.get(cap, '#FF00FF')
        rect = mpatches.Rectangle(
            (lon, lat), res, res,
            facecolor=color, alpha=0.6,
            transform=ccrs.PlateCarree(),
            linewidth=0
        )
        ax_map.add_patch(rect)

canvas_map = FigureCanvasTkAgg(fig_map, master=left_frame)
canvas_map.draw()
canvas_map.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# --- Matplotlib Figure for Temp Graph ---
fig_temp, ax_temp = plt.subplots(figsize=(6, 6))
canvas_temp = FigureCanvasTkAgg(fig_temp, master=right_frame)
canvas_temp.draw()
canvas_temp.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Fonction pour obtenir les coordonnées des clics
def onclick(event):
    if event.inaxes == ax:

        lon, lat = ax.projection.transform_point(event.xdata, event.ydata, ccrs.PlateCarree())
        print(f'coordonnée: Longitude = {lon:.2f}, Latitude = {lat:.2f}, Temperature = {Temp(lat, lon)}')

# --- Click event handler ---
def on_map_click(event):
    if event.inaxes == ax_map:
        lon, lat = event.xdata, event.ydata
        if lon is None or lat is None:
            return
        # Clear previous plot
        ax_temp.clear()
        # Example: plot Temp as a function of t (hours)
        t = np.linspace(0, 24, 100)
        try:
            temp_values = [Temp(lat, lon, hour) for hour in t]
        except TypeError:
            temp_values = [Temp(lat, lon) for hour in t]  # fallback if Temp doesn't take hour
        ax_temp.plot(t, temp_values)
        ax_temp.set_title(f"Température à lat={lat:.2f}, lon={lon:.2f}")
        ax_temp.set_xlabel("Heure")
        ax_temp.set_ylabel("Température (°C)")
        ax_temp.grid(True)
        canvas_temp.draw()

fig_map.canvas.mpl_connect('button_press_event', on_map_click)

# Lier l'événement de clic à la fonction onclick
cid = fig.canvas.mpl_connect('button_press_event', onclick)
#afficher carte
plt.title('World Map')
plt.show()

root.mainloop()

