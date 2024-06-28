# Tâche 1
# Array Class

La classe `Array` implémente un tableau flexible en Python, supportant à la fois des tableaux 1D et 2D, ainsi que diverses opérations mathématiques élémentaires.

## Fonctionnalités
- **Tableaux 1D et 2D :** Gestion des tableaux de dimensions variables.
- **Opérations mathématiques :** Addition, soustraction, multiplication (par un scalaire ou par un autre tableau), division (par un scalaire ou par un autre tableau), et produit scalaire pour les tableaux 1D.
- **Accès aux éléments :** Permet l'accès et la modification des éléments individuels ainsi que des tranches du tableau.
- **Présence d'un élément :** Vérifie si un élément est présent dans le tableau.
- **Représentation :** Méthode pour afficher une représentation textuelle de l'objet `Array`.
- **Longueur du tableau :** Retourne le nombre total d'éléments dans le tableau principal.

## Exemples d'utilisation

```python
from array import Array

# Tableaux 1D
a = Array([1, 2, 3, 4, 5])
b = Array([5, 4, 3, 2, 1])

# Opérations
c = a + b  # Addition
d = a * 2  # Multiplication par un scalaire
e = a @ b  # Produit scalaire

print(f"a: {a}")
print(f"b: {b}")
print(f"c: {c}")
print(f"d: {d}")
print(f"e: {e}")

# Accès aux éléments et longueur
print(f"Longueur de a: {len(a)}")

# Tableaux 2D
f = Array([[1, 2], [3, 4]])
g = Array([[4, 3], [2, 1]])

# Opérations
h = f + g  # Addition
i = f * 2  # Multiplication par un scalaire

print(f"f: {f}")
print(f"g: {g}")
print(f"h: {h}")
print(f"i: {i}")
```

# Tâche 2
## Contributeurs
 - **SODABI Emmanuella : Histogramme en R**
 - **KINZOUN Elfried : Nuage de points en R**
 - **TOKAN Princia : Histogramme en python**
 - **COMADOU Syldon : Nuage de points en python**
   
# Tâche 3
 ## GeniArt
 GeniArt est une application basée sur Tkinter qui utilise un modèle de diffusion pour générer des images à partir de descriptions textuelles. L'application offre également la possibilité de sauvegarder les images générées.
 
 ## Prérequis
 Assurez-vous d'avoir Python 3.7 ou une version ultérieure installée sur votre machine.
 
 ## Installation
 1. Clonez le dépôt ou téléchargez les fichiers sources.
 
 2. Créez et activez un environnement virtuel :
 ### Windows
 ```
 python -m venv venv
 .\venv\Scripts\activate
 ```
 ### Linux/Mac
 ```
 python3 -m venv venv
 source venv/bin/activate
 ```
 
 4. Installez les dépendances nécessaires :
 ```
 pip install -r requirements.txt
 ```
 
 ## Utilisation
 1. Lancez l'application :
 ```
    python app.py
 ```
 3. Entrez une description dans le champ de texte et cliquez sur le bouton "Générer" pour générer une image.
 4. Une fois l'image générée, le bouton "Enregistrer sous" sera activé. Cliquez dessus pour enregistrer l'image sur votre disque.
 
 ## Fonctionnalités
 - Génération d'images : Génération d'images à partir de descriptions textuelles.
 - Sauvegarde d'images : Sauvegarde des images générées.
 - Choix du mode : Choix entre l'utilisation locale du modèle ou une API distante pour la génération d'images.
 
 ## Structure du Code
 - Classe App : Contient toute la logique de l'application.
   - __init__ : Initialise l'application, configure l'interface utilisateur et initialise les widgets.
   - generate_image : Fonction appelée lors du clic sur "Générer". Lance un thread pour la génération d'image.
   - generate_image_thread : Thread de génération d'image. Gère la logique d'appel au modèle local ou distant.
   - display_image : Affiche l'image générée sur le canvas.
   - save_image : Sauvegarde l'image générée sur le disque.
   - switch_api : Permet de basculer entre l'utilisation locale du modèle et une API distante.
   - listen_sse et fetch_generated_image : Gèrent la communication avec l'API distante.
 
 ## Contributeurs
   - **Ismael OGOUBIYI**
   - **Romuald AMEGBEDJI**
   - **Leonce OROU AWA**
 ## Remarques
   * Le modèle est téléchargé et mis en cache dans le répertoire courant.
   * Pour l'utilisation d'une API distante, l'application demande l'URL de l'API.

# Contributions
  ## Tâche 1
  ## Tâche 
  
  -**KINZOUN Elfried** :25%
  -**SODABI Emmanuella** : 20%
  -**TOKAN Princia** : 20%
  -**COMADOU Syldon** : 35%
  ## Tâche 3
   - **Ismael OGOUBIYI** - 32%
   - **Romuald AMEGBEDJI** - 36%
   - **Leonce OROU AWA** - 32%
