# Simulateur de Crack de Mot de Passe

Ce projet est un simulateur de craquage de mot de passe développé en Python, utilisant une interface graphique avec Tkinter. Il propose deux versions : une version simple (v1) et une version optimisée utilisant le multiprocessus (v2).

## À propos du projet

Ce projet a été réalisé **uniquement pour le plaisir** et dans un but éducatif. Il est important d'en faire un **bon usage** et de l'utiliser de manière responsable.

### Ce que j'ai appris

Le développement de ce simulateur a été un excellent moyen d'explorer plusieurs concepts importants du monde actuel de la performance logicielle (enfin je crois ^^ ) :

- **La puissance du Multiprocessing** : Utilisation du module `multiprocessing` pour exploiter plusieurs cœurs du processeur et augmenter considérablement la vitesse de recherche.
- **La gestion des combinaisons** : Découverte de `itertools.product` pour générer des millions de possibilités à la volée de manière efficace.
- **L'optimisation des ressources** : Apprendre à structurer une application avec le `threading` pour conserver une interface fluide pendant les calculs lourds en arrière-plan.

**Quelques conclusions plus personnelles :**
- J'ai bien compris qu'un mot de passe *longggggggggggg* est vraiment plus sécurisé qu'un mot de passe court (et bien plus sûr que "1234").
- J'ai pu redécouvrir les joies de la création d'interface avec `Tkinter`, une bibliothèque qui reste... disons, un peu *vintage* :}

Bien que je ne connaisse pas encore tout le code par cœur, je suis confiant dans le fait que si je devais le retravailler, je n'aurais aucun mal à m'y retrouver et à me rappeler son principe de fonctionnement grâce à sa structure.

## Fonctionnement

Le programme tente de retrouver un mot de passe en testant toutes les combinaisons possibles de caractères (attaque par force brute).

- **cracker_v1.py** : Version de base, mono-cœur.
- **cracker_v2.py** : Version avancée utilisant le multiprocessus pour des performances accrues, avec une interface plus riche (vitesse en mots/sec, barre de progression visuelle, etc.).

## Prérequis

- Python 3.x
- Tkinter (généralement inclus avec Python)

## Utilisation

Pour lancer l'une des versions, exécutez simplement le script correspondant :

```bash
python cracker_v1.py
# ou
python cracker_v2.py
```
