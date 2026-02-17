from flask import Flask, render_template, request, jsonify
from ytmusicapi import YTMusic
import random
import os

app = Flask(__name__)

# Inicializa YTMusic (modo público)
ytmusic = YTMusic()


# =========================
# INTERPRETADOR DE MOOD
# =========================
def interpretar_mood(texto):
    texto = texto.lower()

    if "dormir" in texto or "sono" in texto:
        return "sleep chill relaxing music"
    elif "triste" in texto:
        return "sad emotional songs"
    elif "feliz" in texto:
        return "happy upbeat songs"
    elif "treino" in texto or "academia" in texto:
        return "workout gym music"
    elif "calma" in texto:
        return "relax lo-fi chill"
    elif "indie" in texto:
        return "indie alternative hits"
    else:
        return texto


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
        resultados = ytmusic.search(mood, filter="songs")

        random.shuffle(resultados)

        musicas = []

        for musica in resultados[:30]:
            titulo = musica.get("title")
            artistas = musica.get("artists", [])

            artista_nome = artistas[0]["name"] if artistas else "Desconhecido"

            # Thumbnail maior
            thumbnails = musica.get("thumbnails", [])
            capa = thumbnails[-1]["url"] if thumbnails else ""

            musicas.append({
                "titulo": titulo,
                "artista": artista_nome,
                "capa": capa
            })

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
