Tous ce programmes contiennent un calcul de la température à un point précis de la planète en fonction de sa longitude et de sa latitude.
Il tient compte que l'on soit en dehors de l'équilibre thermique. La nuit, il n'y a pas de terme source, le premier principe de la thermodynamique donne donc dT/dt = -sigmaT^4/C*rho*prof, avec prof une profondeur caractéristique de variation de la température en une journée.
Il tient compte du fait que les rayons n'arrivent pas avec la même incidence sur la Terre selon la latitude et la longitude.

- Hors equilibre, gère les variations quotidiennes.py: 

    Il tient donc de l'heure de la journée et de la saison en laquelle nous nous trouvons.
    Il manque une initialisation du temps (en gros, définir à quoi correspond t = 0).
    Aussi, il prend en compte une valeur moyenne de la capacité thermique de la Terre, il faut en réalité prendre en compte la capacité thermique      de la surface considérée pour le point sur lequel on est.
    Il faudrait y implémenter, une fois terminé, le modèle conducto-convectif.
    Il faudrait prendre en compte l'humidité de l'air en fonction de la zone géographique.

- evolution_temp_avec_albedo_capacite v2.py:

    test pour relier le premier code ci-dessus avec le decoupage de capacitées et l'API de l'Albédo


- Hors equilibre, gère les variations quotidiennes-v3.py :

    version avec l'ablédo suivant le même découpage que la capacité 
    (pas appel API car calcul avec moyenne sur une année)

- Temp_Terre_et_atm_dynamiques.py:

    version avec le système d'équations différentielles gérant l'effet de serre résolu mais pas très précis : mélange entre visible et infrarouge.
    -> atmosphere transparent au visible et opaque a l'infrarouge.

**- Temp_Terre_et_atm_dynamiques_avec_infrarouge.py:**
  
    Version précédente plus précise avec considération de l'infrarouge : l'atmosphère n'est plus opaque à 100% à l'infrarouge.

**Remarque :** Tous ces codes ont une erreur dans le calcul du produit scanlaire dans la fonction dpuiss (corrigé dans la version finale)
