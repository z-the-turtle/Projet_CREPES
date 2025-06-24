# Simulation de convection atmosphérique — Modèle Terre simplifié

Ce script simule, sous forme animée, le déplacement de blocs d'air fragmentés (représentant l'atmosphère) au-dessus d'un sol divisé en deux zones thermiques : une zone de **nuit** et une zone de **jour**, ayant des températures différentes. L’objectif est de visualiser les échanges thermiques selon la **loi de Newton du refroidissement** et de représenter un phénomène de **convection atmosphérique** à l’échelle planétaire de manière intuitive.

---

##  Modèle

- **Modèle terrestre** : la Terre est modélisée comme un segment circulaire de périmètre  
  `2πR ≈ 36 000 km` ([source](https://www.notre-planete.info/terre/chiffres_cle.php)).
- **Blocs d’air** : des blocs se déplacent au-dessus du sol à une vitesse constante de  
  `10 m/s` (vent) ([source](https://meteo-parapente.com/#/)).
- **Température du sol** selon la saison :
  - **Hiver** : nuit = `-10 °C` · jour = `20 °C`
  - **Été**   : nuit = `10 °C` · jour = `40 °C`
  - Ces valeurs ont été fournies par un autre groupe à partir d’un modèle de rayonnement solaire.
  - La **différence constante** de 30 °C entre nuit et jour permet de comparer les effets de convection de manière cohérente.

- **Disposition visuelle** :
  - Côté gauche de la figure : **nuit**
  - Côté droit de la figure : **jour**

---

##  Objectif

Visualiser :
- L’**évolution de la température** des blocs d’air.
- La **puissance thermique échangée** entre le sol et les blocs d’air.
- L’effet du **vent** et du contraste thermique sol/nuit sur la répartition énergétique dans l’atmosphère.

---

##  Loi de Newton du refroidissement

Le modèle repose sur la loi de Newton appliquée à chaque pas de temps (approche discrète) : ![image](https://github.com/user-attachments/assets/4afdb17e-582d-448b-b5ea-d3df37518f10)



Avec :
- `Q` : puissance échangée (W)
- `h` : coefficient de convection thermique (`10 W/m²/°C`)  
  ([source](https://help.solidworks.com/2012/french/SolidWorks/cworks/Convection_Heat_Coefficient.htm))
- `A` : surface d’échange du bloc
- `T_sol` : température du sol
- `T_air` : température du bloc d’air
- `Δt` : durée du pas de temps
- `m` : masse du bloc d’air
- `c` : capacité thermique massique de l’air (≈ 1000 J/kg/°C)

---

##  Paramètres utilisés

| Paramètre                  | Valeur                  | Source |
|---------------------------|-------------------------|--------|
| Largeur totale du sol     | `36 000 000 m`          | [notre-planete.info](https://www.notre-planete.info/terre/chiffres_cle.php) |
| Vitesse du vent           | `10 m/s`                | [meteo-parapente.com](https://meteo-parapente.com/#/) |
| Masse volumique de l’air  | `1.225 kg/m³` à 15 °C   | [Wikipedia](https://fr.wikipedia.org/wiki/Masse_volumique_de_l%27air) |
| Coefficient de convection | `10 W/m²/°C`            | [SolidWorks Help](https://help.solidworks.com/2012/french/SolidWorks/cworks/Convection_Heat_Coefficient.htm) |

---

## Remarques

- Le modèle est volontairement simplifié pour se concentrer sur les effets thermiques principaux.
- Des hypothèses idéalisées sont prises (température uniforme par zone, pas d’échanges entre blocs, pas d’humidité, etc.).
- Cette simulation peut servir de base à une extension prenant en compte l’albédo, l’effet de serre ou la rotation de la Terre.

---



