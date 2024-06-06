from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import csv
import random

app = Flask(__name__)
app.secret_key = 'fvcksapos'

# Database files for different users
DB_FILES = {
    'Oriol': 'sets/set1.csv',
    'Manel': 'sets/set2.csv',
    'Arturo': 'sets/set3.csv'
}

# Load image pairs from CSV and cache them
def load_image_pairs():
    image_pairs = []
    with open(session['db_file'], 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['labelled'] = (row['labelled'] == 'True')
            image_pairs.append(row)
    return image_pairs


# Update image pair in CSV
def update_image_pair(image_pairs, image1, image2, label):
    for pair in image_pairs:
        if pair['image1'] == image1 and pair['image2'] == image2:
            pair['labelled'] = True
            pair['label'] = label
            break
    with open(session['db_file'], 'w', newline='') as file:
        fieldnames = ['image1', 'image2', 'labelled', 'label']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(image_pairs)


# Get a unique pair of images
def get_unique_pair(image_pairs):
    # Filter out labeled pairs
    available_pairs = [pair for pair in image_pairs if not pair['labelled']]
    # If no more unique pairs available, return None
    if not available_pairs:
        return None
    # Randomly select a pair
    return random.choice(available_pairs)


@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        # Load image pairs
        image_pairs = load_image_pairs()
        # Get next unique image pair to label
        image_pair = get_unique_pair(image_pairs)
        if image_pair is None:
            return "All pairs have been labeled."
        return render_template('index.html', image_pair=image_pair)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route('/label', methods=['POST'])
def label():
    try:
        image1 = request.form['image1']
        image2 = request.form['image2']
        label = request.form['label']
        # Load image pairs and update the specific pair
        image_pairs = load_image_pairs()
        update_image_pair(image_pairs, image1, image2, label)
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({"error": str(e)}), 404
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username in DB_FILES:
            session['username'] = username
            session['db_file'] = DB_FILES[username]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('db_file', None)
    return redirect(url_for('login'))
    

if __name__ == '__main__':
    app.run(debug=True)