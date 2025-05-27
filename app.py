from flask import Flask, render_template, request
import csv
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['looma']
collection = db['scans']

# Load device info from CSV
def find_device(serial):
    with open('loomadevices.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['serial'] == serial:
                return row
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    device = None
    success = False

    if request.method == 'POST':
        serial = request.form['serial']
        username = request.form['username']
        location = request.form['location']

        device = find_device(serial)

        if device:
            # Create MongoDB document
            document = {
                'timestamp': datetime.utcnow(),
                'serial': serial,
                'model': device['model'],
                'build': device['build'],
                'username': username,
                'location': location
            }
            collection.insert_one(document)
            success = True

    return render_template('index.html', device=device, success=success)

if __name__ == '__main__':
    app.run(debug=True)
