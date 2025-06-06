Ce programme contient un calcul de la température à un point précis de la planète en fonction de sa longitude et de sa latitude.
Il tient compte que l'on soit en dehors de l'équilibre thermique. La nuit, il n'y a pas de terme source, le premier principe de la thermodynamique donne donc dT/dt = -sigmaT^4/C*rho*prof, avec prof une profondeur caractéristique de variation de la température en une journée.
Il tient compte du fait que les rayons n'arrivent pas avec la même incidence sur la Terre selon la latitude et la longitude.
Il tient donc de l'heure de la journée et de la saison en laquelle nous nous trouvons.
Il manque une initialisation du temps (en gros, définir à quoi correspond t = 0).
Aussi, il prend en compte une valeur moyenne de la capacité thermique de la Terre, il faut en réalité prendre en compte la capacité thermique de la surface considérée pour le point sur lequel on est.
Il faudrait y implémenter, une fois terminé, le modèle conducto-convectif.
Il faudrait prendre en compte l'humidité de l'air en fonction de la zone géographique.
Il faudrait justifier les choix des valeurs de toutes les constantes, dont la plupart ont été prises arbitrairement.
