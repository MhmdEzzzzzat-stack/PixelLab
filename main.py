"""
PixelLab - Advanced Image Processing Lab
Modern Python GUI built with CustomTkinter, Pillow and NumPy.

Install:
    pip install -r requirements.txt

Run:
    python main.py
"""

from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image, ImageOps, ImageDraw


ROOT_DIR = Path(__file__).resolve().parent
BG_PATH = ROOT_DIR / "assets" / "pixellab_background.jpg"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PixelLab(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PixelLab | Advanced Image Processing Lab")
        self.geometry("1440x900")
        self.minsize(1050, 720)
        self.configure(fg_color="#05082b")

        self.original = None
        self.converted = None
        self.original_ctk = None
        self.result_ctk = None
        self.background_ctk = None
        self.background_pil = None
        self.hero_background_ctk = None

        self.create_background()
        self.create_header()
        self.create_hero()
        self.create_workspace()
        self.create_footer()

        self.bind("<Configure>", self._resize_background)

    # ---------- Background and layout ----------
    def create_background(self):
        self.bg_label = ctk.CTkLabel(self, text="", fg_color="#05082b")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.lower()
        self._load_background()

    def _load_background(self):
        if not BG_PATH.exists():
            return
        try:
            w = max(self.winfo_width(), 1050)
            h = max(self.winfo_height(), 720)
            source = Image.open(BG_PATH).convert("RGB")
            source = ImageOps.fit(source, (w, h), method=Image.Resampling.LANCZOS)
            self.background_pil = source.copy()
            self.background_ctk = ctk.CTkImage(
                light_image=source, dark_image=source, size=(w, h)
            )
            self.bg_label.configure(image=self.background_ctk)
            self.bg_label.lower()
            self._refresh_hero_background()
        except Exception:
            pass

    def _resize_background(self, event):
        if event.widget == self:
            self.after(120, self._load_background)

    def _refresh_hero_background(self):
        """Show the matching part of the window wallpaper inside the hero panel."""
        if self.background_pil is None or not hasattr(self, "hero_bg_label"):
            return
        try:
            win_w = max(self.winfo_width(), 1050)
            win_h = max(self.winfo_height(), 720)
            left = int(win_w * 0.06)
            top = int(win_h * 0.12)
            right = int(win_w * 0.94)
            bottom = int(win_h * (0.12 + 0.265))
            crop = self.background_pil.crop((left, top, right, bottom))
            panel_w = max(self.hero.winfo_width(), 700)
            panel_h = max(self.hero.winfo_height(), 180)
            crop = crop.resize((panel_w, panel_h), Image.Resampling.LANCZOS)
            self.hero_background_ctk = ctk.CTkImage(
                light_image=crop, dark_image=crop, size=(panel_w, panel_h)
            )
            self.hero_bg_label.configure(image=self.hero_background_ctk)
            self.hero_bg_label.lower()
        except Exception:
            pass

    def create_header(self):
        self.header = ctk.CTkFrame(
            self, fg_color="#090f3d", corner_radius=24,
            border_width=1, border_color="#3446c9"
        )
        self.header.place(relx=0.025, rely=0.018, relwidth=0.95, relheight=0.075)

        ctk.CTkLabel(
            self.header, text="◉  PixelLab",
            font=ctk.CTkFont(family="Arial", size=25, weight="bold"),
            text_color="#ffffff"
        ).pack(side="left", padx=25)

        ctk.CTkLabel(
            self.header, text="⌂  Home      ⓘ  About      ✉  Contact",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#e7eaff"
        ).pack(side="left", padx=50)

        ctk.CTkLabel(
            self.header, text="✦  PYTHON IMAGE PROCESSING",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#48eaff"
        ).pack(side="right", padx=25)

    def create_hero(self):
        self.hero = ctk.CTkFrame(self, fg_color="transparent", corner_radius=20)
        self.hero.place(relx=0.06, rely=0.12, relwidth=0.88, relheight=0.265)
        self.hero_bg_label = ctk.CTkLabel(self.hero, text="", fg_color="transparent")
        self.hero_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self._refresh_hero_background()

        ctk.CTkLabel(
            self.hero, text="✦  ADVANCED IMAGE PROCESSING LAB",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#43eaff"
        ).pack(anchor="w", padx=28, pady=(13, 0))

        ctk.CTkLabel(
            self.hero, text="PixelLab",
            font=ctk.CTkFont(family="Arial", size=48, weight="bold"),
            text_color="#ffffff"
).pack(anchor="w", padx=25, pady=(0, 0))
        ctk.CTkLabel(
            self.hero, text="Transform pixels into possibilities.",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#f5f6ff"
        ).pack(anchor="w", padx=28)

        ctk.CTkLabel(
            self.hero,
            text="Upload, edit and convert your images with professional quality.",
            font=ctk.CTkFont(size=13),
            text_color="#d8e0ff"
        ).pack(anchor="w", padx=28, pady=(2, 10))

        buttons = ctk.CTkFrame(self.hero, fg_color="transparent")
        buttons.pack(anchor="w", padx=25, pady=(3, 8))

        self.gradient_button(
            buttons, "⬆  Upload Image", self.upload_image, width=180, height=40
        ).pack(side="left", padx=(0, 12))
        self.secondary_button(
            buttons, "▶  Try Demo", self.load_demo, width=135, height=40
        ).pack(side="left")

    def create_workspace(self):
        self.workspace = ctk.CTkFrame(
            self,fg_color="#08134f", corner_radius=26,
            border_width=2, border_color="#a34cff"
        )
        self.workspace.place(relx=0.035, rely=0.425, relwidth=0.93, relheight=0.50)

        # Upload zone
        self.upload_panel = ctk.CTkFrame(
            self.workspace, fg_color="#111e62", corner_radius=18,
            border_width=1, border_color="#578cff"
        )
        self.upload_panel.place(relx=0.018, rely=0.055, relwidth=0.285, relheight=0.72)

        ctk.CTkLabel(
            self.upload_panel, text="☁",
            font=ctk.CTkFont(size=55), text_color="#25dcff"
        ).pack(pady=(14, 0))
        ctk.CTkLabel(
            self.upload_panel, text="Drag & Drop Your Image",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=(0, 2))
        ctk.CTkLabel(
            self.upload_panel, text="or click to browse",
            font=ctk.CTkFont(size=12), text_color="#dce2ff"
        ).pack()

        self.file_label = ctk.CTkLabel(
            self.upload_panel, text="Supports: PNG, JPG, JPEG, WEBP",
            font=ctk.CTkFont(size=11), text_color="#ffffff",
            wraplength=300
        )
        self.file_label.pack(pady=14)

        self.secondary_button(
            self.upload_panel, "Choose Image", self.upload_image, width=170
        ).pack(pady=(0, 12))

        # Conversion area
        self.controls = ctk.CTkFrame(self.workspace, fg_color="transparent")
        self.controls.place(relx=0.32, rely=0.055, relwidth=0.195, relheight=0.72)

        ctk.CTkLabel(
            self.controls, text="🎨  Select Conversion",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=(20, 15))

        self.operation = ctk.StringVar(value="RGB → Grayscale")
        self.operation_menu = ctk.CTkOptionMenu(
            self.controls,
            variable=self.operation,
            values=["RGB → Grayscale", "RGB → CMY"],
            fg_color="#182d78",
            button_color="#315be0",
            button_hover_color="#5144d9",
            dropdown_fg_color="#101c58",
            dropdown_hover_color="#293b91",
            text_color="white",
            font=ctk.CTkFont(size=12),
            dropdown_font=ctk.CTkFont(size=12),
            height=42,
            corner_radius=18
        )
        self.operation_menu.pack(fill="x", padx=3)

        self.gradient_button(
            self.controls, "⟳  Convert Image", self.convert_image,
            width=235, height=54
        ).pack(fill="x", padx=1, pady=(18, 17))


        # Original and output preview cards
        self.original_card, self.original_preview = self.preview_card(
            "▣  Original Image", 0.535
        )
        self.result_card, self.result_preview = self.preview_card(
            "✥  Converted Result", 0.765
        )

        # Bottom controls
        self.secondary_button(
            self.workspace, "⟳  Reset", self.reset, width=135, height=42
        ).place(relx=0.018, rely=0.82)

        self.gradient_button(
            self.workspace, "⬇  Download Result", self.download_result,
            width=210, height=44
        ).place(relx=0.815, rely=0.82)

    def preview_card(self, title, x):
        card = ctk.CTkFrame(
            self.workspace, fg_color="#111d61", corner_radius=16,
            border_width=1, border_color="#3b8cff"
        )
        card.place(relx=x, rely=0.055, relwidth=0.215, relheight=0.72)

        ctk.CTkLabel(
            card, text=title, font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w", padx=11, pady=8)

        preview = ctk.CTkLabel(
            card, text="No image selected",
            font=ctk.CTkFont(size=12), text_color="#b8c7ff",
            fg_color="#080f3b", corner_radius=10
        )
        preview.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        return card, preview

    def create_footer(self):
        self.status = ctk.CTkLabel(
            self,
            text="✦   Powered by PixelLab   •   Python   •   Fast   •   High Quality",
            font=ctk.CTkFont(size=10),
            text_color="#ffffff",
            fg_color="transparent"
        )
        self.status.place(relx=0.33, rely=0.948, relwidth=0.34, relheight=0.024)

    # ---------- Styled buttons ----------
    def gradient_button(self, parent, text, command, width=200, height=48):
        # CTkButton provides the neon-blue/purple visual treatment.
        return ctk.CTkButton(
            parent, text=text, command=command,
            width=width, height=height, corner_radius=25,
            fg_color="#174dff", hover_color="#a000e8",
            border_width=1, border_color="#23dfff",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold")
        )

    def secondary_button(self, parent, text, command, width=160, height=45):
        return ctk.CTkButton(
            parent, text=text, command=command,
            width=width, height=height, corner_radius=24,
            fg_color="#20296f", hover_color="#3445a5",
            border_width=1, border_color="#737cff",
            text_color="white",
            font=ctk.CTkFont(size=13, weight="bold")
        )

    # ---------- Image loading and previews ----------
    def upload_image(self):
        path = filedialog.askopenfilename(
            title="Select image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.webp *.bmp"),
                ("All files", "*.*")
            ]
        )
        if not path:
            return
        try:
            image = Image.open(path).convert("RGB")
            self.set_original(image)
            self.file_label.configure(text=Path(path).name)
            self.set_status("Image loaded successfully.")
        except Exception as exc:
            messagebox.showerror("PixelLab", f"Could not open image:\n{exc}")

    def load_demo(self):
        width, height = 900, 560
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)

        for y in range(height):
            color = (
                int(35 + 190 * (1 - y / height)),
                int(45 + 90 * (1 - y / height)),
                int(110 + 120 * (1 - y / height))
            )
            draw.line((0, y, width, y), fill=color)

        draw.ellipse((620, 105, 760, 245), fill="#ffc078")
        draw.polygon(
            [(0, 390), (170, 260), (330, 405), (510, 285),
             (700, 410), (900, 290), (900, 560), (0, 560)],
            fill="#1e2d69"
        )
        draw.polygon(
            [(0, 465), (220, 360), (430, 485), (650, 370),
             (900, 465), (900, 560), (0, 560)],
            fill="#0a1641"
        )

        self.set_original(image)
        self.file_label.configure(text="Demo landscape")
        self.set_status("Demo loaded. Choose a conversion and press Convert Image.")

    def set_original(self, image):
        self.original = image.copy()
        self.converted = None
        self.update_preview(self.original, self.original_preview, "original")
        self.result_preview.configure(image=None, text="Convert to see result")
        self.result_ctk = None

    def update_preview(self, image, label, which):
        preview = image.copy()
        preview.thumbnail((340, 245), Image.Resampling.LANCZOS)
        photo = ctk.CTkImage(
            light_image=preview, dark_image=preview,
            size=preview.size
        )
        label.configure(image=photo, text="")
        if which == "original":
            self.original_ctk = photo
        else:
            self.result_ctk = photo

    # ---------- Image processing operations ----------
    def convert_image(self):
        if self.original is None:
            messagebox.showinfo("PixelLab", "Please upload an image first.")
            return

        image = self.original.copy()
        choice = self.operation.get()

        try:
            if choice == "RGB → Grayscale":
                result = ImageOps.grayscale(image)
            else:  # RGB → CMY
                result = ImageOps.invert(image)

            self.converted = result
            self.update_preview(result, self.result_preview, "result")
            self.set_status(f"Conversion completed: {choice}")

        except Exception as error:
            messagebox.showerror("Conversion error", str(error))

    # ---------- Save and reset ----------
    def download_result(self):
        if self.converted is None:
            messagebox.showinfo("PixelLab", "Convert an image before downloading.")
            return

        path = filedialog.asksaveasfilename(
            title="Save converted image",
            defaultextension=".png",
            filetypes=[
                ("PNG image", "*.png"),
                ("JPEG image", "*.jpg"),
                ("WEBP image", "*.webp"),
                ("TIFF image", "*.tiff")
            ]
        )
        if not path:
            return

        try:
            self.converted.save(path)
            self.set_status(f"Saved: {Path(path).name}")
            messagebox.showinfo("PixelLab", "Image saved successfully.")
        except Exception as exc:
            messagebox.showerror("Save error", str(exc))

    def reset(self):
        self.original = None
        self.converted = None
        self.original_preview.configure(image=None, text="No image selected")
        self.result_preview.configure(image=None, text="No result yet")
        self.original_ctk = None
        self.result_ctk = None
        self.file_label.configure(text="Supports: PNG, JPG, JPEG, WEBP")
        self.operation.set("RGB → Grayscale")
        self.set_status("Ready. Upload an image or try the demo.")

    def set_status(self, text):
        self.status.configure(text=f"✦   {text}")


if __name__ == "__main__":
    app = PixelLab()
    app.mainloop()
