import os
import json
import sqlite3
from datetime import datetime

import algo
import Manipulation
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)



solaire_data = """date,site,production_kwh
2024-01-15,Site_Lyon,842.5
2024-01-15,Site_Marseille,1203.8
2024-01-16,Site_Lyon,920.1
2024-01-16,Site_Marseille,1150.2"""

eolien_data = [
    {"date": "2024-01-15", "parc": "ParcNord", "energieproduite": 4521.3},
    {"date": "2024-01-15", "parc": "ParcOuest", "energieproduite": 3812.6},
    {"date": "2024-01-16", "parc": "ParcNord", "energieproduite": 5102.8},
    {"date": "2024-01-16", "parc": "ParcOuest", "energieproduite": 4230.1}
]

hydraulique_data = """date|centrale|production
2024-01-15|Barrage_Rhone|12500.0
2024-01-15|Barrage_Loire|8200.5
2024-01-16|Barrage_Rhone|11800.3
2024-01-16|Barrage_Loire|9100.7"""

with open(os.path.join(DATA_DIR, "solaire.csv"), "w", encoding="utf-8") as f:
    f.write(solaire_data)

with open(os.path.join(DATA_DIR, "eolien.json"), "w", encoding="utf-8") as f:
    json.dump(eolien_data, f)

with open(os.path.join(DATA_DIR, "hydraulique.txt"), "w", encoding="utf-8") as f:
    f.write(hydraulique_data)

donnees_normalisees = []
erreurs = []

def log_erreur(message):
    erreurs.append(f"[{datetime.now()}] {message}\n")

#solaire.csv
try:
    if not os.path.exists(os.path.join(DATA_DIR, "solaire.csv")):
        raise FileNotFoundError("solaire.csv absent")
    with open(os.path.join(DATA_DIR, "solaire.csv"), "r", encoding="utf-8") as f:
        lignes = f.readlines()[1:] # Ignorer l'en-tête
        for idx, ligne in enumerate(lignes, start=2):
            parts = ligne.strip().split(",")
            if len(parts) != 3:
                log_erreur(f"solaire.csv ligne {idx} mal formatée")
                continue
            date_str, site, prod_str = parts
            prod = float(prod_str)
            if prod < 0:
                log_erreur(f"Anomalie solaire.csv ligne {idx}: production négative")
                continue
            date_dt = datetime.strptime(date_str, "%Y-%m-%d")
            cout = (prod / 1000.0) * 48.0
            donnees_normalisees.append((date_dt.strftime("%Y-%m-%d"), site, "solaire", prod, cout))
except Exception as e:
    log_erreur(f"Erreur globale sur solaire.csv : {e}")

# Traitement Eolien.json
try:
    if not os.path.exists(os.path.join(DATA_DIR, "eolien.json")):
        raise FileNotFoundError("eolien.json absent")
    with open(os.path.join(DATA_DIR, "eolien.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
        for idx, item in enumerate(data):
            date_str = item.get("date")
            site = item.get("parc")
            prod = float(item.get("energieproduite", 0))
            if prod < 0:
                log_erreur(f"Anomalie eolien.json index {idx}: production négative")
                continue
            date_dt = datetime.strptime(date_str, "%Y-%m-%d")
            cout = (prod / 1000.0) * 52.0
            donnees_normalisees.append((date_dt.strftime("%Y-%m-%d"), site, "eolien", prod, cout))
except Exception as e:
    log_erreur(f"Erreur globale sur eolien.json : {e}")

#traitement hydraulique.txt
try:
    if not os.path.exists(os.path.join(DATA_DIR, "hydraulique.txt")):
        raise FileNotFoundError("hydraulique.txt absent")
    with open(os.path.join(DATA_DIR, "hydraulique.txt"), "r", encoding="utf-8") as f:
        lignes = f.readlines()[1:]
        for idx, ligne in enumerate(lignes, start=2):
            parts = ligne.strip().split("|")
            if len(parts) != 3:
                log_erreur(f"hydraulique.txt ligne {idx} mal formatée")
                continue
            date_str, site, prod_str = parts
            prod = float(prod_str)
            if prod < 0:
                log_erreur(f"Anomalie hydraulique.txt ligne {idx}: production négative")
                continue
            date_dt = datetime.strptime(date_str, "%Y-%m-%d")
            cout = (prod / 1000.0) * 38.0
            donnees_normalisees.append((date_dt.strftime("%Y-%m-%d"), site, "hydraulique", prod, cout))
except Exception as e:
    log_erreur(f"Erreur globale sur hydraulique.txt : {e}")

if erreurs:
    with open(os.path.join(DATA_DIR, "pipeline_erreurs.log"), "w", encoding="utf-8") as f:
        f.writelines(erreurs)


#utilisation de os.path.join pour SQLite
conn = sqlite3.connect(os.path.join(DATA_DIR, "energies.db"))
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS productions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    source TEXT,
    type_energie TEXT,
    production_kwh REAL,
    cout_estime REAL,
    UNIQUE(date, source)
)
""")

for row in donnees_normalisees:
    cursor.execute("""
    INSERT OR IGNORE INTO productions (date, source, type_energie, production_kwh, cout_estime)
    VALUES (?, ?, ?, ?, ?)
    """, row)

conn.commit()


print("1. Production totale par type d'énergie :")
cursor.execute("SELECT type_energie, SUM(production_kwh) FROM productions GROUP BY type_energie")
for r in cursor.fetchall():
    print(f" - {r[0]} : {r[1]} kWh")

print("\n2. Jour le plus productif toutes sources confondues :")
cursor.execute("SELECT date, SUM(production_kwh) as total FROM productions GROUP BY date ORDER BY total DESC LIMIT 1")
jour_top = cursor.fetchone()
if jour_top:
    print(f" - Date : {jour_top[0]} ({jour_top[1]} kWh)")

print("\n3. Coût estimé total par type d'énergie :")
cursor.execute("SELECT type_energie, SUM(cout_estime) FROM productions GROUP BY type_energie")
for r in cursor.fetchall():
    print(f" - {r[0]} : {r[1]:.2f} €")

conn.close()
