import pandas as pd
import matplotlib.pyplot as plt

# Charger le jeu de données
data = pd.read_csv("Housing.csv")

# Créer l'histogramme
plt.figure(figsize=(8, 6))
plt.hist(data["bedrooms"], bins=15, edgecolor="black", alpha=0.7)
plt.xlabel("Nombre de chambres")
plt.ylabel("Fréquence")
plt.title("Répartition des chambres")
plt.grid(axis="y")
plt.show()

