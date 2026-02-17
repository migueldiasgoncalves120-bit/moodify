from flask import Flask, render_template, request, jsonify
import requests
import random
import os

app = Flask(__name__)

DEEZER_API = "https://api.deezer.com/search?q="


# =========================
# FUNÇÃO INTELIGENTE DE MOOD
# =========================
def interpretar_mood(texto):
    texto = texto.lower()

    if "dormir" in texto or "sono" in texto:
        return "sleep chill instrumental"
    elif "triste" in texto:
        return "sad acoustic"
    elif "feliz" in texto:
        return "happy pop"
    elif "treino" in texto or "academia" in texto:
        return "workout electronic"
    elif "calma" in texto:
        return "relax lo-fi"
    elif "indie" in texto:
        return "indie alternative"
    else:
        return texto  # se não reconhecer, usa o texto normal


# =========================
# GERAR MÚSICAS
# =========================
@app.route("/gerar", methods=["POST"])
def gerar():
    data = request.get_json()
    mood_input = data.get("mood", "")

    if not mood_input:
        return jsonify([])

    mood = interpretar_mood(mood_input)

    try:
        response = requests.get(DEEZER_API + mood)
        dados = response.json()
        resultados = dados.get("data", [])

        random.shuffle(resultados)

        musicas = []
        usadas = set()

        for musica in resultados:
            titulo = musica["title"]

            if titulo in usadas:
                continue

            usadas.add(titulo)

            musicas.append({
                "titulo": titulo,
                "artista": musica["artist"]["name"],
                "capa": musica["album"]["cover_medium"]
            })

            if len(musicas) == 30:
                break

        return jsonify(musicas)

    except Exception as e:
        print("Erro:", e)
        return jsonify([])


# =========================
# CURTIR
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
# RENDER + LOCALHOST
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
