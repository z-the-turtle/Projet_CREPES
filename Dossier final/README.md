# Présentation des fichiers et dossiers

Ce projet est structuré en plusieurs dossiers. Chaque dossier contient des fichiers associés à une partie spécifique du développement ou de la modélisation.

## - Albédo

Ce dossier regroupe plusieurs essais et versions de modélisation de l’effet de l’albédo terrestre (réflexion de la lumière solaire par la surface de la Terre) sur les échanges thermiques.

Contenu :
- Scripts testant différentes valeurs d’albédo selon la nature du sol (océans, déserts, neige, etc.).
- Tentatives d’implémentation d’un albédo dynamique, variant selon la latitude, la saison ou l’heure de la journée.

## - Modélisation Convection

Contient les codes principaux de simulation de la convection atmosphérique. Ces fichiers implémentent la loi de Newton pour modéliser les échanges thermiques entre le sol (nuit/jour) et des blocs d’air se déplaçant à vitesse constante.

Contenu :
- Simulations animées de l’évolution thermique des blocs d’air.
- Modèles hiver / été, avec paramètres physiques adaptés (vitesse du vent, température du sol, masse volumique de l’air, etc.).
- Tracés de la puissance échangée en fonction du temps.

## - Anciennes versions code

Ce dossier contient les anciennes versions du code principal utilisé dans le projet. Il permet de retracer l’évolution de l’implémentation et les choix successifs (visuels, paramètres physiques, gestion des blocs, etc.).

## - GUI et code

Ce dossier contient l’interface graphique (GUI) ainsi que le code complet du projet.

Contenu :
- Interface utilisateur interactive pour lancer les simulations.
- Scripts Python du modèle thermique et des animations.
- Fichiers de ressources nécessaires à l’exécution du projet.

---

## 📦 Fichier ZIP final

Le fichier `.zip` fourni regroupe l’ensemble du projet :

- **Document de synthèse** : sources scientifiques et explications du modèle physique.
- **Code source** : scripts Python du projet et de ses bibliothèques associées.
- **Pistes pour l’année suivante** : propositions d’améliorations ou d’extensions.
- **README** : présent dans chaque sous-dossier pour décrire le rôle et le contenu de chaque fichier.
