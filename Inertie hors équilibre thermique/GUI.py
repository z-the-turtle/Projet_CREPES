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

class WorldMapTempViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Carte du monde et Température")
        self.root.geometry("1400x700")
        
        # Setup the layout
        self.setup_layout()
        
        # Create the world map
        self.create_world_map()
        
        # Create the temperature graph
        self.create_temp_graph()
        
        # Setup click events
        self.setup_events()
    
    def setup_layout(self):
        """Setup the main layout with left and right frames"""
        # Left frame for the world map
        self.left_frame = ttk.Frame(self.root, width=700, height=700)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.left_frame.pack_propagate(False)
        
        # Right frame for the temperature graph
        self.right_frame = ttk.Frame(self.root, width=700, height=700)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.right_frame.pack_propagate(False)
        
        # Add labels
        ttk.Label(self.left_frame, text="Carte du Monde (Cliquez pour voir la température)", 
                 font=('Arial', 12, 'bold')).pack(pady=5)
        ttk.Label(self.right_frame, text="Graphique de Température", 
                 font=('Arial', 12, 'bold')).pack(pady=5)
    
    def create_world_map(self):
        """Create the world map with colored zones"""
        # Create matplotlib figure for the world map
        self.fig_map = plt.Figure(figsize=(8, 6), dpi=100)
        self.ax_map = self.fig_map.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        
        # Setup map features
        self.ax_map.coastlines()
        self.ax_map.gridlines(draw_labels=True, alpha=0.5)
        self.ax_map.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
        
        # Color the zones based on capacity
        self.color_zones()
        
        # Add the map to tkinter canvas
        self.canvas_map = FigureCanvasTkAgg(self.fig_map, master=self.left_frame)
        self.canvas_map.draw()
        self.canvas_map.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def color_zones(self):
        """Color the map zones based on capacity function"""
        res = 10  # Resolution in degrees
        
        for lon in np.arange(-180, 180, res):
            for lat in np.arange(-90, 90, res):
                # Get capacity for the center of the cell
                cap = capacite(lat + res/2, lon + res/2)
                color = colours.get(cap, '#FF00FF')  # Default to magenta if not found
                
                # Create rectangle patch
                rect = mpatches.Rectangle(
                    (lon, lat), res, res,
                    facecolor=color, alpha=0.6,
                    transform=ccrs.PlateCarree(),
                    linewidth=0,
                    edgecolor='none'
                )
                self.ax_map.add_patch(rect)
    
    def create_temp_graph(self):
        """Create the temperature graph area"""
        # Create matplotlib figure for temperature graph
        self.fig_temp = plt.Figure(figsize=(8, 6), dpi=100)
        self.ax_temp = self.fig_temp.add_subplot(1, 1, 1)
        
        # Initial empty plot
        self.ax_temp.set_title("Cliquez sur la carte pour voir la température")
        self.ax_temp.set_xlabel("Temps (heures)")
        self.ax_temp.set_ylabel("Température (°C)")
        self.ax_temp.grid(True, alpha=0.3)
        
        # Add the graph to tkinter canvas
        self.canvas_temp = FigureCanvasTkAgg(self.fig_temp, master=self.right_frame)
        self.canvas_temp.draw()
        self.canvas_temp.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_events(self):
        """Setup click events for the map"""
        self.fig_map.canvas.mpl_connect('button_press_event', self.on_map_click)
    
    def on_map_click(self, event):
        """Handle click events on the world map"""
        if event.inaxes == self.ax_map:
            lon, lat = event.xdata, event.ydata
            
            # Check if coordinates are valid
            if lon is None or lat is None:
                return
            
            # Ensure coordinates are within valid ranges
            lon = max(-180, min(180, lon))
            lat = max(-90, min(90, lat))
            
            print(f'Coordonnées cliquées: Longitude = {lon:.2f}, Latitude = {lat:.2f}')
            
            # Update the temperature graph
            self.update_temp_graph(lat, lon)

    def update_temp_graph(self, lat, lon):
        """Update the temperature graph for the given coordinates"""
        try:
            # Clear previous plot
            self.ax_temp.clear()
            
            # Create time array (24 hours)
            t = np.linspace(0, 24, 100)
            
            # Calculate temperature values
            # Check if Temp function accepts time parameter
            try:
                # Try with time parameter first
                temp_values = [Temp(lat, lon, time) for time in t]
            except TypeError:
                try:
                    # Try without time parameter
                    temp_value = Temp(lat, lon)
                    temp_values = [temp_value] * len(t)  # Constant temperature
                except Exception as e:
                    print(f"Error calculating temperature: {e}")
                    temp_values = [20] * len(t)  # Default temperature
            
            # Plot the temperature
            self.ax_temp.plot(t, temp_values, 'b-', linewidth=2)
            self.ax_temp.set_title(f"Température à lat={lat:.2f}°, lon={lon:.2f}°")
            self.ax_temp.set_xlabel("Temps (heures)")
            self.ax_temp.set_ylabel("Température (°C)")
            self.ax_temp.grid(True, alpha=0.3)
            
            # Add some styling
            self.ax_temp.set_xlim(0, 24)
            if len(set(temp_values)) > 1:  # If temperature varies
                temp_range = max(temp_values) - min(temp_values)
                margin = temp_range * 0.1
                self.ax_temp.set_ylim(min(temp_values) - margin, max(temp_values) + margin)
            
            # Redraw the canvas
            self.canvas_temp.draw()
            
            # Print temperature info
            if len(set(temp_values)) > 1:
                print(f'Température variable: {min(temp_values):.1f}°C - {max(temp_values):.1f}°C')
            else:
                print(f'Température: {temp_values[0]:.1f}°C')
                
        except Exception as e:
            print(f"Error updating temperature graph: {e}")
            # Show error message on graph
            self.ax_temp.clear()
            self.ax_temp.text(0.5, 0.5, f"Erreur: {str(e)}", 
                            transform=self.ax_temp.transAxes, 
                            ha='center', va='center', fontsize=12)
            self.ax_temp.set_title("Erreur lors du calcul de la température")
            self.canvas_temp.draw()

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = WorldMapTempViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
