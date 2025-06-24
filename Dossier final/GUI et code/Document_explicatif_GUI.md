Ce programme python permet d'afficher une carte du monde dans une fenêtre Tkinter et de générer une courbe traçant la température prédit par notre modèle (fonction *Temp*).

<summary> Affichage à gauche </summary>
<details>On colorie la carte du monde avec le code couleur correspondant aux approximations très simplifiées de la capacité calorifique que nosu avons faits des terrains diverses du globe.
Il y a aussi une estimation fait sur l'albedo d'une certaine zone qui lui est attribué en fontion de sa longitude et de sa latitude; cela est basé sur un pavage fait de moyennes des valeurs de la NASA.
</details>



**Affichage à droite:**

Le graphique de la température est généré à partir de la fonction Temp dans le fichier Code_avec_appel_biblio.py. Pour générer un graphique il faut cliquer sur un endroit sur la carte à gauche pour qu'il prenne les valeurs de longitude et latitude renvoyées par cette action et les rentre ensuite dans la fonction Temp. Puis, le graphique est affiché à gauche de manière que l'on puisse zoomer et se déplacer sur la courbe. 

**Généralités:**

Durée de fonctionnement: Actuellement le programme se déroule sur un an, pour modifier cela il faut modifier les lignes 31, 32 et 40 en remplançant 365 par le nombre de jours de simulation désiré.

**Installations nécéssaires:**

pip install: pandas, requests, cartopy


