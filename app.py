from flask import Flask, render_template, request, jsonify
import sqlite3
from moodify_v2 import gerar_musicas

app = Flask(__name__)

# ------------------------
# BANCO DE DADOS
# ------------------------

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS curtidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            musica TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ------------------------
# ROTA PRINCIPAL
# ------------------------

@app.route("/")
def home():
    return render_template("index.html")

# ------------------------
# GERAR MÚSICAS
# ------------------------

@app.route("/gerar", methods=["POST"])
def gerar():
    mood = request.json["mood"]

    # salva no histórico
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO historico (mood) VALUES (?)", (mood,))
    conn.commit()
    conn.close()

    musicas = gerar_musicas(mood)

    return jsonify(musicas)

# ------------------------
# CURTIR MÚSICA
# ------------------------

@app.route("/curtir", methods=["POST"])
def curtir():
    musica = request.json["musica"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO curtidas (musica) VALUES (?)", (musica,))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

# ------------------------
# VER HISTÓRICO
# ------------------------

@app.route("/historico")
def historico():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT mood FROM historico ORDER BY id DESC LIMIT 5")
    dados = cursor.fetchall()
    conn.close()

    return jsonify(dados)

# ------------------------

if __name__ == "__main__":
    app.run(debug=True)
