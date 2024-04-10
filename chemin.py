import numpy as np
import matplotlib.pyplot as plt
"""Certain fichier peuvent être mal formé et ne pas être lus correctement par le programme le fichier carte.txt donner dans le rendu est bien formé"""
# Lire la carte à partir du fichier
with open("carte.txt", "r") as file:
    carte = [list(line.strip()) for line in file.readlines()]


def trouver_regions_X(carte):
    regions_X = []  # Liste pour stocker les régions contiguës de "X"
    visited = set()  # Ensemble pour garder une trace des cellules visitées

    def dfs(i, j, region):
        # Vérifie les limites de la matrice et si la cellule n'a pas été visitée
        if 0 <= i < len(carte) and 0 <= j < len(carte[0]) and (i, j) not in visited and carte[i][j] == "X":
            visited.add((i, j))
            region.append((i, j))
            # Parcour les cellules adjacentes
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
                    # Vérifie la différence en x entre le dernier_x et le point actuel
                    diff_x = abs(j - dernier_x[1])

                    # Si la différence en x est supérieure au seuil, enregistrez le dernier_x comme une nouvelle brique
                    if diff_x >= seuil_x:
                        coordonnees_briques.append(dernier_x)
                    # Met à jour le dernier_x avec le point actuel
                    dernier_x = (i, j)

    # Ajoute le dernier_x rencontré à la liste des briques de lait
    if dernier_x is not None:
        coordonnees_briques.append(dernier_x)

    return coordonnees_briques


carte_array1 = np.array(carte)
plt.imshow(carte_array1 == 'X', cmap='gray', interpolation='nearest')
plt.show()

# Met à jour la carte avec les briques détectées
briques = trouver_briques_lait(carte)

# filtre les 3 premières briques les plus a gauche (x le plus petit) en enlevant la première
briques = sorted(briques, key=lambda x: x[1])[1:4]
print(briques)

# Fait un carré de 3x3 autour de chaque brique
for brique in briques:
    for i in range(brique[0] - 1, brique[0] + 2):
        for j in range(brique[1] - 1, brique[1] + 2):
            carte[i][j] = "B"

# Converti la carte en tableau numpy pour affichage
carte_array = np.array(carte)

# Affiche la carte
plt.imshow(carte_array == 'B', cmap='Reds', interpolation='nearest')
plt.show()

# Initialise le tracé
plt.figure()

# Trace la ligne de (0, 0) au premier point
plt.plot([0, briques[0][1]+10], [0, briques[0][0]-10], 'ro-')
plt.plot([briques[0][1]+10, briques[1][1]-10], [briques[0][0]-10, briques[1][0]+10], 'ro-')
plt.plot([briques[1][1]-10, briques[2][1]+10], [briques[1][0]+10, briques[2][0]-10], 'ro-')


# Affiche les points
plt.plot(0, 0, 'bo')  # Point de départ
for brique in briques:
    plt.plot(brique[1], brique[0], 'bo')  # Points des briques de lait

# Configurations de l'affichage
plt.xlabel('Y')
plt.ylabel('X')
plt.title('Trajet du slalom')
plt.grid(True)
plt.axis('equal')
plt.gca().invert_yaxis()  # Inverse l'axe vertical
plt.show()