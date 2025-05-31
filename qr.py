import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from urllib.parse import urlencode

# loading csv
data = pd.read_csv("loomadevices.csv")  # columns: serial, model, build

# Prepare vertical logo
logo = Image.open("Looma-2019.png").convert("RGBA")
logo = logo.resize((100, 100))  # resize as needed
logo = logo.rotate(270, expand=True)

#  Create output directory 
output_dir = "qr_labels"
os.makedirs(output_dir, exist_ok=True)

#  Set fonts 
try:
    font_bold = ImageFont.truetype("arialbd.ttf", 20)
    font_regular = ImageFont.truetype("arial.ttf", 18)
except:
    font_bold = ImageFont.load_default()
    font_regular = ImageFont.load_default()

#  Generate each label
BASE_URL = "http://127.0.0.1:5000/"

for _, row in data.iterrows():
    serial = str(row['serial']).strip()
    model = str(row['model']).strip()
    build = str(row['build']).strip()

    # Construct URL
    query = urlencode({"serial": serial, "model": model, "build": build})
    full_url = BASE_URL + "?" + query

    # Generate QR code
    qr = qrcode.make(full_url)
    qr = qr.resize((100, 100))

    # Create label canvas
    label = Image.new("RGB", (600, 120), "white")
    draw = ImageDraw.Draw(label)

    # Paste QR and logo
    label.paste(qr, (10, 10))
    label.paste(logo, (490, 10), logo)

    # Add text info
    draw.text((130, 20), "Looma Education", font=font_bold, fill="black")
    draw.text((130, 50), "+977 9812345678", font=font_regular, fill="black")
    draw.text((130, 80), f"serial number: {serial}", font=font_bold, fill="black")

    # Save label
    output_path = os.path.join(output_dir, f"{serial}.png")
    label.save(output_path)

    print(f" QR label created for {serial} and {output_path}")
 
