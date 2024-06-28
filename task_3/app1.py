import time

from customtkinter import *
from PIL import Image, ImageTk
from diffusers import StableDiffusionPipeline
import torch
from io import BytesIO
import threading

# Paramétrage de la fenêtre avec Tkinter
fenetre = CTk()
fenetre.geometry('850x750')
fenetre.resizable(width=False , height=False)


spinner = CTkProgressBar(master=fenetre)

spinner.place(relx=0.99, rely=0.33, anchor="e")

# Fonction pour changer le thème
def switch_theme():
    if theme_var.get() == "dark":
        set_appearance_mode("light")
        theme_var.set("light")
        label.config(text_color="white")
        label1.config(text_color="white")
    else:
        set_appearance_mode("dark")
        theme_var.set("dark")
        label.config(text_color="black")
        label1.config(text_color="#C830D1")

# Variable pour le switch de thème
theme_var = StringVar(value="dark")  # Initialement en mode noir
switch = CTkSwitch(master=fenetre, text="Thème", font=("italic", 12), command=switch_theme)
switch.place(relx=0.8, rely=0.05)

total = 50
import sys
def callback_on_step_end(pipe, step: int, timestep: int, latents: torch.FloatTensor, **kwargs):
    global total,spinner
    length = 30

    print(f"Step: {step}, Timestep: {timestep}")

    # Calcul du pourcentage d'avancement
    percent = 100 * (step / float(50))

    # Mise à jour de la barre de progression
    spinner.set(percent/100)

    print(percent/100)
    print("Current",spinner.get())
    return  latents
# Fonction pour générer l'image
def generer():
     # Commencer le spinner
    prompt = Entrer.get()  # Récupérer le texte de l'entrée
    num_images = int(comobox.get().split()[0])  # Récupérer le nombre d'images à générer

    def task():
        pipe = StableDiffusionPipeline.from_pretrained("hf-internal-testing/tiny-stable-diffusion-torch")#initialisation du modele de generation de l'image 

        for _ in range(num_images):
            print("ok")
            image = pipe(prompt,num_inference_steps=50,callback_on_step_end=callback_on_step_end).images[0] #en fonction du nombre d'image demander

            # Convertir l'image pour l'affichage
            image_io = BytesIO()
            image.save(image_io, format='PNG')
            image_io.seek(0)
            img = Image.open(image_io)
            img_tk = ImageTk.PhotoImage(img) #ouverture avec PIL et conversion en objet

            # Mettre à jour le label avec l'image générée
            image_label.config(image=img_tk, text="")
            image_label.image = img_tk  # Sauvegarder une référence pour éviter le garbage collection

        spinner.stop()  # Arrêter le spinner

    threading.Thread(target=task).start()#lancement de la fonction task


# Les labels
label = CTkLabel(master=fenetre, text="Tkinter application UI", font=("vivaldi", 40), text_color="black", fg_color="purple")
label.place(relx=0.55, rely=0.05, anchor="center")
label1 = CTkLabel(master=fenetre, text="Description :", font=("Arial", 20), text_color="#C830D1")
label1.place(relx=0.18, rely=0.2, anchor="w")

# Entrée de l'utilisateur
Entrer = CTkEntry(master=fenetre, placeholder_text="Que voulez-vous...?", width=400, height=100, text_color="#FFCC70")
Entrer.place(relx=0.32, rely=0.15)

# Nombre d'images à générer
comobox = CTkComboBox(master=fenetre, values=["1 image", "2 images", "3 images"], fg_color="#0093E9")
comobox.place(relx=0.8, rely=0.15)

# Cadre pour l'image générée
image_frame = CTkFrame(master=fenetre, width=620, height=420)
image_frame.place(relx=0.6, rely=0.68, anchor="center")

# Zone d'affichage pour l'image générée
image_label = CTkLabel(master=image_frame, text="")
image_label.place(relx=0.6, rely=0.68, anchor="center")

# Spinner (indicateur de chargement)


# Bouton
bouton = CTkButton(master=fenetre, text="GENERER", corner_radius=32, hover_color="#C830D1", command=generer)
bouton.place(relx=0.4, rely=0.33, anchor="center")

fenetre.mainloop()
