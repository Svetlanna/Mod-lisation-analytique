centrales = [
    {"nom": "Centrale A", "type": "Nucléaire", "production": 8500},
    {"nom": "Centrale B", "type": "Solaire", "production": 320},
    {"nom": "Centrale C", "type": "Eolien", "production": 1200},
    {"nom": "Centrale D", "type": "Hydraulique", "production": 4200},
    {"nom": "Centrale E", "type": "Gaz", "production": 2100},
    {"nom": "Centrale F", "type": "Solaire", "production": 890},
    {"nom": "Centrale G", "type": "Eolien", "production": 1850},
    {"nom": "Centrale H", "type": "Nucléaire", "production": 9200},
]


def tri_a_bulles(liste):
    n = len(liste)

    arr = list(liste)
    for i in range(n):
        for j in range(0, n - i - 1):

            if arr[j]["production"] < arr[j + 1]["production"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


centrales_triees = tri_a_bulles(centrales)


def recherche_par_type(liste, type_energie):
    resultats = []
    for c in liste:
        if c["type"].lower() == type_energie.lower():
            resultats.append(c)
    return resultats

total_prod = 0
centrale_max = centrales[0]
centrale_min = centrales[0]
compteur = 0

for c in centrales:
    prod = c["production"]
    total_prod += prod
    compteur += 1

    if prod > centrale_max["production"]:
        centrale_max = c
    if prod < centrale_min["production"]:
        centrale_min = c

moyenne_prod = total_prod / compteur if compteur > 0 else 0

print("Total:", total_prod)
print("Moyenne:", moyenne_prod)
print("Max:", centrale_max["nom"])