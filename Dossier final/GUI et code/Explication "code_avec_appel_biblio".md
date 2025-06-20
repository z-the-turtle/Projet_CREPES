Ce code importe la bibliothèque avec nos fonctions et s'appuie grandement dessus. Il est donc nécessaire qu'il se trouve dans le même dossier que le fichier python librairie_puissances soit dans le même dossier (ou a minima dans le répertoire de travail de python) :
* Premièrement, on définit les constantes utiles pour  le code. Les valeurs pour ces dernières sont justifiées [ici](https://github.com/z-the-turtle/Projet_CREPES/blob/main/Dossier%20final/GUI%20et%20code/Justification%20constantes.md).
* Ensuite, on initialise les températures.
* On met enfin en place la méthode d'Euler pour modéliser la température de la Terre et celle de l'atmosphère, qui obéissent au système différentiel suivant :

$$\begin{cases}
dT_{Terre} = [(1-\alpha)P_{sol} +\sigma (\epsilon T_{atmo}^4-T_{Terre}^4)]\frac{dt}{C_{atmo}\rho_{Terre}Profondeur} \\
dT_{atmo} = \sigma(\mathbf{\epsilon}T_{Terre}^4-2\epsilon T_{atmo}^4)\frac{dt}{C_{atmo}\rho_{atmo}e_{atm}}
\end{cases}$$ 
