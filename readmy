README Technique : Pipeline & Analyse Énergétique


Guide simple et structuré pour les chefs de projet technique


1. Architecture Globale et Gestion des Fichiers

Sécurité & Robustesse OS : La bibliothèque standard os:

os.makedirs(DATA_DIR, exist_ok=True) : Crée le dossier data/ de manière sécurisée sans
erreur s'il existe déjà.
os.path.join(...) : Assure la normalisation des chemins de fichiers pour éviter les problèmes de
séparateurs (/ vs \\).

Blocs with open(...) as f: : Assurent la fermeture automatique des fichiers pour éviter les fuites de
mémoire.


2. Pipeline ETL et Normalisation Hétérogène

Le système consolide des formats d'entrée hétérogènes en un modèle de données unique :

Source Format Séparateur / Structure Règle de Coût
Solaire CSV Virgule (,) avec en-tête (prod / 1000) × 48.0 €
Éolien JSON Tableau d'objets (dictionnaires) (prod / 1000) × 52.0 €
Hydraulique TXT Barre verticale (|) (prod / 1000) × 38.0 €

Gestion des Erreurs & Logging : Chaque source est isolée dans un bloc try...except. Les anomalies
(ex: production négative) sont journalisées avec horodatage :
def log_erreur(message):
erreurs.append(f"[{datetime.now()}] {message}\n")
Les erreurs sont stockées dans pipeline_erreurs.log pour l'audit.

3. Persistance Relationnelle avec SQLite


La base de données SQLite assure la persistance et la fiabilité :
Schéma Déclaratif : Création rigoureuse de la table via CREATE TABLE IF NOT EXISTS.
Dédoublonnage : Utilisation de UNIQUE(date, source) et INSERT OR IGNORE pour éviter les
doublons.
Agrégations : Requêtes SQL optimisées avec SUM(), GROUP BY et ORDER BY ... DESC LIMIT 1.
4. Algorithmes de Tri et Complexité
Implémentation d'un tri à bulles (Bubble Sort) pour structurer les données de production :
•

•

•

•
•

•

Page 1

def tri_a_bulles(liste):
n = len(liste)
arr = list(liste)
for i in range(n):
for j in range(0, n - i - 1):
if arr[j]["production"] < arr[j + 1]["production"]:
arr[j], arr[j + 1] = arr[j + 1], arr[j]
return arr
Analyse : Complexité temporelle de O(n^2) et spatiale de O(n). Idéal pour de petits jeux de données (<50
éléments) grâce à sa simplicité.


5. Indicateurs Clés de Performance (KPIs)
Facturation Client : Totaux annuels, moyennes, client le plus dépensier et mois de charge maximale.
Énergies Renouvelables : Cumuls de production par filière et calcul dynamique des coûts.
Statistiques Globales : Production totale, moyenne par infrastructure et centrale de tête.

6. Recommandations pour le Déploiement


Industrialisation : Remplacer le tri à bulles par Timsort (O(n \log n) via sorted()) si le volume dépasse
10 000 enregistrements.
Surveillance : Mettre en place un système d'alerte en cas de nouvelles erreurs dans
pipeline_erreurs.log.
Tests Unitaires : Utiliser pytest pour valider la non-régression du parsing et des règles SQL.