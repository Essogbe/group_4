import tkinter as tk
from tkinter import messagebox, filedialog
from io import BytesIO
from PIL import Image, ImageTk
import customtkinter as ctk
import threading
import requests
from diffusers import StableDiffusionPipeline
import os
from customtkinter import CTkInputDialog, CTkSlider

current_dir = os.getcwd()
cache_path = os.path.join(current_dir, "cache")


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
        self.prompt_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Entrez votre description....", width=200,
                                         height=50)
        self.prompt_entry.grid(row=0, column=1, padx=10, pady=10)

        self.generate_button = ctk.CTkButton(self.input_frame, text="Générer", height=40, command=self.generate_image)
        self.generate_button.grid(row=1, column=0, columnspan=2, sticky="news", padx=25, pady=10)

        self.save_button = ctk.CTkButton(self.input_frame, text="Enregistrer sous", height=40, command=self.save_image)
        self.save_button.grid(row=2, column=0, columnspan=2, sticky="news", padx=25, pady=10)
        self.save_button.configure(state=ctk.DISABLED)

        self.generated_image = None

        self.use_remote_var = tk.StringVar(value="local")
        self.use_remote_menu = ctk.CTkOptionMenu(self.input_frame, variable=self.use_remote_var,
                                                 values=["local", "remote"], command=self.switch_api)
        self.use_remote_menu.grid(row=3, column=0, columnspan=2, sticky="news", padx=25, pady=10)

        # Ajout des sliders avec labels
        self.steps_label = ctk.CTkLabel(self.input_frame, text="Steps:")
        self.steps_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.slider_steps = CTkSlider(self.input_frame, from_=0, to=100, number_of_steps=10,
                                      command=self.update_steps_label)
        self.slider_steps.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        self.steps_value_label = ctk.CTkLabel(self.input_frame, text="0")
        self.steps_value_label.grid(row=4, column=2, padx=10, pady=10)

        self.temperature_label = ctk.CTkLabel(self.input_frame, text="Temperature:")
        self.temperature_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.slider_temperature = CTkSlider(self.input_frame, from_=0, to=100, number_of_steps=10,
                                            command=self.update_temperature_label)
        self.slider_temperature.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        self.temperature_value_label = ctk.CTkLabel(self.input_frame, text="0")
        self.temperature_value_label.grid(row=5, column=2, padx=10, pady=10)

        self.noise_scale_label = ctk.CTkLabel(self.input_frame, text="Noise Scale:")
        self.noise_scale_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        self.slider_noise_scale = CTkSlider(self.input_frame, from_=0, to=100, number_of_steps=10,
                                            command=self.update_noise_scale_label)
        self.slider_noise_scale.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

        self.noise_scale_value_label = ctk.CTkLabel(self.input_frame, text="0")
        self.noise_scale_value_label.grid(row=6, column=2, padx=10, pady=10)

        self.model_var = tk.StringVar(value="hf-internal-testing/tiny-stable-diffusion-torch")
        self.models = ["hf-internal-testing/tiny-stable-diffusion-torch", "model_1", "model_2"]

        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_var.get(), cache_dir=cache_path)

        self.progressbar = ctk.CTkProgressBar(self.root)
        self.progressbar.pack_forget()

        # Barre de menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=options_menu)

        options_menu.add_command(label="Choix du modèle", command=self.choose_model)
        options_menu.add_command(label="Ajouter un modèle", command=self.add_model)

    def choose_model(self):
        model_choice = tk.Toplevel(self.root)
        model_choice.title("Choix du modèle")
        model_choice.geometry("300x200")

        model_list = tk.Listbox(model_choice)
        model_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for model in self.models:
            model_list.insert(tk.END, model)

        def select_model():
            selected = model_list.curselection()
            if selected:
                self.model_var.set(self.models[selected[0]])
                self.pipe = StableDiffusionPipeline.from_pretrained(self.model_var.get(), cache_dir=cache_path)
                model_choice.destroy()

        select_button = ctk.CTkButton(model_choice, text="Sélectionner", command=select_model)
        select_button.pack(padx=10, pady=10)

    def add_model(self):
        add_model_dialog = CTkInputDialog(title="Ajouter un modèle", text="Entrez le nom du modèle:")
        new_model = add_model_dialog.get_input()
        if new_model:
            self.models.append(new_model)

    def update_steps_label(self, value):
        self.steps_value_label.configure(text=f"{int(value)}")

    def update_temperature_label(self, value):
        self.temperature_value_label.configure(text=f"{int(value)}")

    def update_noise_scale_label(self, value):
        self.noise_scale_value_label.configure(text=f"{int(value)}")

    def switch_api(self, value):
        if value == "remote":
            self.remote_api_url = CTkInputDialog(title="URL de l'API distante", text="Entrez l'URL de l'API distante:")
            self.remote_api_url = self.remote_api_url.get_input()
            if not self.remote_api_url:
                self.use_remote_var.set("local")
            else:
                self.pipe = None
        else:
            self.remote_api_url = ''
            self.pipe = StableDiffusionPipeline.from_pretrained(self.model_var.get(), cache_dir=cache_path)

    def generate_image(self):
        description = self.prompt_entry.get()
        if description:
            self.progressbar.pack(pady=20)
            threading.Thread(target=self.generate_image_thread, args=(description,)).start()

    def generate_image_thread(self, description):
        import torch

        def callback_on_step_end(pipe, step: int, timestep: int, latents: torch.FloatTensor, **kwargs):
            percent = 100 * (step / float(50))
            self.progressbar.set(percent / 100)
            print(f"Step: {step}, Timestep: {timestep}, Progress: {percent}%")
            return latents

        try:
            if self.use_remote_var.get() == "remote":
                self.listen_sse(self.remote_api_url, description)
            else:
                if not self.pipe:
                    self.pipe = StableDiffusionPipeline.from_pretrained(self.model_var.get(), cache_dir=cache_path)
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

            for chunk in response.iter_content(chunk_size=1024):
                stream = chunk.decode("utf-8")
                print(stream)
                if stream.startswith("data: image_id"):
                    self.fetch_generated_image(self.remote_api_url, stream.split("data: image_id")[1])
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
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
        self.canvas.image_tk = image_tk
        self.save_button.configure(state=ctk.NORMAL)

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
