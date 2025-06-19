from math import cos, sin, pi
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
# Import your custom modules
from fonction_découpage_capacité_couleurs import colours, capacite
import matplotlib.patches as mpatches
from Temp_Terre_et_atm_dynamiques_avec_infrarouge import Temp
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def on_map_click(event):
    if event.inaxes != ax_map:
        return

    lon, lat = event.xdata, event.ydata
    if lon is None or lat is None:
        return

    # Arrondir les coordonnées
    lon = round(lon, 2)
    lat = round(lat, 2)

    try:
        temperature = Temp(lat, lon)
        if temperature is None:
            raise ValueError("La fonction Temp a retourné None.")
    except Exception as e:
        temperature = "Erreur: " + str(e)

    label_result.config(text=f"Lat: {lat}°, Lon: {lon}°\nTempérature: {temperature} °C")

# --- Interface principale
root = tk.Tk()
root.title("Carte du monde - Température")
root.geometry("1200x600")

# --- Cadres gauche (carte) et droit (résultat)
frame_left = ttk.Frame(root)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frame_right = ttk.Frame(root, padding=20)
frame_right.pack(side=tk.RIGHT, fill=tk.Y)

ttk.Label(frame_right, text="Température sélectionnée :", font=('Arial', 14)).pack(pady=10)
label_result = ttk.Label(frame_right, text="Cliquez sur la carte", font=('Arial', 12))
label_result.pack(pady=20)

# --- Création de la carte
fig_map = plt.Figure(figsize=(7, 5), dpi=100)
ax_map = fig_map.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax_map.coastlines()
ax_map.set_global()
ax_map.gridlines(draw_labels=True, alpha=0.3)

canvas = FigureCanvasTkAgg(fig_map, master=frame_left)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# --- Connexion du clic
fig_map.canvas.mpl_connect('button_press_event', on_map_click)

# --- Lancement de l'appli
root.mainloop()
