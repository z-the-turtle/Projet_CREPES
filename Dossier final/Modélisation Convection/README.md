### README Convection

**- 1 - Schéma modèle 1D.pdf :**

    Schéma : 
    Explication globale de la modélisation.

**- 1 - Modèle 1D sans échanges thermiques.py :**

    Code : 
    Modélisation du déplacement des blocs d’air de la zone nuit vers la zone jour, c’est-à-dire d’un thermostat à un autre où chaque bloc d'air garde sa température initiale pendant le déplacement. 
    Représenation de 18 blocs faisant chacun 2000 km sont représentés. Le vent va à 10m/s, donc à chaque fois qu'un bloc prend la place du bloc à sa droite il s'est écoulé 55h30.

**- 2 - Evolution températures 1D.py :**

    Code : 
    Représentation de la température de deux blocs d'air placés sur deux sols de températures différentes (-10°C et 20°C) en fonction du temps. 
    Prise en compte des déplacements des blocs d'un sol à l'autre et des échanges thermiques.

**- 3 - Modèle 1D convection.py :**

    Code :
    Représentation de la variation de température des blocs d'air sur un sol découpé en deux thermostats : 10 et 40°C (été) en fonction du temps et du vent.

**- 4 - Modele 1D convection avec puissance.py :**

    Code : 
    Introduction de la modélisation du transfert de chaleur en appliquant une forme discrète de la loi de Newton du refroidissement, à chaque pas de temps dt.         Cf DOCsynthèse pour visualiser la formule. Cette formule permet de prendre en compte la convection dans notre modèle.


**- 5 - Modélisation convection finale**

    Code : 
    Représentation de la puissance échangée sol-air en fonction du temps. 
    360 blocs sur un sol découpé en deux thermostats : 10 et 40°C (été).
    Prise en compte du vent à 10m/s.

**- DOCsynthèse**

    Explication détaillée des codes, sources et modélisations.


    

    




