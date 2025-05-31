import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from urllib.parse import urlencode

# Load CSV
data = pd.read_csv("loomadevices.csv")  # columns: serial, model, build

# Load and rotate logo
logo = Image.open("Looma-2019.png").convert("RGBA")
logo = logo.resize((80, 80))  # Resize as needed
logo = logo.rotate(270, expand=True)  # Rotate to vertical

# Create output directory
output_dir = "qr_labels"
os.makedirs(output_dir, exist_ok=True)

# Set fonts
try:
    font_bold = ImageFont.truetype("arialbd.ttf", 22)
    font_regular = ImageFont.truetype("arial.ttf", 20)
except:
    font_bold = ImageFont.load_default()
    font_regular = ImageFont.load_default()

# Generate each label
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
    label_width = 580
    label_height = 120
    label = Image.new("RGB", (label_width, label_height), "white")
    draw = ImageDraw.Draw(label)

    # Draw darker orange vertical strip with margin
    margin = 10
    orange_strip_width = 45
    orange_strip_height = label_height - 2 * margin
    dark_orange = (128, 40, 0)

    orange_strip = Image.new("RGB", (orange_strip_width, orange_strip_height), dark_orange)

    orange_x = label_width - orange_strip_width - margin
    orange_y = margin
    label.paste(orange_strip, (orange_x, orange_y))

    # Paste QR code
    label.paste(qr, (10, 10))

    # Paste vertical logo centered in orange strip
    logo_x = orange_x + (orange_strip_width - logo.width) // 2
    logo_y = orange_y + (orange_strip_height - logo.height) // 2
    label.paste(logo, (logo_x, logo_y), logo)

    # Add text
    text_x = 130
    draw.text((text_x, 20), "        Looma Education", font=font_bold, fill="black")
    draw.text((text_x, 50), "        +977 9812345678", font=font_regular, fill="black")
    draw.text((text_x, 80), f"        serial number: {serial}", font=font_bold, fill="black")

    # Save image
    output_path = os.path.join(output_dir, f"{serial}.png")
    label.save(output_path)

    print(f"QR label created for {serial} at {output_path}")
