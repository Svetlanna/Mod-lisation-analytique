# Projet Énergie — Algorithmique, Fichiers & Mini Pipeline

Ce projet regroupe trois exercices Python indépendants autour du traitement de données liées à la production d'énergie et à la facturation client.

## 1. `algo.py` — Algorithmique sur une liste de centrales

Ce script travaille sur une liste de centrales (nom, type, production en GWh).

- **Tri à bulles** : la fonction `tri_a_bulles` trie les centrales par production décroissante, sans utiliser `sorted()` ni `.sort()`.
- **Recherche par type** : la fonction `recherche_par_type(liste, type_energie)` renvoie toutes les centrales correspondant à un type d'énergie donné (recherche insensible à la casse).
- **Calculs manuels** : le total de production, la moyenne et la centrale la plus/moins productive sont calculés avec une boucle, sans utiliser `sum()`, `min()` ni `max()`.

Exécution :
```bash
python algo.py
```

## 2. `Manipulation.py` — Fichiers et dictionnaires

Ce script lit le fichier `data/factures.txt` (format `client;nom;mois;montant;type_energie`) et construit un dictionnaire par client contenant :
- son nom et son type d'énergie,
- la liste de ses factures,
- le total et la moyenne annuels.

Il affiche ensuite, pour chaque client, son total annuel et sa facture la plus élevée, puis identifie le client le plus dépensier et le moins dépensier. Un fichier `data/synthese.txt` est généré avec une ligne de résumé par client. Le script calcule aussi le mois où la dépense globale (tous clients confondus) est la plus élevée.

Exécution :
```bash
python Manipulation.py
```

## 3. `pipeline.py` — Consolidation multi-source vers SQLite

Ce script simule la réception de relevés de production dans trois formats différents (CSV pour le solaire, JSON pour l'éolien, texte délimité par `|` pour l'hydraulique) et les consolide dans une base SQLite unique.

Étapes du pipeline :
1. **Extraction** de chaque fichier selon son format propre.
2. **Transformation** : conversion des dates, vérification que la production est positive (les anomalies sont signalées sans bloquer le traitement), et calcul d'un coût estimé (48 €/MWh pour le solaire, 52 €/MWh pour l'éolien, 38 €/MWh pour l'hydraulique).
3. **Chargement** dans la table `productions` de `data/energies.db`, sans doublons (contrainte unique sur `date` + `source`).
4. **Rapport** affiché en console : production totale par type d'énergie, jour le plus productif toutes sources confondues, coût total estimé par type d'énergie.

Si un fichier est absent ou contient des lignes mal formatées, le pipeline continue son exécution avec les autres fichiers et consigne l'erreur dans `data/pipeline_erreurs.log`.

Exécution :
```bash
python pipeline.py
```

## Prérequis

- Python 3 (aucune bibliothèque externe n'est nécessaire : `sqlite3`, `json`, `datetime` et `os` font partie de la bibliothèque standard).

## Ordre d'exécution recommandé

`pipeline.py` importe `algo` et `Manipulation`, donc lancer simplement :
```bash
python pipeline.py
```
exécute les trois scripts à la suite.