### README Convection
>Ce dossier contient une série de scripts et de documents permettant de modéliser la convection thermique dans une approche 1D. Les différentes étapes du projet permettent de passer progressivement d’un modèle simple à une modélisation plus complète prenant en compte les échanges thermiques et la puissance échangée.

## Schéma

**- 1 - Schéma modèle 1D.pdf :**

    Explication globale de la modélisation.
## Codes

**- 1 - Modèle 1D sans échanges thermiques.py :**

    Modélisation du déplacement des blocs d’air de la zone nuit vers la zone jour, c’est-à-dire d’un thermostat à un autre où chaque bloc d'air garde sa température initiale pendant le déplacement. 
    Représentation de 18 blocs de 2000 km chacun. 
    Vent à 10m/s : à chaque fois qu'un bloc prend la place du bloc à sa droite il s'est écoulé 55h30.

**- 2 - Evolution températures 1D.py :**

    Représentation de la température de deux blocs d'air placés sur deux sols de températures différentes (-10°C et 20°C) en fonction du temps. 
    Prise en compte des déplacements des blocs d'un sol à l'autre et des échanges thermiques.

**- 3 - Modèle 1D convection.py :**

    Représentation de la variation de température des blocs d'air sur un sol divisé en deux thermostats : 10 et 40°C (été) ou -10 et 20°C (hiver) en fonction du temps et du vent.

**- 4 - Modele 1D convection avec puissance.py :**

    Introduction de la modélisation du transfert de chaleur en appliquant une forme discrète de la loi de Newton du refroidissement, à chaque pas de temps dt. 
    Cf DOCsynthèse pour visualiser la formule. Cette formule permet de prendre en compte la convection dans notre modèle.


**- 5 - Modélisation convection finale.py**

    Représentation de la puissance échangée sol-air en fonction du temps. 
    360 blocs sur un sol découpé en deux thermostats : 10 et 40°C (été).
    Prise en compte du vent à 10m/s.

## Document d'explication

**- Explications.md**

    Explication détaillée de notre modélisation de la convection.


    

    




