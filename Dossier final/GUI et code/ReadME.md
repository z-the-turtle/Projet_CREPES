**- Affichage_final.py :**

        Interface d'utilisateur qui affiche une carte du monde interactif, l'utilisateur clique dessus pour obtenir une graphique qui affiche l'évolution de la température au cours d'un an.
        modules à installer:
        pip install requests
        pip install pandas
        pip install cartopy
        
**- Code_avec_appel_biblio.py :** 

        Code le plus abouti sans interface graphique : sert de base à l'interface graphique (GUI).

**- Explication_code_avec_appel_biblio.md :** 

        Explication et détails généraux du code **Code_avec_appel_biblio.py**.

**- justification constantes.md :** 
  
        Validation scientifique du code **Code_avec_appel_biblio.py**.

**- albedo_lat_lon_multisampled_3pts.csv :** 
  
        Stockage des albédos obtenus avec les appels API de la NASA.

**- fonction_découpage_capacité_couleurs.py :**

        Cette fonction permet de découper le monde en des zones avec des capacitéc calorifiques différentes (selon le longiude et la latitude), ces capacités calorifiques sont également assignés des couleurs pour permettre le traçage sur la carte du monde dans le GUI.

**- imageterreaveclatlong.jpg :**

        Cette image de la carte du monde avec les lignes de latitude et longitude est utilisé dans l'affichage du GUI pour la carte interactive. 
**- librairie_puissances.py :**

        Bibliothèque regroupant les différents fonctions de calcul utilisées dans le modèle
