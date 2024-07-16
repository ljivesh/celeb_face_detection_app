from flask import Flask, request, send_file, render_template, jsonify
from flask_cors import CORS
from predict import Predict
import requests


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize-celebrity', methods=['POST'])
def recognize_celebrity():
    files = request.files['file']
    print(files)
    files.save('file.jpg')
    pred = Predict('file.jpg')
    celebrity_name = pred[5:]
    print(celebrity_name)

    wikipedia_api_endpoint = f'https://en.wikipedia.org/api/rest_v1/page/summary/{celebrity_name}'

    try:
        # Fetch celebrity information from the Wikipedia API
        response = requests.get(wikipedia_api_endpoint)
        response.raise_for_status()

        # Extract relevant information from the response
        data = response.json()
        celebrity_data = {
            'name': celebrity_name,
            'image': data['thumbnail']['source'],
            'extract': data['extract']
        }

        return jsonify(celebrity_data)

    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the API request
        return jsonify({'error': str(e)}), 500


@app.route('/fetch-celebrity-info', methods=['POST'])
def fetch_celebrity_info():
    # Get the celebrity name from the request
    celebrity_name = request.form.get('celebrity_name')

    # Make a request to the Wikipedia API
    wikipedia_url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=true&explaintext=true&titles={celebrity_name}'
    response = requests.get(wikipedia_url)

    # Return the Wikipedia API response to the frontend
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True)