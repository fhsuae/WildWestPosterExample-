import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps

# Main window
root = tk.Tk()
root.title("Wild West Poster Generator")
root.geometry("600x750")

# Variables
name_var = tk.StringVar()
location_var = tk.StringVar()
template_var = tk.StringVar(value="Classic")
poster_image = None
final_poster = None  # store for saving

# Functions
def upload_photo():
    global poster_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        poster_image = Image.open(file_path)
        poster_image.thumbnail((400, 400))
        img_tk = ImageTk.PhotoImage(poster_image)
        img_label.config(image=img_tk)
        img_label.image = img_tk

def apply_sepia(image):
    """Applies sepia filter to the image."""
    sepia = ImageOps.colorize(ImageOps.grayscale(image), "#704214", "#FFDAB9")
    return sepia

def generate_poster():
    global final_poster
    if not poster_image:
        messagebox.showerror("Error", "Please upload a photo first.")
        return

    name = name_var.get()
    location = location_var.get()
    template = template_var.get()

    # Apply sepia filter
    poster = apply_sepia(poster_image.copy())

    width, height = poster.size
    draw = ImageDraw.Draw(poster)

    # Load font
    try:
        font_title = ImageFont.truetype("western.ttf", 40)
        font_sub = ImageFont.truetype("western.ttf", 30)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Add text based on template
    if template == "Classic":
        draw.text((20, 20), f"Wanted: {name}", font=font_title, fill="brown")
        draw.text((20, height - 60), f"Location: {location}", font=font_sub, fill="brown")
        border_color = "brown"
    elif template == "Wanted":
        draw.text((20, 20), f"WANTED! {name}", font=font_title, fill="darkred")
        draw.text((20, height - 60), f"Last seen in {location}", font=font_sub, fill="darkred")
        border_color = "darkred"
    elif template == "Saloon":
        draw.text((20, 20), f"{name}'s Saloon", font=font_title, fill="saddlebrown")
        draw.text((20, height - 60), f"Located in {location}", font=font_sub, fill="saddlebrown")
        border_color = "saddlebrown"

    # Add border
    border_width = 20
    new_poster = Image.new("RGB", (width + border_width*2, height + border_width*2), border_color)
    new_poster.paste(poster, (border_width, border_width))

    # Display final poster
    final_poster = new_poster
    final_img = ImageTk.PhotoImage(final_poster)
    poster_display.config(image=final_img)
    poster_display.image = final_img

def save_poster():
    if final_poster:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png")])
        if file_path:
            final_poster.save(file_path)
            messagebox.showinfo("Saved", f"Poster saved to {file_path}")
    else:
        messagebox.showerror("Error", "Generate a poster first!")

# UI Widgets
tk.Label(root, text="Name:").pack()
tk.Entry(root, textvariable=name_var).pack()

tk.Label(root, text="Location:").pack()
tk.Entry(root, textvariable=location_var).pack()

tk.Button(root, text="Upload Photo", command=upload_photo).pack(pady=10)

tk.Label(root, text="Select Template:").pack()
ttk.Combobox(root, textvariable=template_var, values=["Classic", "Wanted", "Saloon"]).pack()

tk.Button(root, text="Generate Poster", command=generate_poster).pack(pady=10)
tk.Button(root, text="Save Poster", command=save_poster).pack(pady=5)

img_label = tk.Label(root)
img_label.pack(pady=10)

poster_display = tk.Label(root)
poster_display.pack(pady=10)

root.mainloop()
