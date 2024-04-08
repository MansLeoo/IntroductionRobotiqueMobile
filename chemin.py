import numpy as np
import matplotlib.pyplot as plt

# Lire la carte à partir du fichier
with open("carte.txt", "r") as file:
    carte = [list(line.strip()) for line in file.readlines()]


def trouver_regions_X(carte):
    regions_X = []  # Liste pour stocker les régions contiguës de "X"
    visited = set()  # Ensemble pour garder une trace des cellules visitées

    def dfs(i, j, region):
        # Vérifier les limites de la matrice et si la cellule n'a pas été visitée
        if 0 <= i < len(carte) and 0 <= j < len(carte[0]) and (i, j) not in visited and carte[i][j] == "X":
            visited.add((i, j))
            region.append((i, j))
            # Parcourir les cellules adjacentes
            dfs(i + 1, j, region)
            dfs(i - 1, j, region)
            dfs(i, j + 1, region)
            dfs(i, j - 1, region)

    for i in range(len(carte)):
        for j in range(len(carte[0])):
            if carte[i][j] == "X" and (i, j) not in visited:
                region = []  # Nouvelle région contiguë
                dfs(i, j, region)
                regions_X.append(region)

    return regions_X


def trouver_briques_lait(carte):
    seuil_x = 50  # Seuil de différence en x pour détecter une nouvelle brique de lait
    coordonnees_briques = []  # Liste pour stocker les coordonnées des briques de lait

    # Variables pour stocker les coordonnées du dernier X rencontré
    dernier_x = None

    for i in range(len(carte)):
        for j in range(len(carte[0])):
            if carte[i][j] == "X":
                # Si c'est le premier X rencontré, enregistrez ses coordonnées comme le dernier_x
                if dernier_x is None:
                    dernier_x = (i, j)
                else:
                    # Vérifiez la différence en x entre le dernier_x et le point actuel
                    diff_x = abs(j - dernier_x[1])

                    # Si la différence en x est supérieure au seuil, enregistrez le dernier_x comme une nouvelle brique
                    if diff_x >= seuil_x:
                        coordonnees_briques.append(dernier_x)
                    # Mettez à jour le dernier_x avec le point actuel
                    dernier_x = (i, j)

    # Ajoutez le dernier_x rencontré à la liste des briques de lait
    if dernier_x is not None:
        coordonnees_briques.append(dernier_x)

    return coordonnees_briques


carte_array1 = np.array(carte)
plt.imshow(carte_array1 == 'X', cmap='gray', interpolation='nearest')
plt.show()

# Mettre à jour la carte avec les briques détectées
briques = trouver_briques_lait(carte)

# filtre les 3 premières briques les plus a gauche (x le plus petit) en enlevant la première
briques = sorted(briques, key=lambda x: x[1])[1:4]
print(briques)

# Faire un carré de 3x3 autour de chaque brique
for brique in briques:
    i, j = brique
    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            carte[x][y] = "B"



# Convertir la carte en tableau numpy pour affichage
carte_array = np.array(carte)

# Afficher la carte
plt.imshow(carte_array == 'B', cmap='Reds', interpolation='nearest')
plt.show()

