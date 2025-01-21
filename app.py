from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


# Clé API et ID du moteur de recherche
API_KEY = "AIzaSyDU8TZXPbK0U4lDC_nhq8yWer70PYloNaA"
CX = "c4f6495c4d2f042fb"

@app.route('/')
def home():
    return "Bienvenue sur l'application de recherche de brevets !"

@app.route('/favicon.ico')
def favicon():
    return "", 204

@app.route('/search', methods=['POST'])
def search_patent():
    data = request.json
    query = data.get('query')

    # Requête vers l'API Custom Search
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}"
    response = requests.get(url)

    if response.status_code == 200:
        results = response.json().get('items', [])
        return jsonify({
            "status": "success",
            "results": [
                {
                    "title": item.get('title'),
                    "link": item.get('link'),
                    "snippet": item.get('snippet')
                } for item in results
            ]
        })
    else:
        return jsonify({"status": "error", "message": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
