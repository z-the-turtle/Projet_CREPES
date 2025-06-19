import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Modules personnalisés corrigés ---
from fonction_découpage_capacité_couleurs import colours, capacite
from Temp_Terre_et_atm_dynamiques_avec_infrarouge import (
    albedo, dpuiss, dt, rho_terre, rho_atmosphère, capa_atm, epaisseur_atm,
    Prof, sigma, epsilon, puiss
)

def Temp(lat, lng, days=1):
    """
    Calcule la température de surface sur 'days' jours.
    Renvoie une liste de températures en °C toutes les dt secondes.
    """
    T_T = 280  # K
    T_atm = 220  # K
    temps_steps = int(days * 86400 / dt)
    temp_list = []

    for step in range(temps_steps):
        j = step * dt // 86400  # jour actuel
        h = (step * dt % 86400) / 3600  # heure en décimal
        dT_T = (
            (1 - albedo(lat, lng)) * dpuiss(lat, lng, h, j, puiss)
            + sigma * (epsilon * T_atm**4 - T_T**4)
        ) * dt / (capacite(lat, lng) * rho_terre * Prof)
        dT_atm = (
            sigma * (epsilon * T_T**4 - 2 * epsilon * T_atm**4)
        ) * dt / (capa_atm * rho_atmosphère * epaisseur_atm)

        T_T += dT_T
        T_atm += dT_atm
        temp_list.append(T_T - 273.15)  # convertir en °C

    return temp_list

def color_zones(ax, res=10):
    """Colorie la carte selon capacite/colours."""
    for lon in np.arange(-180, 180, res):
        for lat in np.arange(-90, 90, res):
            cap = capacite(lat + res/2, lon + res/2)
            color = colours.get(cap, '#FF00FF')
            rect = mpatches.Rectangle(
                (lon, lat), res, res, facecolor=color, alpha=0.6,
                transform=ccrs.PlateCarree(), linewidth=0, edgecolor='none'
            )
            ax.add_patch(rect)

def on_map_click(event):
    if event.inaxes != ax_map:
        return
    lon, lat = event.xdata, event.ydata
    if lon is None or lat is None:
        return
    lon, lat = round(lon,2), round(lat,2)
    # Récupérer les températures
    temp_vals = Temp(lat, lon, days=1)
    t = np.linspace(0, 24, len(temp_vals))
    # Tracer
    ax_temp.clear()
    ax_temp.plot(t, temp_vals, 'b-', linewidth=2)
    ax_temp.set_title(f"Température à lat={lat}°, lon={lon}°")
    ax_temp.set_xlabel("Temps (heures)")
    ax_temp.set_ylabel("Température (°C)")
    ax_temp.grid(True, alpha=0.3)
    ax_temp.set_xlim(0, 24)
    if len(set(temp_vals)) > 1:
        y_min, y_max = min(temp_vals), max(temp_vals)
        margin = (y_max - y_min) * 0.1
        ax_temp.set_ylim(y_min - margin, y_max + margin)
    else:
        val = temp_vals[0]
        ax_temp.set_ylim(val - 5, val + 5)
    canvas_temp.draw()

# === Interface Tkinter ===

root = tk.Tk()
root.title("Carte + Température")
root.geometry("1300x700")

frame_left = ttk.Frame(root)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame_right = ttk.Frame(root)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Carte
fig_map = plt.Figure(figsize=(7,5), dpi=100)
ax_map = fig_map.add_subplot(1,1,1, projection=ccrs.PlateCarree())
ax_map.coastlines()
ax_map.set_global()
ax_map.gridlines(draw_labels=True, alpha=0.3)
color_zones(ax_map)
canvas_map = FigureCanvasTkAgg(fig_map, master=frame_left)
canvas_map.draw()
canvas_map.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Graphique de température
fig_temp = plt.Figure(figsize=(7,5), dpi=100)
ax_temp = fig_temp.add_subplot(1,1,1)
ax_temp.set_title("Cliquez sur la carte pour voir la température")
ax_temp.set_xlabel("Temps (heures)")
ax_temp.set_ylabel("Température (°C)")
ax_temp.grid(True, alpha=0.3)
canvas_temp = FigureCanvasTkAgg(fig_temp, master=frame_right)
canvas_temp.draw()
canvas_temp.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Clic
fig_map.canvas.mpl_connect('button_press_event', on_map_click)

root.mainloop()
