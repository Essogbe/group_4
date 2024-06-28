import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from diffusers import StableDiffusionPipeline
import threading

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
        self.prompt_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Entrez votre description....", width=200, height=50)
        self.prompt_entry.grid(row=0, column=1, padx=10, pady=10)

        self.generate_button = ctk.CTkButton(self.input_frame, text="Generate", height=40, command=self.generate_image)
        self.generate_button.grid(row=1, column=0, columnspan=2, sticky="news", padx=25, pady=10)

        self.save_button = ctk.CTkButton(self.input_frame, text="Save", height=40, command=self.save_image)
        self.save_button.grid(row=2, column=0, columnspan=2, sticky="news", padx=25, pady=10)
        self.save_button.grid_remove()

        self.pipe = StableDiffusionPipeline.from_pretrained("hf-internal-testing/tiny-stable-diffusion-torch")

        self.progressbar = ctk.CTkProgressBar(self.root, mode="indeterminate")
        self.progressbar.pack_forget()

    def generate_image(self):
        description = self.prompt_entry.get()
        if description:
            self.progressbar.pack(pady=20)
            self.progressbar.start()
            threading.Thread(target=self.generate_image_thread, args=(description,)).start()

    def generate_image_thread(self, description):
        try:
            # Generation de l'image
            image = self.pipe(description).images[0]
            resized_image = image.resize((512, 512), resample=Image.LANCZOS)
            self.generated_image = resized_image
            image_tk = ImageTk.PhotoImage(resized_image)
            self.root.after(10, self.progressbar.stop)
            self.root.after(10, self.progressbar.pack_forget)  
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
            self.canvas.image_tk = image_tk 
            self.save_button.grid()

        except Exception as e:
            print(f"Error generating image: {e}")

    def save_image(self):
        if self.generated_image:
            file_path = ctk.filedialog.asksaveasfilename(defaultextension=".png",
                                                         filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("All files", "*.*")])
            if file_path:
                self.generated_image.save(file_path)
                print(f"Image saved to {file_path}")
            else:
                print("No image to save")

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
