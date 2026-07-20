import os

contenu_fich = """CLIENT001;Dupont;2024-01;450.20;électricité
CLIENT001;Dupont;2024-02;512.80;électricité
CLIENT001;Dupont;2024-03;389.50;électricité
CLIENT002;Martin;2024-01;1200.00;gaz
CLIENT002;Martin;2024-02;980.50;gaz
CLIENT002;Martin;2024-03;1150.75;gaz
CLIENT003;Bernard;2024-01;320.40;électricité
CLIENT003;Bernard;2024-02;295.80;électricité
CLIENT003;Bernard;2024-03;410.20;électricité"""

clients_data = {}
depenses_par_mois = {}
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Correction : Utilisation de os.path.join
with open(os.path.join(DATA_DIR, "factures.txt"), "w", encoding="utf-8") as f:
    f.write(contenu_fich)

# Correction : Utilisation de os.path.join
with open(os.path.join(DATA_DIR, "factures.txt"), "r", encoding="utf-8") as f:
    for ligne in f:
        elements = ligne.strip().split(";")
        if len(elements) == 5:
            client_id, nom, mois, montant_str, type_energie = elements
            montant = float(montant_str)

            if client_id not in clients_data:
                clients_data[client_id] = {
                    "nom": nom,
                    "type_energie": type_energie,
                    "factures": []
                }
            clients_data[client_id]["factures"].append(montant)

            depenses_par_mois[mois] = depenses_par_mois.get(mois, 0.0) + montant

client_plus_depensier = None
client_moins_depensier = None
max_depense_totale = -1
min_depense_totale = float('inf')

lignes_synthese = []

for cid, info in clients_data.items():
    factures = info["factures"]
    total = sum(factures)
    moyenne = total / len(factures) if factures else 0
    max_facture = max(factures)

    info["total"] = round(total, 2)
    info["moyenne"] = round(moyenne, 2)

    if total > max_depense_totale:
        max_depense_totale = total
        client_plus_depensier = (cid, info["nom"])
    if total < min_depense_totale:
        min_depense_totale = total
        client_moins_depensier = (cid, info["nom"])

    print(f"Client: {info['nom']} | Total Annuel: {info['total']}€ | Facture max: {max_facture}€")
    lignes_synthese.append(f"{cid};{info['nom']};{info['type_energie']};{info['total']};{info['moyenne']}\n")

print(f"\nClient le plus dépensier : {client_plus_depensier[1]} ({max_depense_totale}€)")
print(f"Client le moins dépensier : {client_moins_depensier[1]} ({min_depense_totale}€)")

# Correction : Enregistrement de synthese.txt dans le dossier data
with open(os.path.join(DATA_DIR, "synthese.txt"), "w", encoding="utf-8") as f:
    f.writelines(lignes_synthese)

mois_max = max(depenses_par_mois, key=depenses_par_mois.get)
print(f"Mois avec la dépense globale la plus élevée : {mois_max} ({depenses_par_mois[mois_max]}€)")