from flask import Flask, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import random

load_dotenv() # Load environment variables from a .env file

app = Flask(__name__)
CORS(app) # This allows our frontend to talk to this backend

NASA_API_KEY = os.getenv('NASA_API_KEY')
# Use a default key if you don't have one, but it's rate-limited
if not NASA_API_KEY:
    NASA_API_KEY = "DEMO_KEY"

# --- Helper function to add Carl's simple explanations ---
def add_carls_explanation(api_data, data_type):
    """Takes raw NASA data and adds a kid-friendly explanation."""
    
    if data_type == "apod":
        return {
            "title": api_data.get('title', 'A Cool Space Picture!'),
            "explanation": "Carl's Cosmic Commentary: " + api_data.get('explanation', 'Wow, look at this!')[:150] + "... Isn't space amazing?",
            "kid_friendly_title": "🌟 Carl's Picture of the Day!",
            "image_url": api_data.get('url', ''),
            "date": api_data.get('date', 'Today')
        }
    
    elif data_type == "mars_photo":
       
        rover = api_data.get('rover', {})
        if isinstance(rover, dict):
            rover_name = rover.get('name', 'Curiosity')
        else:
            rover_name = 'Curiosity'
        
        
        camera = api_data.get('camera', {})
        if isinstance(camera, dict):
            camera_name = camera.get('full_name', 'a special camera')
        else:
            camera_name = 'a special camera'
        
        return {
            "rover_name": rover_name,
            "earth_date": api_data.get('earth_date', 'a sunny day on Mars'),
            "camera": camera_name,
            "img_src": api_data.get('img_src', ''),
            "caption": f"📸 Carl says: This photo was taken by the {rover_name} rover on {api_data.get('earth_date', 'a sunny day on Mars')}. It's using its {camera_name} camera!"
        }
    
    elif data_type == "fun_fact":
        return api_data
    
    return api_data

@app.route('/')
def index():
    # This will serve our main HTML page
    return render_template('index.html')

# --- API Endpoint 1: Astronomy Picture of the Day (APOD) ---
@app.route('/api/apod')
def get_apod():
    try:
        response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}')
        response.raise_for_status()
        nasa_data = response.json()
        # Add Carl's magic
        kid_friendly_data = add_carls_explanation(nasa_data, "apod")
        return jsonify(kid_friendly_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Carl couldn't reach NASA. Maybe his antenna is broken? Try again!"}), 500

# --- API Endpoint 2: Latest Mars Rover Photos ---
# --- API Endpoint 2: Latest Mars Rover Photos ---
# --- API Endpoint 2: Mars Rover Photos (Simplified Version) ---
@app.route('/api/mars-photo')
def get_mars_photo():
    try:
        
        import random
        
        
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date=2023-06-01&api_key={NASA_API_KEY}"
        
        print(f"Fetching Mars photos from: {url}")  
        response = requests.get(url)
        response.raise_for_status()
        nasa_data = response.json()
        
        photos = nasa_data.get('photos', [])
        print(f"Found {len(photos)} photos")  
        if photos:
            
            random_photo = random.choice(photos)
            
            
            result = {
                "rover_name": random_photo.get('rover', {}).get('name', 'Curiosity'),
                "earth_date": random_photo.get('earth_date', 'a sunny day on Mars'),
                "camera": random_photo.get('camera', {}).get('full_name', 'a special camera'),
                "img_src": random_photo.get('img_src', ''),
                "caption": f"📸 Carl says: This photo was taken by the {random_photo.get('rover', {}).get('name', 'Curiosity')} rover on {random_photo.get('earth_date', 'a sunny day on Mars')}. It's using its {random_photo.get('camera', {}).get('full_name', 'a special camera')} camera!"
            }
            return jsonify(result)
        else:
            
            print("No photos found, using sample data")
            sample_photos = [
                {
                    "rover_name": "Curiosity",
                    "earth_date": "2023-06-01",
                    "camera": "Mast Camera",
                    "img_src": "https://mars.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/fcam/FLB_486265257EDR_F0481570FHAZ00323M_.JPG",
                    "caption": "📸 Carl says: This is a sample Mars photo from the Curiosity rover! The real NASA photos might be loading slowly."
                },
                {
                    "rover_name": "Perseverance",
                    "earth_date": "2023-05-15",
                    "camera": "Navigation Camera",
                    "img_src": "https://mars.nasa.gov/mars2020-raw-images/pub/ods/surface/sol/00772/ids/edr/browse/ncam/NLF_0772_0753944720_791ECM_N0030000NCAM01001_01_095J01_1200.jpg",
                    "caption": "📸 Carl says: The Perseverance rover took this selfie on Mars! Isn't it cool?"
                }
            ]
            return jsonify(random.choice(sample_photos))

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Mars photos: {e}")
        
        return jsonify({
            "rover_name": "Curiosity",
            "earth_date": "a sunny day on Mars",
            "camera": "Mast Camera",
            "img_src": "https://mars.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/fcam/FLB_486265257EDR_F0481570FHAZ00323M_.JPG",
            "caption": "📸 Carl says: Oops! NASA's connection is a bit slow right now. Here's a sample Mars photo while we wait!"
        }), 200  
# --- API Endpoint 3: A Fun Space Fact ---
@app.route('/api/fun-fact')
def get_fun_fact():
    # Carl has his own list of fun, simple facts!
    fun_facts = [
        "🪐 Did you know? A day on Venus is longer than a year on Venus!",
        "☀️ The Sun is so big that you could fit over 1 million Earths inside it.",
        "🌕 The Moon is slowly drifting away from Earth, about 3.8 centimeters every year.",
        "🪨 There's a massive volcano on Mars called Olympus Mons. It's nearly three times taller than Mount Everest!",
        "🌀 A 'Jupiter Year' (the time it takes to go around the Sun) is almost 12 Earth years. Happy (almost) Birthday, Jupiter!",
        "⭐ The stars you see at night might already be gone. Their light takes so long to reach us that we're seeing them as they were a long, long time ago."
    ]
    return jsonify({"fact": random.choice(fun_facts)})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=10000)