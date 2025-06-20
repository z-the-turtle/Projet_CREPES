import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Version_finale_avec_API_NASA import Temp
from fonction_découpage_capacité_couleurs import colours, capacite

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
    temp_vals = Temp(lat, lon, date_debut="2022-01-01", nb_jours_simulation=365)
    # L'axe X en jours (0 à 365)
    t = np.linspace(0, 365, len(temp_vals))
    # Tracer
    ax_temp.clear()
    ax_temp.plot(t, temp_vals, 'b-', linewidth=2)
    ax_temp.set_title(f"Température à lat={lat}°, lon={lon}°")
    ax_temp.set_xlabel("Temps (jours)")  # Modifié ici
    ax_temp.set_ylabel("Température (°C)")
    ax_temp.grid(True, alpha=0.3)
    ax_temp.set_xlim(0, 365)  # Modifié ici
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
ax_temp.set_xlabel("Temps (heures)")  # Par défaut, au départ
ax_temp.set_ylabel("Température (°C)")
ax_temp.grid(True, alpha=0.3)
canvas_temp = FigureCanvasTkAgg(fig_temp, master=frame_right)
canvas_temp.draw()
canvas_temp.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# === Zoom avec la molette ===
def on_scroll(event):
    if event.inaxes != ax_temp:
        return
    base_scale = 1.2
    # Sens corrigé : molette vers le haut (écarter doigts) = zoom avant
    scale_factor = 1 / base_scale if event.button == 'up' else base_scale

    xlim = ax_temp.get_xlim()
    ylim = ax_temp.get_ylim()
    xdata = event.xdata
    ydata = event.ydata

    new_xlim = [
        xdata - (xdata - xlim[0]) * scale_factor,
        xdata + (xlim[1] - xdata) * scale_factor
    ]
    new_ylim = [
        ydata - (ydata - ylim[0]) * scale_factor,
        ydata + (ylim[1] - ydata) * scale_factor
    ]

    ax_temp.set_xlim(new_xlim)
    ax_temp.set_ylim(new_ylim)
    canvas_temp.draw()

# === Pan (déplacement) avec clic + glisser ===
pan_start = {'x': None, 'y': None, 'xlim': None, 'ylim': None}

def on_button_press(event):
    if event.inaxes != ax_temp:
        return
    pan_start['x'], pan_start['y'] = event.xdata, event.ydata
    pan_start['xlim'] = ax_temp.get_xlim()
    pan_start['ylim'] = ax_temp.get_ylim()

def on_motion(event):
    if event.inaxes != ax_temp or pan_start['x'] is None or pan_start['y'] is None:
        return
    dx = event.xdata - pan_start['x']
    dy = event.ydata - pan_start['y']
    ax_temp.set_xlim(pan_start['xlim'][0] - dx, pan_start['xlim'][1] - dx)
    ax_temp.set_ylim(pan_start['ylim'][0] - dy, pan_start['ylim'][1] - dy)
    canvas_temp.draw()

def on_button_release(event):
    pan_start['x'], pan_start['y'] = None, None

# Connexion des événements
fig_map.canvas.mpl_connect('button_press_event', on_map_click)
fig_temp.canvas.mpl_connect('scroll_event', on_scroll)
fig_temp.canvas.mpl_connect('button_press_event', on_button_press)
fig_temp.canvas.mpl_connect('motion_notify_event', on_motion)
fig_temp.canvas.mpl_connect('button_release_event', on_button_release)

root.mainloop()
