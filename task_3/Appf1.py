import tkinter as tk
from io import BytesIO
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from diffusers import StableDiffusionPipeline
import threading
from sseclient import SSEClient

import requests

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("GeniArt")
        self.root.resizable(width=False, height=False)

        ctk.set_appearance_mode("dark")

        self.canvas = tk.Canvas(self.root, width=512, height=512)
        self.canvas.pack(side="right", padx=20, pady=20)

        self.input_frame = ctk.CTkFrame(self.root, height=100)
        self.input_frame.pack(side="left", padx=20, pady=100)

        self.prompt_label = ctk.CTkLabel(self.input_frame, text="Description:")
        self.prompt_label.grid(row=0, column=0, padx=10, pady=10)
        self.prompt_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Entrez votre description....", width=200, height=50)
        self.prompt_entry.grid(row=0, column=1, padx=10, pady=10)

        self.generate_button = ctk.CTkButton(self.input_frame, text="Generate", height=40, command=self.generate_image)
        self.generate_button.grid(row=1, column=0, columnspan=2, sticky="news", padx=25, pady=10)

        self.pipe = StableDiffusionPipeline.from_pretrained("hf-internal-testing/tiny-stable-diffusion-torch")

        self.progressbar = ctk.CTkProgressBar(self.root)
        self.progressbar.pack_forget()

    def generate_image(self):
        description = self.prompt_entry.get()
        if description:
            self.progressbar.pack(pady=20)

            threading.Thread(target=self.generate_image_thread, args=(description,)).start()

    def listen_sse(self,url, description):
        try:
            url = 'http://localhost:5000/generate_progress'
            response = requests.post(url, json={"text": description}, stream=True)

            client = SSEClient(response.iter_lines())
            for event in client.events():
                if event.event == 'message':
                    message_data = event.data.strip()
                    if message_data.startswith('data:image_id:'):
                        image_id = message_data.split(':')[2]
                        self.fetch_generated_image(image_id)
                        break

        except Exception as e:
            messagebox.showerror("Error", f"Error listening to SSE: {e}")

    def fetch_generated_image(self, url,image_id):
        try:
            url = f'{url}/get_generated_image/{image_id}'
            response = requests.get(url)
            if response.status_code == 200:
                image_bytes = response.content
                image = Image.open(BytesIO(image_bytes))
                image = image.resize((512, 512), resample=Image.LANCZOS)
                image_tk = ImageTk.PhotoImage(image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
                self.canvas.image_tk = image_tk

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching image: {e}")
    def generate_image_thread(self, description):
        import torch
        def callback_on_step_end(pipe, step: int, timestep: int, latents: torch.FloatTensor, **kwargs):

            length = 30

            print(f"Step: {step}, Timestep: {timestep}")

            # Calcul du pourcentage d'avancement
            percent = 100 * (step / float(50))

            # Mise à jour de la barre de progression
            self.progressbar.set(percent / 100)

            print(percent / 100)
            print("Current", self.progressbar.get())
            return latents
        try:
            # Generation de l'image
            image = self.pipe(description,num_inference_steps=50,callback_on_step_end=callback_on_step_end).images[0]
            resized_image = image.resize((512, 512), resample=Image.LANCZOS)
            image_tk = ImageTk.PhotoImage(resized_image)
            self.root.after(10, self.progressbar.stop)
            self.root.after(10,self.progressbar.pack_forget)  
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
            self.canvas.image_tk = image_tk 

        except Exception as e:
            print(f"Error generating image: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
