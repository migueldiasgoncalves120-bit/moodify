from ytmusicapi import YTMusic

yt = YTMusic()

print("🎧 Moodify v2 - Inteligência de Humor Musical\n")

entrada = input("Descreva que tipo de música você quer hoje:\n> ").lower()

# Categorias
emocoes = {
    "triste": "sad",
    "feliz": "happy",
    "melancolico": "melancholic",
    "apaixonado": "romantic",
    "raiva": "angry",
    "nostalgia": "nostalgic"
}

energias = {
    "calma": "calm",
    "suave": "soft",
    "animada": "upbeat",
    "pesada": "heavy",
    "intensa": "intense",
    "relaxante": "relax"
}

generos = {
    "pop": "pop",
    "rock": "rock",
    "funk": "funk",
    "eletronica": "electronic",
    "eletrônica": "electronic",
    "trap": "trap",
    "rap": "rap",
    "lofi": "lofi",
    "sertanejo": "sertanejo"
}

busca_final = []

# Detectar palavras
for palavra in emocoes:
    if palavra in entrada:
        busca_final.append(emocoes[palavra])

for palavra in energias:
    if palavra in entrada:
        busca_final.append(energias[palavra])

for palavra in generos:
    if palavra in entrada:
        busca_final.append(generos[palavra])

# Se não detectar nada
if not busca_final:
    busca_final = ["top hits"]

# Montar busca
query = " ".join(busca_final)

print(f"\n🔎 Buscando por: {query}\n")

resultados = yt.search(query, filter="songs")

musicas = []

for item in resultados[:50]:
    titulo = item.get("title")
    artistas = item.get("artists")
    artista = artistas[0]["name"] if artistas else ""
    musicas.append(f"{titulo} – {artista}")

musicas = list(dict.fromkeys(musicas))[:30]

print("🔥 Aqui estão 30 músicas para sua vibe:\n")

for i, m in enumerate(musicas, 1):
    print(f"{i}. {m}")

print("\n🎶 Moodify entregou sua energia do dia.")
