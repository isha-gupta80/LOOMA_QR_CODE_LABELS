import pandas as pd
import qrcode
import os

# Read device info from CSV
data = pd.read_csv("loomadevices.csv")  # columns: serial, model, build

# Output folder
os.makedirs("qr_codes", exist_ok=True)
for index, row in data.iterrows():
    serial = row['serial']
    model = row['model']
    build = row['build']
    url = f"http://127.0.0.1:5000serial={serial}&model={model}&build={build}"

    qr = qrcode.make(url)
    qr.save(f"qr_codes/{serial}.png")

    print(f"Generated QR for {serial}")