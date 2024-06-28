import pandas as pd
import matplotlib.pyplot as plt

# Charger le fichier CSV
file_path = "Housing.csv"
data = pd.read_csv(file_path)

# Cration du graphique de dispersion
plt.scatter(data['area'], data['price'])
plt.xlabel('Surface en m²')
plt.ylabel('Prix en million')
plt.title('Nuage de points prix/Surface')

#Affichage du graphique
plt.show()
