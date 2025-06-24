Le but du code final est de simuler sous forme animée le déplacement de blocs d'air fragmentés au-dessus d'un sol composé de deux zones thermiques (nuit/jour) avec des températures différentes pour modéliser la convection sur Terre. L'objectif est d'observer l’évolution de la température des blocs d’air au cours de leur déplacement. On considère dans ce modèle la Terre comme un segment de périmètre 2πR(=36000 km), avec un vent de 10m/s, une température de nuit de -10°C et une température de jour de 20°C pour l'hiver et une température de nuit de 10°C et une température de jour de 40°C pour l'été. Pour tous les codes de ce dossier le côté gauche de la figure créée correspond au côté de la Terre où il fait nuit, et le côté droit correspond au côté de la Terre où il fait jour.

**- Modèle 1D sans échanges thermiques.py :**

    Dans le Modèle 1D sans échanges thermiques.py, nous avons modélisé le déplacement des blocs d’air de la zone nuit vers la zone jour, c’est-à-dire d’un thermostat à un autre où chaque bloc d'air garde sa température initiale pendant le déplacement. On a représenté 18 blocs faisant chacun 2 km sont représentés. Le vent va à 10m/s, donc à chaque fois qu'un bloc prend la place du bloc à sa droite il s'est passé 55h30.

**- modele 1D convection.py :**

    Dans ce code on a introduit la modélisation du transfert de chaleur en appliquant une forme discrète de la loi de Newton du refroidissement, à chaque pas de temps dt.Voir Loi de Newton.png pour visualiser la formule. Cette formule permet de prendre en compte la convection dans notre modèle.

**- courbes temperatures.py :**

    Ce code permet de représenter la température de deux blocs d'air placés sur deux sols de températures différentes en fonction du temps. Comme dans les codes précédents, les blocs vont d'un sol à l'autre. On prend en compte les échanges thermiques.

**- Schéma modèle 1D.pdf :**

    Ce schéma explique globalement l'idée de la modélisation.




