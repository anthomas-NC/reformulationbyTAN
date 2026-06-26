import os
import json
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Récupération de la clé API DeepSeek depuis les variables d'environnement
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reformuler", methods=["POST"])
def reformuler():
    data = request.json
    texte = data.get("texte", "")

    prompt = f"""
Reformule ce texte de manière polie, diplomatique et élégante,
dans un style inspiré de Talleyrand.

Texte à reformuler :
{texte}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Tu es un expert en reformulation élégante."},
            {"role": "user", "content": prompt}
        ]
    }

    # Appel API
    response = requests.post(API_URL, headers=headers, json=payload)

    # LOG IMPORTANT POUR DEBUG
    print("DEBUG RAW RESPONSE:", response.text)

    try:
        result = response.json()
        reformulation = result["choices"][0]["message"]["content"]
        return jsonify({"reformulation": reformulation})

    except Exception as e:
        # Retourne l'erreur brute pour comprendre ce que renvoie DeepSeek
        return jsonify({
            "error": f"Erreur API : {str(e)}",
            "raw_response": response.text
        })

# Lancement compatible Render (port dynamique)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
