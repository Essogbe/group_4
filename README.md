# Tâche 1
# Tâche 2
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
   - **Ismael OGOUBIYI** - Développeur principal

## Remarques
   * Le modèle est téléchargé et mis en cache dans le répertoire courant.
   * Pour l'utilisation d'une API distante, l'application demande l'URL de l'API.
