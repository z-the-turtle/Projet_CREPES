>[!WARNING]
>Ce code importe la bibliothèque avec nos fonctions et s'appuie grandement dessus. Il est donc nécessaire qu'il se trouve dans le même dossier que le fichier python ***librairie_puissances*** (ou a minima que le fichier python librairie_puissances soit dans le répertoire de travail de python). De plus, il peut être nécessaire d'avoir à effectuer un ***pip install*** pour les modules "pandas" et "requests".

* Premièrement, on définit les constantes utiles pour  le code. Les valeurs pour ces dernières sont justifiées [ici (Justification constantes.md)](https://github.com/z-the-turtle/Projet_CREPES/blob/main/Dossier%20final/GUI%20et%20code/Justification%20constantes.md).
  
* Ensuite, on initialise les ***températures***.
  
* On met enfin en place la ***méthode d'Euler*** pour modéliser la température de la Terre et celle de l'atmosphère, qui obéissent au système différentiel suivant :

$$\begin{cases}
dT_{Terre} = [(1-\alpha)P_{sol} +\sigma (\epsilon T_{atmo}^4-T_{Terre}^4)]\frac{dt}{C_{atmo}\rho_{Terre}Profondeur} \\
dT_{atmo} = P_{convection} + \sigma(\mathbf{\epsilon}T_{Terre}^4-2\epsilon T_{atmo}^4)\frac{dt}{C_{atmo}\rho_{atmo}e_{atm}}
\end{cases}$$ 

* P_{convection} est ici cédé à l'atmosphère [^1]. $$\alpha$$ est l'albédo de la surface de la Terre considérée et $$\epsilon$$ est l'emissivité de l'atmosphère, c'est-à-dire la proportion des infrarouges qu'elle absorbe et la proportion qu'elle ré-émet (elle n'est pas considérée comme un corps noir mais comme un [corps gris (pages 4 à 7)](https://staff.univ-batna2.dz/sites/default/files/nabil_bessanane/files/partie-i_cours_rayonnement_generalitesdefinitions-m1erm.pdf))

> [!NOTE]
> La fonction renvoie une liste des valeurs de températures très (très) longue et non pas un graphique des températures au cours du temps, si on veut modifier ça, on peut remplacer le `return liste_T` ligne 59 par un `return 0` et enlever le commentaire devant le `plt.show`, si on a fait ça (le `return liste_T` et le fait d'avoir commenté le ***plt.show***, c'est pour convenir aux besoins du GUI))
  
* Vous trouverez à la fin du programme un exemple d'utilisation du code, qui prend donc en entrée, une latitude et une longitude, celles du point sur lequel nous voulons connaître la température de surface.

> [!NOTE]
> On remarquera de plus (quand on plot l'évolution de la température en un point au cours du temps (en décommentant le `plt.show()`, ligne 58)) que la température n'a pas l'air d'être périodique au cours d'un an. C'est normal : au début du code, on initialise la température avec une valeur bateau et notre code met un peu de temps avant de se stabiliser. Ainsi le premier/les deux premiers mois ne sont pas représentatifs de notre modèle. Il faut bien garder cela en tête lors des simulations et ne pas hésiter à faire la simulation sur un temps plus long (un an et demi ou deux).

[^1]:(cf : Dossier "Modélisation convection")
