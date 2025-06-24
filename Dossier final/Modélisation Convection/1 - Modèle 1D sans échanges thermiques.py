import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np

# ===================== PARAMÈTRES =====================
LARGEUR_SOL = 100       # Largeur du sol 
HAUTEUR_SOL = 2         # Hauteur du sol
HAUTEUR_AIR = 5         # Hauteur des blocs d'air
LARGEUR_BLOC = 5        # Largeur de chaque bloc d'air
VITESSE_BLOCS = 1       # Vitesse de déplacement horizontal
NB_BLOCS = LARGEUR_SOL // LARGEUR_BLOC  # Nombre de blocs

# ===================== TEMPÉRATURE DU SOL =====================
def temperature_sol(x):
    """Retourne la température du sol en position x."""
    return 10 if x < LARGEUR_SOL / 2 else 20  # Nuit à gauche, jour à droite

# ===================== INITIALISATION DES BLOCS =====================
positions_blocs = np.arange(0, LARGEUR_SOL, LARGEUR_BLOC)  # Positions initiales (x)
temperatures_blocs = np.array([temperature_sol(x + LARGEUR_BLOC / 2) for x in positions_blocs]) # Température initiale 

# ===================== CRÉATION FIGURE =====================
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(0, LARGEUR_SOL)
ax.set_ylim(0, HAUTEUR_SOL + HAUTEUR_AIR + 2)
ax.axis('off')
plt.title("Masse d'air fragmentée : échanges thermiques jour/nuit", fontsize=14, pad=20)

# ===================== SOL VISUEL =====================
sol_nuit = patches.Rectangle((0, 0), LARGEUR_SOL / 2, HAUTEUR_SOL, facecolor='midnightblue', edgecolor='black')
sol_jour = patches.Rectangle((LARGEUR_SOL / 2, 0), LARGEUR_SOL / 2, HAUTEUR_SOL, facecolor='lightcoral', edgecolor='black')
ax.add_patch(sol_nuit)
ax.add_patch(sol_jour)

# Étiquettes de température du sol
ax.text(25, 0.5, "Sol nuit 10°C", ha='center', fontsize=10, color='white')
ax.text(75, 0.5, "Sol jour 20°C", ha='center', fontsize=10, color='black')

# ===================== BLOCS D'AIR =====================
hauteur_blocs = HAUTEUR_SOL + 0.5  # Position verticale fixe des blocs

blocs_graphiques = []   # Rectangles
etiquettes = []         # Étiquettes de température

for i, x in enumerate(positions_blocs):
    temp = temperatures_blocs[i]
    ratio_couleur = (temp - 10) / 10  # Interpolation de couleur entre bleu (10°C) et rouge (20°C)
    couleur = (ratio_couleur, 0.2, 1 - ratio_couleur)
    
    bloc = patches.Rectangle((x, hauteur_blocs), LARGEUR_BLOC, HAUTEUR_AIR,
                             facecolor=couleur, edgecolor='black')
    ax.add_patch(bloc)
    blocs_graphiques.append(bloc)

    etiquette = ax.text(x + LARGEUR_BLOC / 2, hauteur_blocs + HAUTEUR_AIR / 2,
                        f"{temp:.1f}°C", ha='center', va='center',
                        fontsize=9, color='white', weight='bold')
    etiquettes.append(etiquette)

# ===================== ANIMATION =====================
def mise_a_jour(frame):
    """Fonction appelée à chaque frame pour animer les blocs."""
    global positions_blocs

    # Déplacement horizontal (cyclique)
    positions_blocs = (positions_blocs + VITESSE_BLOCS) % LARGEUR_SOL

    for i in range(NB_BLOCS):
        x = positions_blocs[i]
        temp = temperatures_blocs[i]
        ratio_couleur = (temp - 10) / 10
        couleur = (ratio_couleur, 0.2, 1 - ratio_couleur)

        # Mise à jour position et couleur du bloc
        blocs_graphiques[i].set_x(x)
        blocs_graphiques[i].set_facecolor(couleur)

        # Mise à jour position et texte de l’étiquette
        etiquettes[i].set_position((x + LARGEUR_BLOC / 2, hauteur_blocs + HAUTEUR_AIR / 2))
        etiquettes[i].set_text(f"{temp:.1f}°C")

    return blocs_graphiques + etiquettes

# Lancement de l’animation (300 frames, 100 ms entre chaque image)
ani = animation.FuncAnimation(fig, mise_a_jour, frames=300, interval=100, blit=True)

# Affichage final
plt.tight_layout()
plt.show()
