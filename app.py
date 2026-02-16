import os
from flask import Flask, render_template, request
from ytmusicapi import YTMusic

app = Flask(__name__)
yt = YTMusic()

@app.route("/", methods=["GET", "POST"])
def index():
    musicas = []

    if request.method == "POST":
        entrada = request.form.get("mood", "").lower()

        if entrada:
            resultados = yt.search(entrada, filter="songs")

            for item in resultados[:50]:
                titulo = item.get("title")
                artistas = item.get("artists")
                artista = artistas[0]["name"] if artistas else ""
                musicas.append(f"{titulo} – {artista}")

            musicas = list(dict.fromkeys(musicas))[:30]

    return render_template("index.html", musicas=musicas)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
