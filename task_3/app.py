import tkinter as tk
from tkinter import messagebox, filedialog
from io import BytesIO
from PIL import Image, ImageTk
import customtkinter as ctk
import threading
import requests

from diffusers import StableDiffusionPipeline

from customtkinter import CTkInputDialog

import os

current_dir = os.getcwd()
model_path = os.path.join(current_dir)
# Cache des modèles
cache_path = os.path.join(current_dir, "cache")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("GeniArt")
        self.root.resizable(width=False, height=False)

        ctk.set_appearance_mode("dark")

        self.canvas = tk.Canvas(self.root, width=512, height=512, background="grey")
        self.canvas.pack(side="right", padx=20, pady=20)

        self.input_frame = ctk.CTkFrame(self.root, height=100)
        self.input_frame.pack(side="left", padx=20, pady=100)

        self.prompt_label = ctk.CTkLabel(self.input_frame, text="Description:")
        self.prompt_label.grid(row=0, column=0, padx=10, pady=10)
        self.prompt_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Entrez votre description....", width=200,
                                         height=50)
        self.prompt_entry.grid(row=0, column=1, padx=10, pady=10)

        self.generate_button = ctk.CTkButton(self.input_frame, text="Générer", height=40, command=self.generate_image)
        self.generate_button.grid(row=1, column=0, columnspan=2, sticky="news", padx=25, pady=10)

        # Ajout du bouton "Enregistrer sous"
        self.save_button = ctk.CTkButton(self.input_frame, text="Enregistrer sous", height=40, command=self.save_image)
        self.save_button.grid(row=2, column=0, columnspan=2, sticky="news", padx=25, pady=10)
        self.save_button.configure(state=ctk.DISABLED)  # Désactiver le bouton tant qu'aucune image n'est générée

        self.generated_image = None


        # Ajout du menu de choix "local" ou "remote"
        self.use_remote_var = tk.StringVar(value="local")
        self.use_remote_menu = ctk.CTkOptionMenu(
            self.input_frame,
            variable=self.use_remote_var,
            values=["local", "remote"],
            command=self.switch_api
        )
        self.use_remote_menu.grid(row=3, column=0, columnspan=2, sticky="news", padx=25, pady=10)

        self.pipe = StableDiffusionPipeline.from_pretrained("hf-internal-testing/tiny-stable-diffusion-torch",cache_dir=cache_path)

        self.progressbar = ctk.CTkProgressBar(self.root)
        self.progressbar.pack_forget()

    def switch_api(self, value):
        if value == "remote":
            self.remote_api_url = CTkInputDialog(title="URL de l'API distante", text="Entrez l'URL de l'API distante:")
            self.remote_api_url = self.remote_api_url.get_input()
            if not self.remote_api_url:
                self.use_remote_var.set("local")
            else:
                self.pipe = None  # Réinitialiser le pipeline pour l'API distante
        else:
            self.remote_api_url = ''
            self.pipe = StableDiffusionPipeline.from_pretrained("hf-internal-testing/tiny-stable-diffusion-torch",cache_dir=cache_path)

    def generate_image(self):
        description = self.prompt_entry.get()
        if description:
            self.progressbar.pack(pady=20)
            threading.Thread(target=self.generate_image_thread, args=(description,)).start()

    def generate_image_thread(self, description):
        import torch

        def callback_on_step_end(pipe, step: int, timestep: int, latents: torch.FloatTensor, **kwargs):
            length = 30
            percent = 100 * (step / float(50))
            self.progressbar.set(percent / 100)
            print(f"Step: {step}, Timestep: {timestep}, Progress: {percent}%")
            return latents

        try:
            # Utilisation de l'API locale ou distante selon la sélection
            if self.use_remote_var.get() == "remote":
                self.listen_sse(self.remote_api_url, description)
            else:
                if not self.pipe:
                    self.pipe = StableDiffusionPipeline.from_pretrained(
                        "hf-internal-testing/tiny-stable-diffusion-torch",cache_dir=cache_path)
                image = \
                self.pipe(description, num_inference_steps=50, callback_on_step_end=callback_on_step_end).images[0]
                self.generated_image = image
                self.display_image(image)

        except Exception as e:
            messagebox.showerror("Error", f"Error generating image: {e}")

    def listen_sse(self, url, description):
        try:
            url = f'{url}/generate_progress'
            response = requests.post(url, json={"text": description}, stream=True)
            self.progressbar.set(0.0)

            #données du serveur distant indiquant la progression
            for chunck in response.iter_content(chunk_size=1024):
                stream = chunck.decode("utf-8")
                print(stream)
                if stream.startswith("data: image_id"):
                    self.fetch_generated_image(self.remote_api_url, stream.split("data: image_id")[1]) #id de l'image générée
                    break
                else:
                    self.progressbar.set(float(stream.split("data:")[1]))





        except Exception as e:
            messagebox.showerror("Error", f"Error listening to SSE: {e}")

    def fetch_generated_image(self, url, image_id):
        try:
            url = f'{url}/get_generated_image/{image_id}'
            response = requests.get(url)
            if response.status_code == 200:
                image_bytes = response.content
                image = Image.open(BytesIO(image_bytes))
                self.display_image(image)

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching image: {e}")

    def display_image(self, image):
        resized_image = image.resize((512, 512), resample=Image.LANCZOS)
        image_tk = ImageTk.PhotoImage(resized_image)
        self.root.after(10, self.progressbar.stop)
        self.root.after(10,self.progressbar.pack_forget) 
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
        self.canvas.image_tk = image_tk
        self.save_button.configure(state=ctk.NORMAL)  # Activer le bouton d'enregistrement

    def save_image(self):
        try:
            image = self.generated_image
            if image:
                filename = filedialog.asksaveasfilename(defaultextension=".png",
                                                        filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
                if filename:
                    image.save(filename)
                    messagebox.showinfo("Enregistrement", "L'image a été enregistrée avec succès.")

        except Exception as e:
            messagebox.showerror("Error", f"Error saving image: {e}")


if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
