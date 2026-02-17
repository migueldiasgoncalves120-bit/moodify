from flask import Flask, render_template, request, jsonify
import requests
import random
import os

app = Flask(__name__)

# 🔥 SUA API DO DEEZER (usando busca pública)
DEEZER_API = "https://api.deezer.com/search?q="


# =========================
# GERAR MÚSICAS
# =========================
@app.route("/gerar", methods=["POST"])
def gerar():
    data = request.get_json()
    mood = data.get("mood", "")

    if not mood:
        return jsonify([])

    try:
        response = requests.get(DEEZER_API + mood)
        dados = response.json()

        musicas = []
        resultados = dados.get("data", [])

        # Embaralha para evitar repetir sempre as mesmas
        random.shuffle(resultados)

        for musica in resultados[:10]:  # Limita a 10 músicas
            musicas.append({
                "titulo": musica["title"],
                "artista": musica["artist"]["name"],
                "capa": musica["album"]["cover_medium"]
            })

        return jsonify(musicas)

    except Exception as e:
        print("Erro:", e)
        return jsonify([])


# =========================
# CURTIR MÚSICA
# =========================
@app.route("/curtir", methods=["POST"])
def curtir():
    data = request.get_json()
    musica = data.get("musica")

    print(f"Música curtida: {musica}")

    return jsonify({"status": "ok"})


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# RODAR APP (RENDER + LOCAL)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
