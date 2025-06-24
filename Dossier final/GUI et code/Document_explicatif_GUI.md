Ce programme python permet d'afficher une carte du monde dans une fenêtre Tkinter et de générer une courbe traçant la température prédit par notre modèle (fonction Temp).

Affichage à gauche:

On colorie la carte du monde avec le code couleur correspondant aux approximations très simplifiées de la capacité calorifique que nosu avons faits des terrains diverses du globe.
Il y a aussi une estimation fait sur l'albedo d'une certaine zone qui lui est attribué en fontion de sa longitude et de sa latitude; cela est basé sur un pavage fait de moyennes des valeurs de la NASA.

Affichage à droite:

Le graphique de la température est généré à partir de la fonction Temp dans le fichier Code_avec_appel_biblio.py. Pour générer une graphique il faut cliquer sur un endroit sur la carte à gauche pour qu'il prend les valeurs de longitude et latitude renvoye par cette action, les entre dans la fonction Temp.

